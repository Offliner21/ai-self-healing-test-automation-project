# 🚀 AI-Powered DevSecOps Testing Framework

## 🔍 Features

- ✅ Playwright UI automation (Python)
- 🤖 AI self-healing selectors
- 🛡️ OWASP ZAP security scanning
- 📦 Snyk dependency scanning
- ⚙️ CI/CD with GitHub Actions
- 📊 HTML reports

## 🧠 AI Highlight

Tests automatically recover when UI changes using AI-powered selector healing.

## 🛠️ Tech Stack

Python | Playwright | OWASP ZAP | Snyk | Docker | OpenAI

## ▶️ Run

docker run -d -p 3000:3000 bkimminich/juice-shop


docker run -u zap -p 8080:8080 -i ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -host 0.0.0.0 -port 8080

```bash
pytest
python zap/zap_scan.py