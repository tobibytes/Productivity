from redis import Redis

def get_redis(url):
    host = Redis(host=url)
    return host