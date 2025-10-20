# 🎬 Bollywood Quiz - Quick Start Guide

## 🚨 PYTHON PATH ISSUES? TRY THESE SOLUTIONS:

### **Solution 1: Direct Python File (RECOMMENDED)**
```
1. Right-click on "direct_run.py"
2. Select "Open with" → "Python"
3. OR double-click "direct_run.py" if Python is associated
```

### **Solution 2: Command Line (If Python works)**
```
python direct_run.py
```

### **Solution 3: Fix Python PATH**
1. **Install Python properly:**
   - Go to https://python.org/downloads
   - Download Python 3.11+
   - ✅ CHECK "Add Python to PATH" during installation
   - Restart Command Prompt

2. **Then run:**
   ```
   run_quiz.bat
   ```

### **Solution 4: Microsoft Store Python Fix**
1. **Settings** → **Apps** → **Advanced app settings** → **App execution aliases**  
2. **Enable** both `python.exe` and `python3.exe` toggles
3. **Restart** Command Prompt
4. **Run:** `run_quiz.bat`

### **Solution 5: Manual Installation**
```bash
# Open Command Prompt as Administrator
pip install flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv

# Then run
python app.py
```

## 🎯 Quick Access

Once running, open your browser to:
- **Quiz:** http://localhost:5000
- **Database Status:** http://localhost:5000/status
- **Initialize DB:** http://localhost:5000/init_db

## 📁 Available Launchers

| File | Description |
|------|-------------|
| `direct_run.py` | 🥇 **Best Option** - Pure Python launcher |
| `run_quiz.bat` | Windows batch file (requires Python in PATH) |
| `run_quiz.ps1` | PowerShell script |
| `simple_start.bat` | Simple launcher with Store Python |
| `app.py` | Direct Flask app (if dependencies installed) |

## 🔧 Troubleshooting

### Error: "Python not found"
- Use `direct_run.py` instead
- Or install Python from python.org with PATH option

### Error: "Module not found" 
- Run `direct_run.py` - it auto-installs dependencies
- Or manually: `pip install flask flask-sqlalchemy requests beautifulsoup4 lxml werkzeug python-dotenv`

### Error: "Permission denied"
- Run Command Prompt as Administrator
- Or use `--user` flag: `pip install --user [packages]`

## 🎮 How to Play

1. **Start the application** using any method above
2. **Open browser** to http://localhost:5000
3. **Enter your name** on the landing page
4. **Answer 8 questions** (2 from each difficulty level)
5. **View your results** and see the leaderboard!

## 🏆 Scoring System

- **Easy (10 pts):** Basic movie info
- **Medium (20 pts):** Cast & crew details  
- **Hard (30 pts):** Plot & awards
- **Expert (40 pts):** Trivia & facts
- **Maximum Score:** 200 points

---
**Need Help?** Try `direct_run.py` first - it handles most issues automatically! 🚀