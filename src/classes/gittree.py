'''
A module that contains classes that relate to the Git Tree object.

Classes contained:
    1. GitTreeEntry
    2. GitTree
'''

from __future__ import annotations
import os
import zlib
from pathlib import Path
from dataclasses import dataclass
from sortedcontainers import SortedDict
from classes.gitobj import GitObject
from classes.utils import EntryType, find_kr_git_root
from classes.gitblob import GitBlob


@dataclass
class GitTreeEntry():
    '''
    An object representing the entry of a single file/folder in a Git Tree

    Attributes:
        entry_name (str): The name of the entry (file/folder)
        entry_type (EntryType): indicates whether the entry is a BLOB (file) or TREE (folder)
        entry_hash (bytes): The hash of the blob (if file) or tree (if folder)
    '''
    entry_name: str
    entry_type: EntryType
    entry_hash: bytes


class GitTree(GitObject):
    '''
    An object representing a Git Tree.

    Attributes:
        directory_path (str): path to the directory that the tree represents
        internal_tree (SortedDict[str, GitTreeEntry]): A dict from file/folder name to a GitTreeEntry for the given file/folder
        sha1 (str): The sha1 of the tree's contents written to a file. None if the object has not yet been written to a file.
    '''

    def __init__(self):
        self.directory_path: str = None
        self.internal_tree: SortedDict[str, GitTreeEntry] = SortedDict()
        self.sha1 = None

    def serialize(self: GitTree) -> bytes:
        header: bytes = f'TREE {self.directory_path}\0'.encode()
        body = bytearray()
        for git_entry in self.internal_tree.values():
            body.extend(
                f'{git_entry.entry_name} {str(git_entry.entry_type).split('.')[1]} {git_entry.entry_hash}\n'.encode())
        uncompressed_data: bytes = header + bytes(body)
        return uncompressed_data

    @classmethod
    def init_from_tree_file(cls, tree_file_path: str) -> GitTree:
        out_git_tree: GitTree = GitTree()
        uncompressed_contents: bytes = GitTree.deserialize(tree_file_path)
        null_byte_idx: int = uncompressed_contents.find(b'\0')
        header: str = uncompressed_contents[:null_byte_idx].decode()
        _, dir_path = header.split()
        out_git_tree.directory_path = dir_path
        body = uncompressed_contents[null_byte_idx + 1:].decode()

        print(body)

        for entry_line in body.split('\n')[:-1]:
            file_name, entry_type_str, file_sha1 = entry_line.split()
            curr_git_entry: GitTreeEntry = GitTreeEntry(file_name, EntryType[entry_type_str], file_sha1)
            out_git_tree.internal_tree[file_name] = curr_git_entry

        tree_file_path_split: list[str] = tree_file_path.split('/')
        full_tree_sha1: str = tree_file_path_split[-2] + tree_file_path_split[-1]
        out_git_tree.sha1 = full_tree_sha1

        return out_git_tree

    def write_git_tree_to_file(self) -> None:
        kr_git_root: str = find_kr_git_root(Path.cwd())
        uncompressed_data: bytes = self.serialize()
        uncompressed_sha1: bytes = self.hash(uncompressed_data)
        compressed_data: bytes = zlib.compress(uncompressed_data)
        target_dir_path: str = os.path.join(
            kr_git_root, 'trees', uncompressed_sha1[:2])
        os.makedirs(target_dir_path, exist_ok=True)
        target_dir_path: str = os.path.join(
            target_dir_path, uncompressed_sha1[2:])
        with open(target_dir_path, 'wb') as out_file:
            out_file.write(compressed_data)
        self.sha1 = uncompressed_sha1

    @classmethod
    def init_from_directory(cls, directory_path: str, write_trees: bool) -> GitTree:
        curr_tree: GitTree = GitTree()
        for name in os.listdir(directory_path):
            #TODO: implement a more comprehensive check of files and folders to ignore
            if name == '.kr_git':
                continue
            curr_full_path: str = os.path.join(directory_path, name)
            curr_entry: GitTreeEntry = None
            if os.path.isdir(curr_full_path):
                # if we are at a folder
                if name in curr_tree.internal_tree:
                    print(f'Duplicate name found for folder: {name}')
                    continue
                curr_gittree: GitTree = GitTree.init_from_directory(curr_full_path, write_trees)
                curr_entry = GitTreeEntry(name, EntryType.TREE, curr_gittree.sha1)
            elif os.path.isfile(curr_full_path):
                # if we are at a file
                if name in curr_tree.internal_tree:
                    print(f'Duplicate name found for file: {name}')
                    continue
                curr_gitblob: GitBlob = GitBlob.init_gitblob_from_original_file(
                    curr_full_path)
                curr_gitblob.write_to_file()
                curr_entry = GitTreeEntry(
                    name, EntryType.BLOB, curr_gitblob.sha1)
            
            curr_tree.internal_tree[name] = curr_entry

        if write_trees:
            curr_tree.write_git_tree_to_file()

        return curr_tree
