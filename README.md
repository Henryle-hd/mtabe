
# MTABE CLI - Your AI Study Assistant 🎓

MTABE is a powerful CLI tool that helps you study smarter using AI-powered flashcards and tests. It works with various content sources including YouTube videos, web pages, and local files.

## Installation

```bash
pip install mtabe
```

## Features

- 📝 Create AI-powered flashcards from any study material
- 📝 Generate custom tests with various question types
- 📺 Extract content from YouTube video subtitles
- 🌐 Pull study material from web pages
- 📄 Support for multiple file formats (PDF, DOCX, TXT, XLSX, etc.)

## Usage

### Adding Study Notes

```bash
# Add notes by typing/pasting
mtabe add mynotes -t

# Add notes from a YouTube video
mtabe add physics-lecture -y "https://youtube.com/watch?v=xxxxx"

# Add notes from a webpage
mtabe add chemistry-notes -w "https://example.com/chemistry-lesson"

# Add notes from a local file
mtabe add math-formulas -l "path/to/your/file.pdf"
```

### Creating Flashcards

```bash
# Create flashcards from saved notes
mtabe flash -f mynotes

# Create flashcards directly from YouTube
mtabe flash -y "https://youtube.com/watch?v=xxxxx"

# Create flashcards from a webpage
mtabe flash -w "https://example.com/lesson"

# Create flashcards from a local file
mtabe flash -l "path/to/your/file.pdf"
```

### Generating Tests

```bash
# Generate test from saved notes
mtabe test -f mynotes

# Generate test from YouTube content
mtabe test -y "https://youtube.com/watch?v=xxxxx"

# Generate test from a webpage
mtabe test -w "https://example.com/lesson"

# Generate test from a local file
mtabe test -l "path/to/your/file.pdf"
```

## Supported File Formats

- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- Excel spreadsheets (.xlsx, .xls, .xlsm)
- PowerPoint presentations (.pptx)
- CSV files (.csv)

## First-Time Setup

On first use, MTABE will prompt you to:
1. Enter your Groq API key (get it from https://console.groq.com/keys)
2. Provide your name
3. Specify your education level
4. Define your area of focus (IT, CS, Science, etc.)

This information helps MTABE personalize your learning experience.

## Tips for Best Results

- When requesting flashcards, specify the number you want (e.g., "Give me 10 cards")
- For tests, you can specify question types:
  - Multiple choice
  - True/false
  - Essay
  - Fill in the blank
  - Short explanation
  - Short answer
  - Mix of different types

## Example Commands

```bash
# Create 10 flashcards from a YouTube lecture
mtabe flash -y "https://youtube.com/watch?v=xxxxx"

# Generate a mixed test from saved notes
mtabe test -f chemistry-notes

# Add notes from a PDF textbook
mtabe add chapter5 -l "textbook/chapter5.pdf"
```
