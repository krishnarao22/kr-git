from ..gittree import GitTree
from ..gitcommit import GitCommit
from ..gitref import GitRef

def test_write_tree_commit_ref():
    curr_gt = GitTree.init_from_directory('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src', True)
    new_gt = GitTree.init_from_tree_hash(curr_gt.sha1)
    print(new_gt.internal_tree)
    curr_commit = GitCommit.init_from_tree_object(new_gt)
    curr_commit.write_commit_to_file()
    new_commit = GitCommit.init_from_commit_hash(curr_commit.commit_sha1)
    print(new_commit.root_tree_sha1)
    curr_gr = GitRef.init_using_commit_sha1(new_commit.commit_sha1, 'main')
    curr_gr.write_to_file()
    new_gr = GitRef.init_from_ref_name(curr_gr.ref_name)
    print(new_gr.ref_name)
    print(new_gr.target_commit_sha1)
