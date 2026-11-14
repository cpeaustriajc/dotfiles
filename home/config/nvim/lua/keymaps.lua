local map = vim.keymap.set

map("n", "<leader>w", "<cmd>write<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>quit<cr>", { desc = "Quit window" })
map("n", "<leader>h", "<cmd>nohlsearch<cr>", { desc = "Clear search highlight" })

-- Close the buffer but keep its windows: each one moves to another file buffer,
-- or, when none is open, to the netrw file browser in the closed file's folder.
local function close_buffer()
  local buf = vim.api.nvim_get_current_buf()
  if vim.bo[buf].modified then
    vim.notify("Buffer has unsaved changes; save it first", vim.log.levels.WARN)
    return
  end

  local function usable(b)
    return b ~= buf
      and vim.api.nvim_buf_is_valid(b)
      and vim.bo[b].buflisted
      and vim.bo[b].filetype ~= "netrw"
      and vim.fn.isdirectory(vim.api.nvim_buf_get_name(b)) == 0
  end

  local next_buf = vim.fn.bufnr("#")
  if not usable(next_buf) then
    next_buf = vim.iter(vim.api.nvim_list_bufs()):find(usable)
  end

  for _, win in ipairs(vim.fn.win_findbuf(buf)) do
    vim.api.nvim_win_call(win, function()
      if next_buf then
        vim.api.nvim_win_set_buf(win, next_buf)
      else
        vim.cmd.Explore()
      end
    end)
  end

  if vim.api.nvim_buf_is_valid(buf) then
    vim.cmd.bdelete(buf)
  end
end

map("n", "<leader>bd", close_buffer, { desc = "Close buffer" })

map("n", "<leader>e","<cmd>Explore<cr>", { desc = "Open file browser" })

map("n", "<C-h>", "<C-w>h", { desc = "Move to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Move to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Move to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Move to right window" })

map("n", "[d", function()
  vim.diagnostic.jump({ count = -1, float = true })
end, { desc = "Previous diagnostic" })

map("n", "]d", function()
  vim.diagnostic.jump({ count = 1, float = true })
end, { desc = "Next diagnostic" })

-- Telescope keymaps
map("n", "<leader>ff", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
map("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", { desc = "Live grep" })
map("n", "<leader>fb", "<cmd>Telescope buffers<cr>", { desc = "Find buffers" })
map("n", "<leader>fh", "<cmd>Telescope help_tags<cr>", { desc = "Help tags" })
