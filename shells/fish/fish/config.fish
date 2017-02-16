# Path to your oh-my-fish.
# set fish_path $HOME/.oh-my-fish

# Base16 Shell
# if status --is-interactive
#    eval sh $HOME/.config/base16-shell/scripts/base16-default-dark.sh
# end

# Theme
set fish_theme spaceship

set PATH $HOME/scripts $PATH
# set PATH $HOME/.ellipsis/bin $PATH

set -x SVN_EDITOR vi
set -x EDITOR vi


# Which plugins would you like to load? (plugins can be found in ~/.oh-my-fish/plugins/*)
# Custom plugins may be added to ~/.oh-my-fish/custom/plugins/
# Example format: set fish_plugins autojump bundler

# Path to your custom folder (default path is $FISH/custom)
#set fish_custom $HOME/dotfiles/oh-my-fish

# Load oh-my-fish configuration.
# . $fish_path/oh-my-fish.fish

test -e {$HOME}/.iterm2_shell_integration.fish ; and source {$HOME}/.iterm2_shell_integration.fish
