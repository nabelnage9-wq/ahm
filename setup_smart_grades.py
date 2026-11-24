import os
import sys
import subprocess
from pathlib import Path

FOLDERS = [
    "DATABASE", "STUDENTS", "STUDENT_IMAGES", "EXCEL_FILES",
    "PDF_REPORTS", "WORD_FILES", "EXAMS", "CERTIFICATES",
    "ACADEMIC_YEARS", "BACKUPS", "SYNC_DATA", "SYSTEM_SETTINGS",
]

def main():
    root = Path(os.environ.get("SMART_GRADES_ROOT", r"C:\SMART_GRADES"))
    root.mkdir(parents=True, exist_ok=True)
    for folder in FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    print(f"[OK] Created SMART GRADES folders at: {root}")
    backend_dir = Path(__file__).resolve().parent / "backend"
    subprocess.run([sys.executable, str(backend_dir / "manage.py"), "makemigrations"], check=True)
    subprocess.run([sys.executable, str(backend_dir / "manage.py"), "migrate"], check=True)
    print("[OK] Database initialized successfully.")

if __name__ == "__main__":
    main()
