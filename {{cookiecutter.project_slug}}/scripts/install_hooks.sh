#!/usr/bin/env bash

GIT_PRE_PUSH='#!/usr/bin/env bash
cd $(git rev-parse --show-toplevel)
uv run --locked make lint && uv run --locked make test && uv run make audit
'

HG_HOOKS='[hooks]
pre-push.lint_test = (cd `hg root`; uv run --locked make lint && uv run --locked make test && uv run make audit)
'

if [ -d '.git' ]; then
    echo "$GIT_PRE_PUSH" > .git/hooks/pre-push
    chmod +x .git/hooks/pre-*
elif ! grep -s -q 'pre-push.lint_test' '.hg/hgrc'; then
    echo "$HG_HOOKS" >> .hg/hgrc
fi
