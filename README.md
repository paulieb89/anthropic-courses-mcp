# anthropic-courses-mcp

An MCP server that exposes Anthropic's Skilljar course content as resources and tools, making it available to any MCP-compatible client (Claude Desktop, Claude Code, etc.).

17 courses, 412 lessons — fully bundled in `data/`.

## What's included

| Course | Lessons |
|--------|---------|
| AI Capabilities and Limitations | 14 |
| AI Fluency for Educators | 4 |
| AI Fluency for Nonprofits | 10 |
| AI Fluency for Students | 5 |
| AI Fluency: Framework & Foundations | 14 |
| Building with the Claude API | 85 |
| Claude 101 | 13 |
| Claude Code 101 | 13 |
| Claude Code in Action | 21 |
| Claude with Amazon Bedrock | 83 |
| Claude with Google Cloud's Vertex AI | 93 |
| Introduction to Agent Skills | 6 |
| Introduction to Claude Cowork | 11 |
| Introduction to Model Context Protocol | 14 |
| Introduction to Subagents | 4 |
| Model Context Protocol: Advanced Topics | 15 |
| Teaching AI Fluency | 7 |

## MCP primitives

**Resources**
- `courses://index` — list all courses (slug, title, URL, lesson count)
- `courses://{slug}` — course overview with lesson list and indices
- `courses://{slug}/lessons/{n}` — lesson markdown by zero-based index
- `courses://extras` — list standalone reference documents
- `courses://extras/{slug}` — fetch a reference document

**Tools**
- `search_lessons(query)` — case-insensitive search across all lesson titles; returns slug + lessonIndex for direct resource lookup

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/paulieb89/anthropic-courses-mcp
cd anthropic-courses-mcp
cp .env.example .env
uv run server.py
```

The server runs on `http://0.0.0.0:8000` by default. Set `PORT` in `.env` to change it.

## Claude Desktop config

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "anthropic-courses": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/path/to/anthropic-courses-mcp"
    }
  }
}
```

## Run tests

```bash
uv run pytest
```
