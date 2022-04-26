local status, configs = pcall(require, "nvim-treesitter.configs")
if not status then
  return
end

configs.setup {
  ensure_installed = "maintained",
  sync_install = false,
  ignore_install = { "" },
  highlight = {
    enable = true,
    disable = { "" },
    additional_vim_regex_highlighting = true
  },
  rainbow = {
    enable = true,
    extended_mode = true,
    max_file_lines = nil,
  },
  indent = { enable = true, disable = { "yaml" } },
  context_commentstring = { enable = true, enable_autocmd = false },
}
