import os
from pathlib import Path
from classes.utils import find_kr_git_root
from classes.gittree import GitTree
from classes.gitcommit import GitCommit
from classes.gitref import GitRef
from classes.gitrestore import GitRestore

def init_kr_git_repo() -> None:
    '''
    Initializes the repo file by creating the .git directory
    '''
    try:
        os.mkdir('./.kr_git')
    except(FileExistsError):
        print('There is already a .kr_git folder in this directory – a git repo might already exist.')

def make_commit() -> None:
    '''
    Creates a commit based off the current repository state
    '''
    # TODO: enable using refs other than main
    kr_git_root_path = find_kr_git_root(Path.cwd())
    repo_root_path: Path = Path(kr_git_root_path).parent
    parent_git_tree: GitTree = GitTree.init_from_directory(str(repo_root_path), True)
    # set the parent dir's dirname to None (for restore purposes)
    parent_git_tree.directory_name = None
    current_commit_obj: GitCommit = GitCommit.init_from_tree_object(parent_git_tree)
    current_commit_obj.write_commit_to_file()
    current_ref_obj: GitRef = GitRef.init_using_commit_sha1(current_commit_obj.commit_sha1, 'main')
    current_ref_obj.write_to_file()
    head_file_path: str = os.path.join(kr_git_root_path, 'HEAD')
    with open(head_file_path, 'w', encoding='utf8') as head_file:
        head_file.write(f'main@{current_ref_obj.target_commit_sha1}')
    
def restore(restore_path: str) -> None:
    curr_git_restore_obj: GitRestore = GitRestore(restore_path)
    curr_git_restore_obj.restore()


