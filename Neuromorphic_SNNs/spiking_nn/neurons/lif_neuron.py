"""
Leaky Integrate-and-Fire (LIF) neuron implementation.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple


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
