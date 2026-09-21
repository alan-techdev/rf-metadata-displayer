import sys
from unittest.mock import MagicMock, patch

import pytest
from rfmetadata import _help as bug_report


def test_implementation_cpython():
    """Verify CPython tracking extracts standard versioning details."""
    with patch("platform.python_implementation", return_value="CPython"), \
         patch("platform.python_version", return_value="3.10.3"):

        result = bug_report._implementation()
        assert result == {"name": "CPython", "version": "3.10.3"}


def test_implementation_pypy_final():
    """Verify PyPy logic parses standard structural objects correctly."""

    mock_pypy_info = MagicMock()
    mock_pypy_info.major = 7
    mock_pypy_info.minor = 3
    mock_pypy_info.micro = 9
    mock_pypy_info.releaselevel = "final"

    with patch("platform.python_implementation", return_value="PyPy"), \
         patch.object(sys, "pypy_version_info", mock_pypy_info, create=True):

        result = bug_report._implementation()
        assert result == {"name": "PyPy", "version": "7.3.9"}


def test_implementation_pypy_beta():
    """Verify PyPy appends releaselevel tags if it isn't 'final'."""
    mock_pypy_info = MagicMock()
    mock_pypy_info.major = 7
    mock_pypy_info.minor = 3
    mock_pypy_info.micro = 9
    mock_pypy_info.releaselevel = "beta1"

    with patch("platform.python_implementation", return_value="PyPy"), \
         patch.object(sys, "pypy_version_info", mock_pypy_info, create=True):

        result = bug_report._implementation()
        assert result == {"name": "PyPy", "version": "7.3.9beta1"}


@pytest.mark.parametrize("fallback_impl", ["Jython", "IronPython"])
def test_implementation_fallbacks(fallback_impl):
    """Verify fallback platforms default cleanly to standard python_version."""
    with patch("platform.python_implementation", return_value=fallback_impl), \
         patch("platform.python_version", return_value="2.7.0"):

        result = bug_report._implementation()
        assert result == {"name": fallback_impl, "version": "2.7.0"}


def test_implementation_unknown():
    """Verify an unrecognizable platform returns 'Unknown' configuration."""
    with patch("platform.python_implementation", return_value="GraalVM"):
        result = bug_report._implementation()
        assert result == {"name": "GraalVM", "version": "Unknown"}


def test_info_success(monkeypatch):
    """Verify dictionary assembly structure when system metrics run cleanly."""

    monkeypatch.setattr(bug_report, "rfmetadata_version", "2.4.1")

    with patch("platform.system", return_value="Darwin"), \
         patch("platform.release", return_value="21.4.0"), \
         patch("platform.python_implementation", return_value="CPython"), \
         patch("platform.python_version", return_value="3.11.0"):

        data = bug_report.info()

        assert data["platform"] == {"system": "Darwin", "release": "21.4.0"}
        assert data["implementation"] == {"name": "CPython", "version": "3.11.0"}
        # Note: Your code currently sets 'version': {"version": "2.4.1"} due to a double nest
        assert data["rfmetadata"]["version"] == {"version": "2.4.1"}


def test_info_os_error():
    """Verify OSError constraints fallback cleanly to 'Unknown' labels."""
    with patch("platform.system", side_effect=OSError("Permission Denied")):
        data = bug_report.info()
        assert data["platform"] == {"system": "Unknown", "release": "Unknown"}


def test_bug_reporting_output(capsys, monkeypatch):
    """Verify that bug_reporting pretty prints valid structured JSON."""
    mock_data = {
        "platform": {"system": "Linux", "release": "5.15.0"},
        "implementation": {"name": "CPython", "version": "3.10.0"},
        "rfmetadata": {"version": {"version": "1.0.0"}}
    }
    monkeypatch.setattr(bug_report, "info", lambda: mock_data)

    bug_report.bug_reporting()

    captured = capsys.readouterr()

    import json
    assert json.loads(captured.out) == mock_data
