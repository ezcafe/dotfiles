-- --Set completeopt to have a better completion experience
-- -- menuone: popup even when there's only one match
-- -- noinsert: Do not insert text until a selection is made
-- -- noselect: Do not select, force to select one from the menu
-- vim.opt.completeopt = {'menuone', 'noselect', 'noinsert'}
-- -- shortness: avoid showing extra messages when using completion
-- vim.opt.shortmess = vim.opt.shortmess + { c = true }

-- -- Fixed column for diagnostics to appear
-- -- Show autodiagnostic popup on cursor hover_range
-- -- Goto previous / next diagnostic warning / error
-- -- Show inlay_hints more frequently
-- vim.cmd([[
-- set signcolumn=yes
-- autocmd CursorHold * lua vim.diagnostic.open_float(nil, { focusable = false })
-- ]])

local lsp = require('lsp-zero')

lsp.set_preferences({
    -- Wnables the suggestions of lsp servers when you enter a filetype for the first time
    suggest_lsp_servers = true,
    -- When set to true all installed servers will be initialized on startup
    -- When is set to the string "per-project" only the servers listed with the function .use() will be initialized.
    -- If the value is false servers will be initialized when you call .configure() or .setup_servers().
    setup_servers_on_start = true,
    -- Add keybindings to a buffer with a language server attached
    -- This bindings will trigger actions like go to definition, go to reference, etc.
    set_lsp_keymaps = false,
    -- Use the built-in function vim.diagnostic.config to setup the way error messages are shown in the buffer.
    -- It also creates keymaps to navigate between the location of these errors.
    configure_diagnostics = true,
    -- Tell the language servers what capabilities nvim-cmp supports
    -- https://github.com/VonHeikemen/lsp-zero.nvim#about-nvim-cmp
    cmp_capabilities = true,
    -- Use the default setup for nvim-cmp.
    -- It configures keybindings and completion sources for nvim-cmp.
    manage_nvim_cmp = true,
    -- If set to 'local' it'll try to setup one of the supported installers (nvim-lsp-installer or mason.nvim).
    -- If set to 'lsp-installer' it will setup nvim-lsp-installer.
    -- If set to mason it will setup mason.nvim.
    -- If set to 'global' it will only try to use language servers available globally.
    call_servers = 'local',
    -- They are shown in the "gutter" on the line diagnostics messages are located.
    sign_icons = {
        error = '✘',
        warn = '▲',
        hint = '⚑',
        info = ''
    }
})

lsp.on_attach(function(client, bufnr)
    local bind = vim.keymap.set
    local buf = vim.lsp.buf
    local bufopts = { noremap = true, silent = true, buffer = bufnr }
    local diagnostic = vim.diagnostic

    -- LSP actions
    bind('n', 'gD', buf.declaration, bufopts)
    bind('n', 'gd', buf.definition, bufopts) -- jumps to the definition of the symbol under the cursor
    bind('n', 'gh', buf.hover, bufopts) -- information about the symbol under the cursos in a floating window
    bind('n', 'gi', buf.implementation, bufopts) -- lists all the implementations for the symbol under the cursor in the quickfix window
    bind('n', 'gs', buf.signature_help, bufopts)
    bind('n', 'gt', buf.type_definition, bufopts)
	--bind("n", "<localleader>fn", ":lua vim.lsp.util.rename()<CR>", {}) --> renaname old_fname to new_fname
    bind('n', '<localleader>rn', buf.rename, bufopts)
    bind('n', '<localleader>ca', buf.code_action, bufopts) -- selects a code action available at the current cursor position
    bind('n', 'gr', buf.references, bufopts) -- lists all the references to the symbl under the cursor in the quickfix window
    bind('n', '<localleader>fm', buf.formatting, bufopts) -- formats the current buffer

    --bind('n', '<space>wa', buf.add_workspace_folder, bufopts)
    --bind('n', '<space>wr', buf.remove_workspace_folder, bufopts)
    --bind('n', '<space>wl', function()
    --print(vim.inspect(buf.list_workspace_folders()))
    --end, bufopts)

    -- Diagnostics
    bind('n', 'gl', diagnostic.open_float, bufopts)
    bind('n', '[d', diagnostic.goto_prev, bufopts)
    bind('n', ']d', diagnostic.goto_next, bufopts)
end)

lsp.setup()
