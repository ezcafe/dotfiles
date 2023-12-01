#!/bin/sh

# npm global
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# Backup
cp ~
mkdir -p my_backups
local bkzshrc="my_backups/.zshrc-bk-$(date +"%Y-%m-%d_%H%M")"
cp .zshrc "$bkzshrc" &>/dev/null

# Clone dotfiles
cd ~
git clone --recursive https://github.com/ezcafe/dotfiles.git

# Create ws folder
mkdir ~/ws

# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
# Do you want to update your shell configuration files? ([y]/n) n

# # Add nvim (Require Iterm or other Terminal simulator to work)
# cd ~/.config
# curl -LO https://github.com/neovim/neovim/releases/download/nightly/nvim-macos.tar.gz
# tar xzf nvim-macos.tar.gz
# cp -a ~/dotfiles/nvim ~/.config/nvim
# echo "" >> ~/.zshrc
# echo "source ~/dotfiles/nvim/setup" >> ~/.zshrc
# source ~/.zshrc

# # Add Lite XL
# cd ~/.config
# curl -LO https://github.com/lite-xl/lite-xl/releases/download/v2.0.5/lite-xl-macos-x86_64.dmg
# # -> Run lite-xl-macos-x86_64.dmg and copy app to destination
# # -> Run Lite XL.app
# # -> Quit Lite XL.app
# cd ~/.config/lite-xl
# cp -a ~/dotfiles/lite-xl/init.lua ~/.config/lite-xl/init.lua
# git clone https://github.com/lite-xl/lite-xl-colors
# git clone https://github.com/lite-xl/lite-xl-plugins
# git clone -b 0.1 https://github.com/lite-xl/lite-xl-lsp
# git clone https://github.com/liquidev/lintplus plugins/lintplus
# git clone https://github.com/lite-xl/lite-xl-widgets widget
# rm -r colors
# ln -s lite-xl-colors/colors .
# cd ~/.config/lite-xl/plugins
# ln -s ../lite-xl-plugins/plugins/autoinsert.lua .
# ln -s ../lite-xl-plugins/plugins/bracketmatch.lua .
# #ln -s ../lite-xl-plugins/plugins/console.lua .
# #ln -s ../lite-xl-plugins/plugins/formatter.lua .
# #ln -s ../lite-xl-plugins/plugins/gitdiff_highlight.lua .
# ln -s ../lite-xl-plugins/plugins/gitstatus.lua .
# ln -s ../lite-xl-plugins/plugins/indentguide.lua .
# ln -s ../lite-xl-plugins/plugins/language_containerfile.lua .
# ln -s ../lite-xl-plugins/plugins/language_diff.lua .
# ln -s ../lite-xl-plugins/plugins/language_env.lua .
# ln -s ../lite-xl-plugins/plugins/language_ignore.lua .
# ln -s ../lite-xl-plugins/plugins/language_java.lua .
# ln -s ../lite-xl-plugins/plugins/language_jsx.lua .
# ln -s ../lite-xl-plugins/plugins/language_ts.lua .
# ln -s ../lite-xl-plugins/plugins/language_tsx.lua .
# ln -s ../lite-xl-plugins/plugins/language_yaml.lua .
# #ln -s ../lite-xl-plugins/plugins/lint+.lua .
# ln -s ../lite-xl-plugins/plugins/lsp.lua .
# ln -s ../lite-xl-lsp/lsp .
# ln -s ../lite-xl-lsp/autocomplete.lua .
# ln -s ../lite-xl-plugins/plugins/markers.lua .
# ln -s ../lite-xl-plugins/plugins/navigate.lua .
# ln -s ../lite-xl-plugins/plugins/rainbowparen.lua .
# ln -s ../lite-xl-plugins/plugins/selectionhighlight.lua .
# ln -s ../lite-xl-plugins/plugins/spellcheck.lua .

# # Update
# # Powerlevel10k theme
# cd ~/dotfiles && gpr origin main
# git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull
# # Lite XL Plugins
# cd ~/.config/lite-xl/lite-xl-plugins
# git pull

# Uninstall
# Powerlevel10k theme
# https://github.com/romkatv/powerlevel10k#how-do-i-uninstall-powerlevel10k
