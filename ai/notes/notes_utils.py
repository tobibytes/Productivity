
import redis
from time import sleep
from notes import NoteSummarizer

from db import Database
db = Database()
class NoteSummarizerRedisStreams:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.stream_name = "notes"
        # Create consumer group (run once)
        try:
            self.redis.xgroup_create(name="ai.tasks", groupname="notes", id="0", mkstream=True)
            print("Consumer group created.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Consumer group already exists.")
            else:
                raise
            
    def handle_note_summarize(self, message_id, data):
        note = NoteSummarizer.analyze(data['text'])
        data.pop('text')
        data['note'] = note
        db.add_note(data)
        self.redis.xack('ai.tasks', "notes", message_id)
        data.pop('note')
        data["event"] = "start_embedding_and_flashcard"
        if '_id' in data:
            data.pop('_id')
        self.redis.xadd('ai.tasks', data)
        
            
    def listen(self):
        sleep(2)
        print("starting note service")
        while True:
            messages = self.redis.xreadgroup(
                groupname="notes",
                consumername="worker-1",
                streams={"ai.tasks": ">"},
                count=1,
                block=5000
            )

            if messages:
                for stream, events in messages:
                    for message_id, message_data in events:
                        if message_data["event"] == "start_note_summary":
                            course_id = message_data['course_id']
                            module_id = message_data['module_id']
                            module_item_id = message_data['module_item_id']
                            email = message_data['email']
                            text = db.get_module_item(module_id, module_item_id)['module_item_markdown']
                            data = {
                                "course_id": str(course_id),
                                "module_id": str(module_id),
                                "module_item_id": str(module_item_id),
                                "email": str(email),
                                "text": str(text)
                            }
                            self.handle_note_summarize(message_id, data)
                            
            else:
                print("No new messages. Waiting...")