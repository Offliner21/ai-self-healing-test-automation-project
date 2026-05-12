# 🚀 AI-Powered Self-Healing DevSecOps Testing Framework

## 🔍 Features

* ✅ Playwright UI automation (Python)
* 🤖 AI-powered self-healing selectors
* 🧠 OpenAI DOM analysis + locator recovery
* 🛡️ OWASP ZAP security scanning
* 📦 Snyk dependency scanning
* 🥒 Gherkin / BDD support
* 📊 Allure + HTML reports
* ⚙️ CI/CD-ready architecture

---

## 🧠 AI Highlight

Tests automatically recover from broken locators using:

1. Live DOM extraction
2. LLM-powered locator analysis
3. Runtime selector healing
4. Automatic retry execution

---

## 🛠️ Tech Stack

Python | Playwright | Pytest | OpenAI | Gherkin | Allure | OWASP ZAP | Snyk

---

#First activate the \env via this command below

.\venv\Scripts\activate

## ▶️ Run Juice Shop

```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
```

## ▶️ Run ZAP

```bash
docker run -p 8080:8080 --add-host=host.docker.internal:host-gateway -i ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true ```

---

## ▶️ Run Tests

```bash
python -m pytest tests -v -s
```

---

## ▶️ Run Gherkin Tests

```bash
behave -v

# Generate HTML Behave Report 

behave -f behave_html_formatter:HTMLFormatter -o reports/behave-report.html 

# Open the behave report 

start reports/behave-report.html 
```

---

## ▶️ Run Allure Reports

```bash
python -m pytest tests --alluredir=reports/allure-results

allure generate reports/allure-results --clean -o reports/allure-report

allure open reports/allure-report
```

---

## ▶️ Run Snyk Scan

```bash
snyk test --file=requirements.txt --package-manager=pip
```

## ▶️ Run Snyk Monitor

```bash
snyk monitor --file=requirements.txt --package-manager=pip    
```

## ▶️ Run ZAP Scan

```bash
python zap/zap_scan.py

# Open ZAP report 

start reports\zap_report.html 
```
