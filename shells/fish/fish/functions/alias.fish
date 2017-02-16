function alias -d "Creates a function"
    touch ~/.config/fish/functions/$argv[1].fish
    echo -e "function $argv[1]" > ~/.config/fish/functions/$argv[1].fish
    echo -e "\t$argv[2] \$argv" >> ~/.config/fish/functions/$argv[1].fish
    echo -e "end" >> ~/.config/fish/functions/$argv[1].fish
end
