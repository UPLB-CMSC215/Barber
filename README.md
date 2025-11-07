# BARBERS ALGORITHM

## Requirements
- Python v3.10.15
- python3-venv
- Pillow
- CustomTkinter
- CairoSVG
- pyinstaller

## Installation (MacOS)
**A.** Install Python using Homebrew
```cli
brew install python@3.10.15
brew install python3-venv
```

> IMPORTANT: Please make sure to install the exact version of Python to prevent threading issues.

**B.** Create a Python virtual environment inside the project directory
```python
python3 -m venv venv
```

**C.** Activate virtual environment
```cli
source venv/bin/activate
```

**D.** Install other requirements
```python
python -m pip install -r requirements.txt
```

**E.** Run the application
```python
python src/studio/main.py
```