FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./amqp_setup.py .
COPY ./order.py .
CMD ["python", "./order.py"]