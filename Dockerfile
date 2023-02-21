FROM python:3.6

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src/backend /code/app

CMD ["python", "main.py", $SERVER_IP, 8080]
