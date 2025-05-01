# WebAutomation Project

This project is a **Web Automation** framework using **Python**, **Selenium**, **Behave (BDD)**, `webdriver-manager` for automatic browser driver management, and **Allure Reports** for generating test execution reports.

---

## 📌 Project Overview

The WebAutomation project is designed to perform automated tests on the **SauceDemo** website using **Behavior Driven Development (BDD)** principles. It includes:

- **Selenium WebDriver**: For automating browser interactions  
- **Behave**: For writing BDD-style test scenarios  
- **WebDriver Manager**: To auto-manage browser drivers (no manual download required)  
- **Allure Reports**: For rich test reporting  
- **BrowserStack Integration**: For running tests in the cloud across multiple devices/browsers

---

## ⚙️ Project Setup

### ✅ Prerequisites

- Python 3.x (Recommended: Python 3.8 or higher)
- pip (Python package manager)
- Google Chrome (or another browser)
- Allure CLI (for generating reports)

---

### 🔧 Installation

```
git clone https://github.com/your-username/webautomation.git
cd webautomation
pip install -r requirements.txt 
 ```



🧪 Run Tests (Locally & on BrowserStack)
```
behave
```

☁️ Run on BrowserStack
```angular2html
export RUN_ENV=browserstack
behave

```

On Windows:
```angular2html
set RUN_ENV=browserstack
behave

```