import json
import pytest
from pathlib import Path
from loader import load_courses, load_extras


# ── load_courses ──────────────────────────────────────────────────────────────

def test_load_courses_returns_valid_courses(data_dir):
    courses = load_courses(data_dir)
    assert "course-one" in courses
    assert "course-two" in courses


def test_load_courses_excludes_underscore_prefixed_files(data_dir):
    courses = load_courses(data_dir)
    assert "_batch-report" not in courses


def test_load_courses_skips_files_missing_required_keys(data_dir):
    courses = load_courses(data_dir)
    assert "malformed" not in courses


def test_load_courses_lesson_structure(data_dir):
    courses = load_courses(data_dir)
    lessons = courses["course-one"]["lessons"]
    assert len(lessons) == 2
    assert lessons[0]["title"] == "Intro to Things"
    assert lessons[1]["title"] == "Advanced Topics"


def test_load_courses_raises_on_missing_data_path():
    with pytest.raises(RuntimeError, match="DATA_PATH"):
        load_courses(Path("/nonexistent/does-not-exist"))


def test_load_courses_raises_on_zero_valid_courses(tmp_path):
    # Only a _ file exists — nothing valid loads
    (tmp_path / "_only.json").write_text("[]")
    with pytest.raises(RuntimeError, match="No valid"):
        load_courses(tmp_path)
