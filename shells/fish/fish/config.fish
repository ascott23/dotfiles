###############################################################################
#
# Path variable
#
###############################################################################
set PATH $HOME/scripts $PATH
set PATH $HOME/scripts/dotfiles $PATH

###############################################################################
#
# Globals
#
# -x exports to the env, -u makes it universal, and -g makes it global
#
###############################################################################
set -x SVN_EDITOR vim
set -x EDITOR vim

###############################################################################
#
# Theme stuff
#
###############################################################################
set fish_theme spaceship

# Base16 Shell
if status --is-interactive
   eval sh $HOME/.config/base16-shell/scripts/base16-ocean.sh
end


###############################################################################
#
# Other stuff
#
###############################################################################
test -e {$HOME}/.iterm2_shell_integration.fish ; and source {$HOME}/.iterm2_shell_integration.fish
set -g fish_user_paths "/usr/local/opt/openssl@1.1/bin" $fish_user_paths
set -g fish_user_paths "/usr/local/sbin" $fish_user_paths
