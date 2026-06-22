FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We'll map the source code via volumes during dev or copy it
CMD ["tail", "-f", "/dev/null"]
