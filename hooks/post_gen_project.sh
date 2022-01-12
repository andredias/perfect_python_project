#!/bin/bash

poetry update
if [ "{{cookiecutter.version_control}}" == "hg" ]; then
    hg init .
    hg add
    hg commit -m 'Initial project structure'
else
    mv .hgignore .gitignore
    git init .
    sed -i 1d .gitignore
    git add -A .
    git commit -m 'Initial project structure'
fi

poetry run make install_hooks
