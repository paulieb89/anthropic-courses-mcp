import json
import pytest
from pathlib import Path


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    """Minimal fixture corpus used by all tests.

    Contains:
    - 2 valid courses (course-one: 2 lessons, course-two: 1 lesson)
    - 1 utility file excluded by _ prefix (_batch-report.json)
    - 1 invalid JSON excluded by schema check (malformed.json)
    - INDEX.md excluded from extras
    - 1 extras MD file (extra_guide.md → slug: extra-guide)
    - 1 MD file with matching JSON (course-one.md — NOT an extra)
    """
    course1 = {
        "courseTitle": "Course One",
        "courseUrl": "https://example.com/course-one",
        "lessonCount": 2,
        "lessons": [
            {
                "title": "Intro to Things",
                "href": "https://example.com/1",
                "markdown": "## Intro to Things\n\nContent one.",
            },
            {
                "title": "Advanced Topics",
                "href": "https://example.com/2",
                "markdown": "## Advanced Topics\n\nContent two.",
            },
        ],
    }
    (tmp_path / "course-one.json").write_text(json.dumps(course1))

    course2 = {
        "courseTitle": "Course Two",
        "courseUrl": "https://example.com/course-two",
        "lessonCount": 1,
        "lessons": [
            {
                "title": "Basics",
                "href": "https://example.com/3",
                "markdown": "## Basics\n\nContent three.",
            },
        ],
    }
    (tmp_path / "course-two.json").write_text(json.dumps(course2))

    # Excluded: _ prefix
    (tmp_path / "_batch-report.json").write_text('[{"courseUrl": "x", "status": "ok"}]')

    # Excluded: missing required keys
    (tmp_path / "malformed.json").write_text('{"foo": "bar"}')

    # Excluded from extras: INDEX.md
    (tmp_path / "INDEX.md").write_text("# Index\n- course-one\n- course-two\n")

    # Extra (MD with no JSON pair)
    (tmp_path / "extra_guide.md").write_text("# Extra Guide\n\nSome extra content.")

    # MD with matching JSON — NOT an extra
    (tmp_path / "course-one.md").write_text("# Course One full text.")

    return tmp_path
