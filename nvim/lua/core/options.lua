-- https://neovim.io/doc/user/options.html#options

-- local backup_dir = vim.fn.stdpath('data').."/.cache"

local options = {
    g = {
        mapleader = " ", -- set leader key
		maplocalleader = ",", -- set leader key

        -- Explorer
        netrw_banner = 0, -- Hide the banner
        -- netrw_browse_split = 3, -- Open file in tab
        netrw_liststyle = 3, -- Set tree view
        netrw_winsize = 30, -- Change the size of the Netrw window to 30%

        -- end g
    },
    opt = {
        -- General
        errorbells = true,
        mouse = 'a', -- Enable mouse support for all modes
        -- shada = "'100,<50,f50,n"..backup_dir.."/shada/shada",
        timeoutlen = 300, -- Time in milliseconds to wait for a mapped sequence to complete.
        updatetime = 300, -- Length of time to wait before triggering the plugin
        visualbell = true,

        -- Neovim UI
		background = 'dark',
        -- colorcolumn = '80',
        cursorline = true, -- Highlight the text line of the cursor
        --fillchars = { eob = " " }, -- Disable `~` on nonexistent lines
        number = true, -- Show line number
        relativenumber = true, -- Show relative line number
        showmatch = true, -- Highlight matching parenthesis
        signcolumn = 'yes', -- Always show the sign column
        splitbelow = true, -- Horizontal split to the bottom
        splitright = true, -- Vertical split to the right
        syntax = 'on', -- Allow syntax highlighting
        termguicolors = true, -- Enable 24-bit RGB colors

        -- Statusline
        laststatus = 0, -- Hide status line
        ruler = false, -- Hide the location and scroll position
        statusline = '%{expand("%:p:h:t")}/%t%m %= %l,%c',

        -- Folding
        foldcolumn = 'auto', -- show a small column on the left of the window to indicate folds
        -- foldmethod = 'indent', -- Folding by indent

        -- Wrap
        -- linebreak = true, -- Break whole word
        -- colorcolumn = '80', -- Highlight column at 80
        -- go to previous/next line with h,l,left arrow and right arrow
        -- when cursor reaches end/beginning of line
        whichwrap = "<>[]hl",
        wrap = false,

        -- Tabs, indent
        copyindent = true, -- Copy whatever characters were used for indenting on the existing line
        breakindent = true, -- Every wrapped line will continue visually indented
        expandtab = true, -- Use spaces instead of tabs
        preserveindent = true, -- Preserve indent structure as much as possible
        shiftwidth = 4, -- Shift 4 spaces when tab
        smartindent = true, -- Autoindent new lines
        tabstop = 4, -- 1 tab == 4 spaces

        -- Memory, CPU
        history = 50, -- Remember N lines/commands in history
        lazyredraw = true, -- Faster scrolling
        synmaxcol = 240, -- Max column for syntax highlight

        -- end opt
    }
}

function setOptions(options)
    for scope, table in pairs(options) do
        for setting, value in pairs(table) do
            vim[scope][setting] = value
        end
    end
end

setOptions(options)
