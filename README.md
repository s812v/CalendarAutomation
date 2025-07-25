# 🗓️ Auto Calendar Logger for Coding Sessions

This project automatically tracks your coding sessions in VS Code (or any file modifications) and logs them as events in a **Google Calendar**.

It combines:
- **File system monitoring** (using `watchdog`) to detect when you start working
- **Inactivity detection** (via timers) to determine when you've stopped
- **Google Calendar API** to log the session with timestamps and project name

---

## ✅ What It Does

- Watches a target folder (like your VS Code projects directory)
- Starts a "session" when a file is modified
- Ends the session after **30 minutes of inactivity**
- Ignores sessions shorter than **10 minutes**
- Logs valid sessions as calendar events in your Google Calendar (including the project folder name)

---

## 🏗️ Project Structure
│
├── monitor.py # Watches directory, detects sessions
├── calendar_integration.py # Handles Google Calendar API logic
├── credentials.json # Google API credentials 
├── token.json # Generated after first login (auto-created)

