#!/usr/bin/env bash

GIT_PRE_COMMIT='#!/bin/bash
cd $(git rev-parse --show-toplevel)
poetry run make lint
'

GIT_PRE_PUSH='#!/bin/bash
cd $(git rev-parse --show-toplevel)
poetry run make test
'

HG_HOOKS='[hooks]
precommit.lint = (cd `hg root`; poetry run make lint)
pre-push.test = (cd `hg root`; poetry run make test)
'

if [ -d '.git' ]; then
    echo "$GIT_PRE_COMMIT" > .git/hooks/pre-commit
    echo "$GIT_PRE_PUSH" > .git/hooks/pre-push
    chmod +x .git/hooks/pre-*
elif ! grep -s -q 'precommit.lint' '.hg/hgrc'; then
    echo "$HG_HOOKS" >> .hg/hgrc
fi
