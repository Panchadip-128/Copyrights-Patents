# Neural Audio Morphing Lab

**Real-time interactive blending of two audio sources with reverb, visuals, and creative control.**

---

## Overview

A creative audio lab that lets you explore the morphing of two distinct sounds in real time. Built for interactive experimentation, it allows users to control the morph level, choose from various blending styles, and visualize the transformation through waveforms and spectrograms.

Whether you're a sound artist, an educator, or just curious about audio transformation, this project brings an intuitive, hands-on approach to audio fusion.

---

## Features

### Core Morphing Features

| Feature | Screenshot | Description |
|---------|-----------|-------------|
| **Real-Time Morphing Slider** | <img src="https://github.com/user-attachments/assets/afad2fa6-dd92-4a32-ac86-a4b87f131b1f" width="450"/> | Instantly blend between two audio sources using an interactive slider. |
| **Blend Curve Selection** | <img src="https://github.com/user-attachments/assets/eeca7b95-2f4e-47ce-be7c-65a59a959a9a" width="450"/> | Choose from linear, sine, exponential, logarithmic, or step-style morph transitions. |
| **Dynamic Envelope Matching** | <img src="https://github.com/user-attachments/assets/5290e192-56ac-4da0-bba5-b1b776f8e93c" width="450"/> | Natural blending guided by amplitude envelopes of both sources. |
| **Waveform & Spectrogram Visuals** | <img src="https://github.com/user-attachments/assets/41f4da85-fc25-4822-9a2b-c623b868cb56" width="450"/> <img src="https://github.com/user-attachments/assets/fee5e4c0-595c-4f97-9bfb-ff24421c93f3" width="450"/> <img src="https://github.com/user-attachments/assets/699e0955-1627-4747-aa5d-6c10e9423e65" width="450"/> | Dark-themed UI visualizations of source sounds and blended output. |
| **Built-in Reverb Effect** | – | Add atmospheric depth to your audio output with a simple reverb toggle. |

---

### Research-Oriented XAI Visualizations

| Feature | Visualization | Description |
|---------|-----------|-------------|
| **Frequency Band Contribution** | <img src="https://github.com/user-attachments/assets/139de4b3-e80e-472a-b098-20349ca8c6a5" width="500"/> | Splits FFT spectrum into multiple bands and shows normalized energy contributions. |
| **Energy Flow Between Sources** | <img src="https://github.com/user-attachments/assets/62bc47a7-e37c-42e3-86af-a812f1687505" width="500"/> | Visualizes how energy shifts between the two sources over time. |
| **Spectral XAI Overlay** | <img src="https://github.com/user-attachments/assets/88e6d976-00b2-48d1-ae69-120fae39be3e" width="500"/> | Displays log-frequency spectrogram with spectral centroid and bandwidth overlays. |
| **Morph Curve Influence Analysis** | <img src="https://github.com/user-attachments/assets/90f7e25e-a291-49c8-9d79-61fbbfea92ae" width="500"/> | Compares different morph curves and their effect on mean amplitude. |
| **Feature Overlay on Spectrogram** | <img src="https://github.com/user-attachments/assets/7b0dfa5e-ddd6-42ca-9dfb-7dccd8b2a20f" width="500"/> | Combines multiple analyses over the spectrogram for in-depth interpretation. |
| **Waterfall Spectrogram** | <img src="https://github.com/user-attachments/assets/06c5bcf2-4e0d-4e0b-9d44-264a6c1592c1" width="450"/> | Shows frequency evolution over time in 3D-like waterfall view. |
| **MFCC PCA Embeddings Distribution** | <img src="https://github.com/user-attachments/assets/f10c3363-401b-4edf-a723-c445183917cd" width="450"/> | Visualizes clustering and distribution of MFCC-based PCA embeddings. |
| **Real-Time Spectral Analyzer** | <img src="https://github.com/user-attachments/assets/15cdece1-ac24-40bf-974b-a4c21b6725aa" width="450"/> <img src="https://github.com/user-attachments/assets/ce2dfb11-588c-4d3b-8390-2a69554acfe7" width="450"/> | Live FFT-based visualization of morphed audio frequencies over time. |

---

## Use Cases

- Audio experimentation and remixing  
- Signal processing demos and teaching  
- Creative sound design projects  
- Exploratory tools for musicians and hobbyists

---

## Highlights

### Core Audio Morphing

- Instant feedback via **live sound playback** and **dynamic visualizations**.  
- Smooth and flexible audio transformations:
  - Designed for **ease of use** and **creative exploration**.  
- Support for multiple **blend curves**: Linear, Exponential, Logarithmic, Step, Sine.  
- Real-time **morph factor adjustment**.

### Research-Oriented XAI Visualizations

1. **Frequency Band Contribution** – normalized energy per FFT band.  
2. **Top Dominant Frequencies** – interpretable top N frequency magnitudes.  
3. **Energy Flow Between Sources** – Hilbert transform-based energy visualization.  
4. **Spectral XAI Overlay** – log-frequency spectrogram with spectral centroid/bandwidth.  
5. **Morph Curve Influence Analysis** – curve vs amplitude analysis for optimization.

### Fully Interactive Dashboard

- Sliders and dropdowns for real-time control of morphing factor and blend curve.  
- Integrated visualizations: Waveform, Frequency contributions, Top frequencies, Energy flow, Spectral overlay, Morph curve influence.

### Technical Enhancements

- Uses `scipy.signal.hilbert` for **accurate envelope computation**.  
- Handles variable-length audio sources with proper normalization.  
- Generates **publication-quality visualizations** for research or presentations.

---

## Authors

- Advithiya Duddu  
- Panchadip Bhattacharjee
