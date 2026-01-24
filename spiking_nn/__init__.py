"""
Event-Driven Spiking Neural Network Framework with STDP Learning
Author: [Your Name]
Date: January 2026

Copyright Notice (India):
© 2026 [Your Name/Institution]. All Rights Reserved.

This software is protected under the Copyright Act, 1957 (as amended) of India.
"""

__version__ = "1.0.0"
__author__ = "[Your Name]"
__copyright__ = "© 2026 [Your Name/Institution]. All Rights Reserved."

from .neurons.lif_neuron import LIFNeuron
from .synapses.stdp_synapse import STDPSynapse
from .layers.spiking_layer import SpikingLayer
from .network.snn import SpikingNeuralNetwork
from .utils.spike_event import SpikeEvent
from .encoding.encoders import PoissonEncoder, LatencyEncoder, RateDecoder

__all__ = [
    'LIFNeuron',
    'STDPSynapse',
    'SpikingLayer',
    'SpikingNeuralNetwork',
    'SpikeEvent',
    'PoissonEncoder',
    'LatencyEncoder',
    'RateDecoder',
]
