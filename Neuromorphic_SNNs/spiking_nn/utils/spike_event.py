"""
Spike event data structures.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

from dataclasses import dataclass


@dataclass
class SpikeEvent:
    """Represents a single spike event in the network."""
    neuron_id: int
    layer_id: int
    timestamp: float
    potential: float
