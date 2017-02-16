#!/bin/bash

# Turns a directory of pictures into a single "comic book file"

find ${1} -type d -not -empty -print0 | while IFS= read -r -d '' dir; do
  if find "$dir" -maxdepth 1 -type f | read f; then
    zip "${2}$(basename "$dir").cbz" "$dir"/*
  fi
done
