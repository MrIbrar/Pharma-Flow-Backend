FROM python:3.12-slim

# System dependencies for OpenCV, tesseract, and others
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose the port
EXPOSE 8080

# Gunicorn launch
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
