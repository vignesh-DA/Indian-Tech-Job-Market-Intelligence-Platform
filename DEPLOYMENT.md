# 📋 Project Setup & Deployment Guide

## Complete Setup Instructions

### Windows Setup

1. **Open PowerShell/Command Prompt in project directory**

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure API credentials:**
   ```powershell
   copy .env.example .env
   # Edit .env file and add your Adzuna credentials
   ```

5. **Fetch initial data:**
   ```powershell
   python fetch_jobs.py
   ```

6. **Run the application:**
   ```powershell
   streamlit run app.py
   # OR simply run:
   run.bat
   ```

### Linux/Mac Setup

1. **Open terminal in project directory**

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env file and add your Adzuna credentials
   ```

5. **Make run script executable:**
   ```bash
   chmod +x run.sh
   ```

6. **Fetch initial data:**
   ```bash
   python fetch_jobs.py
   ```

7. **Run the application:**
   ```bash
   streamlit run app.py
   # OR simply run:
   ./run.sh
   ```

## Getting Adzuna API Credentials

1. Go to https://developer.adzuna.com/
2. Click "Sign Up" (it's free!)
3. Create an account
4. Click "Create Application"
5. Fill in basic details (any name works)
6. You'll receive:
   - **App ID**: A numeric ID (e.g., 12345678)
   - **App Key**: A 32-character key

## Environment Variables Setup

Create `.env` file with:

```env
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

**Important**: 
- Never commit `.env` to Git (it's in .gitignore)
- The app will work without credentials but won't fetch data
- You can fetch data later using the UI button

## Project Structure Explained

```
gravitohacks/
│
├── app.py                          # Homepage with market overview
│
├── pages/                          # Multi-page Streamlit app
│   ├── 1_🎯_Job_Recommendations.py  # ML-powered job matching
│   ├── 2_📊_Market_Dashboard.py     # Analytics and insights
│   └── 3_💾_Saved_Jobs.py           # Saved jobs and profile
│
├── src/                            # Core application logic
│   ├── __init__.py                 # Package initializer
│   ├── data_loader.py              # CSV data loading with caching
│   ├── scrapers.py                 # Adzuna API integration
│   ├── recommendation_engine.py    # ML matching algorithm
│   ├── analytics.py                # Dashboard calculations
│   ├── exception.py                # Custom exception handling
│   ├── logger.py                   # Logging configuration
│   └── utils.py                    # Utility functions
│
├── data/                           # Job data storage (CSV files)
│   └── jobs_YYYY_MM_DD.csv         # Daily job data files
│
├── models/                         # Saved ML models
│   └── recommendation_model.pkl    # Trained TF-IDF model
│
├── logs/                           # Application logs
│   └── MM_DD_YYYY_HH_MM_SS.log    # Timestamped log files
│
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                 # Theme and server settings
│
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup configuration
├── .env.example                    # Environment variables template
├── .env                           # Your credentials (not in Git)
├── .gitignore                     # Git ignore rules
├── fetch_jobs.py                  # Script to fetch initial data
├── run.bat                        # Windows startup script
├── run.sh                         # Linux/Mac startup script
├── README.md                      # Comprehensive documentation
└── QUICKSTART.md                  # Quick start guide
```

## How It Works

### Data Flow

```
Adzuna API → fetch_jobs.py → data/jobs_*.csv → data_loader.py → Streamlit App
                                                      ↓
                                              recommendation_engine.py
                                                      ↓
                                              ML Matching Algorithm
                                                      ↓
                                              Personalized Results
```

### ML Recommendation Algorithm

1. **Data Collection**: Fetch jobs from Adzuna API
2. **Text Vectorization**: Convert job descriptions to TF-IDF vectors
3. **User Profile**: Create vector from user skills and preferences
4. **Similarity Calculation**: Cosine similarity between user and jobs
5. **Weighted Scoring**: 
   - Skills match: 70%
   - Experience match: 20%
   - Location match: 10%
6. **Ranking**: Sort by final score and return top N matches

### Caching Strategy

- Data loading cached for 1 hour (`@st.cache_data(ttl=3600)`)
- ML model cached in memory
- Reduces API calls and improves performance

## Running the Application

### Method 1: Direct Streamlit Command
```bash
streamlit run app.py
```

### Method 2: Using Run Scripts
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Method 3: Python Module
```bash
python -m streamlit run app.py
```

## Common Tasks

### Fetch New Job Data
```bash
python fetch_jobs.py
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clear Streamlit Cache
Press `C` in the running app, or:
```bash
streamlit cache clear
```

### View Logs
```bash
# Windows
type logs\*.log

# Linux/Mac
cat logs/*.log
```

### Export Data
Use the "Export to CSV" buttons in the app UI

## Deployment Options

### 1. Streamlit Cloud (Recommended - Free)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub account
4. Select repository and branch
5. Set main file: `app.py`
6. Add secrets in dashboard:
   ```
   ADZUNA_APP_ID = "your_id"
   ADZUNA_APP_KEY = "your_key"
   ```
7. Click Deploy!

### 2. Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set ADZUNA_APP_ID=your_id
heroku config:set ADZUNA_APP_KEY=your_key
git push heroku main
```

### 3. Railway

1. Connect GitHub repository
2. Add environment variables
3. Railway auto-detects Streamlit
4. Deploy automatically

### 4. Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t job-intelligence .
docker run -p 8501:8501 job-intelligence
```

## Performance Optimization

### For Large Datasets
- Increase cache TTL
- Filter data before processing
- Use database instead of CSV (optional)

### For Slow Loading
- Reduce number of jobs fetched
- Increase cache duration
- Use pagination in results

### For Memory Issues
- Load only recent 30 days
- Clear old CSV files
- Reduce model features

## API Rate Limits

Adzuna Free Tier:
- 1000 API calls per month
- 50 results per call maximum
- 1 call per second rate limit

**Best Practices**:
- Fetch data once per day
- Cache results locally
- Use stored CSV for display
- Only fetch when needed

## Troubleshooting

### No data directory
```bash
mkdir data models logs
```

### Permission denied on run.sh
```bash
chmod +x run.sh
```

### Port already in use
```bash
# Change port in .streamlit/config.toml
[server]
port = 8502

# Or kill existing process
# Windows: taskkill /F /IM streamlit.exe
# Linux/Mac: pkill -f streamlit
```

### Import errors
```bash
pip install -r requirements.txt --force-reinstall
```

### API errors
- Check credentials in .env
- Verify internet connection
- Check Adzuna API status
- Review logs for details

## Security Best Practices

1. **Never commit .env file**
   - Already in .gitignore
   - Use .env.example as template

2. **Use environment variables**
   - For API credentials
   - For sensitive configuration

3. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

4. **Review logs regularly**
   - Check for errors
   - Monitor API usage
   - Identify issues early

## Monitoring & Maintenance

### Daily Tasks
- Check app is running
- Verify data freshness
- Review error logs

### Weekly Tasks
- Fetch new job data
- Clear old logs
- Update dependencies

### Monthly Tasks
- Review API usage
- Analyze user patterns
- Update documentation
- Retrain ML model

## Support & Resources

- **Documentation**: README.md, QUICKSTART.md
- **Logs**: logs/ directory
- **Adzuna API Docs**: https://developer.adzuna.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **scikit-learn Docs**: https://scikit-learn.org

## Development Workflow

### Adding New Features

1. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Implement changes in appropriate module:
   - Data processing → `src/data_loader.py`
   - ML algorithm → `src/recommendation_engine.py`
   - UI components → page files or `app.py`
   - Analytics → `src/analytics.py`

3. Test locally:
   ```bash
   streamlit run app.py
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

5. Create pull request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Log important operations
- Handle exceptions properly

## License

MIT License - See LICENSE file

## Contributors

CS Majors Team
- Email: vigneshgogula9@gmail.com

---

**Built with ❤️ using Streamlit, Python, and Adzuna API**

Last Updated: December 22, 2025
