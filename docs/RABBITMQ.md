# Dokumentasi Instalasi dengan RabbitMQ

## Instalasi RabbitMQ di Docker
```
$ docker run -d --name rabbitmq \
    -p 5672:5672 -p 15672:15672 \
    -e RABBITMQ_DEFAULT_USER=p3mi \
    -e RABBITMQ_DEFAULT_PASS=password \
    rabbitmq:3-management
```
Untuk membuka management panel, buka `http://<host>:15672` dan gunakan username `p3mi` dan password `password`.

## Instalasi Redis (with persistence) di Docker
```
$ docker volume create redis_data
$ docker run --name redis -d -p 6379:6379 -v redis_data:/data redis redis-server --appendonly yes
```


## Menjalankan Crawler dengan RabbitMQ

Gunakan environment variable `RABBITMQ_URL` untuk mengatur connection string RabbitMQ dan `MONGODB_URI` untuk mengatur connection string MongoDB.


Connection string RabbitMQ memiliki format sebagai berikut:
```
amqp://username:password@host:port/vhost
```

Apabila Anda menjalankan RabbitMQ sesuai perintah Docker di atas, maka connection string akan seperti ini:
```
amqp://p3mi:password@rabbitmq:5672/
```

### Menjalankan dengan Docker

Repo ini dilengkapi dengan Dockerfile yang dapat digunakan untuk menjalankan kode dengan Docker.

#### Build Image
```
$ cd genericwebcrawlerprototype
$ docker build -t p3mi/crawler .
```

#### Run Image (Single Worker)
```
$ docker run -d --name crawler-worker \
    -e RABBITMQ_URL=amqp://p3mi:password@rabbitmq:5672/ \
    -e MONGODB_URL=mongodb://localhost:27017/ \
    p3mi/crawler
```


### Menjalankan dengan Python

#### Install dependencies
```
$ pip install -r requirements.txt
```

#### Run rabbitmq.py
```
$ RABBITMQ_URL=amqp://p3mi:password@rabbitmq:5672/ MONGODB_URL=mongodb://localhost:27017/ python3 rabbitmq.py
```

## Menjalankan Requeuer

Requeuer merupakan service yang akan melakukan pengantrean kembali tautan-tautan yang dihasilkan dari hasil crawling namun belum dicrawl.
Requeuer menggunakan Redis untuk menyimpan daftar URL yang pernah di-crawl.

Kode sumber requeuer ada pada repo [didithilmy/crawler-job-manager](https://gitlab.informatika.org/didithilmy/crawler-job-manager). Lihat README pada repo requeuer untuk panduan pemakaian.