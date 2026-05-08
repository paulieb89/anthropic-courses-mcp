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


# ── courses://{slug} ──────────────────────────────────────────────────────────

def test_get_course_returns_overview_for_known_slug(data_dir):
    from loader import load_courses
    from server import _get_course
    courses = load_courses(data_dir)
    result = json.loads(_get_course(courses, "course-one"))
    assert result["courseTitle"] == "Course One"
    assert result["lessonCount"] == 2


def test_get_course_lessons_list_has_lesson_index(data_dir):
    from loader import load_courses
    from server import _get_course
    courses = load_courses(data_dir)
    result = json.loads(_get_course(courses, "course-one"))
    lessons = result["lessons"]
    assert lessons[0]["lessonIndex"] == 0
    assert lessons[0]["title"] == "Intro to Things"
    assert lessons[1]["lessonIndex"] == 1
    assert lessons[1]["title"] == "Advanced Topics"


def test_get_course_lesson_index_is_zero_based(data_dir):
    from loader import load_courses
    from server import _get_course
    courses = load_courses(data_dir)
    result = json.loads(_get_course(courses, "course-two"))
    assert result["lessons"][0]["lessonIndex"] == 0


def test_get_course_returns_error_string_for_unknown_slug(data_dir):
    from loader import load_courses
    from server import _get_course
    courses = load_courses(data_dir)
    result = _get_course(courses, "does-not-exist")
    assert "not found" in result.lower()
    assert "does-not-exist" in result
