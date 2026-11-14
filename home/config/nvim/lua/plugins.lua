-- Neovim 0.12's built-in package manager is available as vim.pack.

if vim.pack == nil then
  vim.notify("vim.pack is unavailable; this config expects Neovim 0.12+", vim.log.levels.WARN)
  return
end

-- Add telescope and its dependencies
vim.pack.add({
  "https://github.com/nvim-lua/plenary.nvim",
  "https://github.com/nvim-telescope/telescope.nvim",
  "https://github.com/neovim/nvim-lspconfig",
})

-- nvim-lspconfig supplies each server's start command, file types and project root markers.
--
-- C: clangd reads the compile database that `meson setup build` writes to
-- build/compile_commands.json, so it checks code with the project's own flags,
-- cross-compiling ones included. Homebrew's clangd matches Homebrew's clang version;
-- the Xcode one (/usr/bin/clangd) is the fallback.
local brew_clangd = "/opt/homebrew/opt/llvm/bin/clangd"
if vim.fn.executable(brew_clangd) == 1 then
  vim.lsp.config("clangd", { cmd = { brew_clangd } })
end

-- Meson: muon checks meson.build files as you type.
vim.lsp.enable({ "clangd", "muon" })

-- Setup telescope with sensible defaults
require("telescope").setup({
  defaults = {
    file_ignore_patterns = { "node_modules", ".git/", ".cache/" },
    sorting_strategy = "ascending",
    layout_config = {
      prompt_position = "top",
    },
  },
  pickers = {
    find_files = {
      hidden = true,
    },
  },
})
