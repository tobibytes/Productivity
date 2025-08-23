from flashcard_utils import FlashCardRedisStreams


fcrs = FlashCardRedisStreams()

if __name__ == "__main__":
    fcrs.listen()
