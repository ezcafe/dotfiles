require 'core/utils/themes'

local maps = {
    -- Normal --
    n = {
        -- Standard Operations
        [";"] = { ":", desc = "Remap ; to :" },
        ["<leader>q"] = { "<cmd>close<cr>", desc = "Close window" },
        ["<leader>c"] = { "<cmd>tabclose<cr>", desc = "Close tab" },
        ["<leader>w"] = { "<cmd>w<cr>", desc = "Save" },
        ["<C-q>"] = { "<cmd>qa<cr>", desc = "Force Quit" },
        --["<C-s>"] = { "<cmd>w<cr>", desc = "Save file" },

        -- Move around splits using Ctrl + {h,j,k,l}
        ["<C-h>"] = { "<C-w>h", desc = "Focus split on the left" },
        ["<C-j>"] = { "<C-w>j", desc = "Focus split on the bottom" },
        ["<C-k>"] = { "<C-w>k", desc = "Focus split on the top" },
        ["<C-l>"] = { "<C-w>l", desc = "Focus split on the right" },

        -- Buffers
        ["<leader>bc"] = { ":bdelete<CR>", desc = "Close buffer" },
        --["<leader>bh"] = { ":bnext<CR>", desc = "Next buffer" },
        --["<leader>bl"] = { ":bprevious<CR>", desc = "Previous buffer" },
        --["<leader>bn"] = { "<cmd>enew<cr>", desc = "New File" },

        -- Explorer
        ["<leader>e"] = { ":Lexplore<cr>", desc = "Open Explore" },
        ["<leader>ec"] = { ":Lexplore %:p:h<cr>", desc = "Open Explore in the directory of the current file" },

        -- Find
        ["<leader>fb"] = { ":Telescope buffers<cr>", desc = "Find Buffers" },
        --["<leader>fc"] = { ":Telescope commands<cr>", desc = "Find Commands" },
        --["<leader>fch"] = { ":Telescope command_history<cr>", desc = "Find Commands History" },
        ["<leader>ff"] = { ":Telescope find_files<cr>", desc = "Find Files" },
        ["<leader>ffh"] = { ":Telescope find_files hidden=true<cr>", desc = "Find Files" },
        ["<leader>fj"] = { ":Telescope jumplist<cr>", desc = "Find Jump List" },
        --["<leader>fk"] = { ":Telescope keymaps<cr>", desc = "Find Keymaps" },
        ["<leader>fm"] = { ":Telescope marks<cr>", desc = "Find Marks" },
        ["<leader>fo"] = { ":Telescope oldfiles<cr>", desc = "Find Oldfiles" },
        --["<leader>fq"] = { ":Telescope quickfix<cr>", desc = "Find Quickfix" },
        --["<leader>fqh"] = { ":Telescope quickfixhistory<cr>", desc = "Find Quickfix History" },
        ["<leader>fr"] = { ":Telescope registers<cr>", desc = "Find Registers" },
        ["<leader>fs"] = { ":Telescope live_grep<cr>", desc = "Find String" },
        ["<leader>fsh"] = { ":Telescope search_history<cr>", desc = "Find String History" },
        --["<leader>ft"] = { ":Telescope tags<cr>", desc = "Find Tags" },
        ["<leader>fw"] = { ":Telescope grep_string<cr>", desc = "Find Word under Cursor" },

        ["<leader>fd"] = { ":Telescope diagnostics bufnr=0<cr>", desc = "Lists Diagnostics" },
        --["<leader>gt"] = { ":Telescope lsp_type_definitions<cr>", desc = "Code Type" },
        --["<leader>gd"] = { ":Telescope lsp_definitions<cr>", desc = "Code Definitions" },
        --["<leader>gr"] = { ":Telescope lsp_references<cr>", desc = "Code References" },
        --["<leader>gi"] = { ":Telescope lsp_implementations<cr>", desc = "Code Implementations" },
        --["<leader>gs"] = { ":Telescope lsp_document_symbols<cr>", desc = "Code Document Symbols" },

        ["<leader>gb"] = { ":Telescope git_branches<cr>", desc = "Git Branches" },
        ["<leader>gc"] = { ":Telescope git_commits<cr>", desc = "Git Commits" },
        ["<leader>gs"] = { ":Telescope git_status<cr>", desc = "Git Status" },
        --["<leader>gst"] = { ":Telescope git_stash<cr>", desc = "Git Stash" },

        -- Gitsigns
        ["<leader>gj"] = { function() require("gitsigns").next_hunk() end, desc = "Next git hunk" },
        ["<leader>gk"] = { function() require("gitsigns").prev_hunk() end, desc = "Previous git hunk" },
        ["<leader>gl"] = { function() require("gitsigns").blame_line() end, desc = "View git blame" },
        ["<leader>gL"] = { function() require("gitsigns").blame_line { full = true } end, desc = "View git blame" },
        ["<leader>gp"] = { function() require("gitsigns").preview_hunk() end, desc = "Preview git hunk" },
        ["<leader>gd"] = { function() require("gitsigns").diffthis() end, desc = "View git diff" },
        ["<leader>gD"] = { function() require("gitsigns").diffthis('~') end, desc = "View git diff" },
        ["<leader>ga"] = { function() require("gitsigns").stage_buffer() end, desc = "Stage git buffer" },
        ["<leader>gu"] = { function() require("gitsigns").reset_buffer_index() end, desc = "Unstage git buffer" },
        ["<leader>gr"] = { function() require("gitsigns").reset_buffer() end, desc = "Reset git buffer" },
        ["<leader>gA"] = { function() require("gitsigns").stage_hunk() end, desc = "Stage git hunk" },
        ["<leader>gU"] = { function() require("gitsigns").undo_stage_hunk() end, desc = "Unstage git hunk" },
        ["<leader>gR"] = { function() require("gitsigns").reset_hunk() end, desc = "Reset git hunk" },

        -- git-conflict
        ["<leader>co"] = { '<Plug>(git-conflict-ours)', desc = "Conflict: Choose Ours" },
        ["<leader>ct"] = { '<Plug>(git-conflict-theirs)', desc = "Conflict: Choose Theirs" },
        ["<leader>cb"] = { '<Plug>(git-conflict-both)', desc = "Conflict: Choose Both" },
        ["<leader>c0"] = { '<Plug>(git-conflict-none)', desc = "Conflict: Choose None" },
        ["<leader>ck"] = { '<Plug>(git-conflict-prev-conflict)', desc = "Conflict: Next" },
        ["<leader>cj"] = { '<Plug>(git-conflict-next-conflict)', desc = "Conflict: Previous" },

        -- Comment
        ["<leader>/"] = { function() require("Comment.api").toggle.linewise.current() end, desc = "Toggle comment line" },

        -- Search
        ["<Esc>"] = { "<cmd>noh<CR>", desc = "Clear highlights" },

        -- Terminal
        -- ["<leader>t"] = { "<cmd>vsplit | terminal<cr>", desc = "Open Terminal" },
        ["<leader>t"] = { "<cmd>lua require('FTerm').toggle()<cr>", desc = "Terminal Toggle" },

        -- Unit test
        -- ["<leader>us"] = { "<cmd>TestSuite<cr>", desc = "Run the whole test suite" },
        -- ["<leader>uf"] = { "<cmd>TestFile<cr>", desc = "Run all tests for the current file" },
        -- ["<leader>ue"] = { "<cmd>TestEdit<cr>", desc = "Edit tests for the current file" },
        -- ["<leader>un"] = { "<cmd>TestNearest<cr>", desc = "Run the test nearest to the cursor" },
        -- ["<leader>ul"] = { "<cmd>TestLast<cr>", desc = "Rerun the latest test" },
        -- ["<leader>uv"] = { "<cmd>TestVisit<cr>", desc = "Open the last run test in the current buffer" },
        -- ["<leader>ui"] = { "<cmd>TestInfo<cr>", desc = "Show an information about the plugin" },

        -- Utils
        ["<C-c>"] = { '"+y', desc = "Copy to clipboard" },
        ["<C-v>"] = { '"+p', desc = "Paste from clipboard" },

        -- end Normal --
    },

    -- Insert --
    i = {
        ["jj"] = { "<Esc>", desc = "Map Esc to jj" },

        -- go to  beginning and end
        ["<C-b>"] = { "<ESC>^i", desc = "beginning of line" },
        ["<C-e>"] = { "<End>", desc = "end of line" },

        -- navigate within insert mode
        ["<C-h>"] = { "<Left>", desc = "move left" },
        ["<C-l>"] = { "<Right>", desc = "move right" },
        ["<C-j>"] = { "<Down>", desc = "move down" },
        ["<C-k>"] = { "<Up>", desc = "move up" },

        -- end Insert --
    },

    -- Visual --
    v = {
        -- Indent text
        ["<"] = { "<gv", desc = "Unindent line" },
        [">"] = { ">gv", desc = "Indent line" },

        -- Comment
        ["<leader>/"] = {
            "<esc><cmd>lua require('Comment.api').toggle.linewise(vim.fn.visualmode())<cr>",
            desc = "Toggle comment line",
        },

        -- Copy and Paste
        ["<C-c>"] = { '"+y', desc = "Copy to clipboard" },
        ["<C-v>"] = { '"+p', desc = "Paste from clipboard" },

        -- end Visual --
    },

    -- Visual block --
    cx = {

        -- Visual block --
    },

    -- Term --
    t = {
        ["<Esc>"] = { "<C-\\><C-n>", desc = "Escape terminal mode" },

        -- Terminal
        -- ["<leader>t"] = { "<cmd>vsplit | terminal<cr>", desc = "Open Terminal" },
        ["<leader>t"] = { "<cmd>lua require('FTerm').toggle()<cr>", desc = "Terminal Toggle" },

        -- end Term --
    },

    -- Command --
    c = {
        ["Ps"] = { "PackerSync", desc = "Packer Sync" },
        -- ["T"] = { "vsplit | terminal", desc = "Open Terminal" },
        ["T"] = { "lua require('FTerm').toggle()", desc = "Terminal Toggle" },
        ["Tc"] = { "lua require('FTerm').exit()", desc = "Terminal Exit" },
        ["Tyc"] = { "lua require('FTerm').run({'yarn', 'commit'})", desc = "Terminal Run yarn commit" },
        ["Tyi"] = { "lua require('FTerm').run({'yarn', 'install'})", desc = "Terminal Run yarn install" },
        ["Tys"] = { "lua require('FTerm').run({'yarn', 'start'})", desc = "Terminal Run yarn start" },
        ["Tyt"] = { "lua require('FTerm').run({'yarn', 'test', vim.api.nvim_buf_get_name(0)})",
            desc = "Terminal Run yarn test" },

        -- diffview
        ["Gs"] = { "DiffviewOpen", desc = "Git status" },
        ["GC"] = { "DiffviewClose", desc = "Git close" },
        ["Gc"] = { "DiffviewFileHistory", desc = "Git commits" },
        ["Gf"] = { "DiffviewFileHistory %", desc = "Git file history" },

        ["Sc"] = { "set ignorecase!", desc = "Toggle Ignore/No Ignore case" },
        -- ["Sn"] = { "set nu!", desc = "Toggle line number" },
        -- ["Ss"] = { "set spell!", desc = "Enable or disable spell checking" },
        --["St"] = { "exec &bg=='light'? 'set bg=dark' : 'set bg=light'", desc = "Switch theme" },
        ["St"] = { "lua ToggleTheme()", desc = "Switch theme" },
        ["Su"] = { "exec &ls==0? 'set cc=80 ls=3 ruler sc smd' : 'set colorcolumn= laststatus=0 noruler noshowcmd noshowmode'",
            desc = "Switch colorcolumn, status line, ..." },

        -- end Command --
    },

}

function setMappings(map_table, base)
    local map = vim.keymap.set

    -- iterate over the first keys for each mode
    for mode, maps in pairs(map_table) do
        -- iterate over each keybinding set in the current mode
        for keymap, options in pairs(maps) do
            -- build the options for the command accordingly
            if options then
                local cmd = options
                if type(options) == "table" then
                    cmd = options[1]
                    options[1] = nil
                else
                    options = {}
                end
                if mode == "c" then
                    vim.cmd(":command! " .. keymap .. " " .. cmd)
                else
                    -- extend the keybinding options with the base provided and set the mapping
                    map(mode, keymap, cmd, vim.tbl_deep_extend("force", options, base or {}))
                end
            end
        end
    end
end

setMappings(maps)
