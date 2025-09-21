#!/usr/bin/env python3
"""
Example YouTube Channel Script

This is an example script showing the recommended structure and best practices
for scripts in this project.

Usage:
    python examples/example_script.py --name "Your Name"

Requirements:
    - Python 3.8+
    - No additional requirements for this example
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.common import setup_logging, get_project_root


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example script for YouTube channel automation"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main() -> None:
    """Main function with script logic."""
    args = parse_arguments()
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logging(log_level=log_level)
    
    logger.info("Starting example script")
    logger.info(f"Project root: {get_project_root()}")
    
    # Example script logic
    message = f"Hello, {args.name}! This is an example YouTube channel script."
    print(message)
    logger.info(f"Generated message: {message}")
    
    logger.info("Example script completed successfully")


if __name__ == "__main__":
    main()