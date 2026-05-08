import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_courses(data_path: Path) -> dict[str, dict]:
    """Load all valid course JSON files from data_path.

    Returns a dict keyed by slug (filename minus .json).
    Excludes files starting with '_'. Skips files missing
    'courseTitle' or 'lessons' keys with a warning.

    Raises RuntimeError if data_path does not exist or no
    valid course files are found.
    """
    if not data_path.exists():
        raise RuntimeError(
            f"DATA_PATH '{data_path}' does not exist. "
            "Set DATA_PATH to the directory containing course JSON files."
        )

    courses: dict[str, dict] = {}
    for path in sorted(data_path.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            logger.warning("Skipping %s — invalid JSON: %s", path.name, exc)
            continue

        if "courseTitle" not in data or "lessons" not in data:
            logger.warning(
                "Skipping %s — missing 'courseTitle' or 'lessons' keys", path.name
            )
            continue

        slug = path.stem  # filename without .json
        courses[slug] = data

    if not courses:
        raise RuntimeError(
            f"No valid course JSON files found in '{data_path}'. "
            "Expected files with 'courseTitle' and 'lessons' keys."
        )

    return courses


def load_extras(data_path: Path, courses: dict[str, dict]) -> dict[str, dict]:
    """Load MD-only files that have no matching JSON course.

    Returns a dict keyed by slug (filename: lowercase, underscores -> hyphens,
    .md stripped). Excludes INDEX.md and any .md whose stem matches a course slug.
    Each value is {'filename': str, 'content': str}.
    """
    course_stems = set(courses.keys())
    extras: dict[str, dict] = {}

    for path in sorted(data_path.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        if path.stem in course_stems:
            continue

        slug = path.stem.lower().replace("_", "-")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            logger.warning("Skipping %s — encoding error: %s", path.name, exc)
            continue
        extras[slug] = {
            "filename": path.name,
            "content": content,
        }

    return extras
