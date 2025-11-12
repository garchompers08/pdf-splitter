# PDF Splitter

A simple local web application built with Flask that allows you to upload a PDF file, select specific pages or page ranges, and download a new PDF containing only the selected pages.

## Features

- **Upload PDF files** - Simple drag-and-drop interface
- **Select pages** - Choose individual pages or ranges (e.g., "1-3,5,7-10")
- **Download split PDF** - Get a new PDF with only your selected pages
- **Local processing** - All operations happen on your computer, no internet required
- **Clean interface** - Simple and intuitive design
- **Error handling** - Clear error messages for invalid inputs
- **Status messages** - Visual feedback for successful operations

## Requirements

- Python 3.7 or higher
- Flask 3.0.0
- pypdf 3.17.1

## Installation

1. Clone this repository:
```bash
git clone https://github.com/garchompers08/pdf-splitter.git
cd pdf-splitter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to:
   - Click "Choose PDF File" and select your PDF
   - Enter page numbers or ranges (e.g., "1-3,5,7-10")
   - Click "Split PDF" to download the extracted pages

## Page Range Format

You can specify pages in several ways:

- **Single pages**: `1,3,5` - Extracts pages 1, 3, and 5
- **Ranges**: `1-5` - Extracts pages 1 through 5
- **Combined**: `1-3,5,7-10` - Extracts pages 1-3, 5, and 7-10

## Technical Details

- **Backend**: Flask (Python web framework)
- **PDF Processing**: pypdf library
- **Frontend**: HTML, CSS, JavaScript
- **File uploads**: Handled securely with Werkzeug
- **Max file size**: 16 MB

## Project Structure

```
pdf-splitter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Client-side validation
└── uploads/              # Temporary file storage (auto-created)
```

## License

MIT License