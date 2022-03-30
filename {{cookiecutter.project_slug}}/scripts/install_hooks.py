#!/usr/bin/env python

import sys
from pathlib import Path


GIT_PRE_COMMIT = '''\
#!/bin/bash
cd $(git rev-parse --show-toplevel)
poetry run make lint
'''

GIT_PRE_PUSH = '''\
#!/bin/bash
cd $(git rev-parse --show-toplevel)
poetry run make test
'''

HG_HOOKS = '''
[hooks]
precommit.lint = (cd `hg root`; poetry run make lint)
pre-push.test = (cd `hg root`; poetry run make test)
'''


def install_hooks() -> None:
    parent = Path(__file__).parent.parent
    git_path = parent / '.git'
    hg_path = parent / '.hg'

    if git_path.exists():
        for hook, script in (('pre-commit', GIT_PRE_COMMIT), ('pre-push', GIT_PRE_PUSH)):
            hook_path = git_path / 'hooks' / hook
            with open(hook_path, 'w') as f:
                f.write(script)
            hook_path.chmod(0o755)
    elif hg_path.exists():
        hgrc_path = hg_path / 'hgrc'
        if not hgrc_path.exists() or HG_HOOKS not in hgrc_path.read_text():
            with open(hgrc_path, 'a') as f:
                f.write(HG_HOOKS)
    else:
        sys.exit('No Git or Mercurial repository found')
    return


if __name__ == '__main__':
    install_hooks()
