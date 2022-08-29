#!/bin/sh

git config --global user.name "Your Name"
git config --global user.email you@example.com

# Clone dotfiles
cd ~
git clone --recursive https://github.com/ezcafe/dotfiles.git

# VSCode stuffs
mkdir ~/Library/Application\ Support/Code/User
ln -sv ~/dotfiles/vscode/QDT.code-snippets ~/Library/Application\ Support/Code/User/snippets/QDT.code-snippets
ln -sv ~/dotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json

# Create ws folder
mkdir ~/ws

# Install zsh
# https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH#install-and-set-up-zsh-as-default
# Install ohmyzsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# Install font
# https://github.com/romkatv/powerlevel10k#meslo-nerd-font-patched-for-powerlevel10k
# Install powerlevel10k theme
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git $HOME/.oh-my-zsh/custom/themes/powerlevel10k
# Install zsh-autosuggestions plugin
git clone https://github.com/zsh-users/zsh-autosuggestions $HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions
# Install zsh-syntax-highlighting/ plugin
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

# Update gitconfig + gitignore
echo ~/dotfiles/git/gitconfig >> ~/.gitconfig
echo ~/dotfiles/git/gitignore >> ~/.gitignore

# Add this to .zshrc
echo "source ~/dotfiles/setup" >> ~/.zshrc

# Update
# cd ~/dotfiles && gpr origin main
# git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull

# Uninstall
# powerlevel10k
# https://github.com/romkatv/powerlevel10k#how-do-i-uninstall-powerlevel10k
