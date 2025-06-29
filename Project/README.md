# Wit – Custom Version Control System

A lightweight, simplified Git-like version control system written in Python.  
This tool allows you to initialize a repository, track file changes, commit snapshots, and restore previous states — all via command-line.

---

## 📦 Project Structure

- `classes.py` – Core data structures: `File`, `Commit`, `Repository`
- `functions.py` – Utility functions for file handling, serialization, and more
- `wit.py` – Main CLI logic built using Click

---

## 🚀 Features

- Initialize a local repository with `wit init`
- Track files using `wit add`
- Commit changes with `wit commit -m "message"`
- View logs using `wit log`
- Check project status via `wit status`
- Revert to previous states using `wit checkout <commit_id>`

---

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd PROJECT
pip install -r requirements.txt
# WIT – Version Control System
```
Make sure `click` and `pyfiglet` are installed.

---

## 🔧 Usage
### Initialize a repo

```bash
wit init
```

### Add files to staging
```bash
wit add file1.py file2.py
# or add all files
wit add .
```

### Commit your work
```bash
wit commit -m "Initial commit"
```

### View the commit history
```bash
wit log
```

### Check the current status
```bash
wit status
```

### Revert to a previous commit
```bash
wit checkout <commit_id>
```

---

## 🧠 How it works
- A `.wit` directory is created in your root project.
- Inside it:
- `/Staging/` stores the staging copy
- `/Commited/` stores snapshots of committed states
- `repo.json` stores all metadata (commits, staging files, etc.)
- `prev.json` tracks the last commit used for rollback/merge logic.

---

## 📈 Planned Features
- `wit push` – Lint analysis & remote upload (to be implemented)
- Restore & delete commands
- Remote repository integration

---

## 🛡️ Disclaimer
This is a learning project to understand how version control systems work internally. It is not intended to replace Git in production.

---

## 🧑‍💻 Author
Developed with ❤️ as part of a code versioning workshop.


---
