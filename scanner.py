import json
import os
import subprocess
import sys
import tempfile


def scan_python_code(code: str) -> list[dict]:
    findings = []

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, "submitted_code.py")

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(code)

        # Security scanning using Bandit
        try:
            result = subprocess.run(
                [
                    sys.executable, "-m", "bandit",
                    "-f", "json", filepath
                ],
                capture_output=True,
                text=True,
                timeout=20
            )

            data = json.loads(result.stdout or "{}")

            for item in data.get("results", []):
                findings.append({
                    "source": "Bandit",
                    "severity": item.get("issue_severity"),
                    "line": item.get("line_number"),
                    "rule": item.get("test_id"),
                    "title": item.get("issue_text")
                })

        except Exception as error:
            findings.append({
                "source": "Bandit",
                "severity": "INFO",
                "title": "Security scan failed",
                "details": str(error)
            })

        # Code quality scanning using Ruff
        try:
            result = subprocess.run(
                [
                    sys.executable, "-m", "ruff",
                    "check", "--output-format", "json", filepath
                ],
                capture_output=True,
                text=True,
                timeout=20
            )

            for item in json.loads(result.stdout or "[]"):
                findings.append({
                    "source": "Ruff",
                    "severity": "LOW",
                    "line": item.get("location", {}).get("row"),
                    "rule": item.get("code"),
                    "title": item.get("message")
                })

        except Exception as error:
            findings.append({
                "source": "Ruff",
                "severity": "INFO",
                "title": "Code quality scan failed",
                "details": str(error)
            })

    return findings