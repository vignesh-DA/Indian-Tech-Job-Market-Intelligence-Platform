# 🚀 Quick Start Guide

Get the Indian Tech Job Market Intelligence Platform up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- pip package manager
- Internet connection
- Command line/terminal access

## Step-by-Step Setup

### 1. Install Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Streamlit (web framework)
- pandas, numpy (data processing)
- scikit-learn (machine learning)
- plotly (visualizations)
- requests (API calls)

**Expected time**: 2-3 minutes

### 2. Get API Credentials (Required for Real Data)

To fetch real job data:

1. Visit: https://developer.adzuna.com/
2. Click "Sign Up" (free account)
3. Create a new application
4. Copy your **App ID** and **App Key**

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your credentials:

```
ADZUNA_APP_ID=your_actual_app_id_here
ADZUNA_APP_KEY=your_actual_app_key_here
```

### 4. Fetch Initial Job Data

Run the fetch script:

```bash
python fetch_jobs.py
```

This will:
- Connect to Adzuna API
- Fetch jobs for multiple roles and locations
- Save data to `data/jobs_<date>.csv`
- Take 2-3 minutes

**Expected output**:
```
✅ SUCCESS! Fetched 400 jobs
   Companies: 150
   Locations: 6
```

### 5. Launch the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

## Using the Application

### Home Page
- View market overview
- See total jobs, companies, locations
- Manually fetch more jobs if needed

### 🎯 Job Recommendations
1. Click "Job Recommendations" in the sidebar
2. Select your skills (multi-select dropdown)
3. Enter your desired role (e.g., "Software Engineer")
4. Choose experience level
5. Select preferred location
6. Click **"Find Matching Jobs"**
7. Review your personalized matches with scores!

### 📊 Market Dashboard
1. Click "Market Dashboard" in the sidebar
2. Explore interactive charts:
   - Salary trends by location
   - Top in-demand skills
   - Hiring companies
   - Posting trends
3. Use filters to narrow down data
4. Export data as CSV

### 💾 Saved Jobs
1. Save jobs from recommendations page
2. Manage your saved jobs
3. Track applications
4. Export your list

## Troubleshooting

### "No job data available"
**Solution**: Run `python fetch_jobs.py` or click "Fetch Latest Jobs" button

### "Module not found" errors
**Solution**: 
```bash
pip install -r requirements.txt
```

### API credentials not working
**Solution**: 
1. Double-check your App ID and App Key
2. Make sure .env file is in the project root
3. Restart the Streamlit app

### Port already in use
**Solution**:
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9
```

Then run `streamlit run app.py` again

## Without API Credentials

If you don't have Adzuna API credentials yet:

1. You can still run the app: `streamlit run app.py`
2. The app will work but won't have job data initially
3. You'll see a message: "No job data available"
4. Get credentials and use the "Fetch Latest Jobs" button

## Next Steps

1. ✅ Set up your profile in Job Recommendations
2. ✅ Explore market insights in Dashboard
3. ✅ Save interesting jobs
4. ✅ Export data for your job search
5. ✅ Schedule daily data refresh (optional)

## Daily Data Refresh (Optional)

To keep data fresh, fetch jobs daily:

**Windows** - Create a scheduled task:
```bash
# Run fetch_jobs.py daily at 9 AM
schtasks /create /tn "FetchJobs" /tr "python E:\Project\gravitohacks\fetch_jobs.py" /sc daily /st 09:00
```

**Linux/Mac** - Add to crontab:
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/gravitohacks && python fetch_jobs.py
```

## Performance Tips

- The app caches data for 1 hour for better performance
- Clear cache: Press `C` in the app
- Filter data to reduce load time
- Export data for offline analysis

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review troubleshooting section
- Check logs in `logs/` directory
- Verify API credentials at https://developer.adzuna.com/

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Fetch job data
python fetch_jobs.py

# Run the app
streamlit run app.py

# Update dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version

# Verify installation
pip list | findstr streamlit
```

## File Structure Overview

```
gravitohacks/
├── app.py              ← Main application (run this)
├── fetch_jobs.py       ← Data fetching script
├── requirements.txt    ← Dependencies
├── .env               ← Your API credentials
├── pages/             ← App pages
├── src/               ← Core logic
├── data/              ← Job data (CSV files)
└── models/            ← ML models
```

## What You Should See

After successful setup:

1. **Home Page**: Shows 300-500 jobs, companies, locations
2. **Recommendations**: Personalized job matches with 60-90% scores
3. **Dashboard**: Interactive charts with real data
4. **Saved Jobs**: Empty initially, populate by saving jobs

## Success Checklist

- [ ] Dependencies installed
- [ ] API credentials configured
- [ ] Initial jobs fetched (300+ jobs)
- [ ] App running on localhost:8501
- [ ] Can navigate all 3 pages
- [ ] Can see recommendations
- [ ] Can view dashboard charts
- [ ] Can save jobs

---

**You're all set! Start exploring job opportunities!** 🎉

For detailed documentation, see [README.md](README.md)
