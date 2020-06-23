import os
import traceback
import json
import pika
from src.genericWebCrawler.spiders.crawler import load_scraper, load_scraper_google


AMQP_REQUEST_EXCHANGE = 'crawl_request'
AMQP_FOLLOW_LINKS_EXCHANGE = 'crawl_result_follow_links'


def get_follow_links(results):
    all_follow_links = set()
    for root_url in results:
        crawl_results = results[root_url]
        for crawl_result in crawl_results:
            follow_links = crawl_result.get('FollowLinks', [])
            all_follow_links.update(follow_links)

    return all_follow_links


def publish_follow_links(channel, results):
    print("[*] Publishing follow links to broker")
    follow_links = get_follow_links(results)
    body = json.dumps(list(follow_links))
    channel.basic_publish(exchange=AMQP_FOLLOW_LINKS_EXCHANGE, routing_key='', body=body.encode())
    print("[x] Follow links published")


def message_received(channel, message_body):
    data = json.loads(message_body)
    type = data.get('type', 'url')
    search_query = data.get('search_query')
    keywords = data.get('keywords')
    allowed_domains = data.get('allowed_domains')
    urls = data.get('urls')
    depth = data.get('depth', 0)

    if type == 'search':
        result = load_scraper_google(search_query=search_query, filter_keywords=keywords, allowed_domains=allowed_domains, depth=depth)
    elif type == 'url':
        result = load_scraper(root_urls=urls, filter_keywords=keywords, allowed_domains=allowed_domains, depth=depth)
    else:
        result = None

    if result:
        publish_follow_links(channel, result)

def main():
    rabbitmq_url = os.getenv('RABBITMQ_URL')
    connection_params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters=connection_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=AMQP_FOLLOW_LINKS_EXCHANGE, exchange_type='fanout')

    channel.exchange_declare(exchange=AMQP_REQUEST_EXCHANGE, exchange_type='fanout')
    queue = channel.queue_declare(queue=AMQP_REQUEST_EXCHANGE + '_queue')
    queue_name = queue.method.queue

    channel.queue_bind(exchange=AMQP_REQUEST_EXCHANGE, queue=queue_name)

    print("[*] Waiting for crawl request")

    for method_frame, properties, body in channel.consume(queue_name):
        print('[*] Received message', method_frame, properties, body)
        try:
            message_received(channel, body)
            channel.basic_ack(method_frame.delivery_tag)
        except Exception:
            print(traceback.format_exc())
            channel.basic_nack(method_frame.delivery_tag, requeue=False)

        print("[*] Waiting for crawl request")

if __name__ == "__main__":
    main()
