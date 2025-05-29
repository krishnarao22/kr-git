## KR-Git

A small rebuild of git in python. The binary executable file is under `src/dist`.

The goal of this project was to emulate the key structures of Git. Key objects such as:

* Blobs
* Trees
* Commits
* Refs

have been implemented and can be viewed under the `/src/classes` directory.

These objects are hashed using `sha1`, serialized, compressed using `zlib`, and written to files in the `.kr_git` directory, which is created using the `init` command.

#### Supported Commands

1. `krgit init`

    This simply creates the `.kr_git` directory

2. `krgit commit`

    Commits all the files and folders under the root directory of the repository (where the `.kr_git` directory is). Creates all the blobs and trees and creates a commit object.

3. `krgit restore <target_path>`

    Takes the commit in the `.kr_git/HEAD` file and uses it to reconstruct the entire repository at a specified `target_path`.
