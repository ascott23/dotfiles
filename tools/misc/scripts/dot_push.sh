#!/bin/bash

# Goes and adds + commits + pushes any changes made
# If there's an arg it's added to the commit msg
# Writes all the installed fisherman plugins to a file

DOT_LOC="${HOME}/dotfiles"
FISH_LOC="${DOT_LOC}/shells/fish"
FISHER_LOC="${FISH_LOC}/fisherman"
PLUGIN_FILE="${FISH_LOC}/plugins"

# Fisherman plugins
cd ${FISHER_LOC}

# Clear the file
rm ${PLUGIN_FILE}

# For each directory, echo its name to the plugin file
for i in $(ls -d */);
do
   echo ${i%%/} >> ${PLUGIN_FILE}
done

# Git stuff
cd ${DOT_LOC}

commit_msg="$(date)"

# Append the commit message
if [[ "$#" -eq 1 ]]; then
   commit_msg="${commit_msg} ${1}"
fi

git add --all
git commit -m "$commit_msg"
git push
