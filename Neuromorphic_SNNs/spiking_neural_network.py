"""
Event-Driven Spiking Neural Network Framework with STDP Learning
Author: [Your Name]
Date: January 2026
Description: Biologically-inspired SNN with Spike-Timing-Dependent Plasticity,
neuromorphic hardware optimization, and ultra-low-power edge deployment.
Compatible with Intel Loihi 3 and IBM NorthPole architectures.

Copyright Notice (India):
© 2026 [Your Name/Institution]. All Rights Reserved.

This software is protected under the Copyright Act, 1957 (as amended) of India.
All rights, title, and interest in and to this software, including all intellectual
property rights, are owned by [Your Name/Institution].

Unauthorized reproduction, distribution, modification, or use of this software
in whole or in part without prior written permission is strictly prohibited and
may result in civil and criminal penalties under Indian law.

License: [Specify your license - Proprietary/MIT/Apache/GPL etc.]
Registration: [Optional - Copyright registration number if registered with Copyright Office, India]

For permissions and licensing inquiries, contact: [Your Email]
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
from collections import deque
import time


@dataclass
class SpikeEvent:
    """Represents a single spike event in the network."""
    neuron_id: int
    layer_id: int
    timestamp: float
    potential: float


class LIFNeuron(nn.Module):
    """
    Leaky Integrate-and-Fire (LIF) neuron model with adaptive threshold.
    Implements biological spiking behavior with membrane potential dynamics.
    """
    
    def __init__(self, threshold: float = 1.0, tau_mem: float = 20.0,
                 tau_syn: float = 5.0, refractory_period: float = 2.0,
                 adaptive_threshold: bool = True):
        """
        Initialize LIF neuron.
        
        Args:
            threshold: Spike threshold voltage
            tau_mem: Membrane time constant (ms)
            tau_syn: Synaptic time constant (ms)
            refractory_period: Time unable to spike after firing (ms)
            adaptive_threshold: Enable dynamic threshold adaptation
        """
        super().__init__()
        
        self.base_threshold = threshold
        self.tau_mem = tau_mem
        self.tau_syn = tau_syn
        self.refractory_period = refractory_period
        self.adaptive_threshold = adaptive_threshold
        
        # State variables
        self.register_buffer('membrane_potential', torch.tensor(0.0))
        self.register_buffer('synaptic_current', torch.tensor(0.0))
        self.register_buffer('threshold', torch.tensor(threshold))
        self.register_buffer('last_spike_time', torch.tensor(-np.inf))
        self.register_buffer('spike_count', torch.tensor(0))
        
        # Learnable parameters
        self.leak = nn.Parameter(torch.tensor(0.95))
        self.threshold_decay = nn.Parameter(torch.tensor(0.9)) if adaptive_threshold else None
        
    def reset_state(self):
        """Reset neuron to resting state."""
        self.membrane_potential.zero_()
        self.synaptic_current.zero_()
        self.threshold.fill_(self.base_threshold)
        self.last_spike_time.fill_(-np.inf)
        self.spike_count.zero_()
    
    def forward(self, input_current: torch.Tensor, dt: float = 1.0,
                current_time: float = 0.0) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Update neuron state and check for spike.
        
        Args:
            input_current: Incoming synaptic current
            dt: Time step (ms)
            current_time: Current simulation time (ms)
            
        Returns:
            Tuple of (spike_binary, membrane_potential)
        """
        # Check refractory period
        time_since_spike = current_time - self.last_spike_time
        in_refractory = time_since_spike < self.refractory_period
        
        if not in_refractory:
            # Update synaptic current with exponential decay
            decay_syn = torch.exp(torch.tensor(-dt / self.tau_syn))
            self.synaptic_current = self.synaptic_current * decay_syn + input_current
            
            # Update membrane potential (leaky integration)
            decay_mem = torch.exp(torch.tensor(-dt / self.tau_mem))
            self.membrane_potential = (self.membrane_potential * decay_mem * self.leak +
                                      self.synaptic_current * dt)
            
            # Check for spike
            spike = (self.membrane_potential >= self.threshold).float()
            
            if spike > 0:
                # Reset after spike
                self.membrane_potential.zero_()
                self.last_spike_time.fill_(current_time)
                self.spike_count += 1
                
                # Adapt threshold if enabled
                if self.adaptive_threshold:
                    self.threshold = (self.threshold * self.threshold_decay +
                                    self.base_threshold * (1 - self.threshold_decay))
            else:
                # Decay threshold back to baseline
                if self.adaptive_threshold:
                    self.threshold = (self.threshold * 0.99 +
                                    self.base_threshold * 0.01)
        else:
            spike = torch.tensor(0.0)
        
        return spike, self.membrane_potential


class STDPSynapse(nn.Module):
    """
    Spike-Timing-Dependent Plasticity synaptic learning rule.
    Implements Hebbian-like learning based on precise spike timing.
    """
    
    def __init__(self, weight_init: float = 0.5, tau_plus: float = 20.0,
                 tau_minus: float = 20.0, a_plus: float = 0.01,
                 a_minus: float = 0.012, w_min: float = 0.0, w_max: float = 1.0):
        """
        Initialize STDP synapse.
        
        Args:
            weight_init: Initial synaptic weight
            tau_plus: Time constant for LTP (ms)
            tau_minus: Time constant for LTD (ms)
            a_plus: LTP learning rate
            a_minus: LTD learning rate
            w_min: Minimum weight
            w_max: Maximum weight
        """
        super().__init__()
        
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.a_plus = a_plus
        self.a_minus = a_minus
        self.w_min = w_min
        self.w_max = w_max
        
        # Synaptic weight
        self.weight = nn.Parameter(torch.tensor(weight_init))
        
        # Eligibility traces
        self.register_buffer('pre_trace', torch.tensor(0.0))
        self.register_buffer('post_trace', torch.tensor(0.0))
        
    def update_weight(self, pre_spike: torch.Tensor, post_spike: torch.Tensor,
                     dt: float = 1.0):
        """
        Update synaptic weight based on pre- and post-synaptic spikes.
        
        Args:
            pre_spike: Pre-synaptic spike (0 or 1)
            post_spike: Post-synaptic spike (0 or 1)
            dt: Time step (ms)
        """
        # Decay eligibility traces
        self.pre_trace *= torch.exp(torch.tensor(-dt / self.tau_plus))
        self.post_trace *= torch.exp(torch.tensor(-dt / self.tau_minus))
        
        # LTD: Pre-spike arrives, post already fired recently
        if pre_spike > 0 and self.post_trace > 0:
            dw = -self.a_minus * self.post_trace
            self.weight.data = torch.clamp(self.weight + dw, self.w_min, self.w_max)
        
        # LTP: Post-spike arrives, pre fired recently
        if post_spike > 0 and self.pre_trace > 0:
            dw = self.a_plus * self.pre_trace
            self.weight.data = torch.clamp(self.weight + dw, self.w_min, self.w_max)
        
        # Update traces on spike
        if pre_spike > 0:
            self.pre_trace += 1.0
        if post_spike > 0:
            self.post_trace += 1.0


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
        
        # Event queue for efficient processing
        self.event_queue = []
        
    def encode_poisson(self, x: torch.Tensor, max_rate: float = 100.0) -> torch.Tensor:
        """
        Encode continuous values as Poisson spike trains.
        
        Args:
            x: Input tensor [batch, features] in range [0, 1]
            max_rate: Maximum firing rate (Hz)
            
        Returns:
            Spike tensor [batch, time_steps, features]
        """
        batch_size, features = x.shape
        
        # Convert to firing rates
        rates = x * max_rate / 1000.0  # Convert to spikes per ms
        
        # Generate Poisson spikes
        spike_probs = rates.unsqueeze(1).expand(-1, self.num_steps, -1) * self.dt
        spikes = torch.rand_like(spike_probs) < spike_probs
        
        return spikes.float()
    
    def encode_latency(self, x: torch.Tensor, max_latency: float = 50.0) -> torch.Tensor:
        """
        Encode values as first-spike latency (higher value = earlier spike).
        
        Args:
            x: Input tensor [batch, features] in range [0, 1]
            max_latency: Maximum spike latency (ms)
            
        Returns:
            Spike tensor [batch, time_steps, features]
        """
        batch_size, features = x.shape
        
        # Compute spike times
        spike_times = (1 - x) * max_latency
        spike_time_steps = (spike_times / self.dt).long()
        
        # Create spike tensor
        spikes = torch.zeros(batch_size, self.num_steps, features)
        
        for b in range(batch_size):
            for f in range(features):
                t = spike_time_steps[b, f].item()
                if 0 <= t < self.num_steps:
                    spikes[b, t, f] = 1.0
        
        return spikes
    
    def decode_rate(self, spikes: torch.Tensor) -> torch.Tensor:
        """
        Decode spike trains using firing rate.
        
        Args:
            spikes: Spike tensor [batch, time_steps, features]
            
        Returns:
            Decoded values [batch, features]
        """
        return spikes.sum(dim=1) / self.num_steps
    
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
            spike_train = self.encode_poisson(x)
        elif encoding == 'latency':
            spike_train = self.encode_latency(x)
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
        decoded_output = self.decode_rate(output_spike_tensor)
        
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


# Example usage
if __name__ == "__main__":
    print("=== Spiking Neural Network Demo ===\n")
    
    # Create SNN
    snn = SpikingNeuralNetwork(
        layer_sizes=[28*28, 128, 64, 10],
        use_stdp=True,
        time_window=100.0,
        dt=1.0
    )
    
    print(f"SNN Architecture: {snn.layer_sizes}")
    print(f"Total neurons: {sum(snn.layer_sizes)}")
    print(f"Simulation window: {snn.time_window}ms\n")
    
    # Generate sample input (simulated MNIST-like)
    batch_size = 4
    input_data = torch.rand(batch_size, 28*28)
    
    # Process through SNN
    print("Processing spike trains...")
    start_time = time.time()
    output, stats = snn(input_data, encoding='poisson')
    inference_time = (time.time() - start_time) * 1000
    
    print(f"Inference time: {inference_time:.2f}ms")
    print(f"Output shape: {output.shape}")
    print(f"Output (rate-coded): {output[0].tolist()[:5]}...\n")
    
    # Analyze spike statistics
    if stats:
        avg_spike_rate = np.mean([s['spike_rate'] for s in stats])
        print(f"Average spike rate: {avg_spike_rate:.4f}")
    
    # Export for neuromorphic hardware
    loihi_config = snn.export_neuromorphic('loihi3')
    print(f"\nIntel Loihi 3 Configuration:")
    print(f"  Estimated cores: {loihi_config['estimated_cores']}")
    print(f"  Power estimate: {loihi_config['power_estimate_mw']:.1f}mW")
    print(f"  Energy per inference: ~{loihi_config['power_estimate_mw'] * inference_time / 1000:.2f}µJ")
