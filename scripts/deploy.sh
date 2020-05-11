#!/bin/bash
version=$1
remote_server=$2

if [ -z "$version" -o -z "$remote_server" ]; then
    echo "Usage: $0  version  remote_server"
    exit 1
fi

python setup.py sdist
scp dist/django-xenforo-${version}.tar.gz ${remote_server}:
rm -rf build dist django_xenforo.egg-info
