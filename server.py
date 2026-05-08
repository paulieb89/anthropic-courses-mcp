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


def _search_lessons(courses: dict[str, dict], query: str) -> list[dict]:
    """Case-insensitive substring search across all lesson titles.

    Returns list of {slug, courseTitle, lessonIndex, lessonTitle}.
    lessonIndex is zero-based and can be used directly in courses://{slug}/lessons/{n}.
    Returns empty list when nothing matches.
    """
    query_lower = query.lower()
    results = []
    for slug, data in sorted(courses.items()):
        for i, lesson in enumerate(data["lessons"]):
            if query_lower in lesson["title"].lower():
                results.append(
                    {
                        "slug": slug,
                        "courseTitle": data["courseTitle"],
                        "lessonIndex": i,
                        "lessonTitle": lesson["title"],
                    }
                )
    return results


def _get_extras_index(extras: dict[str, dict]) -> str:
    """Return JSON list of extras with slug and filename."""
    result = [
        {"slug": slug, "filename": data["filename"]}
        for slug, data in sorted(extras.items())
    ]
    return json.dumps(result)


def _get_extra(extras: dict[str, dict], slug: str) -> str:
    """Return extra document markdown or descriptive error string."""
    if slug not in extras:
        available = ", ".join(sorted(extras.keys()))
        return f"Extra '{slug}' not found. Available extras: {available}"
    return extras[slug]["content"]


def _get_lesson(courses: dict[str, dict], slug: str, n: str) -> str:
    """Return lesson markdown by course slug and zero-based index, or a descriptive error string."""
    if slug not in courses:
        return f"Course '{slug}' not found."
    try:
        idx = int(n)
    except ValueError:
        return f"'{n}' is not a valid lesson index. Expected a non-negative integer."
    lessons = courses[slug]["lessons"]
    if idx < 0 or idx >= len(lessons):
        return (
            f"Lesson index {idx} is out of range for course '{slug}'. "
            f"Valid indices: 0–{len(lessons) - 1}."
        )
    return lessons[idx]["markdown"]


def _get_course(courses: dict[str, dict], slug: str) -> str:
    """Return JSON course overview or descriptive error string."""
    if slug not in courses:
        available = ", ".join(sorted(courses.keys()))
        return f"Course '{slug}' not found. Available courses: {available}"

    data = courses[slug]
    lessons = [
        {
            "lessonIndex": i,
            "title": lesson["title"],
            "href": lesson.get("href", ""),
        }
        for i, lesson in enumerate(data["lessons"])
    ]
    result = {
        "courseTitle": data["courseTitle"],
        "courseUrl": data.get("courseUrl", ""),
        "lessonCount": data.get("lessonCount", len(data["lessons"])),
        "lessons": lessons,
    }
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

    @mcp.resource("courses://{slug}", mime_type="application/json")
    def get_course(slug: str) -> str:
        """Get course overview: title, lesson count, and list of lessons with indices."""
        return _get_course(courses, slug)

    @mcp.resource("courses://{slug}/lessons/{n}", mime_type="text/markdown")
    def get_lesson(slug: str, n: str) -> str:
        """Get a single lesson's markdown content by course slug and zero-based index."""
        return _get_lesson(courses, slug, n)

    @mcp.resource("courses://extras", mime_type="application/json")
    def get_extras_index() -> str:
        """List all standalone reference documents (MD files with no course JSON)."""
        return _get_extras_index(extras)

    @mcp.resource("courses://extras/{slug}", mime_type="text/markdown")
    def get_extra(slug: str) -> str:
        """Get a standalone reference document by slug."""
        return _get_extra(extras, slug)

    @mcp.tool()
    def search_lessons(
        query: Annotated[str, Field(
            description="Search term to match against lesson titles (case-insensitive substring match)"
        )],
    ) -> list[dict]:
        """Search lesson titles across all courses.

        Returns matching lessons with their course slug and lesson index.
        Use the returned slug + lessonIndex to fetch content via courses://{slug}/lessons/{n}.
        Returns an empty list when nothing matches.
        """
        return _search_lessons(courses, query)

    return mcp


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    data_path_str = os.environ.get("DATA_PATH")
    if not data_path_str:
        raise RuntimeError("DATA_PATH environment variable is not set. Copy .env.example to .env and set DATA_PATH.")
    data_path = Path(data_path_str)
    mcp = build_server(data_path)
    if "--stdio" in sys.argv:
        mcp.run(transport="stdio")
    else:
        port = int(os.environ.get("PORT", "8000"))
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
