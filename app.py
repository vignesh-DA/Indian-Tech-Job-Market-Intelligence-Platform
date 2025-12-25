"""
Indian Tech Job Market Intelligence Platform
Main Streamlit App
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
from src.logger import logging
from src.exception import CustomException
from src.data_loader import load_recent_jobs
from src.scrapers import fetch_and_save_jobs

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Indian Tech Job Market Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'skills': [],
        'role': 'Software Engineer',
        'experience': '0-2 years',
        'location': 'Bangalore',
        'preferred_locations': []
    }

if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []

if 'applications' not in st.session_state:
    st.session_state.applications = []

# Data Management state
if 'fetch_in_progress' not in st.session_state:
    st.session_state.fetch_in_progress = False

if 'fetch_status' not in st.session_state:
    st.session_state.fetch_status = None  # 'success', 'error', or None

if 'fetch_message' not in st.session_state:
    st.session_state.fetch_message = ""

if 'last_updated_timestamp' not in st.session_state:
    st.session_state.last_updated_timestamp = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def fetch_jobs_callback():
    """Callback function to handle job fetching with proper state management"""
    st.session_state.fetch_in_progress = True
    st.session_state.fetch_status = None
    st.session_state.fetch_message = ""
    
    try:
        app_id = os.getenv('ADZUNA_APP_ID')
        app_key = os.getenv('ADZUNA_APP_KEY')
        
        result = fetch_and_save_jobs(app_id, app_key)
        
        if result is not None and not result.empty:
            st.session_state.fetch_status = 'success'
            st.session_state.fetch_message = f"✅ Successfully updated! {len(result)} jobs fetched."
            st.session_state.last_updated_timestamp = datetime.now()
            logging.info(f"Job fetch successful: {len(result)} jobs")
        else:
            st.session_state.fetch_status = 'error'
            st.session_state.fetch_message = "❌ Failed to fetch jobs. Please try again."
            logging.warning("Job fetch returned empty data")
            
    except Exception as e:
        st.session_state.fetch_status = 'error'
        st.session_state.fetch_message = f"❌ Error: {str(e)}"
        logging.error(f"Error fetching jobs: {str(e)}")
    
    finally:
        st.session_state.fetch_in_progress = False


def get_last_updated_display():
    """Get formatted last updated timestamp from latest CSV file"""
    try:
        data_dir = "data"
        if not os.path.exists(data_dir):
            return "Never"
        
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if not csv_files:
            return "Never"
        
        file_paths = [os.path.join(data_dir, f) for f in csv_files]
        latest_file = max(file_paths, key=os.path.getmtime)
        
        mod_time = os.path.getmtime(latest_file)
        last_updated = datetime.fromtimestamp(mod_time)
        
        return last_updated.strftime("%B %d, %Y at %I:%M %p")
    except Exception as e:
        logging.error(f"Error getting last updated time: {str(e)}")
        return "Unknown"


def initialize_session_state():
    """Initialize session state variables"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'skills': [],
            'experience': '0-2 years',
            'location': 'Bangalore',
            'role': 'Software Engineer'
        }
    
    if 'saved_jobs' not in st.session_state:
        st.session_state.saved_jobs = []
    
    if 'jobs_loaded' not in st.session_state:
        st.session_state.jobs_loaded = False


def display_home():
    """Display home page content"""
    try:
        # Header
        st.markdown('<h1 class="main-header">🇮🇳 Indian Tech Job Market Intelligence</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        ### Welcome to Your AI-Powered Job Search Assistant
        
        Discover smarter job matches and career insights tailored just for you.
        """)
        
        # Features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🎯 Smart Recommendations
            - ML-powered job matching
            - Skills gap analysis
            - Learning suggestions
            - Top 10 personalized matches
            """)
        
        with col2:
            st.markdown("""
            #### 📊 Market Intelligence
            - Real-time salary trends
            - Top in-demand skills
            - Hiring companies
            - Location insights
            """)
        
        with col3:
            st.markdown("""
            #### 💾 Save & Track
            - Bookmark favorite jobs
            - Build your profile
            - Track applications
            - Career planning tools
            """)
        
        st.divider()
        
        # Quick Stats
        st.subheader("📈 Market Overview")
        
        # Load jobs data
        jobs_df = load_recent_jobs(days=30)
        
        if not jobs_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Jobs</div>
                    <div class="stat-value">{len(jobs_df):,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                companies = jobs_df['company'].nunique()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Companies Hiring</div>
                    <div class="stat-value">{companies:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                locations = jobs_df['location'].nunique()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Locations</div>
                    <div class="stat-value">{locations}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Calculate average salary
                valid_salaries = jobs_df[
                    (jobs_df['salary_min'] > 0) & 
                    (jobs_df['salary_max'] > 0)
                ]
                if not valid_salaries.empty:
                    avg_sal = (valid_salaries['salary_min'] + valid_salaries['salary_max']) / 2
                    avg_salary = int(avg_sal.mean())
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Avg Salary (₹)</div>
                        <div class="stat-value">{avg_salary/100000:.1f}L</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="stat-card">
                        <div class="stat-label">Avg Salary</div>
                        <div class="stat-value">N/A</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.session_state.jobs_loaded = True
        else:
            st.warning("⚠️ No job data available. Please fetch jobs first.")
            st.session_state.jobs_loaded = False
        
        st.divider()
        
        # Getting Started
        st.subheader("🚀 Getting Started")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **First Time Here?**
            1. Navigate to **🎯 Job Recommendations**
            2. Enter your skills and preferences
            3. Get personalized job matches
            4. Save jobs you're interested in
            """)
        
        with col2:
            st.markdown("""
            **Explore Market Trends**
            1. Visit **📊 Market Dashboard**
            2. Filter by location or date
            3. Analyze salary trends
            4. Discover top skills to learn
            """)
        
        st.divider()
        
        # Data Management Section
        st.subheader("📥 Data Management")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("""
            Keep your job database up to date by fetching the latest opportunities from our data source.
            """)
        
        with col2:
            # Fetch button with disabled state during loading
            if st.session_state.fetch_in_progress:
                st.button(
                    "⏳ Fetching latest jobs…",
                    disabled=True,
                    use_container_width=True,
                    type="primary"
                )
                st.info("⏳ Fetching fresh job data. This may take up to 3 minutes. Please do not refresh or leave this page.")
            else:
                st.button(
                    "📥 Fetch Latest Jobs",
                    on_click=fetch_jobs_callback,
                    use_container_width=True,
                    type="primary"
                )
        
        with col3:
            pass  # Spacing
        
        # Status messages
        if st.session_state.fetch_status == 'success':
            st.success(st.session_state.fetch_message, icon="✅")
            st.session_state.fetch_status = None  # Clear after displaying
        
        if st.session_state.fetch_status == 'error':
            st.error(st.session_state.fetch_message, icon="❌")
            st.session_state.fetch_status = None  # Clear after displaying
        
        # Last updated timestamp
        st.divider()
        last_updated_str = get_last_updated_display()
        st.caption(f"Last updated: {last_updated_str}")
        
    except Exception as e:
        logging.error(f"Error in display_home: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        raise CustomException(e, sys)


def main():
    """Main application entry point"""
    try:
        # Initialize session state
        initialize_session_state()
        
        # Sidebar
        with st.sidebar:
            st.image("https://img.icons8.com/fluency/96/000000/job.png", width=80)
            st.title("Navigation")
            st.markdown("""
            Use the pages above to navigate:
            - 🎯 **Job Recommendations**
            - 📊 **Market Dashboard**
            - 💾 **Saved Jobs & Profile**
            """)
            
            st.divider()
            
            # Quick profile preview
            st.subheader("Your Profile")
            profile = st.session_state.user_profile
            st.write(f"**Role**: {profile['role']}")
            st.write(f"**Location**: {profile['location']}")
            st.write(f"**Experience**: {profile['experience']}")
            if profile['skills']:
                st.write(f"**Skills**: {len(profile['skills'])} selected")
            
            st.divider()
            
            # Footer
            st.markdown("""
            ---
            **About**
            
            Built with ❤️ using:
            - Streamlit
            - Adzuna API
            - scikit-learn
            - Plotly
            
            © 2025 Tech Job Intelligence
            """)
        
        # Display home page
        display_home()
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        st.error("An unexpected error occurred. Please check the logs.")
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
