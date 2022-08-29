# Neovim

## Getting Started

```
# Install Packer
git clone --depth 1 https://github.com/wbthomason/packer.nvim\
 ~/.local/share/nvim/site/pack/packer/start/packer.nvim

# Sync Packages
nvim
:PackerSync
:qa!


```

## Key maps

### Normal mode

#### General

- `ZZ` write the file and exit

#### Moving around [text](https://neovim.io/doc/user/usr_02.html#02.3) and [file](https://neovim.io/doc/user/usr_03.html#03.1)

- `h` go left 1 char
- `j` go down 1 line
- `k` go up 1 line
- `l` go right 1 char

- `<count>h` go left <count> of chars
- `<count>j` go down <count> of lines
- `<count>k` go up <count> of lines
- `<count>l` go right <count> of chars

- `w` go to start of next word
- `e` go to end of next word
- `b` go to start of previous word

- `f<char>` go to first <char> in line (search to the right)
- `F<char>` go to first <char> in line (search to the left)
- `<count>f<char>` go to the <count>th <char> in line

- `0` go to start of line
- `^` go to first char of line
- `$` go to end of line

- `H` go to top of viewport
- `M` go to middle of viewport
- `L` go to bottom of viewport

- `Ctrl + e` scroll down 1 line
- `Ctrl + y` scroll up 1 line
- `Ctrl + u` scroll up half of viewport
- `Ctrl + d` scroll down half of viewport
- `Ctrl + b` scroll up to previous (backwards) viewport
- `Ctrl + f` scroll down to next (forwards) viewport

- `zt` scroll current line to top of viewport
- `zz` scroll current line to middle of viewport
- `zb` scroll current line to bottm of viewport

- `gg` go to start of file
- `G`  go to end of file
- `<count>G` go to the <count>th line

#### [Moving around code block](https://neovim.io/doc/user/usr_29.html)

- `%` go to the matching pair of (), {}, [] or if-else
- `[#` jump to the start if-else
- `]#` jump forward to the next if-else
- `[[` move to the start of outer code block
- `][` to find the end of outer cblock
- `[{` move to start of current block
- `]}` jump to the end

#### [Text editing](https://neovim.io/doc/user/usr_02.html#02.4)

##### Usefull commands

- `.` repeat the last change
- `r` replace char under cursor with 
- `R` replace chars under cursor until Esc

- `c` or `s` change 1 char
- `ciw` change word
- `cc` change line
- `C` change to end of line
- `S` change whole line

- `x` delete char
- `diw` delete word
- `dd` delete line
- `D` delete to end of line

- `p` paste text after cursor
- `P` paste text before cursor
- `xp` swap chars

- `J` delete line break (Join 2 lines)

- `u` undo change
- `U` undo changes in line
- `Ctrl + R` redo change

- `o` open a new line below current line
- `O` open a new line above current line

- `yiw` yank text to register
- `yy` copy (yank) line to register

- `gUiw` make word upper case
- `gUU` or `gUgU` upper case for whole line
- `guiw` make word lower case
- `guu` or `gugu` lower case for whole line
- `g~iw` swap case
- `g~~` or `g~g~` swap case for whole line

- `>>` indent line
- `<count>>>` increase the indent of <count> lines

##### Operator with Position and Count

- `<operator>i<position>` do <operator> inner <position>
- `<operator>a<position>` do <operator> around <position>

Example
- `ci<quote>` change inner <quote> such as "", '' or ``
- `ca<quote>` change <quote> and text inner it
- `di<pair>` delete inner <pair> such as [], {} or ()
- `di<pair>` delete <pair> and text inner it
- `d^` delete to the first char of line
- `d$` delete to end of line
- `<count>r<char>` replace char under cursor with <char>, repeated <count> times
- `d<count>w` delete <count> words once
- `<count>dw` delete one word <count> times
- `<count-1>d<count-2>w` delete <count-2> words, repeated <count-1> times
- `<count>p` paste <count> times

#### [Searching](https://neovim.io/doc/user/usr_03.html#03.8) 

- `*` search word under cursor
- `#` search word under cursor backward

- `/<word>` search <word> in file (search forward)
- `?<word>` search <word> backward in file

- `<count>n` go to next result
- `<count>N` go to previous result

- `/<word>\>` match the end of the word for <word>
- `/\<<word>` match the start of the word for <word>
- `/\<<word>\>` match the whole word for <word>

- `/^<word>` search for <word> at start of line
- `/<word>$` search for <word> at end of line
- `/<char-1>.<char-2>` search for word has 1st char is <char-1> and third char is <char-2>

- `/<Up>` previous search in history
- `/<Down>` next search in history
- `/<char><Up>` previous search start with <char> in history

[More info](https://neovim.io/doc/user/usr_27.html#27.2)

#### [Marks](https://neovim.io/doc/user/usr_03.html#03.10)

- `` `` `` jump to previous position
- `Ctrl + o` jump to the older position
- `Ctrl + i` or `<Tab>` jump to the newer position

- `m<char>` mark the position under cursor as mark <char>
- `` `<char> `` go to mark <char>
- `` '<char> `` go to mark <char>, start of line

##### [Record and playback commands](https://neovim.io/doc/user/usr_10.html#10.1)

### Insert mode

#### [Normal mode command](https://neovim.io/doc/user/usr_24.html#24.10)
- `Ctrl + o + <normal-mode-command>` run Normal mode command in Insert mode

#### [Auto complete](https://neovim.io/doc/user/usr_24.html#24.3)

- `Ctrl + p` show auto complete options
- `Ctrl + x + Ctrl + o` show code completion

By default, Vim searches the following places:

	1. Current file
	2. Files in other windows
	3. Other loaded files (hidden buffers)
	4. Files which are not loaded (inactive buffers)
	5. Tag files
	6. All files #included by the current file

### Command mode

#### General

- `q` quit
- `q!` quit without save
- `wq` write the file and quit

- `'0` back to where you left Vim, use `:marks` to get the numbers
- `browse oldfiles` select file to reopen
- `browse buffer`

- `:<Up>` previous command in history
- `:<Down>` next command in history
- `:<char><Up>` previous command start with <char>

- `Shift + Left` move 1 word left
- `Ctrl + w` delete 1 word
- `Ctrl + u` delete all
- `Ctrl + b` move to begin of text
- `Ctrl _ e` move to end of text
- `Ctrl + c` or `Esc` cancel the command

- `!<shell-program>` execute shell program

#### Replace text - [Substitution](https://neovim.io/doc/user/usr_10.html#10.2)

- `%s/<old-text>/<new-text>/` replace <old-text> with <new-text>, changes only the first occurrence on each line in file
- `%s/<old-text>/<new-text>/g` changes every occurrence on each line in file

- `%s/<old-text>/<new-text>/c` ask you for confirmation before it performs each substitution. At this point, you must enter one of the following answers:

	y		      Yes; make this change.
	n		      No; skip this match.
	a		      All; make this change and all remaining ones without
			      further confirmation.
	q		      Quit; don't make any more changes.
	l		      Last; make this change and then quit.
	CTRL-E		Scroll the text one line up.
	CTRL-Y		Scroll the text one line down.

- `<line>s/<old-text>/<new-text>/` changes texts in 1 line only
- `<from-line>,<to-line>s/<old-text>/<new-text>/` changes texts in range <from-line> to <to-line> only

- `%s/\<<old-text>/<new-text>/g` replace <old-text> which is at the start of a word only (`\<` start of word)
- `%s/\<<old-text>\>/<new-text>/g` replace <old-text> which is matching whole word only (`\<` start of word, `\>` end of word)

- `%s/\s\+$//` remove whitespace at the end of every line (This finds white space characters (\s), 1 or more of them (\+), before the end-of-line ($))

To replace text in many files, we can use [Record and Playback feature](https://neovim.io/doc/user/usr_12.html#12.1)

#### [Command ranges](https://neovim.io/doc/user/usr_10.html#10.3)

- `.<command>` run <command> on current line only
- `.,$<command>` run <command> from cursor to the end
- `%<command>` or `1,$<command>` run <command> from the first to the last line
- `.,.+<number><command>` run <command> from current line to <number> lines down 

We can use pattern in a range.
We can use mouse to select a range (`'<,'>` The '< and '> are actually marks, placed at the start and end of the Visual selection)

#### [The global command](https://neovim.io/doc/user/usr_10.html#10.4)

#### Marks

- `jumps` list of positions
- `marks` list of marks

#### [Tab page](https://neovim.io/doc/user/tabpage.html#tab-page)

- `tab split` open current file in a new tab page
- `tabedit <file>` open <file> in a new tab page
- `tab <command>` run command in a new tab page (ex: tab help gt)
- `gt` switch between tab pages (Goto Tab)
- `split` open a new window - Horizontal
- `split <file>` open <file> in a new window

- `vnew` or `vertical new` open new empty window - Vertical
- `vsplit` open a new window - Vertical
- `vplit <file>` open <file> in a new window - Vertial

- `close` close a window
- `only` close other windows

- `CTRL-W h` move to the window on the left
- `CTRL-W j` move to the window below
- `CTRL-W k` move to the window above
- `CTRL-W l` move to the window on the right
- `CTRL-W t` move to the TOP window
- `CTRL-W b` move to the BOTTOM window

Resize window: Position the mouse pointer on a status line. Now press the left mouse button and drag. The status line will move, thus making the window on one side higher and the other smaller.

#### [Get help](https://neovim.io/doc/user/usr_02.html#02.8)

#### File handling

- `edit <file>` start edit an existing <file>
- `file <file>` change the name of the <file>
- `saveas <file>` save the <file> under a new name

#### [Using an external program](https://neovim.io/doc/user/usr_10.html#10.9)

### [Visual mode](https://neovim.io/doc/user/usr_04.html#04.4)

#### Start Visual mode

From Normal mode, press

- `v` start Visual mode
- `V` select 1 line
- `Ctrl + v` select 1 block

#### Select texts

Use moving keys to select text/line/block in Visual mode

### Explorer

#### General
- `i` change listing style
- `I` toggle banner
- `Ctrl + l` refresh
- `s` change sorting style
- `r` reverse sorting order

#### Navigation

- `Enter` open a file/directory
- `o` Horizontally split window and display file
- `v` Vertically split window and display file
- `t` Open file in a new tab

- `-` go up to the parent directory
- `u` go back to the previous directory in the history
- `gb` jump to the most recent directory saved on the "Bookmarks". To create a bookmark we use `mb`

#### File operations

- `gh` toggle hidden files
- `%` create new file, need to use `write` command to save file
- `R` rename a file
- `d` creates a directory
- `D` or `Del` deletes a file or an empty directory. vim will not let us delete a non-empty directory

### [Sessions](https://neovim.io/doc/user/usr_21.html)

### [Buffers](https://neovim.io/doc/user/usr_22.html#22.4)

- `:ls` or `:buffers` get buffer list
- `:buffer <buffer-number>` load buffer <vuffer-number> in the list
- `:buffer <part-of-file-name>` load buffer by file name
- `:sbuffer <buffer-number>` open buffer in new window

- `:hide` hide a buffer
- `:bnext` go to next buffer
- `:bprevious`	go to previous buffer
- `bdelete <buffer-number>` delete buffer from list

### Register

- `"<char>yiw` yank word into register named <char>
- `Ctrl + r + <char>` paste word in register <char>

### [Abbreviations](https://neovim.io/doc/user/usr_24.html#24.7)

- `:iabbrev <shortcut> <full-word>` add a new shortcut after press Space
- `:iab` is the same as `:iabbrev`
- `:abbreviate` list all abbreviations
- `:unabbreviate <shortcut>` to delete abbreviation
- `:abclear` remove all abbreviation

### [Folding](https://neovim.io/doc/user/usr_28.html)

- `:zfap` fold a paragraph manually
- `:zo` open the fold
- `:zc` close the fold
- `:zr` (reduce) and `zm` (more) to open and close nested folds of several levels.
- `:zR` open all level
- `:zM` close old level
- `:zn` disable folding
- `:zi` to toggle

### [Tags](https://neovim.io/doc/user/usr_29.html)

- `:tag <tag-name>` go to <tag-name> definition
- `Ctrl + ]` go to definition of word under cursor
- `Ctrl + t` or `3 + Ctrl + t` go to the preceding tag

- `:tags` shows the list of tags that you traversed through
- `:tag` or `:<count>tag` go to the tag in the tags list
- `:tag <part-of-tag-name><Tab>` will auto complete tag name 
- `:tnext` jump to next matches for the same tag
- `:tprevious` jump to previous matches for the same tag

- `:stag <tag-name>` open in split window
- `Ctrl + w + ]` open definition of word under cursor in new window

- `:ptag <tag-name>` open a preview window to display <tag-name>
- `:pclose` close preview window
- `CTRL-W }` open definition of word under cursor in preview window

### [Telescopee](https://github.com/nvim-telescope/telescope.nvim#default-mappings)

### [LSP](https://github.com/VonHeikemen/lsp-zero.nvim#default-keybindings-1)

### [nvim-cmp](https://github.com/VonHeikemen/lsp-zero.nvim#default-keybindings)
