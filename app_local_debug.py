"""Compatibility entry point using the shared UI and secure API configuration.

Run with: streamlit run app_local_debug.py
Without a configured key, enter a SiliconFlow key in the sidebar password field.
"""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
