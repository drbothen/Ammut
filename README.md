## Ammut – Development Guide (Dev Container + uv Workspace)

This repo is a Python monorepo managed with uv and a VS Code Dev Container.

### Prerequisites
- Docker + VS Code with "Dev Containers" extension

### Open the Dev Container
1. In VS Code: Command Palette → "Dev Containers: Reopen in Container".
2. Post-create steps will:
   - Install uv and ensure it’s on PATH
   - Create `.venv` (Python 3.12)
   - Run `uv sync --workspace` to install all deps

### Project Layout
- Root workspace: `pyproject.toml`
  - `[tool.uv.workspace].members = ["src/agent", "src/mcp", "src/server"]`
  - `requires-python = ">=3.12"`
- Subprojects (each has its own `pyproject.toml`):
  - `src/agent/`
  - `src/mcp/` (depends on `fastmcp`)
  - `src/server/` (depends on `fastapi`)

### Using uv
- Sync everything (root):
  ```bash
  uv sync --workspace
  ```
- Add a dependency to a specific project:
  ```bash
  # Examples
  uv add --project src/server uvicorn[standard]
  uv add --project src/mcp fastmcp
  uv add --project src/agent httpx
  ```
- Add dev-only tools (to a project):
  ```bash
  uv add --dev --project src/server ruff pytest
  ```
- Run commands in a project environment:
  ```bash
  uv run --project src/server python -c "import fastapi; print(fastapi.__version__)"
  # pattern for apps (after you add code):
  # uv run --project src/server uvicorn app:app --reload
  ```
- Lockfile and checks:
  ```bash
  uv lock            # update/create uv.lock
  uv lock --check    # verify lock matches pyproject(s)
  ```

### Working outside the container (optional)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.12 .venv
uv sync --workspace
```

### Notes
- VS Code is configured to use `${workspaceFolder}/.venv` automatically.
- uv cache is mounted to your host (`~/.cache/uv`) for faster rebuilds.