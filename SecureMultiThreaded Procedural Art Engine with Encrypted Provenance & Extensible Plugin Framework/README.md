# SecureMultiThreaded Procedural Art Engine with Encrypted Provenance & Extensible Plugin Framework

## Overview

This Java-based project is an advanced procedural art generator that combines **multi-threading**, a **flexible plugin system**, and **encrypted provenance tracking** to create unique and verifiable digital art outputs. Designed with modularity and security in mind, it supports multiple procedural algorithms and ensures the integrity and authorship of generated content through cryptographic hashing and AES encryption.

The engine uses a Domain-Specific Language (DSL) style configuration interface to customize patterns, themes, sizes, emotions, licensing, and versioning, making it highly adaptable for artistic and software copyright purposes.

## Key Features

- **Multi-Threaded Execution**  
  Efficient concurrency to generate complex, computationally intensive patterns, fully leveraging modern multi-core processors for improved performance.

- **Plugin Architecture**  
  Modular design enabling seamless integration of new procedural art algorithms without modifying core engine code. Current patterns include Triangle, Diamond, and Hourglass shapes, with scope for fractal trees, cellular automata, and L-systems.

- **Encrypted Provenance Tracking**  
  Embeds cryptographically signed metadata alongside artwork outputs, using SHA-256 hashes and AES encryption, ensuring authenticity, authorship, and tamper-evidence.

- **Configurable via Domain-Specific Language (DSL)**  
  Simple, human-readable DSL input to specify pattern type, theme, size, emotion, license, version, and cryptographic options, facilitating both casual use and automated batch generation.

- **Robust Cryptography**  
  Implements industry-standard SHA-256 hashing for digital fingerprints and AES encryption to securely encode provenance data, enabling copyright protection and integrity verification.

## Novelty

Unlike typical procedural art generators, this engine uniquely integrates **cryptographic provenance** to protect generated digital assets, making it suitable for software copyright claims and trusted artistic outputs. Its extensible plugin framework fosters community-driven algorithm innovation, while multi-threading enhances scalability and efficiency, allowing creation of intricate and large-scale digital patterns in practical runtimes.

## Output

The engine produces the following upon execution:

- ASCII art representing the procedural pattern  
- Metadata including pattern details, license, version, and generation timestamp  
- SHA-256 cryptographic fingerprint for uniqueness and authenticity  
- Encrypted provenance data (Base64-encoded) containing signed metadata and hashes  

## Potential Extensions

- Develop a graphical user interface (GUI) for interactive pattern design and configuration  
- Integrate with blockchain technologies to provide decentralized provenance verification  
- Support exporting generated art to graphical formats such as SVG or PNG  
- Expand plugin library with advanced algorithms using fractal geometry, cellular automata, and L-systems  

## Authors:

- Dr Gururaj H.L 
- Panchadip Bhattacharjee  
- Advithiya Duddu  

---

*This project aims to elevate procedural art generation with modern cryptographic safeguards and modular extensibility, bridging creativity and security.*
