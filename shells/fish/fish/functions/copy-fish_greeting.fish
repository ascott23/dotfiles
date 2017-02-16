# name: spaceship
# A fish theme with spaceships in mind


## Set this options in your config.fish (if you want to)
# set -g theme_display_user yes
# set -g default_user default_username

set -l black      (set_color black)
set -l red        (set_color red)
set -l green      (set_color green)
set -l yellow     (set_color yellow)
set -l blue       (set_color blue)
set -l magenta    (set_color magenta)
set -l cyan       (set_color cyan)
set -l white      (set_color white)
set -l bg_black   (set_color -b black)
set -l bg_red     (set_color -b red)
set -l bg_green   (set_color -b green)
set -l bg_yellow  (set_color -b yellow)
set -l bg_blue    (set_color -b blue)
set -l bg_magenta (set_color -b magenta)
set -l bg_cyan    (set_color -b cyan)
set -l bg_white   (set_color -b white)
set -l normal     (set_color normal)

set newline '
'

function fish_greeting #-d "Greeting message on shell session start up"
    fish_logo
end
