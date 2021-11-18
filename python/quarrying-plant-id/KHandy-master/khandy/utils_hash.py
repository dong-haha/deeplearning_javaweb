import hashlib


def calc_hash(content, hash_object=None):
    hash_object = hash_object or hashlib.md5()
    if isinstance(hash_object, str):
        hash_object = hashlib.new(hash_object)
    hash_object.update(content)
    return hash_object.hexdigest()


def calc_file_hash(filename, hash_object=None, chunk_size=1024 * 1024):
    hash_object = hash_object or hashlib.md5()
    if isinstance(hash_object, str):
        hash_object = hashlib.new(hash_object)
    
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_object.update(chunk)
    return hash_object.hexdigest()

    