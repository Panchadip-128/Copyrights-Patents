"""
Spiking layer implementation with LIF neurons and STDP synapses.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
import torch.nn as nn
from typing import Tuple, Dict
from collections import deque

from ..neurons.lif_neuron import LIFNeuron
from ..synapses.stdp_synapse import STDPSynapse


class SpikingLayer(nn.Module):
    """
    Layer of LIF neurons with STDP synapses for event-driven processing.
    """
    
    def __init__(self, in_features: int, out_features: int,
                 use_stdp: bool = True, lateral_inhibition: bool = True):
        """
        Initialize spiking layer.
        
        Args:
            in_features: Number of input neurons
            out_features: Number of output neurons
            use_stdp: Enable STDP learning
            lateral_inhibition: Enable winner-take-all inhibition
        """
        super().__init__()
        
        self.in_features = in_features
        self.out_features = out_features
        self.use_stdp = use_stdp
        self.lateral_inhibition = lateral_inhibition
        
        # Create neurons
        self.neurons = nn.ModuleList([
            LIFNeuron() for _ in range(out_features)
        ])
        
        # Create synapses
        if use_stdp:
            self.synapses = nn.ModuleList([
                nn.ModuleList([
                    STDPSynapse() for _ in range(in_features)
                ])
                for _ in range(out_features)
            ])
        else:
            # Fixed weights
            self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        
        # Spike history for temporal coding
        self.spike_history = deque(maxlen=100)
        
    def reset_state(self):
        """Reset all neurons and clear spike history."""
        for neuron in self.neurons:
            neuron.reset_state()
        self.spike_history.clear()
    
    def forward(self, input_spikes: torch.Tensor, dt: float = 1.0,
                current_time: float = 0.0) -> Tuple[torch.Tensor, Dict]:
        """
        Process input spikes through layer.
        
        Args:
            input_spikes: Binary spike tensor [batch, in_features]
            dt: Time step
            current_time: Current simulation time
            
        Returns:
            Tuple of (output_spikes, layer_stats)
        """
        batch_size = input_spikes.shape[0]
        output_spikes = torch.zeros(batch_size, self.out_features, 
                                    device=input_spikes.device)
        membrane_potentials = torch.zeros_like(output_spikes)
        
        for b in range(batch_size):
            neuron_spikes = []
            
            for j, neuron in enumerate(self.neurons):
                # Compute input current from all synapses
                input_current = torch.tensor(0.0)
                
                for i in range(self.in_features):
                    if input_spikes[b, i] > 0:
                        if self.use_stdp:
                            weight = self.synapses[j][i].weight
                        else:
                            weight = self.weight[j, i]
                        
                        input_current += weight * input_spikes[b, i]
                
                # Update neuron
                spike, potential = neuron(input_current, dt, current_time)
                
                output_spikes[b, j] = spike
                membrane_potentials[b, j] = potential
                neuron_spikes.append(spike.item())
                
                # STDP weight updates
                if self.use_stdp and self.training:
                    for i in range(self.in_features):
                        self.synapses[j][i].update_weight(
                            input_spikes[b, i], spike, dt
                        )
            
            # Lateral inhibition: only strongest neuron spikes
            if self.lateral_inhibition and output_spikes[b].sum() > 1:
                max_idx = membrane_potentials[b].argmax()
                inhibited_spikes = torch.zeros_like(output_spikes[b])
                inhibited_spikes[max_idx] = output_spikes[b, max_idx]
                output_spikes[b] = inhibited_spikes
            
            # Record spike pattern
            self.spike_history.append({
                'time': current_time,
                'spikes': neuron_spikes,
                'batch': b
            })
        
        stats = {
            'mean_potential': membrane_potentials.mean().item(),
            'spike_rate': output_spikes.sum().item() / (batch_size * self.out_features),
            'active_neurons': (output_spikes.sum(0) > 0).sum().item()
        }
        
        return output_spikes, stats
