from ..gitrestore import GitRestore

def test_restore():
    curr_restore_obj = GitRestore('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/restore')
    curr_restore_obj.restore()