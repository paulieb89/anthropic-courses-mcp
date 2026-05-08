# anthropic-courses-mcp

FastMCP server exposing Anthropic Skilljar course content as MCP resources.

## Key conventions
- `loader.py` — pure data loading; `load_courses(path)` and `load_extras(path, courses)` return dicts
- `server.py` — all MCP primitives; `build_server(data_path)` factory pattern for testability
- Handler helpers are module-level functions prefixed with `_` (e.g. `_get_index`)
- Resources return descriptive error strings on bad input — never raise
- Tool returns empty list on no match — never raise

## Run
cp .env.example .env  # edit DATA_PATH and PORT
uv run server.py

## Test
uv run pytest
