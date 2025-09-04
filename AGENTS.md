# Repository Guidelines

## Project Structure & Module Organization
- `ai-prompt`: Bash entrypoint; sets up `.venv`, installs `requirements.txt`, detects Raycast, then runs Python.
- `ai_prompt_executor.py`: Python core; model mapping, provider detection, prompt execution, output saving.
- `prompts/`: Prompt library (`user/` and `system/`); filenames (without extension) become prompt names. Supports `.md` and `.txt`.
- `ai-output/`: Default output directory (Markdown `.md` by default; `.txt` supported). Timestamped or named via `--output-name`.
- `.env.example` / `.env`: API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- `requirements.txt`: Python dependencies.

## Build, Test, and Development Commands
- Setup: `cp .env.example .env && chmod +x ./ai-prompt`
- Run (wrapper): `./ai-prompt --prompt "Hello" --model gpt-5-mini --system-prompt developer`
- Run (direct): `python ai_prompt_executor.py --prompt "Hello"`
- Prompt/model lists: `./ai-prompt --list-prompts` | `./ai-prompt --list-models`
- Manage venv manually: `source .venv/bin/activate && pip install -r requirements.txt`
- Simulate Raycast: `TERM=dumb ./ai-prompt "test"`

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indents, type hints where helpful, snake_case for files/functions, concise docstrings.
- Bash: Keep compatibility with Raycast (no ANSI when `TERM=dumb`); reuse the existing color/printing helpers.
- Dependencies: Minimize additions; update `requirements.txt` when needed.
- Filenames: Keep current names (`ai-prompt`, `ai_prompt_executor.py`); avoid breaking CLI flags.

## Testing Guidelines
- No formal test suite yet; verify via smoke runs (see commands above) and edge cases (file prompts, library prompts, missing keys, custom output paths).
- If adding logic, include lightweight tests under `tests/` (e.g., `tests/test_models.py`, `pytest -q`) and document any new dev deps.

## Commit & Pull Request Guidelines
- Commits: Imperative subject (“Add model mapping”), concise body with rationale and usage example when relevant.
- PRs: Clear description, linked issues, reproduction/verification commands, and note any changes to flags, output format, or environment.
- Update docs (`README.md`, this file) when behavior or flags change. Never commit secrets; keep `.env` local.

## Architecture Overview & Tips
- Two-layer design: Bash wrapper for environment; Python core for providers and I/O.
- Provider selection: Simplified model names map to API models; provider auto-detected by name.
- Configuration: Prefer `.env`; avoid printing API keys; be mindful of API costs when changing defaults.
