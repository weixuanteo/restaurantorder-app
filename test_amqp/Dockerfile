FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./test_amqp.py .
COPY ./amqp_setup.py .
CMD ["python", "./test_amqp.py"]