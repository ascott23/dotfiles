#!/bin/bash

# Goes and pulls + installs dotfiles
# Any args passed to the install script
# Installs any missing fisherman plugins
DOT_LOC="${HOME}/dotfiles"
GIT_REPO="https://github.com/ascott23/dotfiles.git"
FISH_LOC="${DOT_LOC}/shells/fish"
FISHER_LOC="${FISH_LOC}/fisherman"
PLUGIN_FILE="${FISH_LOC}/plugins"

# Git stuff
cd ${HOME}

if [[ ! -d ${DOT_LOC} ]]; then
   # Dotfiles dir doesn't exist
   git clone ${GIT_REPO} ${DOT_LOC}
fi

cd ${DOT_LOC}

git pull

./install "${@}"

# Fisherman plugins
to_install=""

cd ${FISHER_LOC}

# Read the lines of plugin, for the plugins not found in fisherman, add them to the install cmd
while read plugin; do
  if [[ ! -d "${FISHER_LOC}/${plugin}/" ]]; then
     to_install+=" ${plugin}"
  fi
done <${PLUGIN_FILE}

echo "The following plugins were missing:${to_install}"
fish -c "fisher install${to_install}"
