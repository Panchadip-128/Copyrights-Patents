"""
Spiking Neural Network implementation.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import List, Tuple, Dict

from ..layers.spiking_layer import SpikingLayer
from ..encoding.encoders import PoissonEncoder, LatencyEncoder, RateDecoder


class SpikingNeuralNetwork(nn.Module):
    """
    Multi-layer Spiking Neural Network with temporal dynamics.
    Optimized for neuromorphic hardware deployment.
    """
    
    def __init__(self, layer_sizes: List[int], use_stdp: bool = True,
                 time_window: float = 100.0, dt: float = 1.0):
        """
        Initialize SNN.
        
        Args:
            layer_sizes: List of layer dimensions
            use_stdp: Enable STDP learning
            time_window: Simulation time window (ms)
            dt: Time step resolution (ms)
        """
        super().__init__()
        
        self.layer_sizes = layer_sizes
        self.use_stdp = use_stdp
        self.time_window = time_window
        self.dt = dt
        self.num_steps = int(time_window / dt)
        
        # Build layers
        self.layers = nn.ModuleList([
            SpikingLayer(layer_sizes[i], layer_sizes[i+1], use_stdp=use_stdp)
            for i in range(len(layer_sizes) - 1)
        ])
        
        # Encoders and decoders
        self.poisson_encoder = PoissonEncoder(time_window, dt)
        self.latency_encoder = LatencyEncoder(time_window, dt)
        self.rate_decoder = RateDecoder(time_window, dt)
        
        # Event queue for efficient processing
        self.event_queue = []
    
    def forward(self, x: torch.Tensor, encoding: str = 'poisson') -> Tuple[torch.Tensor, List[Dict]]:
        """
        Forward pass through SNN.
        
        Args:
            x: Input tensor [batch, features]
            encoding: Input encoding method ('poisson' or 'latency')
            
        Returns:
            Tuple of (decoded_output, layer_stats_list)
        """
        # Reset all neurons
        for layer in self.layers:
            layer.reset_state()
        
        # Encode input
        if encoding == 'poisson':
            spike_train = self.poisson_encoder.encode(x)
        elif encoding == 'latency':
            spike_train = self.latency_encoder.encode(x)
        else:
            raise ValueError(f"Unknown encoding: {encoding}")
        
        # Process through network over time
        all_stats = []
        output_spikes_over_time = []
        
        for t in range(self.num_steps):
            current_time = t * self.dt
            layer_input = spike_train[:, t, :]
            
            # Forward through layers
            for layer in self.layers:
                layer_output, stats = layer(layer_input, self.dt, current_time)
                layer_input = layer_output
                all_stats.append(stats)
            
            output_spikes_over_time.append(layer_output)
        
        # Stack temporal outputs
        output_spike_tensor = torch.stack(output_spikes_over_time, dim=1)
        
        # Decode output
        decoded_output = self.rate_decoder.decode(output_spike_tensor)
        
        return decoded_output, all_stats
    
    def compute_energy(self, spike_counts: torch.Tensor, 
                      energy_per_spike: float = 1e-12) -> float:
        """
        Estimate energy consumption (Joules).
        
        Args:
            spike_counts: Number of spikes per neuron
            energy_per_spike: Energy per spike event (J), typical ~1pJ
            
        Returns:
            Total energy in Joules
        """
        total_spikes = spike_counts.sum().item()
        return total_spikes * energy_per_spike
    
    def export_neuromorphic(self, target_hardware: str = 'loihi3') -> Dict:
        """
        Export network configuration for neuromorphic hardware.
        
        Args:
            target_hardware: Target platform ('loihi3', 'northpole', 'spinnaker')
            
        Returns:
            Hardware-specific configuration dictionary
        """
        config = {
            'hardware': target_hardware,
            'num_layers': len(self.layers),
            'layer_sizes': self.layer_sizes,
            'total_neurons': sum(self.layer_sizes),
            'time_window_ms': self.time_window,
            'dt_ms': self.dt
        }
        
        if target_hardware == 'loihi3':
            config['compartments_per_core'] = 1024
            config['estimated_cores'] = int(np.ceil(sum(self.layer_sizes) / 1024))
            config['power_estimate_mw'] = config['estimated_cores'] * 0.5
        
        elif target_hardware == 'northpole':
            config['cores'] = 256
            config['neurons_per_core'] = sum(self.layer_sizes) // 256
            config['power_estimate_mw'] = 25  # Typical NorthPole power
        
        return config
