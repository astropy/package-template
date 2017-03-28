#!/bin/bash
set -ev
if [[ "${TRAVIS_PULL_REQUEST}" = "false" && "$TRAVIS_OS_NAME" = "linux" ]]; then
    #openssl aes-256-cbc -K $encrypted_b62220aba756_key -iv $encrypted_b62220aba756_iv -in publish-key.enc -out ~/.ssh/publish-key -d
    #chmod u=rw,og= ~/.ssh/publish-key
    #echo "Host github.com" >> ~/.ssh/config
    #echo "  IdentityFile ~/.ssh/publish-key" >> ~/.ssh/config
    git --version
    git remote set-url origin git@github.com:astropy/package-template
    git fetch origin master:master
    git checkout master
fi
