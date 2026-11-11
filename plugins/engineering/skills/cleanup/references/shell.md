# Processes and containers

Commands for the process and container steps of `SKILL.md`.

- Prove a process: `kill -0 <pid>` succeeds (alive) and `lsof -a -p <pid> -d cwd` shows this
  checkout.
- Stop it by its PID: `kill <pid>`, never by name or port.
- Containers and volumes this session named: `docker rm -f <name>` and `docker volume rm <name>`.
- Tool config to inventory includes `.claude/launch.json`; evidence includes `test-results/`,
  `artifacts/` and `.claude/work/<topic>/`.
