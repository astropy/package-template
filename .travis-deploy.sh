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

    # Add astropy_helpers manually at the version in the cookiecutter template
    git submodule add https://github.com/astropy/astropy-helpers astropy_helpers || true
    git submodule update --init
    cd astropy_helpers
    # parse the json with jq to get the helpers version
    helpers_version=$(jq -r ".cookiecutter.astropy_helpers_version" $HOME/.cookiecutter_replay/package-template.json)
    git checkout $helpers_version
    cp ah_bootstrap.py ../
    cd ..
    git add astropy_helpers ah_bootstrap.py

    git commit --allow-empty -m "Update rendered version to ""$TRAVIS_COMMIT"
    git push origin master
fi
