#!/bin/bash
set -eva

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
    git checkout rendered
    rsync -avz --delete --exclude .git/ ../packagename/ ./
    git add -A
    git commit -m "Update rendered version to ""$TRAVIS_COMMIT"

    # Add astropy_helpers manually at the version in the cookiecutter template
    git submodule add https://github.com/astropy/astropy-helpers astropy_helpers || true
    git submodule update --init
    cd astropy_helpers
    helpers_version=$(jq -r ".astropy_helpers_version" $base_dir/cookiecutter.json)
    # parse the json with jq to get the helpers version
    git checkout $helpers_version
    cp ah_bootstrap.py ../
    cp ez_setup.py ../
    cd ..
    git add astropy_helpers ah_bootstrap.py
    # we might not have changes to commit
    git commit "Update astropy_helpers to ""$helpers_version" || true
    git push origin rendered
fi
