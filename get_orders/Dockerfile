FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./get_orders.py .
CMD ["python", "./get_orders.py"]