# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLEXSRFFPROTECTION=false

# Run main.py to prepare data, then launch Streamlit
CMD ["bash", "-c", "python src/main.py && streamlit run src/ui.py"]
