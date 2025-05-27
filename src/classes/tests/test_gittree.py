from ..gittree import GitTree

# def test_write_tree():
#     curr_gt = GitTree.init_from_directory('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src', True)
#     print(curr_gt.sha1)

def test_init_from_tree_file():
    curr_gt = GitTree.init_from_tree_file('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src/.kr_git/trees/75/2f4f44ca7bd33df622eccbdd0baf6990cc0c20')
    print(curr_gt.internal_tree)