import subprocess
import os
from typing import Optional, Literal, List
from pathlib import Path

class VectorConverter:
    """A class to convert images to vector formats using Inkscape."""
    
    WINDOWS_DEFAULT_PATHS = [
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files\Inkscape\inkscape.exe",
    ]
    
    SUPPORTED_FORMATS = Literal['ai', 'eps']
    SUPPORTED_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    
    def __init__(self, inkscape_path: Optional[str] = None):
        """
        Initialize the converter with path to Inkscape executable.
        
        Args:
            inkscape_path (str, optional): Path to Inkscape executable. 
                If None, tries to find it automatically.
                
        Raises:
            FileNotFoundError: If Inkscape executable cannot be found.
        """
        self.inkscape_path = self._find_inkscape(inkscape_path)

    def _find_inkscape(self, custom_path: Optional[str] = None) -> str:
        """
        Find the Inkscape executable path.
        
        Args:
            custom_path (str, optional): User-provided path to Inkscape executable.
            
        Returns:
            str: Valid path to Inkscape executable.
            
        Raises:
            FileNotFoundError: If Inkscape executable cannot be found.
        """
        if custom_path and os.path.exists(custom_path):
            return custom_path
            
        for path in self.WINDOWS_DEFAULT_PATHS:
            if os.path.exists(path):
                return path
                    
        raise FileNotFoundError(
            "Inkscape not found. Please install Inkscape or provide the correct path."
        )
    
    def _run_inkscape_command(self, command: List[str], operation: str) -> None:
        """
        Execute an Inkscape command safely.
        
        Args:
            command (List[str]): Command to execute.
            operation (str): Name of operation for error messages.
            
        Raises:
            subprocess.CalledProcessError: If command execution fails.
        """
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stderr:
                print(f"Warning during {operation}:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"{operation} command failed: {e.stdout}\n{e.stderr}")
            raise
    
    def _convert_to_svg(self, input_path: Path, svg_path: Path) -> None:
        """
        Convert input image to SVG format.
        
        Args:
            input_path (Path): Path to input image.
            svg_path (Path): Path for output SVG file.
        """
        trace_command = [
            str(self.inkscape_path),
            '--export-filename', str(svg_path),
            '--export-type=svg',
            str(input_path)
        ]
        self._run_inkscape_command(trace_command, "SVG conversion")
    
    def _convert_svg_to_vector(
        self,
        svg_path: Path,
        output_path: Path,
        output_format: SUPPORTED_FORMATS
    ) -> None:
        """
        Convert SVG to final vector format.
        
        Args:
            svg_path (Path): Path to input SVG file.
            output_path (Path): Path for output file.
            output_format (str): Target format ('ai' or 'eps').
        """
        if output_format == 'eps':
            export_command = [
                str(self.inkscape_path),
                '--export-filename', str(output_path),
                '--export-type=eps',
                str(svg_path)
            ]
            self._run_inkscape_command(export_command, "EPS conversion")
            
        else:  
            # AI format
            # For AI, we export as PDF which is AI-compatible
            pdf_path = str(output_path).replace('.ai', '.pdf')
            export_command = [
                str(self.inkscape_path),
                '--export-filename', pdf_path,
                '--export-type=pdf',
                str(svg_path)
            ]
            self._run_inkscape_command(export_command, "PDF conversion")
            os.rename(pdf_path, str(output_path))

    def convert(
        self,
        input_path: str,
        output_format: SUPPORTED_FORMATS = 'ai',
        output_folder: str = "result_vector"
    ) -> List[str]:
        """
        Convert image(s) to vector format. Handles both single files and folders.
        
        Args:
            input_path (str): Path to input image file or folder.
            output_format (str): Target format ('ai' or 'eps').
            output_folder (str): Path to folder where vector files will be saved.
            
        Returns:
            List[str]: List of paths to the converted files.
            
        Raises:
            FileNotFoundError: If input path doesn't exist.
        """
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Input path not found: {input_path}")

        # Create output folder if it doesn't exist
        output_folder = Path(output_folder).resolve()
        output_folder.mkdir(parents=True, exist_ok=True)

        converted_files = []
        errors = []

        if input_path.is_file():
            if input_path.suffix.lower() not in self.SUPPORTED_IMAGE_EXTENSIONS:
                raise ValueError(f"Unsupported file type: {input_path.suffix}")
            
            try:
                output_path = output_folder / f"{input_path.stem}.{output_format}"
                # Convert to SVG first
                svg_path = output_folder / f"{input_path.stem}_temp.svg"
                try:
                    self._convert_to_svg(input_path, svg_path)
                    self._convert_svg_to_vector(svg_path, output_path, output_format)
                    converted_files.append(str(output_path))
                    print(f"Successfully converted: {input_path.name}")
                finally:
                    if svg_path.exists():
                        os.remove(svg_path)
            except Exception as e:
                errors.append(f"Error converting {input_path.name}: {str(e)}")
                print(f"Failed to convert: {input_path.name}")

        elif input_path.is_dir():
            for file_path in input_path.iterdir():
                if file_path.suffix.lower() in self.SUPPORTED_IMAGE_EXTENSIONS:
                    try:
                        output_path = output_folder / f"{file_path.stem}.{output_format}"
                        # Convert to SVG first
                        svg_path = output_folder / f"{file_path.stem}_temp.svg"
                        try:
                            self._convert_to_svg(file_path, svg_path)
                            self._convert_svg_to_vector(svg_path, output_path, output_format)
                            converted_files.append(str(output_path))
                            print(f"Successfully converted: {file_path.name}")
                        finally:
                            if svg_path.exists():
                                os.remove(svg_path)
                    except Exception as e:
                        errors.append(f"Error converting {file_path.name}: {str(e)}")
                        print(f"Failed to convert: {file_path.name}")

        # Report any errors that occurred
        if errors:
            print("\nConversion Errors:")
            for error in errors:
                print(error)

        return converted_files

def main():
    """Example usage of the VectorConverter class."""
    try:
        # Create converter
        converter = VectorConverter()
        
        # Convert either a single file or a folder
        converted_files = converter.convert(
            input_path="input_images",  # "folder name (input_images) for multiple images" or "image name(sample.jpg) for single images" 
            # input_path="sample.jpg",
            output_format="eps",  # "ai (Adobe Illustrator) " or "eps (Encapsulated PostScript) "  
            output_folder="result_vector"
        )
        print(f"\nConversion complete. Converted {len(converted_files)} files.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
