#!/usr/bin/env bash

dotfiles="${HOME}/dotfiles"
fisher_path="${dotfiles}/shells/fish/fisherman"
plugins="${fisher_path}/*"

cd ${dotfiles}

# Backup the plugins
cp -r ${fisher_path} ${fisher_path}.bak

for plugin in ${plugins}
do
   path=`realpath --relative-to="${dotfiles}" "${plugin}"`
   url=`grep "url = " "${plugin}/.git/config"`
   git rm -rf ${plugin}
   git submodule add ${url:6} ${path}
done
