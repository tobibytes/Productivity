
import redis
from redis.commands.search.field import TagField, VectorField, TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from db import Database
from time import sleep
import sys
from json import dumps, loads

db = Database()
from embedding import EmbeddingService


import re

def escape_tag(value: str) -> str:
    return value.replace('@', r'\@').replace('.', r'\.').replace(' ', r'\ ')
class EmbeddingRedisService:
    def __init__(self, host="redis", port=6379):
        self.redis = redis.Redis(host=host, port=port)
        self.index_name = "myindex"
        self.doc_prefix = "doc:"
        
        
    def create_index(self, vector_dimensions: int):
        try:
            # Check if index exists
            info = self.redis.ft(self.index_name).info()
            print("Indexed fields:", info["attributes"])
            print("ℹ️ Index already exists, dropping and recreating...")
            self.redis.ft(self.index_name).dropindex(delete_documents=False)
        except Exception as e:
            print("ℹ️ Index does not exist or already dropped:", e)

        # Define schema
        schema = (
            TagField("course_id"),
            TagField("tag"),
            TagField("module_item_id"),
            TagField("module_id"),
            TextField("content"),
            TagField("email"),
            VectorField(
                "vector", "FLAT", {
                    "TYPE": "FLOAT32",
                    "DIM": vector_dimensions,
                    "DISTANCE_METRIC": "COSINE",
                }
            ),
        )

        # Define prefix and create index
        definition = IndexDefinition(prefix=["doc:"], index_type=IndexType.HASH)

        self.redis.ft(self.index_name).create_index(fields=schema, definition=definition)
        print("✅ Index created successfully.")
                
    def search(self, data, k=2):
        """
        Search for the nearest neighbors of a given vector in Redis.

        Args:
            data (dict): Dictionary containing the vector and other metadata.
            k (int): Number of nearest neighbors to retrieve.

        Returns:
            list: List of dictionaries containing the search results.
        """
        # Convert the vector to bytes
        vector = data['vector'].tobytes()
        
        # Perform the search
        results = self._search(data, k=k)
        
        return results
            
            
    def _search(self, data, k):
        # Create a query object
            
        # Execute the query
        q_filter = self.prepare_filter(course_id=data.get('course_id', None), module_item_id=data.get('module_item_id', None), module_id=data.get('module_id', None), email=data.get('email', None))
        sys.stdout.write(q_filter)
        sys.stdout.flush()
        
        q = self.prepare_knn_query(k=k, _filter=q_filter)
        q_params = {"vec": data['vector'].tobytes()}
        results = self.redis.ft(self.index_name).search(q, q_params)
        
        # Process the results
        return [
            {
                "content": doc.content,
                "course_id": doc.course_id,
                "module_item_id": doc.module_item_id,
                "module_id": doc.module_id,
            }
            for doc in results.docs
        ]
        
    def prepare_knn_query(self, k: int, return_fields=None, _filter: str = None, vector_field: str= "vector") -> Query:
        """
        Prepares a Redis KNN vector search query using the hybrid search syntax.

        Args:
            vector_field (str): The name of the vector field in your index (e.g., "vector").
            k (int): The number of nearest neighbors to retrieve.
            return_fields (list): List of fields to return. Default includes common fields.
            _filter (str): Optional RedisSearch filter string (e.g., '@course_id:{123}').

        Returns:
            redis.commands.search.query.Query: Prepared Query object.
        """
        if return_fields is None:
            return_fields = [ "content","course_id", "module_id", "module_item_id", "__vector_score"]

        base_query = f"*=>[KNN {k} @{vector_field} $vec]"

        if _filter:
            base_query = f"({_filter})=>[KNN {k} @{vector_field} $vec]"
            sys.stdout.write(base_query)
            sys.stdout.flush()
            

        q = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("__vector_score")
            .paging(0, k)
            .dialect(2)  # Required for hybrid queries with KNN
        )

        return q
    def prepare_filter(self, course_id=None, module_item_id=None, module_id=None, email=None):
        filters = []
        if course_id:
            filters.append(f"@course_id:{{{escape_tag(course_id)}}}")
        if module_item_id:
            filters.append(f"@module_item_id:{{{escape_tag(module_item_id)}}}")
        if email:
            filters.append(f"@email:{{{escape_tag(email)}}}")
        if module_id:
            filters.append(f"@module_id:{{{escape_tag(module_id)}}}")
        return " ".join(filters) if filters else None
        
            
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
        
    def handle_search_embedding(self, msg_id, data):
        contents = self.ers.search(data)
        self.redis.set(f"{data['uuid']}", dumps(contents))
        self.redis.xack("ai.tasks", "embedder", msg_id )
        print('completed search embedding')
            
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
                        if message_data["event"] == "search_embedding":
                            # course_id = message_data['course_id']
                            # module_id = message_data['module_id']
                            # module_item_id = message_data['module_item_id']
                            email = message_data['email']
                            text = message_data['text']
                            vector = EmbeddingService.generate_embeddings(text)
                            data = {
                                # "course_id": course_id,
                                # "module_id": module_id,
                                # "module_item_id": module_item_id,
                                "email": email,
                                "text": text,
                                "vector": vector,
                                "uuid": message_data["uuid"],
                            }
                            self.handle_search_embedding(message_id, data)
                            
                            
                            
                        elif message_data["event"] == "start_embedding" or 'embedding' in message_data["event"]:
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
                                "texts": EmbeddingService.split_text(text),
                                "uuid": message_data["uuid"],
                            }
                            self.handle_start_embedding(message_id, data)
                            
                            
                            
                            
            else:
                print("No new messages. Waiting...")
                
                