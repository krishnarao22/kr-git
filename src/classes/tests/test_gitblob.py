from ..gitblob import GitBlob

def test_write_and_deserialize_blob():
    curr_gb = GitBlob.init_gitblob_from_original_file('/Users/krishnarao/Documents/UIUC/Extracurriculars/projects/kr-git/src/classes/gitrestore.py')
    curr_gb.write_to_file()
    curr_gb = GitBlob.init_gitblob_from_blob_hash(curr_gb.sha1)
    print(curr_gb.file_path)
    print(curr_gb.binary_data.decode())