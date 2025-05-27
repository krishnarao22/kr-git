import os

def init_kr_git_repo() -> int:
    '''
    Initializes the repo file by creating the .git directory
    '''
    try:
        os.mkdir('./.kr_git')
    except(FileExistsError):
        print('There is already a .kr_git folder in this directory – a git repo might already exist.')

    #TODO: create a tree object and write to .git dir
    #TODO: create a commit object
