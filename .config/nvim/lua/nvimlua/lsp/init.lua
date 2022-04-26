local status_ok, _ = pcall(require, "lspconfig")
if not status_ok then
  return
end

require "nvimlua.lsp.lsp-installer"
require("nvimlua.lsp.handlers").setup()
require "nvimlua.lsp.null-ls"
