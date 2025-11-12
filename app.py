from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
import re

app = Flask(__name__)
app.secret_key = 'pdf-splitter-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_page_ranges(page_range_str, max_pages):
    """
    Parse page ranges like "1-3,5,7-9" into a list of page numbers.
    
    Args:
        page_range_str: String containing page ranges
        max_pages: Maximum number of pages in the PDF
    
    Returns:
        List of page numbers (0-indexed) or None if invalid
    """
    pages = set()
    
    # Remove whitespace
    page_range_str = page_range_str.replace(' ', '')
    
    if not page_range_str:
        return None
    
    # Split by comma
    parts = page_range_str.split(',')
    
    for part in parts:
        if '-' in part:
            # Handle range like "1-3"
            try:
                start, end = part.split('-')
                start, end = int(start), int(end)
                
                if start < 1 or end > max_pages or start > end:
                    return None
                
                for page in range(start, end + 1):
                    pages.add(page - 1)  # Convert to 0-indexed
            except ValueError:
                return None
        else:
            # Handle single page like "5"
            try:
                page = int(part)
                if page < 1 or page > max_pages:
                    return None
                pages.add(page - 1)  # Convert to 0-indexed
            except ValueError:
                return None
    
    return sorted(list(pages))


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and PDF splitting."""
    
    # Check if file was uploaded
    if 'pdf_file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['pdf_file']
    
    # Check if filename is empty
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return redirect(url_for('index'))
    
    # Get page ranges
    page_ranges = request.form.get('page_ranges', '')
    
    if not page_ranges:
        flash('Please specify page ranges', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read PDF
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        
        # Parse page ranges
        pages_to_extract = parse_page_ranges(page_ranges, total_pages)
        
        if pages_to_extract is None:
            flash(f'Invalid page ranges. PDF has {total_pages} pages. Use format like "1-3,5,7"', 'error')
            os.remove(filepath)
            return redirect(url_for('index'))
        
        if not pages_to_extract:
            flash('No valid pages selected', 'error')
            os.remove(filepath)
            return redirect(url_for('index'))
        
        # Create new PDF with selected pages
        writer = PdfWriter()
        for page_num in pages_to_extract:
            writer.add_page(reader.pages[page_num])
        
        # Save output file
        output_filename = f"split_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_filepath, 'wb') as output_file:
            writer.write(output_file)
        
        # Clean up original file
        os.remove(filepath)
        
        flash(f'Successfully extracted {len(pages_to_extract)} page(s)', 'success')
        
        # Send file for download
        return send_file(
            output_filepath,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        # Clean up files on error
        if os.path.exists(filepath):
            os.remove(filepath)
        if 'output_filepath' in locals() and os.path.exists(output_filepath):
            os.remove(output_filepath)
        
        flash(f'Error processing PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.after_request
def cleanup_files(response):
    """Clean up temporary files after response is sent."""
    # This will run after the response is sent to client
    # But we can't delete the file being sent, so we'll clean it up on next request
    return response


if __name__ == '__main__':
    print("Starting PDF Splitter Web App...")
    print("Access the app at: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
