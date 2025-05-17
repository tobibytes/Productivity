
import redis
from time import sleep

from db import Database
db = Database()

class ControllerRedisStream:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.stream_name = "controller"
        # Create consumer group (run once)
        try:
            self.redis.xgroup_create(name="ai.tasks", groupname="controller", id="0", mkstream=True)
            print("Consumer group created.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Consumer group already exists.")
            else:
                raise
            
    def handle_start_analysis(self, message_id, data):
        data["event"] = "start_note_summary"
        if '_id' in data:
            data.pop('_id')
        self.redis.xadd("ai.tasks", data)
        self.redis.xack('ai.tasks', "analysis", message_id)
        
            
    def listen(self):
        sleep(2)
        print("starting controller service")
        while True:
            messages = self.redis.xreadgroup(
                groupname="controller",
                consumername="worker-1",
                streams={"ai.tasks": ">"},
                count=1,
                block=5000
            )

            if messages:
                for stream, events in messages:
                    for message_id, message_data in events:
                        if message_data["event"] == "start_full_analysis":
                            email = message_data['email']
                            mod_items = db.get_user_courses_modules_module_items_id(email)
                            for mod_item in mod_items:
                                self.handle_start_analysis(message_id, mod_item)
                            
            else:
                print("No new messages. Waiting...")