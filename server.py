import json
import logging
import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field

from loader import load_courses, load_extras

load_dotenv()
logger = logging.getLogger(__name__)


# ── Helper functions (pure, testable without MCP protocol) ────────────────────

def _get_index(courses: dict[str, dict]) -> str:
    """Return JSON list of all courses with slug, title, URL, lessonCount."""
    result = [
        {
            "slug": slug,
            "courseTitle": data["courseTitle"],
            "courseUrl": data.get("courseUrl", ""),
            "lessonCount": data.get("lessonCount", len(data["lessons"])),
        }
        for slug, data in sorted(courses.items())
    ]
    return json.dumps(result)


# ── Server factory ────────────────────────────────────────────────────────────

def build_server(data_path: Path) -> FastMCP:
    """Create and return a configured FastMCP instance.

    Resources and tools are bound over the in-memory dicts loaded from data_path.
    """
    courses = load_courses(data_path)
    extras = load_extras(data_path, courses)

    mcp = FastMCP("anthropic-courses")

    @mcp.resource("courses://index", mime_type="application/json")
    def get_index() -> str:
        """List all Anthropic courses with slug, title, URL, and lesson count."""
        return _get_index(courses)

    return mcp


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data_path_str = os.environ.get("DATA_PATH")
    if not data_path_str:
        raise RuntimeError("DATA_PATH environment variable is not set. Copy .env.example to .env and set DATA_PATH.")
    data_path = Path(data_path_str)
    port = int(os.environ.get("PORT", "8000"))
    mcp = build_server(data_path)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
