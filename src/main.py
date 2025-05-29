#!/usr/bin/env python3

import sys
import command_functions as cmd

def handle_arguments(args: list[str]):

    assert(len(args) > 1), "kr-git requires at least one argument!"

    if sys.argv[1] == 'init':
        cmd.init_kr_git_repo()
    elif sys.argv[1] == 'commit':
        cmd.make_commit()
    elif sys.argv[1] == 'restore':
        assert(len(args) == 2), "For restore, please supply a path in which to restore to (and no other extra arguments)"


if __name__ == '__main__':

    handle_arguments(sys.argv)



    