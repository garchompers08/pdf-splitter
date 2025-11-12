// Update file name display when file is selected
document.getElementById('pdf_file').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'No file chosen';
    document.getElementById('file-name').textContent = fileName;
});

// Form validation
document.getElementById('upload-form').addEventListener('submit', function(e) {
    const fileInput = document.getElementById('pdf_file');
    const pageRanges = document.getElementById('page_ranges');
    
    // Check if file is selected
    if (!fileInput.files || fileInput.files.length === 0) {
        e.preventDefault();
        alert('Please select a PDF file');
        return false;
    }
    
    // Check if page ranges are provided
    if (!pageRanges.value.trim()) {
        e.preventDefault();
        alert('Please enter page ranges');
        return false;
    }
    
    // Validate page range format
    const pageRangePattern = /^[\d\s,-]+$/;
    if (!pageRangePattern.test(pageRanges.value)) {
        e.preventDefault();
        alert('Invalid page range format. Use numbers, hyphens, and commas only (e.g., "1-3,5,7")');
        return false;
    }
    
    // Show loading state
    const submitButton = document.querySelector('.submit-button');
    submitButton.textContent = 'Processing...';
    submitButton.disabled = true;
});

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});
