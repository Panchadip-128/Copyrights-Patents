"""
Spike-Timing-Dependent Plasticity (STDP) synapse implementation.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
import torch.nn as nn


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
