#!/bin/sh

cd ~
git clone --recursive https://github.com/ezcafe/dotfiles.git ~

# Backup
mv ~/.bash_profile ~/.bash_profile-bk
mv ~/.gitignore ~/.gitignore-bk
mv ~/.zshrc ~/.zshrc-bk

# Symlink configs
ln -sv "~/dotfiles/bash/bash_profile" ~/.bash_profile
ln -sv "~/dotfiles/git/gitignore" ~/.gitignore
ln -sv "~/dotfiles/zsh/zshrc" ~/.zshrc

# Source configs
cd ~/dotfiles && source zsh/zshrc && ..

# VSCode stuffs
mkdir ~/Library/Application\ Support/Code/User
cp ~/dotfiles/vscode/* ~/Library/Application\ Support/Code/User

# Create ws folder
mkdir ~/ws