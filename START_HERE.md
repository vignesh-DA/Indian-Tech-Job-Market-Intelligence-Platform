# 🚀 START HERE - Quick Instructions

## Get Your Job Intelligence Platform Running in 3 Steps!

### Step 1: Install Dependencies (2 minutes)
Open terminal/command prompt in this folder and run:

```bash
pip install -r requirements.txt
```

Wait for all packages to install...

### Step 2: Get API Credentials (3 minutes)

1. Visit: https://developer.adzuna.com/
2. Click "Sign Up" (free!)
3. Create new application
4. Copy your **App ID** and **App Key**

5. Create `.env` file by copying the example:
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

6. Open `.env` and paste your credentials:
   ```
   ADZUNA_APP_ID=paste_your_app_id_here
   ADZUNA_APP_KEY=paste_your_app_key_here
   ```

### Step 3: Launch! (1 minute)

**Option A - Fetch data first (recommended):**
```bash
python fetch_jobs.py
streamlit run app.py
```

**Option B - Use run script:**
```bash
# Windows: Double-click run.bat
# Or in terminal:
run.bat

# Mac/Linux:
./run.sh
```

**Option C - Launch directly and fetch later:**
```bash
streamlit run app.py
# Use "Fetch Latest Jobs" button in the app
```

## 🎉 That's It!

Your browser will open at: **http://localhost:8501**

## First-Time Usage:

1. **Homepage**: See market overview
2. **Job Recommendations** (sidebar):
   - Select your skills (e.g., Python, React, AWS)
   - Enter role: "Software Engineer"
   - Choose experience: "2-5 years"
   - Select location: "Bangalore"
   - Click "Find Matching Jobs"
3. **View Results**: See your personalized top 10 matches!
4. **Save Jobs**: Click 💾 on jobs you like
5. **Explore Dashboard**: Check market trends and salary insights

## 📚 Need More Help?

- **Quick Setup**: Read [QUICKSTART.md](QUICKSTART.md)
- **Full Docs**: Read [README.md](README.md)
- **Deployment**: Read [DEPLOYMENT.md](DEPLOYMENT.md)
- **Summary**: Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## ❓ Common Issues

**"No job data available"**
→ Run: `python fetch_jobs.py`

**"Import errors"**
→ Run: `pip install -r requirements.txt`

**"Can't fetch jobs"**
→ Check your API credentials in .env file

**"Port already in use"**
→ Close other Streamlit apps or change port in .streamlit/config.toml

## 🎯 You're All Set!

Enjoy your AI-powered job search platform!

---

**Questions?** Check the documentation files or review logs/ directory for errors.

**Happy Job Hunting! 🚀**
