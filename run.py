"""
TravelMind AI - Multi-Agent Travel Planning Platform
====================================================

Entry point for the TravelMind AI application.

Usage:
    python run.py              # Launch the Streamlit UI
    python run.py --api        # Launch the FastAPI backend
    python run.py --test       # Run the test suite
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def run_streamlit():
    """Launch the Streamlit dashboard."""
    print("🚀 Starting TravelMind AI Streamlit dashboard...")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "ui/app.py"],
        cwd=PROJECT_ROOT,
    )


def run_api():
    """Launch the FastAPI backend server."""
    print("🚀 Starting TravelMind AI FastAPI backend...")
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"],
        cwd=PROJECT_ROOT,
    )


def run_tests():
    """Run the test suite."""
    print("🧪 Running TravelMind AI test suite...")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=PROJECT_ROOT,
    )


def main():
    parser = argparse.ArgumentParser(
        description="TravelMind AI - Multi-Agent Travel Planning Platform"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Launch the FastAPI backend instead of the Streamlit UI",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test suite",
    )
    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.api:
        run_api()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()