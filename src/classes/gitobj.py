import hashlib
import zlib
from abc import ABC, abstractmethod

class GitObject(ABC):
    @abstractmethod
    def serialize(self) -> bytes:
        pass

    @classmethod
    def deserialize(cls, file_path: str) -> bytes:
        with open(file_path, 'rb') as f:
            return zlib.decompress(f.read())

    @classmethod
    def hash(cls, data: bytes) -> str:
        return hashlib.sha1(data).hexdigest()
    
    @classmethod
    def compress(cls, data: bytes) -> bytes:
        return zlib.compress(data)
    
