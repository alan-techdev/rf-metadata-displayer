import sys
from unittest.mock import MagicMock, patch

import pytest
from src.rfmetadata import main


@pytest.fixture(autouse=True)
def mock_metadata(monkeypatch):
    monkeypatch.setattr(main, "__version__", "1.0.0")
    monkeypatch.setattr(main, "__author__", "Test Author")
    monkeypatch.setattr(main, "__description__", "Test Desc")
    monkeypatch.setattr(main, "__license__", "MIT")
    monkeypatch.setattr(main, "__title__", "rfmetadata")
    monkeypatch.setattr(main, "__url__", "http://test.com")
    monkeypatch.setattr(main, "bug_reporting", MagicMock())


@pytest.mark.parametrize("flag, expected_output", [
    (["--version"], "Version: 1.0.0\n"),
    (["--author"], "Author: Test Author\n"),
    (["--description"], "Description: Test Desc\n"),
    (["--license"], "License: MIT\n"),
    (["--title"], "Title: rfmetadata\n"),
    (["--url"], "URL: http://test.com\n"),
])
def test_main_metadata_flags(flag, expected_output, capsys):
    """Test that metadata flags print the correct string and exit early."""
    # Patch sys.argv to simulate running: rfmetadata --version (etc.)
    with patch.object(sys, 'argv', ['rfmetadata'] + flag):
        main.main()

    # Capture whatever was printed to stdout
    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_main_report_bug_flag():
    """Test that --report-bug triggers the bug_reporting function."""
    with patch.object(sys, 'argv', ['rfmetadata', '--report-bug']):
        main.main()

    main.bug_reporting.assert_called_once()
