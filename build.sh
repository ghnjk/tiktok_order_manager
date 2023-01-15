#!/usr/bin/env bash

rm -f tiktok_tools.tgz
rm -rf tiktok_tools
mkdir tiktok_tools

cp -r conf tiktok_tools/
cp -r data tiktok_tools/
cp -r libs tiktok_tools/
cp *.py tiktok_tools/
cp *.sh tiktok_tools/
cp *.bat tiktok_tools/
cp *.md tiktok_tools/
cp requirements.txt tiktok_tools/
mkdir tiktok_tools/log
mkdir tiktok_tools/tmp
mkdir tiktok_tools/upload

tar -zcf tiktok_tools.tgz tiktok_tools
rm -rf tiktok_tools
