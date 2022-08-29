local status_ok, indent_blankline = pcall(require, "indent_blankline")
if not status_ok then return end

indent_blankline.setup {
    char_list = { '|', '¦', '┆', '┊' },
    context_highlight_list = {
        'IndentBlanklineIndent1',
        'IndentBlanklineIndent2',
        'IndentBlanklineIndent3',
        'IndentBlanklineIndent4',
        'IndentBlanklineIndent5',
        'IndentBlanklineIndent6',
		'IndentBlanklineIndent7',
    },
    context_patterns = {
        "declaration", "expression", "jsx_element",
        "jsx_self_closing_element", "^object", "pattern", "primary_expression",
        "statement", "switch_body"
    },
    show_current_context = true,
    use_treesitter = true,
}
