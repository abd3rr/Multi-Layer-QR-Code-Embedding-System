# Secure Multi-Layer QR Code Embedding System

This system is a comprehensive solution for embedding multiple binary images, such as QR codes, into a host QR code. It employs advanced image processing techniques to securely encode additional data layers within a QR code, while ensuring the augmented QR code remains scannable by standard readers.

## Features

### Part I: Single QR Embedding
- **Voronoi Diagram Generation**: Creates a Voronoi diagram from randomly placed seeds.
- **Classification Key**: Partitions seeds into two distinct sets and creates a corresponding key for embedding.
- **Bitwise Embedding**: Utilizes bitwise operations for embedding based on the classification and Voronoi regions.

### Part II: Multiple QR Embedding
- **Multi-Image Insertion**: An algorithm to insert up to five binary images into a host QR code.
- **Image Retrieval**: An algorithm to extract hidden QR codes from an augmented QR code.

### Part III: Secure Augmented QR Code
- **Enhanced Voronoi Diagram**: Generates a Voronoi diagram with 3 regions for complex spatial encoding.
- **Secure Embedding Algorithm**: Encodes 4 binary images into the host QR code using permutations tied to Voronoi regions.
- **Customized Extraction**: A decoding process that uses the Voronoi diagram and specified permutations to retrieve the embedded images.

## Technologies Used
- **Language**: Python 3.11
- **Dependencies**: Managed via `requirements.txt`.


