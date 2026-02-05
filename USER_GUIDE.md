# Truth Engine - User Guide

This guide explains how to use the Truth Engine (Python Debugger) to fix code errors using AI and verified sandboxed execution.

## 🚀 Quick Start (Local Demo)

The system is currently set up to run locally for demonstration purposes.

### 1. Start the Frontend Application
Open a terminal in the project folder:
```bash
cd frontend
npm run dev
```
**Access the app at:** [http://localhost:3000](http://localhost:3000)

---

## 📝 How to Use

### Step 1: Input Your Code
1.  On the **left panel**, paste your Python code into the code editor.
    *   *Example inputs are safe! The system is designed to handle broken code.*
2.  The system will automatically detect libraries (e.g., NumPy, Pandas) and display badges.

### Step 2: Input the Error Log
1.  Copy the traceback or error message you received when running your code.
2.  Paste it into the **"Error Log / Traceback"** text area below the code editor.
    *   *Example:* `ZeroDivisionError: division by zero`

### Step 3: Verify & Fix
1.  Click the **🚀 Verify & Fix** button.
2.  **Watch the Console** (Right Panel):
    *   The system will connect to the AI engine.
    *   It analyzes the error structure.
    *   It generates potential fixes (Candidates).
    *   It runs each candidate in a secure sandbox.
    *   *Green logs* indicate success, *Red logs* indicate failure.

### Step 4: Review the Solution
1.  Once a verified fix is found, the **Diff Viewer** will appear.
2.  **Left Side**: Your original broken code.
3.  **Right Side**: The verified fixed code (highlighted in green).
4.  Click **📋 Copy Fixed Code** to use it in your project.

---

## 🧪 Example Scenarios to Try

### Scenerio A: ZeroDivisionError
**Code:**
```python
def average(numbers):
    return sum(numbers) / len(numbers)

print(average([]))
```
**Error Log:**
```
ZeroDivisionError: division by zero
```
**Expected Fix:** The AI will add a check for empty list or use `max(len(numbers), 1)`.

### Scenario B: Type Error
**Code:**
```python
def greet(name, age):
    return "Hi " + name + ", you are " + age

greet("Alice", 30)
```
**Error Log:**
```
TypeError: can only concatenate str (not "int") to str
```
**Expected Fix:** `str(age)` will be added.

---

## ⚙️ Architecture Info

- **Frontend**: Next.js 14 with Monaco Editor (VS Code style).
- **Backend**: Python 3.12 (Lambda functions).
- **Security**: All code is sanitized before execution. `os.system`, `subprocess`, and file system access are restricted.
- **AI Models**: Gemini 1.5 Pro / Groq Llama 3 / DeepSeek V3 (Auto-switching).
