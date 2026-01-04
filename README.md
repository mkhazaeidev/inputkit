# 📦 inputkit

## 1. Introduction

**inputkit** is a Python package designed to make terminal input simple, clean, and reliable.

It helps developers ask users for information like usernames, passwords, phone numbers, or emails, and make sure the input is valid before continuing the program.

The package is cross-platform and works smoothly on **Windows**, **Linux**, and **macOS**, so you can focus on your application logic instead of handling input details.

Whether you are building a small CLI tool or a larger terminal-based application, **inputkit** gives you a better and more comfortable input experience.

---

## 2. Project Story & Design Scenario

Imagine you are building a command-line application.

You ask the user for a username.  
They enter something too short.  
You ask again.  

Then you need a password — it must be hidden.  
Then a mobile number — it must follow a specific format.

Very quickly, your code becomes full of:
- repeated input loops
- unclear error messages
- mixed logic for asking and validating input

This is where **inputkit** comes in.

The idea behind this project is simple:

> Let developers **ask questions naturally**, and let the package **handle correctness politely**.

**inputkit** separates two responsibilities:
- **Asking for input**
- **Validating the input**

This separation makes your code:
- easier to read
- easier to maintain
- easier to extend in the future

The user gets clear questions.  
The developer gets clean and readable code.

---

## 3. Project Structure

The project is organized in a clean and professional way:

```bash
inputkit/
├── src/
│   └── inputkit/
│       ├── prompt/
│       ├── validators/
│       ├── errors/
│       ├── utils/
│       └── _internal/
│
├── tests/
├── docs/
├── README.md
├── LICENSE
├── pyproject.toml
├── CHANGELOG.md
└── MANIFEST.in
```

Each part has a clear responsibility, which makes the project easy to understand and extend.

---

## 4. Installation

You can install **inputkit** using `pip`:

```bash
pip install inputkit
```

After installation, the package is ready to use in your Python project.

---

## 5. Basic Usage

Using inputkit feels natural and readable.

### Simple example

```python
from inputkit import prompt
from inputkit.validators import isusername, ispassword

username = prompt.username(
    "Enter your username",
    validators=[isusername]
)

secret = prompt.password(
    "Enter your password",
    validators=[ispassword]
)
```

You ask for input.
The package takes care of validation.

If the input is not valid, the user is asked again in a friendly way.

No manual loops.
No messy checks.
Just clean interaction.

---

## ✨ Final Notes

inputkit is designed to grow with your project.

You can start small, and later build more complex terminal experiences without changing how your code feels.

If you like clean CLI design and readable Python code, this package is for you.
