local fn = vim.fn
-- Install packer
local install_path = fn.stdpath("data") .. "/site/pack/packer/start/packer.nvim"
if fn.empty(fn.glob(install_path)) > 0 then
	PACKER_BOOTSTRAP = fn.system({
		"git",
		"clone",
		"--depth",
		"1",
		"https://github.com/wbthomason/packer.nvim",
		install_path,
	})
	print("Installing packer.\nPlease reopen Neovim ...")
	vim.cmd([[packadd packer.nvim]])
end

-- Command that reloads neovim when plugins.lua is changed
vim.cmd([[
  augroup packer_user_config
    autocmd!
    autocmd BufWritePost plugins.lua source <afile> | PackerSync
  augroup end
]])

-- Don't error on first use if packer is not installed
local status, packer = pcall(require, "packer")
if not status then
	return
end

-- Have packer use a popup window
packer.init({
	display = {
		open_fn = function()
			return require("packer.util").float({ border = "rounded" })
		end,
	},
})

return packer.startup(function(use)
	-- Plugins Here
	use("wbthomason/packer.nvim") -- Plugin Manager
  use("lewis6991/impatient.nvim")
	use("nvim-lua/popup.nvim") -- Popup Api
	use("nvim-lua/plenary.nvim") -- Functions for other plugins
	use("nvim-telescope/telescope.nvim") -- Searcher
	use("nvim-telescope/telescope-media-files.nvim") -- See media in Telescope
	use({ "nvim-treesitter/nvim-treesitter", run = ":TSUpdate" })
	use("p00f/nvim-ts-rainbow")
	use("JoosepAlviste/nvim-ts-context-commentstring")
	use("windwp/nvim-autopairs")
	use("numToStr/Comment.nvim") -- Comment stuff
	use("lewis6991/gitsigns.nvim")
	use("kyazdani42/nvim-web-devicons")
	use("kyazdani42/nvim-tree.lua")
	use("akinsho/bufferline.nvim")
	use("moll/vim-bbye")
	use("akinsho/toggleterm.nvim")
  use("folke/which-key.nvim")
  use("nvim-lualine/lualine.nvim")
  use("mattn/emmet-vim")

	-- cmp plugins
	use("hrsh7th/nvim-cmp") -- The completion plugin
	use("hrsh7th/cmp-buffer") -- buffer completions
	use("hrsh7th/cmp-path") -- path completions
	use("hrsh7th/cmp-cmdline") -- commandline completions
	use("saadparwaiz1/cmp_luasnip") -- snippet completions
	use("David-Kunz/cmp-npm") -- npm completions
	use("hrsh7th/cmp-nvim-lua") -- nvim lua api completions
	use("hrsh7th/cmp-nvim-lsp") -- cpm lsp completions

	-- lsp plugins
	use("neovim/nvim-lspconfig") -- enable engine
	use("williamboman/nvim-lsp-installer") -- language server installer
	use("jose-elias-alvarez/null-ls.nvim") -- for formatters and linters

	-- snippets
	use("L3MON4D3/LuaSnip") -- snippet engine
	use("rafamadriz/friendly-snippets") -- snippet collection

	-- Colorschemes
	use("ful1e5/onedark.nvim") -- OneDark color scheme

	if PACKER_BOOTSTRAP then
		require("packer").sync()
	end
end)
