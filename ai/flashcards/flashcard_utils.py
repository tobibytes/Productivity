
import redis
from time import sleep
from flashcard import FlashCardGenerator

from db import Database
db = Database()
class FlashCardRedisStreams:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.stream_name = "flashcards"
        # Create consumer group (run once)
        try:
            self.redis.xgroup_create(name="ai.tasks", groupname="flashcards", id="0", mkstream=True)
            print("Consumer group created.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Consumer group already exists.")
            else:
                raise
            
    def handle_start_flashcard(self, message_id, data):
        flashcards = FlashCardGenerator.generate_flashcards(data['text'])
        data['flashcards'] = flashcards
        data.pop('text')
        db.add_flashcard(data)
        if '_id' in data:
            data.pop('_id')
        self.redis.xack('ai.tasks', "flashcards", message_id)
        
            
    def listen(self):
        sleep(2)
        print("starting flashcard service")
        while True:
            messages = self.redis.xreadgroup(
                groupname="flashcards",
                consumername="worker-1",
                streams={"ai.tasks": ">"},
                count=1,
                block=5000
            )

            if messages:
                for stream, events in messages:
                    for message_id, message_data in events:
                        if message_data["event"] == "start_flashcard" or 'flashcard' in message_data["event"]:
                            course_id = message_data['course_id']
                            module_id = message_data['module_id']
                            module_item_id = message_data['module_item_id']
                            email = message_data['email']
                            text = db.get_note(module_item_id)['note']['analysis']
                            data = {
                                "course_id": course_id,
                                "module_id": module_id,
                                "module_item_id": module_item_id,
                                "email": email,
                                "text": text
                            }
                            self.handle_start_flashcard(message_id, data)
                            
            else:
                print("No new messages. Waiting...")