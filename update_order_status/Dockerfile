FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./update_order_status.py .
CMD ["python", "./update_order_status.py"]