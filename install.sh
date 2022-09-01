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
echo "" >> ~/.gitconfig
echo ~/dotfiles/git/gitconfig >> ~/.gitconfig
echo "" >> ~/.gitignore
echo ~/dotfiles/git/gitignore >> ~/.gitignore

# Add this to .zshrc
echo "" >> ~/.zshrc
echo "source ~/dotfiles/setup" >> ~/.zshrc

# Add nvim (Require Iterm or other Terminal simulator to work)
curl --output ~/.config/nvim-macos.tar.gz -L https://github.com/neovim/neovim/releases/download/nightly/nvim-macos.tar.gz
tar xzf ~/.config/nvim-macos.tar.gz
cp -a ~/dotfiles/nvim ~/.config/nvim
echo "" >> ~/.zshrc
echo "source ~/dotfiles/nvim/setup" >> ~/.zshrc

# Add Lite XL
curl -LO https://github.com/lite-xl/lite-xl/releases/download/v2.0.5/lite-xl-macos-x86_64.dmg
# -> Run lite-xl-macos-x86_64.dmg and copy app to destination
# -> Run Lite XL.app
# -> Quit Lite XL.app
cd ~/.config/lite-xl
cp -a ~/dotfiles/lite-xl/init.lua ~/.config/lite-xl/init.lua
git clone https://github.com/lite-xl/lite-xl-colors
git clone https://github.com/lite-xl/lite-xl-plugins
rm -r colors
ln -s lite-xl-colors/colors .
cd ~/.config/lite-xl/plugins
ln -s ../lite-xl-plugins/plugins/autoinsert.lua .
ln -s ../lite-xl-plugins/plugins/bracketmatch.lua .
ln -s ../lite-xl-plugins/plugins/console.lua .
ln -s ../lite-xl-plugins/plugins/formatter.lua .
ln -s ../lite-xl-plugins/plugins/gitdiff_highlight.lua .
ln -s ../lite-xl-plugins/plugins/gitstatus.lua .
ln -s ../lite-xl-plugins/plugins/indentguide.lua .
ln -s ../lite-xl-plugins/plugins/language_containerfile.lua .
ln -s ../lite-xl-plugins/plugins/language_diff.lua .
ln -s ../lite-xl-plugins/plugins/language_env.lua .
ln -s ../lite-xl-plugins/plugins/language_ignore.lua .
ln -s ../lite-xl-plugins/plugins/language_java.lua .
ln -s ../lite-xl-plugins/plugins/language_jsx.lua .
ln -s ../lite-xl-plugins/plugins/language_ts.lua .
ln -s ../lite-xl-plugins/plugins/language_tsx.lua .
ln -s ../lite-xl-plugins/plugins/language_yaml.lua .
ln -s ../lite-xl-plugins/plugins/lint+.lua .
ln -s ../lite-xl-plugins/plugins/lsp.lua .
ln -s ../lite-xl-plugins/plugins/markers.lua .
ln -s ../lite-xl-plugins/plugins/navigate.lua .
ln -s ../lite-xl-plugins/plugins/rainbowparen.lua .
ln -s ../lite-xl-plugins/plugins/selectionhighlight.lua .
ln -s ../lite-xl-plugins/plugins/spellcheck.lua .

# Update
# Powerlevel10k theme
# cd ~/dotfiles && gpr origin main
# git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull
# Lite XL Plugins
# cd ~/.config/lite-xl/lite-xl-plugins
# git pull

# Uninstall
# Powerlevel10k theme
# https://github.com/romkatv/powerlevel10k#how-do-i-uninstall-powerlevel10k
