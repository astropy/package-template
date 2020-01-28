#!/bin/bash
set -evax

if [[ "${TRAVIS_PULL_REQUEST}" = "false" && "$TRAVIS_OS_NAME" = "linux" && $TASK = 'render' ]]; then
    openssl aes-256-cbc -K $encrypted_c554857c6215_key -iv $encrypted_c554857c6215_iv -in github_deploy_key.enc -out ~/.ssh/publish-key -d
    chmod u=rw,og= ~/.ssh/publish-key
    echo "Host github.com" >> ~/.ssh/config
    echo "  IdentityFile ~/.ssh/publish-key" >> ~/.ssh/config

    base_dir=$(pwd)

    cd ../test/
    git clone git@github.com:astropy/package-template rendered
    cd rendered
    git --version
    git config --global user.name "Travis CI"
    git config --global user.email "travis@travis.ci"
    git remote update
    git checkout master
    rsync -avz --delete --exclude .git/ ../packagename/ ./
    git add -A
    git commit --allow-empty -m "Update rendered version to ""$TRAVIS_COMMIT"
    git push origin master
fi
