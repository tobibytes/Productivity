FROM python:3.13

WORKDIR /app

COPY ai/notes/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy service code and shared module
COPY ai/notes ./
COPY shared ./shared

CMD ["python3", "main.py"]

