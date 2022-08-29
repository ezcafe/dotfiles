require('lualine').setup {
    options = {
        theme = 'catppuccin',
        globalstatus = true,
        component_separators = { left = '', right = '' },
        section_separators = { left = '', right = '' },
    },
    sections = {
        lualine_a = { 'branch' },
        lualine_b = { 'filename' },
        lualine_c = { 'diff' },
        lualine_x = { {
            'diagnostics',
            symbols = {
                error = ' ',
                warn = ' ',
                info = ' ',
                hint = 'ﴞ ',
            }
        } },
        lualine_y = { 'location' },
        lualine_z = { 'os.date("%H:%M")' }
    },
    inactive_sections = {
        lualine_a = {},
        lualine_b = {},
        lualine_c = {},
        lualine_x = {},
        lualine_y = {},
        lualine_z = {}
    },
    tabline = {},
    winbar = {},
    inactive_winbar = {},
    extensions = {}
}

