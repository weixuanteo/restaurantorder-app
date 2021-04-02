FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./get_restaurant_items.py .
CMD ["python", "./get_restaurant_items.py"]