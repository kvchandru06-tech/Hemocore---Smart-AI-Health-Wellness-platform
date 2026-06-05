# AI-Driven-Blood-Report-Analyzer
## 🚀 Installation Guide

### Prerequisites

Make sure the following are installed:

* 🐍 Python 3.10+
* 🗄️ MySQL
* 📦 pip (Python Package Manager)
* 🌐 Git

### Clone the Repository

```bash
git clone https://github.com/your-username/Hemocore.git
cd Hemocore
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### Install Required Packages

```bash
pip install flask
pip install mysql-connector-python
pip install pandas
pip install numpy
pip install scikit-learn
pip install matplotlib
pip install seaborn
```

Or install all at once:

```bash
pip install -r requirements.txt
```

### Configure Database

1. Install MySQL.
2. Create a database named `hemocore`.
3. Update database credentials in the project configuration file.

### Run the Project

```bash
python app.py
```

### Open in Browser

```text
http://127.0.0.1:5000
```
