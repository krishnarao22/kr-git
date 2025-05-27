import sys
from initialization import init_kr_git_repo


if __name__ == '__main__':

    args: list[str] = sys.argv

    assert(len(args) > 1), "kr-git requires at least one argument!"

    # init case
    if sys.argv[1] == 'init':
        init_kr_git_repo()

