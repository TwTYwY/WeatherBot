FROM python:3.13.2
WORKDIR /app
COPY . .
RUN mkdir ./images
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]