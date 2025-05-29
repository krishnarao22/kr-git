'''
Contains the gitblob class, which pertains to the Git BLOB object type
'''
from __future__ import annotations
import zlib
import os
from pathlib import Path
from classes.utils import find_kr_git_root
from classes.gitobj import GitObject

class GitBlob(GitObject):
    '''
    Represents a BLOB object (which is a representation for an individual code file).

    Attributes:
        file_path (str): absolute path of the file that the object is representing.
        binary_data (bytes): Uncompressed binary data of the file's contents.
        sha1 (str): sha1 hash of the GitBlob object. None if the object has not been written to a file yet.
    '''

    def __init__(self):
        '''
        Default constructor, creates an empty object.
        '''
        self.file_path: str = None
        self.binary_data: bytes = None
        self.sha1: str = None

    def serialize(self: GitBlob) -> bytes:
        '''
        Returns uncompressed data to put in the final file

        Args:
            self: the object to serialize
        
        Returns:
            bytes: the serialized (but uncompressed) data to put into the blob file
        '''
        header: bytes = f'blob {self.file_path} {len(self.binary_data)}\0'.encode()
        out: bytes = header + self.binary_data
        return out


    def write_to_file(self: GitBlob) -> None:
        '''
        Takes a GitBlob object, serializes it, compresses it,  and writes it to its appropriate location in .kr_git/blobs/...

        Args:
            self: the object to write to a file
        
        Returns:
            None
        '''
        uncompressed_serialized_content: bytes = self.serialize()
        uncompressed_sha1: str = self.hash(uncompressed_serialized_content)
        compressed_content = zlib.compress(uncompressed_serialized_content)
        kr_git_root_path: Path = find_kr_git_root(Path('.').resolve())
        target_dir_path: Path = kr_git_root_path / 'blobs' / uncompressed_sha1[:2]
        os.makedirs(target_dir_path, exist_ok=True)
        target_file_path: Path = target_dir_path / uncompressed_sha1[2:]
        with open(str(target_file_path), 'wb') as out_file:
            out_file.write(compressed_content)
        self.sha1 = uncompressed_sha1

    @classmethod
    def init_gitblob_from_original_file(cls, target_file_path: str) -> GitBlob:
        '''
        Takes in an original code file (not a serialized blob file) and creates a GitBlob object out of it. This is a class method.

        Args:
            cls: the GitBlob class
            target_file_path (str): the file path of the file to create a GitBlob object out of.
        
        Returns:
            GitBlob: the complete GitBlob object from the target file
        '''
        out_gb_obj: GitBlob = GitBlob()
        out_gb_obj.file_path = target_file_path
        with open(target_file_path, 'rb') as f:
            out_gb_obj.binary_data = f.read()
        return out_gb_obj

    @classmethod
    def init_gitblob_from_blob_file(cls, file_path: str) -> GitBlob:
        '''
        Takes in a serialized blob file (that would be stored in the .kr_git repo) and creates a GitBlob object out of it. This is a class method.
        '''
        decompressed_file_contents: bytes = GitBlob.deserialize(file_path)
        null_byte_idx: int = decompressed_file_contents.find(b'\0')
        serialized_header: bytes = decompressed_file_contents[:null_byte_idx]
        print(serialized_header.decode().split())
        _, curr_file_path, _ = serialized_header.decode().split()
        serialized_blob_contents: bytes = decompressed_file_contents[null_byte_idx + 1:]
        out_gitblob_obj = GitBlob()
        out_gitblob_obj.binary_data = serialized_blob_contents
        out_gitblob_obj.file_path = curr_file_path
        file_path_arr: list[str] = file_path.split('/')
        out_gitblob_obj.sha1 = file_path_arr[-2] + file_path_arr[-1]
        return out_gitblob_obj

    @classmethod
    def init_gitblob_from_blob_hash(cls, blob_hash: str) -> GitBlob:
        kr_git_root_path: str = find_kr_git_root(Path.cwd())
        target_blob_file_path: str = os.path.join(kr_git_root_path, 'blobs', blob_hash[:2], blob_hash[2:])
        return cls.init_gitblob_from_blob_file(target_blob_file_path)
