# Magic Square Sequence Generation with LSTM

## Overview

This project explores generating valid 3x3 Magic Squares using a deep learning approach. It leverages a sequence prediction model based on an LSTM neural network to learn and generate magic square sequences, starting from known valid examples.

## Project Motivation

Magic squares are fascinating mathematical structures where the sums of numbers in every row, column, and both main diagonals are equal (the magic constant, 15 in this case). Generating such sequences programmatically presents an interesting challenge in sequential data modeling and combinatorial pattern recognition.

## Dataset

- The dataset consists of 8 unique classic 3x3 magic squares.
- Each magic square sequence has 9 numbers (1 through 9), arranged so that every row, column, and diagonal sums to 15.
- Sequences are prepared in subsequences of length 4 to predict the next number in the series.

## Model Architecture

- A simple LSTM-based sequence predictor with:
  - An embedding layer to represent numbers as vectors.
  - One LSTM layer for temporal sequence modeling.
  - A linear output layer to predict the next number in the sequence.
- Trained using cross-entropy loss and AdamW optimizer.

## Training Procedure

- Trained on subsequences extracted from the 8 magic squares.
- Batch size of 8, trained for 300 epochs.
- Model learns to predict the next number based on the preceding 4 numbers.

## Sequence Generation

- The model generates candidate magic squares by predicting next numbers iteratively from a random seed.
- Generated sequences are validated using a function checking the magic square properties.
- Multiple attempts generate a collection of valid magic squares.

## Additional Features

- **Magic-ness Metric:** Measures how closely a generated square matches the ideal magic square sums.
- **Dynamic MIDI Creation:** Converts generated sequences into MIDI music files with tempo based on magic-ness — faster tempo for squares closer to ideal.
- **Visualization:** Matplotlib-based plots visualize the generated magic squares with clear formatting.
- **Validation and Evaluation:** Calculates training accuracy and number of valid magic squares generated.

## Results

- The model successfully generates multiple valid magic squares beyond the training set.
- Dynamic MIDI files demonstrate creative potential linking mathematical properties with musical expression.
- Visualizations provide an intuitive display of the generated sequences.

<img width="268" alt="image" src="https://github.com/user-attachments/assets/acf34f5d-007d-47db-842e-22c6bdc5fa39" />


## Code Structure Highlights

- LSTM-based PyTorch model for sequence prediction.
- Dataset preparation using PyTorch `TensorDataset` and `DataLoader`.
- Training loop with loss tracking.
- Functions for validating magic squares, generating sequences, and evaluating the model.
- Utilities for MIDI file creation and visualization.

---

