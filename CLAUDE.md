# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# anthropic-courses-mcp

FastMCP server exposing Anthropic Skilljar course content as MCP resources.

## Key conventions
- `loader.py` — pure data loading; `load_courses(path)` and `load_extras(path, courses)` return dicts
- `server.py` — all MCP primitives; `build_server(data_path)` factory pattern for testability
- Handler helpers are module-level functions prefixed with `_` (e.g. `_get_lesson`) — test these directly, not via MCP protocol
- Resources return descriptive error strings on bad input — never raise
- Tool returns empty list on no match — never raise

## Data format
Course files are JSON with required keys `courseTitle` and `lessons` (array of `{title, href, markdown}`). Files prefixed with `_` (e.g. `_batch-report.json`) are silently skipped by the loader. `INDEX.md` and any `.md` whose stem matches a course slug are excluded from extras.

## Transport
Runs as `streamable-http` on `0.0.0.0:{PORT}`.

## Run
```
cp .env.example .env  # edit DATA_PATH and PORT
uv run server.py
```

## Test
```
uv run pytest                          # all tests
uv run pytest tests/test_server.py    # single file
uv run pytest -k test_get_lesson      # single test
```
