# Sample Rate Converter V1

A Python-based batch audio sample rate converter.

## Features

- Converts WAV files between sample rates
- Supports 44,100 Hz and 48,000 Hz output
- Batch processes multiple WAV files
- Preserves stereo audio
- Includes quality and aliasing analysis tests

## Usage

Place input WAV files inside the input/ folder and run:
python converter.py
Converted files are written to the output directory.

## Testing

Run the test suite with:
python test_src.py
python test_src_quality.py
python test_src_sweep.py
python test_aliasing.py

## Project Purpose

This project is part of an AI-assisted audio engineering and analysis system focused on reliable, distribution-ready audio processing.


## Requirements

- Python 3.11+
- NumPy
- SciPy
- SoundFile

Install dependencies:

```bash
pip install -r requirements.txt
