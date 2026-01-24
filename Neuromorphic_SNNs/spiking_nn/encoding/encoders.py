"""
Spike encoding and decoding schemes.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
from typing import Optional


class PoissonEncoder:
    """Encode continuous values as Poisson spike trains."""
    
    def __init__(self, time_window: float, dt: float, max_rate: float = 100.0):
        """
        Initialize Poisson encoder.
        
        Args:
            time_window: Simulation time window (ms)
            dt: Time step resolution (ms)
            max_rate: Maximum firing rate (Hz)
        """
        self.time_window = time_window
        self.dt = dt
        self.max_rate = max_rate
        self.num_steps = int(time_window / dt)
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode continuous values as Poisson spike trains.
        
        Args:
            x: Input tensor [batch, features] in range [0, 1]
            
        Returns:
            Spike tensor [batch, time_steps, features]
        """
        batch_size, features = x.shape
        
        # Convert to firing rates
        rates = x * self.max_rate / 1000.0  # Convert to spikes per ms
        
        # Generate Poisson spikes
        spike_probs = rates.unsqueeze(1).expand(-1, self.num_steps, -1) * self.dt
        spikes = torch.rand_like(spike_probs) < spike_probs
        
        return spikes.float()


class LatencyEncoder:
    """Encode values as first-spike latency (higher value = earlier spike)."""
    
    def __init__(self, time_window: float, dt: float, max_latency: float = 50.0):
        """
        Initialize latency encoder.
        
        Args:
            time_window: Simulation time window (ms)
            dt: Time step resolution (ms)
            max_latency: Maximum spike latency (ms)
        """
        self.time_window = time_window
        self.dt = dt
        self.max_latency = max_latency
        self.num_steps = int(time_window / dt)
    
    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode values as first-spike latency.
        
        Args:
            x: Input tensor [batch, features] in range [0, 1]
            
        Returns:
            Spike tensor [batch, time_steps, features]
        """
        batch_size, features = x.shape
        
        # Compute spike times
        spike_times = (1 - x) * self.max_latency
        spike_time_steps = (spike_times / self.dt).long()
        
        # Create spike tensor
        spikes = torch.zeros(batch_size, self.num_steps, features)
        
        for b in range(batch_size):
            for f in range(features):
                t = spike_time_steps[b, f].item()
                if 0 <= t < self.num_steps:
                    spikes[b, t, f] = 1.0
        
        return spikes


class RateDecoder:
    """Decode spike trains using firing rate."""
    
    def __init__(self, time_window: float, dt: float):
        """
        Initialize rate decoder.
        
        Args:
            time_window: Simulation time window (ms)
            dt: Time step resolution (ms)
        """
        self.time_window = time_window
        self.dt = dt
        self.num_steps = int(time_window / dt)
    
    def decode(self, spikes: torch.Tensor) -> torch.Tensor:
        """
        Decode spike trains using firing rate.
        
        Args:
            spikes: Spike tensor [batch, time_steps, features]
            
        Returns:
            Decoded values [batch, features]
        """
        return spikes.sum(dim=1) / self.num_steps
