# Quick Start - Real-Time Implementation

## Get Started in 2 Minutes

### 1. Start the App
```bash
cd e:\Project\gravitohacks
streamlit run app.py
```

**Output:**
```
Local URL: http://localhost:8501
```

### 2. Open in Browser
Click the URL or go to: **http://localhost:8501**

### 3. Explore Features
- 🏠 **Home**: See market overview, fetch new jobs
- 🎯 **Job Recommendations**: Get personalized job matches
- 📊 **Market Dashboard**: Analyze trends and salaries
- 💾 **Saved Jobs**: Bookmark your favorite positions

## Fetch Real-Time Data

### Option A: From UI (Easiest)
1. Go to Home page
2. Scroll to "🔄 Data Management"
3. Click **"🔄 Fetch Latest Jobs"**
4. Wait for completion
5. Data updates automatically

### Option B: From Terminal
```bash
python fetch_jobs.py
```

### Option C: From Python
```python
from src.scrapers import fetch_and_save_jobs
from dotenv import load_dotenv
import os

load_dotenv()
result = fetch_and_save_jobs(
    os.getenv('ADZUNA_APP_ID'),
    os.getenv('ADZUNA_APP_KEY')
)
print(f"Fetched {len(result)} jobs" if result else "Fetch failed")
```

## Key Features Ready to Use

### 🎯 Smart Recommendations
- Enter your skills
- Get matched jobs ranked by relevance
- See matched and missing skills
- Get learning suggestions

### 📊 Market Insights
- Real-time salary trends
- Top in-demand skills
- Company hiring patterns
- Location-based analysis
- Time-series visualization

### 💾 Job Management
- Save jobs you like
- Track your saved list
- Plan your applications
- Build your profile

## Data Status

| Item | Status |
|------|--------|
| Jobs Available | ✅ 3,567 jobs |
| API Credentials | ✅ Configured |
| Recommendation Engine | ✅ Ready |
| Real-Time Fetch | ✅ Ready |

## Need Help?

### Check If App Is Working
```bash
# In a new terminal
curl http://localhost:8501
```

### View Logs
```bash
type logs\*.log | tail -20
```

### Reset Everything
```bash
# Delete models (will retrain automatically)
del models\recommendation_model.pkl

# Restart app
streamlit run app.py
```

## API Info

**Service**: Adzuna Job API
**Regions**: India (configured for Indian tech jobs)
**Credentials**: Set in `.env` ✅

### Update Credentials (if needed)
1. Sign up at: https://developer.adzuna.com/
2. Get App ID and App Key
3. Edit `.env`:
   ```env
   ADZUNA_APP_ID=your_id
   ADZUNA_APP_KEY=your_key
   ```
4. Restart app

## Performance

- **First Load**: ~3 seconds (uses existing data)
- **Fetch Fresh**: ~30-60 seconds (API depends on responsiveness)
- **Job Search**: <1 second
- **Recommendations**: ~1-2 seconds
- **Dashboard**: ~2-5 seconds

## What Happens Behind the Scenes

1. **Load Data**: App loads all CSV files from `data/` folder
2. **Train Model**: Creates TF-IDF vectorizer for job matching
3. **Cache Data**: Stores in memory for 1 hour
4. **On Fetch**: Downloads fresh jobs from Adzuna API
5. **Auto Save**: Saves new jobs with today's date
6. **Retrain Model**: Updates recommendations with new data

## Troubleshooting Quick Fixes

### App Won't Start
```bash
# Kill any existing Streamlit process
taskkill /F /IM python.exe

# Try again
streamlit run app.py
```

### Fetch Not Working
1. Check internet connection
2. Verify `.env` has valid credentials
3. Try again (API might be slow)
4. Check `logs/` for errors

### No Jobs Showing
1. Make sure `data/jobs_2025_12_23.csv` exists
2. Refresh page (F5)
3. Restart app: `Ctrl+C` then `streamlit run app.py`

## Next Steps

1. ✅ Start the app
2. ✅ Test all 3 pages
3. ✅ Try fetching new jobs
4. ✅ Generate recommendations
5. ✅ Explore market dashboard
6. ✅ Save some jobs
7. ✅ Review data freshness

**Everything is ready. Start exploring!**

```bash
streamlit run app.py
```

---
📱 Open: http://localhost:8501
🚀 Status: Ready for production
✅ All features working
