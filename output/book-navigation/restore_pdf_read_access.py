"""Restore folder-inherited access to the two compiled Windows PDFs."""
from pathlib import Path
import hashlib
import os
import subprocess


def repair():
    if os.name != "nt":
        raise SystemExit("This repair is for Windows only.")
    output = (Path(__file__).resolve().parents[2] / "output/pdf").resolve()
    for name in ("Maths-with-Friends-Primary-1-Textbook.pdf",
                 "Maths-with-Friends-Primary-1-Workbook.pdf"):
        path = (output / name).resolve()
        if path.parent != output or not path.is_file():
            raise ValueError(f"Missing or unexpected compiled PDF: {name}")
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        subprocess.run(["icacls.exe", str(path), "/inheritance:e"], check=True)
        if hashlib.sha256(path.read_bytes()).hexdigest() != before:
            raise ValueError(f"Unexpected PDF content change: {name}")
    print("Both PDFs inherit normal output-folder access; contents are unchanged.")


if __name__ == "__main__":
    repair()
