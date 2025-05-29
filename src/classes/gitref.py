from __future__ import annotations
import os
from pathlib import Path
from classes.gitobj import GitObject
from classes.utils import find_kr_git_root

class GitRef(GitObject):

    def __init__(self):
        self.ref_name: str = None
        self.target_commit_sha1: str = None

    def serialize(self) -> bytes:
        header: bytes = f'REF {self.ref_name}\0'.encode()
        body: bytes = f'{self.target_commit_sha1}'.encode()
        return header + body

    def write_to_file(self) -> None:
        if not self.ref_name or not self.target_commit_sha1:
            print('Missing fields in ref object. Cannot write to file')
            print(self.ref_name, self.target_commit_sha1)
            return
        uncompressed_content: bytes = self.serialize()
        compressed_content: bytes = self.compress(uncompressed_content)
        target_dir = os.path.join(find_kr_git_root(Path.cwd()), 'refs')
        os.makedirs(target_dir, exist_ok=True)
        target_file_path = os.path.join(target_dir, self.ref_name)
        with open(target_file_path, 'wb') as out_file:
            out_file.write(compressed_content)

    @classmethod
    def init_using_commit_sha1(cls, input_commit_sha1: str, ref_name: str) -> GitRef:
        curr_gr: GitRef = GitRef()
        curr_gr.target_commit_sha1 = input_commit_sha1
        curr_gr.ref_name = ref_name
        return curr_gr

    @classmethod
    def init_from_ref_file(cls, ref_file_path: str) -> GitRef:
        curr_ref_obj: GitRef = GitRef()
        curr_ref_obj.ref_name = os.path.dirname(ref_file_path)
        uncompressed_content: bytes = GitRef.deserialize(ref_file_path)
        null_byte_idx = uncompressed_content.find(b'\0')
        body = uncompressed_content[null_byte_idx + 1:]
        curr_ref_obj.target_commit_sha1 = body.decode()
        return curr_ref_obj

    @classmethod
    def init_from_ref_name(cls, ref_name: str) -> GitRef:
        kr_git_root_path: str = find_kr_git_root(Path.cwd())
        target_path = os.path.join(kr_git_root_path, 'refs', ref_name)
        return cls.init_from_ref_file(target_path)
