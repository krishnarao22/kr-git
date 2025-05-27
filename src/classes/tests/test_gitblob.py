from ..gitblob import GitBlob

def test_write_blob():
    curr_gb = GitBlob.init_gitblob_from_original_file('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src/notes.txt')
    curr_gb.write_to_file()
    
def test_deserialize_blob():
    curr_gb = GitBlob.init_gitblob_from_blob_file('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src/.kr_git/blobs/01/bb5971dbba0816ebf92895ef63c5302cc8d360')
    print(curr_gb.file_path)
    print(f'SHA1: {curr_gb.sha1}')
    print(curr_gb.binary_data.decode())