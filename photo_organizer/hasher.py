import hashlib
import os


def get_hash(file_path, size_threshold):
    """
    Get the hash of a given file, using either MD5 or just the size in bytes
    If the size is too big, MD5 will not be run and the byte size will be used instead
    - This is to save some power and time, as large files are unlikely to have byte size conflict
    - Also for Cloud files it avoids downloading the file again
    @param file_path: The file path
    @param size_threshold: The threshold of whether the hash should be calculated by MD5 or size
    @return: The MD5 hash or size value
    """
    size = os.path.getsize(file_path)
    if size > size_threshold:
        return str(os.path.getsize(file_path))

    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()
