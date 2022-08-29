local status_ok, catppuccin = pcall(require, 'catppuccin')
if not status_ok then
    vim.notify("module catppuccin not found!")
    return
end

vim.g.catppuccin_flavour = "mocha" -- latte, frappe, macchiato, mocha

-- https://github.com/catppuccin/nvim
catppuccin.setup({
    dim_inactive = {
        enabled = true,
        shade = "dark",
        percentage = 0.15,
    },
    transparent_background = false,
    term_colors = true,
    integrations = {
        -- Enable plugins
        cmp = true,
        gitsigns = true,
        indent_blankline = {
            enabled = true,
            colored_indent_levels = true,
        },
        native_lsp = {
            enabled = true,
            virtual_text = {
                errors = { "italic" },
                hints = { "italic" },
                warnings = { "italic" },
                information = { "italic" },
            },
            underlines = {
                errors = { "underline" },
                hints = { "underline" },
                warnings = { "underline" },
                information = { "underline" },
            },
        },
        telescope = true,
        treesitter = true,
        ts_rainbow = true,
		
        -- Diable plugins
        aerial = false,
        barbar = false,
        beacon = false,
        bufferline = false,
        coc_nvim = false,
        dap = {
            enabled = false,
            enable_ui = false,
        },
        dashboard = false,
        fern = false,
        gitgutter = false,
        hop = false,
        leap = false,
        lightspeed = false,
        lsp_saga = false,
        lsp_trouble = false,
        markdown = false,
        mini = false,
        navic = false,
        neogit = false,
        neotree = {
            enabled = false,
            show_root = true,
            transparent_panel = false,
        },
        notify = false,
        nvimtree = {
            enabled = false,
            show_root = true,
            transparent_panel = false,
        },
        overseer = false,
        telekasten = false,
        symbols_outline = false,
        vim_sneak = false,
        vimwiki = false,
		which_key = false,
    },
})

local colorscheme = "catppuccin"

local status_ok, _ = pcall(vim.cmd, "colorscheme " .. colorscheme)
if not status_ok then
    vim.notify("colorscheme " .. colorscheme .. " not found!")
    return
end

vim.api.nvim_create_autocmd("OptionSet", {
    pattern = "background",
    callback = function()
        vim.cmd("Catppuccin " .. (vim.v.option_new == "light" and "latte" or "mocha"))
    end,
})

