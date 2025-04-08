from pubsub import PubSub
from bot import analyze
from db import add_summary_to_db


sub = PubSub("redis")
print('subscriber')
sub.subscribe_to_channel("canvas", analyze, add_summary_to_db)
print('subscriber')