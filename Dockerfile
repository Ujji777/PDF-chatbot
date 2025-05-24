# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system packages needed for OCR + PDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files (optional)
RUN python manage.py collectstatic --noinput || true

# Expose port 8000
EXPOSE 8000

# Run Gunicorn for production server
CMD ["gunicorn", "chatbot_project.wsgi:application", "--bind", "0.0.0.0:8000"]
