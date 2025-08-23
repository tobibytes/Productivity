FROM python:3.13

WORKDIR /app

COPY payment/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy service code and shared module
COPY payment ./
COPY shared ./shared

EXPOSE 4242

CMD ["python3", "main.py"]
