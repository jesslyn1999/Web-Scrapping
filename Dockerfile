FROM python:3

ADD ./requirements.txt /crawler/requirements.txt
WORKDIR /crawler
RUN pip install -r requirements.txt

COPY . /crawler

CMD ["python", "-u", "rabbitmq.py"]