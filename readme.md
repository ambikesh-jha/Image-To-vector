# Image to Vector Converter

A Python utility for converting image files (PNG, JPG) to vector formats (AI, EPS) using Inkscape.

## Requirements :

- Python 3.7+
- Inkscape installed on your system
- Inkscape Download link : https://inkscape.org/release/inkscape-1.4/windows/64-bit/msi/?redirected=1


## Usage

Basic usage:
```python

# Initialize converter
converter = VectorConverter()

# Convert PNG to AI
result = converter.convert_to_vector(
    input_path="image.png",
    output_format="ai"
)
```

## Supported Formats

Input:
- PNG
- JPG/JPEG

Output:
- AI (Adobe Illustrator)
- EPS (Encapsulated PostScript)
