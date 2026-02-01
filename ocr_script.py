#!/usr/bin/env python3
"""
PDF to Markdown Converter using OLMOCR

This script converts PDF files to Markdown format using the OLMOCR model
via LM Studio. It extracts text from each page and processes it through
the vision-language model to produce clean Markdown output.

Usage:
    python ocr_script.py /path/to/input.pdf
"""

import json
import re
import asyncio
import sys
import os
from pathlib import Path
from openai import OpenAI
from pypdf import PdfReader
from olmocr.pipeline import build_page_query
from tqdm import tqdm

# Configure LM Studio client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

async def convert_pdf_to_markdown(pdf_path, output_file):
    """
    Convert PDF file to Markdown using OLMOCR model.
    
    Args:
        pdf_path: Path to the input PDF file
        output_file: Path where the Markdown file will be saved
    """
    
    # Initialize PDF reader
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    full_markdown = []

    print(f"Processing {num_pages} pages...")

    # Process each page in the PDF
    for page_num in tqdm(range(1, num_pages + 1)):
        
        # Build query for the current page
        query = await build_page_query(
            pdf_path, 
            page=page_num, 
            target_longest_image_dim=1024, 
            model_name='allenai/olmocr-2-7b@q4_k_m'
        )
        
        # Send request to LM Studio
        response = client.chat.completions.create(**query)
        
        # Extract content from response
        content = response.choices[0].message.content
        
        # Try to parse as JSON (expected format)
        try:
            json_content = json.loads(content)
            if 'natural_text' in json_content:
                full_markdown.append(json_content['natural_text'])
            else:
                # Fallback: use string representation if 'natural_text' key not found
                full_markdown.append(str(json_content))
        except json.JSONDecodeError:
            # If not JSON, try to extract text from YAML-like format
            match = re.search(r'---[\s\S]*?---([\s\S]*)', content)
            if match:
                text_content = match.group(1).strip()
                full_markdown.append(text_content)
            else:
                # Use raw content if no separators found
                full_markdown.append(content)
    
    # Save the accumulated Markdown to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(full_markdown))
    
    print(f"\nConversion complete! File saved at: {output_file}")

def main():
    """
    Main function to handle command-line execution.
    """
    
    # Check if PDF file path was provided
    if len(sys.argv) < 2:
        print("Error: Please provide a PDF file path")
        print("Usage: python ocr_script.py /path/to/input.pdf")
        sys.exit(1)
    
    # Get input PDF path from command line argument
    pdf_input = sys.argv[1]
    
    # Convert to Path object for easier manipulation
    pdf_path = Path(pdf_input)
    
    # Check if file exists
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_input}")
        sys.exit(1)
    
    # Check if file is a PDF
    if pdf_path.suffix.lower() != '.pdf':
        print(f"Error: File is not a PDF: {pdf_input}")
        sys.exit(1)
    
    # Generate output path (same directory, same name with .md extension)
    output_path = pdf_path.with_suffix('.md')
    
    # Check if output file already exists
    if output_path.exists():
        print(f"Warning: Output file already exists: {output_path}")
        overwrite = input("Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Conversion cancelled.")
            sys.exit(0)
    
    print(f"Input PDF: {pdf_path}")
    print(f"Output Markdown: {output_path}")
    
    # Run the conversion
    asyncio.run(convert_pdf_to_markdown(str(pdf_path), str(output_path)))

if __name__ == "__main__":
    main()