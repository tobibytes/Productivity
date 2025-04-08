from redis import Redis
def get_redis(url):
    host = Redis(host=url, port=6379)
    return host

class PubSub:
    def __init__(self, url):
        self.host = get_redis(url)


    def publish_message(self, channel, message):
        self.host.publish(channel, message)
        # print(f"Published: {message} to channel: {channel}")

    def subscribe_to_channel(self, channel):
        pubsub = self.host.pubsub()
        pubsub.subscribe(channel)
        print(f"Subscribed to channel: {channel}")
        for message in pubsub.listen():
            if message["type"] == "message":
                print(f"Received: {message['data'].decode()} from channel: {message['channel'].decode()}")