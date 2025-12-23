# 🇮🇳 Indian Tech Job Market Intelligence Platform

A complete AI-powered job search and market intelligence platform built with Streamlit and Python. Get personalized job recommendations, real-time market insights, and career guidance powered by machine learning.

## 🚀 Features

### 1. **AI-Powered Job Recommendations** 🎯
- ML-based job matching using TF-IDF and cosine similarity
- Skills gap analysis with learning suggestions
- Personalized scoring (Skills: 70%, Experience: 20%, Location: 10%)
- Top 10 customized job matches

### 2. **Market Intelligence Dashboard** 📊
- Real-time salary trends by location and role
- Top in-demand skills analysis
- Hiring companies insights
- Location-based statistics
- Job posting trends over time
- Interactive charts with Plotly

### 3. **Saved Jobs & Profile Management** 💾
- Bookmark favorite jobs
- Application tracker
- Profile completeness tracking
- Export data to CSV

### 4. **Real-Time Data** 🔄
- Integration with Adzuna API
- Automated data refresh
- 30-day rolling data display
- Historical data for model training

## 📁 Project Structure

```
gravitohacks/
├── app.py                          # Main Streamlit app (Homepage)
├── pages/                          # Multi-page app
│   ├── 1_🎯_Job_Recommendations.py
│   ├── 2_📊_Market_Dashboard.py
│   └── 3_💾_Saved_Jobs.py
├── src/                           # Core modules
│   ├── __init__.py
│   ├── data_loader.py            # Data loading and caching
│   ├── scrapers.py               # Adzuna API integration
│   ├── recommendation_engine.py  # ML recommendation logic
│   ├── analytics.py              # Dashboard calculations
│   ├── exception.py              # Custom exception handling
│   ├── logger.py                 # Logging configuration
│   └── utils.py                  # Utility functions
├── data/                          # CSV job data storage
├── models/                        # Saved ML models
├── logs/                          # Application logs
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── setup.py                      # Package setup
└── README.md                     # This file
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn (TF-IDF, cosine similarity)
- **Visualization**: Plotly, Altair
- **Data Source**: Adzuna Jobs API
- **Scheduling**: APScheduler
- **Database**: CSV files (lightweight, no DB setup needed)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Adzuna API credentials (free signup)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd gravitohacks
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get Adzuna API Credentials
1. Visit [Adzuna Developer Portal](https://developer.adzuna.com/)
2. Sign up for a free account
3. Create an application
4. Copy your `App ID` and `App Key`

### Step 5: Configure Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your credentials
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

### Step 6: Fetch Initial Job Data
```bash
# Run the scraper directly to fetch jobs
python -c "from src.scrapers import fetch_and_save_jobs; fetch_and_save_jobs()"
```

Or use the "Fetch Latest Jobs" button in the app interface.

## 🚀 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Application

1. **Home Page**: View market overview and fetch latest jobs
2. **Job Recommendations**: 
   - Enter your skills in the sidebar
   - Select experience level and location
   - Click "Find Matching Jobs"
   - Review personalized recommendations
3. **Market Dashboard**: 
   - Explore salary trends
   - Discover top skills
   - Analyze hiring companies
4. **Saved Jobs**: 
   - Manage bookmarked jobs
   - Track applications
   - Export data

## 📊 Data Pipeline

### Data Collection
```python
# Automatic data collection from Adzuna API
from src.scrapers import fetch_and_save_jobs

# Fetch jobs for multiple roles and locations
jobs_df = fetch_and_save_jobs()
```

### Data Storage
- Jobs saved as: `data/jobs_YYYY_MM_DD.csv`
- Format: `job_id, title, company, skills, location, experience, salary, posted_date, url`
- Automatic deduplication based on job_id

### Caching Strategy
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_recent_jobs(days=30):
    # Loads only recent 30 days of data
    # Reduces memory and improves performance
```

## 🤖 ML Recommendation Algorithm

### Matching Algorithm
```python
def calculate_match(user_skills, job_skills, user_exp, job_exp):
    # Skills Match: 70% weight (TF-IDF + cosine similarity)
    skills_score = cosine_similarity(user_vector, job_vectors)
    
    # Experience Match: 20% weight
    exp_score = calculate_experience_similarity()
    
    # Location Match: 10% weight
    location_score = calculate_location_match()
    
    # Final Score
    final_score = (skills_score * 0.7 + 
                   exp_score * 0.2 + 
                   location_score * 0.1) * 100
    
    return final_score, matched_skills, missing_skills
```

### Model Training
- Uses TF-IDF vectorization on job descriptions
- Trains on historical 6-12 months of data
- Saves model to `models/recommendation_model.pkl`
- Automatic retraining with new data

## 🔧 Configuration

### Streamlit Configuration
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"

[server]
port = 8501
headless = true
```

### Logging
Logs are stored in `logs/` directory with timestamps.

## 📈 Performance Optimization

- **Caching**: All data loading functions use `@st.cache_data`
- **Lazy Loading**: Load only last 30 days for display
- **Session State**: User profile stored in session
- **Vectorization**: Pre-computed TF-IDF vectors

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard:
   ```
   ADZUNA_APP_ID = "your_app_id"
   ADZUNA_APP_KEY = "your_app_key"
   ```
5. Deploy!

### Deploy to Heroku/Railway/Render
Similar process - add environment variables in platform settings.

## 🐛 Troubleshooting

### Issue: No job data available
**Solution**: Run the fetch jobs script or click "Fetch Latest Jobs" button

### Issue: API rate limit exceeded
**Solution**: Adzuna free tier has limits. Wait or upgrade plan.

### Issue: Module import errors
**Solution**: Ensure virtual environment is activated and all packages installed

### Issue: Port already in use
**Solution**: Change port in `.streamlit/config.toml` or kill process:
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8501 | xargs kill
```

## 📝 API Rate Limits

Adzuna API Free Tier:
- 1000 calls/month
- 50 results per call
- Rate limit: 1 call/second

Optimize usage:
- Fetch data once daily
- Cache results
- Use stored CSV data for display

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👏 Acknowledgments

- [Adzuna API](https://www.adzuna.com/) for job data
- [Streamlit](https://streamlit.io/) for the amazing framework
- [scikit-learn](https://scikit-learn.org/) for ML tools
- [Plotly](https://plotly.com/) for interactive visualizations

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check troubleshooting section
- Review Adzuna API documentation

## 🔮 Future Enhancements

- [ ] Email notifications for new matching jobs
- [ ] Resume parser and auto-skill extraction
- [ ] Interview preparation resources
- [ ] Salary negotiation insights
- [ ] Company reviews integration
- [ ] Job application autofill
- [ ] Career path recommendations
- [ ] Skill demand predictions

---

**Built with ❤️ using Streamlit and Python**

Last Updated: December 22, 2025