import json
import pytest
from pathlib import Path
from server import build_server, _get_index


# ── courses://index ───────────────────────────────────────────────────────────

def test_get_index_returns_list_of_courses(data_dir):
    from loader import load_courses
    courses = load_courses(data_dir)
    result = json.loads(_get_index(courses))
    slugs = [c["slug"] for c in result]
    assert "course-one" in slugs
    assert "course-two" in slugs


def test_get_index_entry_shape(data_dir):
    from loader import load_courses
    courses = load_courses(data_dir)
    result = json.loads(_get_index(courses))
    entry = next(c for c in result if c["slug"] == "course-one")
    assert entry["courseTitle"] == "Course One"
    assert entry["courseUrl"] == "https://example.com/course-one"
    assert entry["lessonCount"] == 2


def test_get_index_excludes_extras(data_dir):
    from loader import load_courses, load_extras
    courses = load_courses(data_dir)
    result = json.loads(_get_index(courses))
    slugs = [c["slug"] for c in result]
    assert "extra-guide" not in slugs
