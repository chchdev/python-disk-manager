import os
import time
import sys
import subprocess
from pathlib import Path

def main():
    # Needs to be runnning 24-7
    while True:
        try:
            project_root = Path(__file__).resolve().parents[1]
            script_path = project_root / "src" / "space.py"
            subprocess.run([sys.executable, str(script_path)], check=True)
            
            # Run every 3 hours
            time.sleep(3 * 60 * 60)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()