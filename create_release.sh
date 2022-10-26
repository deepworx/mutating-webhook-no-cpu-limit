#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

if ! [ -z "$(git status --porcelain)" ]; then
    echo "ERROR - Working directory is not clean!"
    exit 2
fi

# get current version
line="$(grep -oP 'version = "[0-9]+[.][0-9]+[.][0-9]+"' pyproject.toml)"
version=($(grep -oP '[0-9]+' <<< $line))
currver=${version[0]}.${version[1]}.${version[2]}

if [ "$1" == "patch" ]; then
    nextver=${version[0]}.${version[1]}.$((${version[2]}+1))
    echo "Create Patch Release ($currver -> $nextver)"
fi

if [ "$1" == "minor" ]; then
    nextver=${version[0]}.$((${version[1]}+1)).0
    echo "Create Minor Release ($currver -> $nextver)"
fi

# Replace in Files
sed -i "s/version = \"[0-9]\+.[0-9]\+.[0-9]\+\"/version = \"$nextver\"/" pyproject.toml
sed -i "s/__version__ = '[0-9]\+.[0-9]\+.[0-9]\+'/__version__ = '$nextver'/" app/__init__.py
sed -i "s/version: [0-9]\+.[0-9]\+.[0-9]\+/version: $nextver/" charts/mutating-webhook-no-cpu-limit/Chart.yaml
sed -i "s/appVersion: [0-9]\+.[0-9]\+.[0-9]\+/appVersion: $nextver/" charts/mutating-webhook-no-cpu-limit/Chart.yaml

git add pyproject.toml app/__init__.py charts/mutating-webhook-no-cpu-limit/Chart.yaml


git commit -am "Change version ${currver} -> ${nextver}"
git tag -a ${nextver} -m "Change version ${currver} -> ${nextver}"

git push --follow-tags
