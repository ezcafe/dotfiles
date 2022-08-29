-- Automatically install packer
local fn = vim.fn
local install_path = fn.stdpath "data" .. "/site/pack/packer/start/packer.nvim"
if fn.empty(fn.glob(install_path)) > 0 then
    PACKER_BOOTSTRAP = fn.system {
        "git",
        "clone",
        "--depth",
        "1",
        "https://github.com/wbthomason/packer.nvim",
        install_path,
    }
    print "Installing packer close and reopen Neovim..."
    vim.cmd [[packadd packer.nvim]]
end

-- Use a protected call so we don't error out on first use
local status_ok, packer = pcall(require, 'packer')
if not status_ok then
    return
end

-- Have packer use a popup window
packer.init {
    display = {
        open_fn = function()
            return require("packer.util").float { border = "rounded" }
        end,
    },
}

-- Install your plugins here
return packer.startup(function(use)
    ---------------------
    -- Package Manager --
    ---------------------

    use 'wbthomason/packer.nvim'

    ----------------------
    -- Dependencies --
    ----------------------

    -- Improve startup time
    -- Call impatient plugin before all others to improve performance.
    -- Keep this line here.
    use {
        'lewis6991/impatient.nvim',
        config = function() require 'plugins/impatient' end,
    }

    -- Common utils
    use 'nvim-lua/plenary.nvim'

    -- Icons
    -- use 'kyazdani42/nvim-web-devicons'

    ----------------------
    -- UI --
    ----------------------

    -- Colorschemes
    -- use {
    --     'joshdick/onedark.vim',
    --     config = function() require 'plugins/theme-onedark' end
    -- }
    -- use {
    --     "catppuccin/nvim",
    --     as = "catppuccin",
    --     config = function() require 'plugins/theme-catppuccin' end,
    -- }
    use {
        "olimorris/onedarkpro.nvim",
        config = function() require 'plugins/theme-onedarkpro' end,
    }

    -- Whichkey
    -- use 'folke/which-key.nvim'

    -- Install Telescope
    use 'nvim-telescope/telescope.nvim'

    -- Syntax highlighting
    use {
        'nvim-treesitter/nvim-treesitter',
        -- event = { "BufRead", "BufNewFile" }, -- this config has issue with nvim-ts-rainbow
        config = function() require 'plugins/nvim-treesitter' end,
        run = function() require('nvim-treesitter.install').update({ with_sync = true }) end
    }

    -- Context based commenting
    use { 'JoosepAlviste/nvim-ts-context-commentstring', after = 'nvim-treesitter' }
    use {
        'numToStr/Comment.nvim',
        config = function() require 'plugins/comment' end,
    }

    -- Parenthesis highlighting
    use { 'p00f/nvim-ts-rainbow', after = 'nvim-treesitter' }

    -- Indent line
    use {
        'lukas-reineke/indent-blankline.nvim',
        event = "BufRead",
        config = function() require 'plugins/indent-blankline' end,
    }

    -- Highlighting other uses of the word under the cursor
    use 'RRethy/vim-illuminate'

    -- Loading status
    -- use {
    -- 	'j-hui/fidget.nvim',
    -- 	config = function() require 'plugins/fidget' end,
    -- }

    -- use {
    -- 	'nvim-lualine/lualine.nvim',
    -- 	config = function() require 'plugins/lualine' end,
    -- }

    ----------------------
    -- LSP --
    ----------------------

    use {
        'VonHeikemen/lsp-zero.nvim',
        requires = {
            -- LSP Support
            { 'neovim/nvim-lspconfig' },
            { 'williamboman/nvim-lsp-installer' },

            -- Autocompletion
            { 'hrsh7th/nvim-cmp' }, -- Completion framework
            { 'hrsh7th/cmp-buffer' },
            { 'hrsh7th/cmp-path' },
            { 'saadparwaiz1/cmp_luasnip' },
            { 'hrsh7th/cmp-nvim-lsp' }, -- LSP completion source
            { 'hrsh7th/cmp-nvim-lua' },

            -- Snippets
            { 'L3MON4D3/LuaSnip' },
            { 'rafamadriz/friendly-snippets' },
        },
        config = function() require 'plugins/lsp-zero' end
    }

    ---------------------
    -- Git --
    ---------------------

    -- Git integration
    use {
        'lewis6991/gitsigns.nvim',
        event = "BufEnter",
        config = function() require('gitsigns').setup {} end,
    }
    use {
        'sindrets/diffview.nvim',
        config = function() require 'plugins/diffview' end
    }
    use {
        'akinsho/git-conflict.nvim',
        event = "BufEnter",
        config = function() require('plugins/git-conflict') end,
    }

    ---------------------
    -- Utils --
    ---------------------

    -- Unit test - Not working
    -- use {
    -- 	"klen/nvim-test",
    -- 	config = function() require('plugins/nvim-test') end,
    -- }

    -- Terminal
    use {
		'numToStr/FTerm.nvim',
		config = function() require('plugins/FTerm') end,
	}

    -- Automatically set up your configuration after cloning packer.nvim
    -- Put this at the end after all plugins
    if PACKER_BOOTSTRAP then
        require("packer").sync()
    end
end)
