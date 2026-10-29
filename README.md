# Smart Recommendation System

A personalized career recommendation system for students that suggests learning paths, skills to develop, and learning resources.

## Run locally

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies and start the application:

   ```powershell
   pip install -r requirements.txt
   python app.py
   ```

3. Open http://127.0.0.1:5000 in your browser.

The SQLite database (`students.db`) is created in the current directory when the app starts. Student profiles can be viewed at `/profiles`.
