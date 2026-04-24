"""Pytest configuration — add scripts/ to sys.path so tests can import tts package."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
