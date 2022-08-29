vim.schedule(function()
  require'core/options'
  require'core/keymaps'
  require'core/native-plugins'
  require'core/auto-commands'
  require'core/user-commands'
  
  require'plugins/packer'
end)
