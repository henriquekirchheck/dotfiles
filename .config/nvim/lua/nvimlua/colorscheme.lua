colorscheme = "onedark"

local status, colors = pcall(require, colorscheme)

if not status then
  vim.notify("Colorscheme " .. colorscheme .. " not found!")
  return
end

colors.setup({
  hide_inactive_statusline = false,
  highlight_linenumber = false,
  sidebars = {"terminal", "packer"},
  transparent = false,
  comment_style = "NONE",
  keyword_style = "NONE",
  function_style = "NONE",
  variable_style = "NONE",
  dark_sidebar = true,
  dark_float = true,
  hide_end_of_buffer = true,
})

