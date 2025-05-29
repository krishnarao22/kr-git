from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime
from classes.gitobj import GitObject
from classes.gittree import GitTree
from classes.utils import find_kr_git_root
class GitCommit(GitObject):
    '''
    An object to represent a git commit.

    Attributes:
        root_tree_sha1 (str): sha1 of the root tree that this commit will point to.
        commit_sha1 (str): sha1 of the contents of the commit. None if the commit has not been written to a file yet
    '''

    def __init__(self):
        self.root_tree_sha1: str = None
        self.commit_sha1: str = None
        self.commit_time: str = None
    
    def serialize(self) -> bytes:
        header: bytes = f'COMMIT {self.commit_time}\0'.encode()
        body: bytes = f'{self.root_tree_sha1}'.encode()
        return header + body
    
    def write_commit_to_file(self) -> None:
        kr_git_root_path: str = find_kr_git_root(Path.cwd())
        
        uncompressed_content: bytes = self.serialize()
        uncompressed_sha1: str = GitCommit.hash(uncompressed_content)
        compressed_content: bytes = GitCommit.compress(uncompressed_content)

        target_file_path: str = os.path.join(kr_git_root_path, 'commits', uncompressed_sha1[:2])
        os.makedirs(target_file_path, exist_ok=True)
        target_file_path = os.path.join(target_file_path, uncompressed_sha1[2:])
        
        with open(target_file_path, 'wb') as out_file:
            out_file.write(compressed_content)
        
        self.commit_sha1 = uncompressed_sha1


    @classmethod
    def init_from_tree_object(cls, root_tree: GitTree) -> GitCommit:
        '''
        Creates a GitCommit object from a GitTree. Instantiates the root_tree_sha1 field, but does not compute the hash of the GitCommit object.

        Args:
            cls: the GitCommit class
            root_tree (GitTree): the object representing the root tree of the repository.

        Returns:
            GitCommit: the GitCommit object representing a commit that uses root_tree as the main tree.
        '''
        if not root_tree.sha1:
            print('Cannot instantiate commit object from tree that has not been written to a file!')
            return
        curr_commit_obj: GitCommit = GitCommit()
        curr_commit_obj.root_tree_sha1 = root_tree.sha1
        curr_commit_obj.commit_time = str(datetime.now())
        return curr_commit_obj

    @classmethod
    def init_from_commit_file(cls, commit_file_path: str) -> GitCommit:
        curr_commit_obj: GitCommit = GitCommit()
        deserialized_content: bytes = GitCommit.deserialize(commit_file_path)
        null_byte_idx: int = deserialized_content.find(b'\0')
        header: str = deserialized_content[:null_byte_idx].decode()
        first_space_idx: int = header.find(' ')
        commit_time = header[first_space_idx + 1:]
        curr_commit_obj.commit_time = commit_time
        body: str = deserialized_content[null_byte_idx + 1:].decode()
        curr_commit_obj.root_tree_sha1 = body.strip()
        split_commit_file_path: list[str] = commit_file_path.split('/')
        curr_commit_obj.commit_sha1 = split_commit_file_path[-2] + split_commit_file_path[-1]
        return curr_commit_obj

    @classmethod
    def init_from_commit_hash(cls, commit_hash: str) -> GitCommit:
        kr_git_root_path: str = find_kr_git_root(Path.cwd())
        commit_file_path: str = os.path.join(kr_git_root_path, 'commits', commit_hash[:2], commit_hash[2:])
        return cls.init_from_commit_file(commit_file_path)
