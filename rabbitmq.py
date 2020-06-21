import os
import json
import pika
from genericWebCrawler.genericWebCrawler.spiders.crawler import load_scraper

def start_scraping_job(google_query, keywords, allowed_domains=None, depth=0):
    load_scraper(google_query, keywords, allowed_domains, depth)

AMQP_EXCHANGE = 'crawl_request'

def message_received(message_body):
    data = json.loads(message_body)
    type = data.get('type', 'url')
    search_query = data.get('search_query')
    keywords = data.get('keywords')
    allowed_domains = data.get('allowed_domains')
    urls = data.get('urls')
    depth = data.get('depth', 0)

    if type == 'search':
        start_scraping_job(google_query=search_query, keywords=keywords, allowed_domains=allowed_domains, depth=depth)

def main():
    rabbitmq_url = os.getenv('RABBITMQ_URL')
    connection_params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters=connection_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=AMQP_EXCHANGE, exchange_type='fanout')
    queue = channel.queue_declare(queue=AMQP_EXCHANGE + '_queue')
    queue_name = queue.method.queue

    channel.queue_bind(exchange=AMQP_EXCHANGE, queue=queue_name)

    print("[*] Waiting for crawl request")

    for method_frame, properties, body in channel.consume(queue_name):
        print('[*] Received message', method_frame, properties, body)
        try:
            message_received(body)
            channel.basic_ack(method_frame.delivery_tag)
        except Exception as e:
            print("Processing error", e)
            channel.basic_nack(method_frame.delivery_tag, requeue=False)

        print("[*] Waiting for crawl request")

if __name__ == "__main__":
    main()
