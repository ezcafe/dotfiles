local colorscheme = "onedarkpro"

local status_ok, _ = pcall(vim.cmd, "colorscheme " .. colorscheme)
if not status_ok then
    vim.notify("colorscheme " .. colorscheme .. " not found!")
    return
end

require("onedarkpro").setup({
    dark_theme = "onedark_dark", -- The default dark theme: onedark, onedark_vivid, onedark_dark
    light_theme = "onelight", -- The default light theme
    plugins = {
        -- disable all of the plugins
        all = false,

        -- https://github.com/olimorris/onedarkpro.nvim#electric_plug-supported-plugins
        gitsigns = true,
        indentline = true,
        native_lsp = true,
        nvim_cmp = true,
        nvim_ts_rainbow = true,
        packer = true,
        telescope = true,
        treesitter = true,
    },
    options = {
        underline = true, -- Use the colorscheme's opinionated underline styles?
        undercurl = true, -- Use the colorscheme's opinionated undercurl styles?
        cursorline = true, -- Use cursorline highlighting?
        terminal_colors = true, -- Use the colorscheme's colors for Neovim's :terminal?
        window_unfocused_color = true, -- When the window is out of focus, change the normal background?
    }
})

-----------------------------------------------------------------------

---https://github.com/olimorris/onedarkpro.nvim/blob/main/lua/onedarkpro/lib/highlight.lua#L37
---Create highlights the new Neovim way
---@param highlights table
---@return nil
function neovim_hl(highlights, ns_id)
    ns_id = ns_id or 0

    for group, opts in pairs(highlights) do
        local values = {}
        values.fg = opts.fg
        values.bg = opts.bg
        values.sp = opts.sp
        vim.api.nvim_set_hl(ns_id, group, values)
    end
end

-----------------------------------------------------------------------

local colors = require("onedarkpro").get_colors(vim.g.onedarkpro_theme)

local indentline = {
    IndentBlanklineIndent1 = { fg = colors.red },
    IndentBlanklineIndent2 = { fg = colors.orange },
    IndentBlanklineIndent3 = { fg = colors.yellow },
    IndentBlanklineIndent4 = { fg = colors.green },
    IndentBlanklineIndent5 = { fg = colors.blue },
    IndentBlanklineIndent6 = { fg = colors.cyan },
    IndentBlanklineIndent7 = { fg = colors.purple },
}
neovim_hl(indentline)

local nvim_ts_rainbow = {
    rainbowcol1 = { fg = colors.red },
    rainbowcol2 = { fg = colors.orange },
    rainbowcol3 = { fg = colors.yellow },
    rainbowcol4 = { fg = colors.green },
    rainbowcol5 = { fg = colors.blue },
    rainbowcol6 = { fg = colors.cyan },
    rainbowcol7 = { fg = colors.purple },
}
neovim_hl(nvim_ts_rainbow)

