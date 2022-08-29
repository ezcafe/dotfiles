-- Disable builtin plugins
local disabled_built_ins = {
    --"2html_plugin",
    "bugreport",
    --"compiler",
    --"ftplugin",
    --"getscript",
    --"getscriptPlugin",
    --"gzip",
    --"logipat",
    --"matchit",
    --"netrw",
    --"netrwPlugin",
    --"netrwSettings",
    --"netrwFileHandlers",
    --"optwin",
    --"remote_plugins",
    --"rplugin",
    --"rrhelper",
    --"spellfile_plugin",
    --"synmenu",
    --"tar",
    --"tarPlugin",
    "tutor",
    --"vimball",
    --"vimballPlugin",
    --"zip",
    --"zipPlugin",
}

local g = vim.g

for _, plugin in pairs(disabled_built_ins) do
    g["loaded_" .. plugin] = 1
end

local default_providers = {
    --"node",
    "perl",
    "python3",
    "ruby",
}

for _, provider in ipairs(default_providers) do
    g["loaded_" .. provider .. "_provider"] = 0
end
