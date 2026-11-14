local group = vim.api.nvim_create_augroup("starter", { clear = true })

vim.api.nvim_create_autocmd("TextYankPost", {
  group = group,
  callback = function()
    vim.hl.on_yank({ timeout = 120 })
  end,
})

-- Built-in completion and format keys for any language server, such as clangd.
-- Neovim's default LSP keys also apply: K hover, grn rename, gra code action,
-- grr references, gri implementation, gO symbols.
vim.api.nvim_create_autocmd("LspAttach", {
  group = group,
  callback = function(args)
    local client = vim.lsp.get_client_by_id(args.data.client_id)
    if not client then
      return
    end

    if client:supports_method("textDocument/completion") then
      vim.lsp.completion.enable(true, client.id, args.buf, { autotrigger = true })
    end

    vim.keymap.set("n", "gd", vim.lsp.buf.definition, { buffer = args.buf, desc = "Go to definition" })
    vim.keymap.set({ "n", "x" }, "<leader>cf", function()
      vim.lsp.buf.format({ async = true })
    end, { buffer = args.buf, desc = "Format code" })

    if client.name == "clangd" then
      vim.keymap.set("n", "<leader>ch", "<cmd>LspClangdSwitchSourceHeader<cr>", {
        buffer = args.buf,
        desc = "Switch between source and header",
      })
    end
  end,
})

-- Treesitter highlighting for C; Neovim ships the C parser.
vim.api.nvim_create_autocmd("FileType", {
  group = group,
  pattern = { "c" },
  callback = function(args)
    pcall(vim.treesitter.start, args.buf)
  end,
})

vim.api.nvim_create_autocmd("BufReadPost", {
  group = group,
  callback = function()
    local mark = vim.api.nvim_buf_get_mark(0, '"')
    local line_count = vim.api.nvim_buf_line_count(0)

    if mark[1] > 0 and mark[1] <= line_count then
      pcall(vim.api.nvim_win_set_cursor, 0, mark)
    end
  end,
})
