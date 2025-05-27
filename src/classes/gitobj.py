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

    def hash(self, data: bytes) -> str:
        return hashlib.sha1(data).hexdigest()
    
