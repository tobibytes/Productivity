FROM python:3.13

WORKDIR /app
RUN apt-get update && apt-get install -y \
    libreoffice \
    fonts-dejavu \
    curl \
    wget \
    unzip \
    gnupg \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optional: Ensure soffice is in PATH
ENV PATH="/usr/lib/libreoffice/program:${PATH}"
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]