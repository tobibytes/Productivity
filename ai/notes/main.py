from notes_utils import NoteSummarizerRedisStreams

nsrs = NoteSummarizerRedisStreams()

if __name__ == "__main__":
    nsrs.listen()
