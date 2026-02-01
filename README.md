# PDF to Markdown Converter with OLMOCR

A Python script that converts PDF files to clean Markdown format using the OLMOCR vision-language model via LM Studio.

## Features

- **High-quality OCR**: Uses the `allenai/olmocr-2-7b` model for accurate text extraction
- **Command-line interface**: Simple usage with automatic output path generation
- **Batch processing**: Processes all pages in a PDF automatically
- **Progress tracking**: Visual progress bar with tqdm
- **Robust parsing**: Handles multiple response formats from the model

## Prerequisites

- Python 3.8+
- LM Studio running locally with OLMOCR model loaded
- Required Python packages

## Installation

1. Clone or download this script
2. Install dependencies:

```bash
pip install openai pypdf tqdm
```

3. Install OLMOCR:

```bash
pip install olmocr
```

4. Start LM Studio and load the OLMOCR model:
   - Model: `allenai/olmocr-2-7b`
   - Quantization: `q4_k_m` (recommended)
   - Ensure LM Studio API server is running on `http://localhost:1234`

## Usage

Basic usage:

```bash
python ocr_script.py path/to/your/document.pdf
```

This will create `path/to/your/document.md` automatically.

### Command Line Options

Currently supports:
- Input PDF file path (required)
- Output path is automatically generated in the same directory with `.md` extension

## How It Works

1. **PDF Reading**: Uses PyPDF to read the PDF file structure
2. **Page Processing**: Each page is sent to LM Studio as an image
3. **OCR Processing**: OLMOCR model extracts and formats text from the image
4. **Response Parsing**: Handles both JSON and YAML-like response formats
5. **Markdown Assembly**: Combines all pages into a single Markdown file

## Response Format Handling

The script handles two response formats from the model:

1. **JSON format**: `{"natural_text": "extracted text here"}`
2. **YAML separator format**: `---\nmetadata\n---\nextracted text here`

## Output

The script produces a Markdown file with:
- Each PDF page's content as a separate section
- Clean formatting suitable for documentation, notes, or further processing
- UTF-8 encoding for international character support

## Example

```bash
# Convert a PDF file
python ocr_script.py ~/Documents/research_paper.pdf

# Output will be created at:
# ~/Documents/research_paper.md
```

## Troubleshooting

### Common Issues

1. **LM Studio not running**:
   ```
   Error: Connection refused
   ```
   Solution: Start LM Studio and ensure the API server is enabled

2. **Model not loaded**:
   ```
   Error: Model not found
   ```
   Solution: Load `allenai/olmocr-2-7b` in LM Studio

3. **Memory issues**:
   ```
   Error: CUDA out of memory
   ```
   Solution: Use smaller PDFs or increase LM Studio's context size

### Verbose Mode

To debug, you can add print statements to see the raw response:

```python
# Add this after line 45 in the script
print(f"Raw response for page {page_num}: {content[:200]}...")
```

## Performance Notes

- Processing speed depends on your GPU/CPU and LM Studio settings
- Large PDFs may take several minutes to process
- Memory usage scales with PDF page size and resolution

## Limitations

- Requires LM Studio running locally
- Model may struggle with complex layouts or handwritten text
- Processing is sequential (one page at a time)

## License

This script is provided as-is for educational and personal use.

## Acknowledgments

- [OLMOCR](https://github.com/allenai/olmocr) by AllenAI for the OCR model
- [LM Studio](https://lmstudio.ai/) for local model serving
- [PyPDF](https://pypdf.readthedocs.io/) for PDF handling
