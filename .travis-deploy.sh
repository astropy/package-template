#!/bin/bash
set -eva

if [[ "${TRAVIS_PULL_REQUEST}" = "false" && "$TRAVIS_OS_NAME" = "linux" && -z "$EXTRA_CONTEXT" ]]; then
    openssl aes-256-cbc -K $encrypted_c554857c6215_key -iv $encrypted_c554857c6215_iv -in github_deploy_key.enc -out ~/.ssh/publish-key -d
    chmod u=rw,og= ~/.ssh/publish-key
    echo "Host github.com" >> ~/.ssh/config
    echo "  IdentityFile ~/.ssh/publish-key" >> ~/.ssh/config
    cd ../test/packagename
    git --version
    git remote add origin git@github.com:astropy/package-template
    git remote update
    git push origin master:rendered -f
fi
