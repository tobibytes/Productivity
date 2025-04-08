FROM python:3.12

WORKDIR /app

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python3", "main.py"]