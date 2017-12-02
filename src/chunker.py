
def read_in_chunks(filename, chunk_size):
    with open(filename, 'r') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data
