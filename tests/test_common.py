"""
Tests for common utility functions.
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.common import setup_logging, get_project_root, ensure_directory


def test_setup_logging():
    """Test logging setup function."""
    logger = setup_logging(log_level="INFO")
    assert logger is not None
    assert logger.name == "utils.common"


def test_get_project_root():
    """Test project root detection."""
    root = get_project_root()
    assert root.is_dir()
    assert (root / "scripts").exists()
    assert (root / "utils").exists()


def test_ensure_directory():
    """Test directory creation utility."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "test_subdir"
        
        # Directory should not exist initially
        assert not test_path.exists()
        
        # Create directory
        result = ensure_directory(str(test_path))
        
        # Verify directory was created
        assert test_path.exists()
        assert test_path.is_dir()
        assert result == test_path


def test_ensure_directory_existing():
    """Test ensure_directory with existing directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use existing directory
        result = ensure_directory(temp_dir)
        
        # Should return the path without error
        assert result == Path(temp_dir)
        assert result.exists()
        assert result.is_dir()