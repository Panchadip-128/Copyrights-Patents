"""
Demo script for Spiking Neural Network.

Copyright: © 2026 [Your Name/Institution]. All Rights Reserved.
"""

import torch
import numpy as np
import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from spiking_nn import SpikingNeuralNetwork


def main():
    """Run SNN demonstration."""
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
    
    # Test latency encoding
    print("\n\nTesting latency encoding...")
    output_latency, _ = snn(input_data, encoding='latency')
    print(f"Latency-encoded output: {output_latency[0].tolist()[:5]}...")


if __name__ == "__main__":
    main()
