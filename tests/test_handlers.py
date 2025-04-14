import pytest

from reports import HandlersReport


@pytest.fixture
def sample_log_lines():
    return [
        "2023-01-01 12:00:00 INFO django.requests GET /api/v1/products/",
        "2023-01-01 12:00:01 DEBUG django.requests POST /api/v1/auth/login/",
        "2023-01-01 12:00:02 WARNING django.requests GET /api/v1/products/",
        "2023-01-01 12:00:03 ERROR django.requests GET /admin/dashboard/",
        "2023-01-01 12:00:04 CRITICAL django.requests POST /api/v1/auth/login/",
        "2023-01-01 12:00:05 INFO django.requests GET /api/v1/products/",
        "2023-01-01 12:00:06 INFO django.core.management DatabaseError: "
        "Deadlock detected",
    ]


def test_process_line(sample_log_lines):
    report = HandlersReport()
    for line in sample_log_lines:
        report.process_line(line)

    assert report.total_requests == 6
    assert report.data["/api/v1/products/"]["INFO"] == 2
    assert report.data["/api/v1/products/"]["WARNING"] == 1
    assert report.data["/api/v1/auth/login/"]["DEBUG"] == 1
    assert report.data["/api/v1/auth/login/"]["CRITICAL"] == 1
    assert report.data["/admin/dashboard/"]["ERROR"] == 1


def test_merge():
    report1 = HandlersReport()
    report1.process_line(
        "2023-01-01 12:00:00 INFO django.requests GET /api/v1/products/")
    report1.process_line(
        "2023-01-01 12:00:01 DEBUG django.requests POST /api/v1/auth/login/")

    report2 = HandlersReport()
    report2.process_line(
        "2023-01-01 12:00:02 WARNING django.requests GET /api/v1/products/")
    report2.process_line(
        "2023-01-01 12:00:03 ERROR django.requests GET /admin/dashboard/")

    report1.merge(report2)

    assert report1.total_requests == 4
    assert report1.data["/api/v1/products/"]["INFO"] == 1
    assert report1.data["/api/v1/products/"]["WARNING"] == 1
    assert report1.data["/api/v1/auth/login/"]["DEBUG"] == 1
    assert report1.data["/admin/dashboard/"]["ERROR"] == 1


def test_format(sample_log_lines):
    report = HandlersReport()
    for line in sample_log_lines:
        report.process_line(line)

    formatted = report.format()
    assert "Total requests: 6" in formatted
    assert "/api/v1/products/" in formatted
    assert "/api/v1/auth/login/" in formatted
    assert "/admin/dashboard/" in formatted
    assert "DEBUG" in formatted
    assert "INFO" in formatted
    assert "WARNING" in formatted
    assert "ERROR" in formatted
    assert "CRITICAL" in formatted
