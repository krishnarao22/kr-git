import os
from pathlib import Path
from classes.gittree import GitTree, GitTreeEntry
from classes.gitcommit import GitCommit
from classes.gitblob import GitBlob
from classes.utils import EntryType, find_kr_git_root, find_commit_hash_from_head_file

class GitRestore:

    def __init__(self, restore_target_dir_path: str):
        self.target_dir_path: str = restore_target_dir_path
        self.kr_git_root: str = find_kr_git_root(Path.cwd())

    def _restore_file(self, blob_sha1: str, current_path: str) -> None:
        curr_blob_object: GitBlob = GitBlob.init_gitblob_from_blob_hash(blob_sha1)
        curr_file_name: str = os.path.basename(curr_blob_object.file_path)
        curr_file_path = os.path.join(current_path, curr_file_name)
        print(f'RESTORING AT {curr_file_path}')
        try:
            with open(curr_file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(curr_blob_object.binary_data.decode())
        except UnicodeDecodeError:
            with open(curr_file_path, 'wb') as out_file:
                out_file.write(curr_blob_object.binary_data)


    def _restore_tree(self, tree_hash: str, current_path: str) -> None:
        curr_tree_object: GitTree = GitTree.init_from_tree_hash(tree_hash)
        print(f'CURR TREE DIRNAME: {curr_tree_object.directory_name}')
        curr_dir_path: str = os.path.join(current_path, curr_tree_object.directory_name)
        print(f'RESTORING TREE AT {curr_dir_path}')
        os.makedirs(curr_dir_path, exist_ok=True)
        for entry_name in curr_tree_object.internal_tree:
            curr_tree_entry: GitTreeEntry = curr_tree_object.internal_tree[entry_name]
            if curr_tree_entry.entry_type == EntryType.BLOB:
                self._restore_file(curr_tree_entry.entry_hash, curr_dir_path)
            elif curr_tree_entry.entry_type == EntryType.TREE:
                self._restore_tree(curr_tree_entry.entry_hash, curr_dir_path)

    def restore(self) -> None:
        target_commit_hash: str = find_commit_hash_from_head_file(os.path.join(self.kr_git_root, 'HEAD'))
        curr_commit_obj: GitCommit = GitCommit.init_from_commit_hash(target_commit_hash)
        self._restore_tree(curr_commit_obj.root_tree_sha1, self.target_dir_path)

