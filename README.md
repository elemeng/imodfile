# imodfile

## Description
`imodfile` is a Python project designed for parsing, modifying, and converting IMOD files. It allows users to apply various coordinate operations to IMOD files and convert them to Relion starfiles. This tool is particularly useful for researchers and developers working with 3D electron microscopy data.

## Features
- Parse IMOD files and extract model data.
- Apply coordinate transformations (add, subtract, multiply, divide) to model points.
- Convert IMOD files to Relion starfiles.
- Command-line interface for easy usage.

## Installation
To install the required dependencies, in the code directory, run:
```bash
pip install uv 
uv sync
```

## Usage
### Convert IMOD files and apply coordinate operations
```bash
python convert.py input_file output_file --add 10 --subtract 5 --multiply 2 --divide 1 --format mod
```
- `input_file`: Path to the input IMOD file.
- `output_file`: Path to the output file.
- `--add`: Add constant to coordinates.
- `--subtract`: Subtract constant from coordinates.
- `--multiply`: Multiply coordinates by constant.
- `--divide`: Divide coordinates by constant.
- `--format`: Output file format: 'mod' or 'star'.

### Example
Convert an IMOD file and add 10 to all coordinates:
```bash
python convert.py example.mod output.mod --add 10 --format mod
```

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. 