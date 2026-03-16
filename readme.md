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

# Vector Image Conversion Service

A modern web application that converts raster images (PNG, JPG, BMP, GIF) to vector formats (AI, EPS) using Inkscape. Built with FastAPI, this service provides a clean web interface for batch conversions with automatic file management.

## Features

### Image Conversion
- **Input Formats**: PNG, JPG, JPEG, BMP, GIF
- **Output Formats**: 
  - AI (Adobe Illustrator) - via PDF intermediate
  - EPS (Encapsulated PostScript) - direct export
- **Batch Processing**: Convert multiple images in one upload

### Web Interface
- **Drag-and-drop ready**: File upload form with multiple selection
- **Format Selection**: Choose between AI and EPS output
- **Instant Feedback**: Success/error messages for each file
- **Direct Download**: Click to download converted files

### Technical Features
- **Two-Stage Conversion**: Images → SVG → Target format for optimal quality
- **Automatic Cleanup**: Temporary files removed after conversion
- **Error Handling**: Graceful failure with user-friendly messages
- **Cross-Platform**: Windows paths configured, easily extensible

## How It Works

1. **Upload**: User selects multiple images and chooses output format
2. **Process**: 
   - Images saved temporarily
   - Each image converted to SVG using Inkscape
   - SVG converted to target format (AI/EPS)
   - Temporary files cleaned up
3. **Download**: Converted files available for download

## Installation

### Prerequisites
- [Inkscape](https://inkscape.org/release/) installed (Windows paths configured)
- Python 3.7+

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/vector-conversion-service.git
cd vector-conversion-service

# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Create directory structure
mkdir -p static templates uploaded_images result_vector
