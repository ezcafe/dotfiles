function ToggleTheme()
	if vim.o.background == "dark" then
	  vim.o.background = "light"
	else
	  vim.o.background = "dark"
	end
end