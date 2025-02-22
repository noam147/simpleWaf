
MAX_CONNECTION_NUMBER = 19
MINIMAL_CHUNK_SIZE = 20  # in bytes
MAX_CONNECTION_TIME = 20  # in seconds
MAX_TIME_BETWEEN_CHUNKS = 4  # in seconds


def check_connection(connection_number: int):
    print("same ip address connected: "+str(connection_number)+" times")
    if connection_number > MAX_CONNECTION_NUMBER:
        return False
    return True


def check_chunk(chunk_size: int):
    if chunk_size < MINIMAL_CHUNK_SIZE:
        return False
    return True
