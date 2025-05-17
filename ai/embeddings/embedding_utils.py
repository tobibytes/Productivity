
import redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from db import Database
from time import sleep

db = Database()
from embedding import EmbeddingService
class EmbeddingRedisService:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port)
        self.index_name = "index"
        self.doc_prefix = "doc:"
        
        
    def create_index(self, vector_dimensions: int):
        try:
            # check to see if index exists
            self.redis.ft(self.index_name).info()
            print("Index already exists!")
        except:
            # schema
            schema = (
                TagField("tag"),                       # Tag Field Name
                VectorField("vector",                  # Vector Field Name
                    "FLAT", {                          # Vector Index Type: FLAT or HNSW
                        "TYPE": "FLOAT32",             # FLOAT32 or FLOAT64
                        "DIM": vector_dimensions,      # Number of Vector Dimensions
                        "DISTANCE_METRIC": "COSINE",   # Vector Search Distance Metric
                    }
                ),
            )

            # index Definition
            definition = IndexDefinition(prefix=[self.doc_prefix], index_type=IndexType.HASH)

            # create Index
            self.redis.ft(self.index_name).create_index(fields=schema, definition=definition)
            
            
    def save_embeddings(self, embeddings, data, tag="openai"):
        pipe = self.redis.pipeline()
        try:
            for i, embedding in enumerate(embeddings):      
                    pipe.hset(f"doc:{data['module_item_id']};notes:{i};email:{str(data['email'])}", mapping = {
                        "vector": embedding.tobytes(),
                        "content": str(data['texts'][i]),
                        "course_id": str(data['course_id']),
                        "module_item_id": str(data['module_item_id']),
                        "email": str(data['email']),
                        "module_id": str(data['module_id']),
                        "tag": str(tag),
                    })
            return pipe.execute()
            
        except Exception as e:
            print('e', e)
        
        
class EmbeddingRedisStreams:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.stream_name = "embeddings_stream"
        self.ers = EmbeddingRedisService()
        # Create consumer group (run once)
        try:
            self.ers.create_index(1536)
            self.redis.xgroup_create(name="ai.tasks", groupname="embedder", id="0", mkstream=True)
            print("Consumer group created.")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Consumer group already exists.")
            else:
                raise
            
    def handle_start_embedding(self, msg_id, data):
        embedding_chunks = []
        for text in data['texts']:
            embedding_chunk = EmbeddingService.generate_embeddings(text)
            embedding_chunks.append(embedding_chunk)
        if embedding_chunks:
            self.ers.save_embeddings(embedding_chunks, data)
            print('completed embedding')
        self.redis.xack("ai.tasks", "embedder", msg_id )
        
            
    def listen(self):
        sleep(2)
        print("starting embedding service")
        while True:
            messages = self.redis.xreadgroup(
                groupname="embedder",
                consumername="worker-1",
                streams={"ai.tasks": ">"},
                count=1,
                block=5000
            )

            if messages:
                for stream, events in messages:
                    for message_id, message_data in events:
                        if message_data["event"] == "start_embedding" or 'embedding' in message_data["event"]:
                            course_id = message_data['course_id']
                            module_id = message_data['module_id']
                            module_item_id = message_data['module_item_id']
                            email = message_data['email']
                            text = db.get_note(module_item_id, email)['note']['analysis']
                            data = {
                                "course_id": course_id,
                                "module_id": module_id,
                                "module_item_id": module_item_id,
                                "email": email,
                                "texts": EmbeddingService.split_text(text)
                            }
                            self.handle_start_embedding(message_id, data)
                            
                            
                            
            else:
                print("No new messages. Waiting...")