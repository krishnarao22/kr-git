from enum import Enum
from pathlib import Path

class EntryType(Enum):
    BLOB = 1
    TREE = 2

def find_kr_git_root(curr_path: Path) -> str:
    '''
    Finds the .kr_git repo. Used by internal objects to conduct read and write operations.

    Args:
        curr_path: Path object representing the path from which to start the search
    
    Returns:
        Path: the final path of the .kr_git repo
    
    Throws:
        FileNotFoundError: if the .kr_git repo cannot be found
    '''
    while curr_path != curr_path.parent:
        kr_git_path: Path = curr_path / '.kr_git'
        if kr_git_path.is_dir():
            return kr_git_path
        curr_path = curr_path.parent
    raise FileNotFoundError('No parent kr_git repository found')

def find_commit_hash_from_head_file(head_path: str) -> str:
    with open(head_path, 'r') as head_file:
        head_contents = head_file.read()
    return head_contents.split('@')[1]