import os
import traceback
import json
import pika
from src.genericWebCrawler.spiders.crawler import begin_crawl, get_links_from_keyword, init_crawl_request


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


def publish_follow_links(channel, root_urls, results, request_id, keywords='', allowed_domains=None, depth=0):
    print("[*] Publishing follow links to broker")
    follow_links = get_follow_links(results)

    message = {
        'request_id': request_id,
        'root_urls': root_urls,
        'follow_links': list(follow_links),
        'keywords': keywords,
        'allowed_domains': allowed_domains,
        'depth': depth
    }

    body = json.dumps(message)
    channel.basic_publish(exchange=AMQP_FOLLOW_LINKS_EXCHANGE, routing_key='', body=body.encode())
    print("[x] Follow links published")


def message_received(channel, message_body):
    data = json.loads(message_body)
    type = data.get('type', 'url')
    search_query = data.get('search_query')
    keywords = data.get('keywords', '')
    allowed_domains = data.get('allowed_domains')
    root_urls = data.get('urls')
    request_id = data.get('request_id')
    depth = data.get('depth', 0)

    if type == 'search':
        root_urls = get_links_from_keyword(search_query=search_query, filter_keywords=keywords)

        if request_id is None:
            _, request_id = init_crawl_request(search_query=search_query, filter_keywords=keywords, root_urls_list=root_urls)

        results = begin_crawl(request_id=request_id, root_urls=root_urls, filter_keywords=keywords, allowed_domains=allowed_domains, depth=depth, stop_after_crawl=False)
    elif type == 'url':
        if request_id is None:
            _, request_id = init_crawl_request(search_query='', filter_keywords=keywords, root_urls_list=root_urls)

        results = begin_crawl(request_id=request_id, root_urls=root_urls, filter_keywords=keywords, allowed_domains=allowed_domains, depth=depth, stop_after_crawl=False)
    else:
        results = None

    if results:
        publish_follow_links(channel=channel, root_urls=root_urls, results=results,
                             request_id=request_id, keywords=keywords, allowed_domains=allowed_domains, depth=depth)

def main():
    print("[*] Starting up RabbitMQ listener...")
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
