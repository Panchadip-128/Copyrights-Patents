# Spiking Neural Network Framework

**Event-Driven Spiking Neural Network with STDP Learning**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

## Copyright Notice

**© 2026 [Your Name/Institution]. All Rights Reserved.**

This software is protected under the Copyright Act, 1957 (as amended) of India. All rights, title, and interest in and to this software, including all intellectual property rights, are owned by [Your Name/Institution].

Unauthorized reproduction, distribution, modification, or use of this software in whole or in part without prior written permission is strictly prohibited and may result in civil and criminal penalties under Indian law.

## Overview

A biologically-inspired Spiking Neural Network (SNN) framework with Spike-Timing-Dependent Plasticity (STDP), optimized for neuromorphic hardware deployment. Compatible with Intel Loihi 3 and IBM NorthPole architectures.

### Key Features

- **Biologically Accurate Models**: LIF neurons with adaptive thresholds and refractory periods
- **STDP Learning**: Hebbian-like synaptic plasticity based on precise spike timing
- **Multiple Encoding Schemes**: Poisson rate coding and temporal latency coding
- **Neuromorphic Hardware Support**: Export configurations for Intel Loihi 3 and IBM NorthPole
- **Ultra-Low Power**: Optimized for edge deployment with energy consumption tracking
- **Event-Driven Processing**: Efficient spike-based computation

## Installation

```bash
# Clone the repository
git clone https://github.com/[yourusername]/spiking-neural-network.git
cd spiking-neural-network

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

```python
from spiking_nn import SpikingNeuralNetwork
import torch

# Create a spiking neural network
snn = SpikingNeuralNetwork(
    layer_sizes=[784, 128, 64, 10],  # Input -> Hidden -> Output
    use_stdp=True,                   # Enable learning
    time_window=100.0,               # 100ms simulation
    dt=1.0                           # 1ms time step
)

# Generate input data
input_data = torch.rand(4, 784)  # Batch of 4 samples

# Forward pass with Poisson encoding
output, stats = snn(input_data, encoding='poisson')

print(f"Output shape: {output.shape}")
print(f"Average spike rate: {stats[0]['spike_rate']:.4f}")
```

## Project Structure

```
cprt/
├── spiking_nn/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── neurons/             # Neuron models
│   │   ├── __init__.py
│   │   └── lif_neuron.py    # Leaky Integrate-and-Fire neuron
│   ├── synapses/            # Synaptic plasticity
│   │   ├── __init__.py
│   │   └── stdp_synapse.py  # STDP learning rule
│   ├── layers/              # Network layers
│   │   ├── __init__.py
│   │   └── spiking_layer.py # Spiking layer implementation
│   ├── network/             # Network architectures
│   │   ├── __init__.py
│   │   └── snn.py           # Main SNN class
│   ├── encoding/            # Spike encoding/decoding
│   │   ├── __init__.py
│   │   └── encoders.py      # Poisson, latency, rate coding
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── spike_event.py   # Spike event data structure
├── examples/                # Example scripts
│   └── demo.py             # Demonstration script
├── tests/                   # Test suite
│   └── __init__.py
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
└── LICENSE                # License file
```

## Usage Examples

### Running the Demo

```bash
python examples/demo.py
```

### Creating Custom Networks

```python
from spiking_nn import SpikingNeuralNetwork
from spiking_nn.neurons import LIFNeuron
from spiking_nn.layers import SpikingLayer

# Custom layer with specific parameters
layer = SpikingLayer(
    in_features=784,
    out_features=128,
    use_stdp=True,
    lateral_inhibition=True
)
```

### Neuromorphic Hardware Export

```python
# Export configuration for Intel Loihi 3
loihi_config = snn.export_neuromorphic('loihi3')
print(f"Estimated cores: {loihi_config['estimated_cores']}")
print(f"Power estimate: {loihi_config['power_estimate_mw']:.1f}mW")

# Export for IBM NorthPole
northpole_config = snn.export_neuromorphic('northpole')
```

## Architecture Details

### LIF Neuron Model

The Leaky Integrate-and-Fire neuron implements:
- Membrane potential dynamics with exponential decay
- Synaptic current integration
- Adaptive threshold mechanism
- Refractory period enforcement

### STDP Learning

Spike-Timing-Dependent Plasticity:
- Long-Term Potentiation (LTP): Pre-before-post strengthening
- Long-Term Depression (LTD): Post-before-pre weakening
- Exponential eligibility traces
- Configurable learning windows

### Encoding Schemes

1. **Poisson Encoding**: Rate-based stochastic spike generation
2. **Latency Encoding**: First-spike timing represents value
3. **Rate Decoding**: Spike count normalization

## Hardware Requirements

- Python 3.8+
- PyTorch 2.0+
- NumPy 1.24+
- 4GB+ RAM recommended
- GPU optional (CPU-compatible)

## Performance

- **Inference Speed**: ~10-50ms per batch (CPU)
- **Energy Efficiency**: ~0.1-1µJ per inference (estimated for neuromorphic hardware)
- **Scalability**: Supports networks with 10K+ neurons

## Contributing

This is proprietary software. For collaboration inquiries, contact [Your Email].

## Citation

If you use this software in your research, please cite:

```bibtex
@software{spiking_nn_2026,
  author = {[Your Name]},
  title = {Event-Driven Spiking Neural Network Framework with STDP Learning},
  year = {2026},
  publisher = {[Your Institution]},
  version = {1.0.0}
}
```

## License

© 2026 [Your Name/Institution]. All Rights Reserved.

This software is protected under Indian copyright law. See [LICENSE](LICENSE) for details.

## Contact

- Author: [Your Name]
- Email: [Your Email]
- Institution: [Your Institution]

## Acknowledgments

Inspired by advances in neuromorphic computing, particularly Intel Loihi 3 and IBM NorthPole architectures (2026).

---

**Protected under the Copyright Act, 1957 (as amended) of India**
