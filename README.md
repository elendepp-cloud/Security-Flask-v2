# Security Lab

A simple educational web security lab built with Flask.

The project demonstrates:

* Reflected XSS
* Stored XSS
* DOM XSS
* File Upload
* Path Traversal
* OS Command Injection
* CSRF
* IDOR

Each lab is designed for learning and local testing.

---

## Project Components

The project has **three Flask servers**:

| Component             |   Port | Purpose              |
| --------------------- | -----: | -------------------- |
| `app.py`              | `5000` | Main web application |
| `evil-server/evil.py` | `5001` | CSRF attack server   |
| `idor-lab/idor.py`    | `5002` | IDOR laboratory      |

---

## Setup

Go to the project directory:

```bash
cd ~/security-lab-v2
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

If the virtual environment does not exist:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# Run the Project

For the full project, run the three servers in **three separate terminals**.

### Terminal 1 — Evil Server

```bash
cd ~/security-lab-v2
source venv/bin/activate
python3 evil-server/evil.py
```

Runs on:

```text
http://127.0.0.1:5001
```

CSRF attack page:

```text
http://127.0.0.1:5001/ad
```

---

### Terminal 2 — IDOR Lab

```bash
cd ~/security-lab-v2
source venv/bin/activate
python3 idor-lab/idor.py
```

Runs on:

```text
http://127.0.0.1:5002
```

Login page:

```text
http://127.0.0.1:5002/login
```

---

### Terminal 3 — Main Application

```bash
cd ~/security-lab-v2
source venv/bin/activate
python3 app.py
```

Main application:

```text
http://127.0.0.1:5000
```

---

# CSRF Lab

CSRF requires **two servers**:

```text
Main App     → http://127.0.0.1:5000
Evil Server  → http://127.0.0.1:5001
```

Start both:

```bash
python3 app.py
```

and:

```bash
python3 evil-server/evil.py
```

Then open:

```text
http://127.0.0.1:5000
```

and:

```text
http://127.0.0.1:5001/ad
```

The Evil Server simulates a malicious external website that attempts to send requests to the main application.

The lab demonstrates the difference between:

* 🔴 Vulnerable CSRF
* 🟢 Protected CSRF

---

# IDOR Lab

IDOR runs as a separate application.

Start:

```bash
python3 idor-lab/idor.py
```

Open:

```text
http://127.0.0.1:5002/login
```

The lab demonstrates how changing an object ID can expose another user's data when the server does not properly check authorization.

---

# Quick Start

Run these commands in three terminals:

### Terminal 1

```bash
python3 evil-server/evil.py
```

### Terminal 2

```bash
python3 idor-lab/idor.py
```

### Terminal 3

```bash
python3 app.py
```

Then open:

```text
Main App:    http://127.0.0.1:5000
Evil Server: http://127.0.0.1:5001
IDOR Lab:    http://127.0.0.1:5002
```

---

## Stop the Servers

Press:

```text
Ctrl + C
```

in each terminal.

---

