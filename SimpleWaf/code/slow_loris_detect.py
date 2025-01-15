
MAX_CONNECTION_NUMBER = 5
MINIMAL_CHUNK_SIZE = 20  # in bytes
MAX_CONNECTION_TIME = 20  # in seconds
MAX_TIME_BETWEEN_CHUNKS = 4  # in seconds


def check_connection(connection_number: int):
<<<<<<< HEAD
    print(connection_number)
=======
>>>>>>> c81f28f (fixed conflict in routing)
    if connection_number > MAX_CONNECTION_NUMBER:
        return False
    return True


def check_chunk(chunk_size: int):
    if chunk_size < MINIMAL_CHUNK_SIZE:
        return False
    return True
