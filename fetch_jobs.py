"""
Quick Start Script
Fetch initial job data to populate the database
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers import fetch_and_save_jobs
from src.logger import logging

def main():
    """Fetch initial job data"""
    print("=" * 60)
    print("Indian Tech Job Market Intelligence Platform")
    print("Quick Start - Fetching Initial Job Data")
    print("=" * 60)
    print()
    
    # Check for API credentials
    app_id = os.getenv('ADZUNA_APP_ID')
    app_key = os.getenv('ADZUNA_APP_KEY')
    
    if not app_id or not app_key or app_id == 'YOUR_APP_ID':
        print("⚠️  WARNING: Adzuna API credentials not found!")
        print()
        print("To fetch real job data:")
        print("1. Sign up at https://developer.adzuna.com/")
        print("2. Get your App ID and App Key")
        print("3. Create a .env file with:")
        print("   ADZUNA_APP_ID=your_app_id")
        print("   ADZUNA_APP_KEY=your_app_key")
        print()
        print("For now, you can still run the app, but you'll need to")
        print("fetch jobs using the 'Fetch Latest Jobs' button in the UI.")
        print()
        return
    
    print("✓ API credentials found")
    print()
    print("Fetching jobs from Adzuna API...")
    print("This may take a few minutes...")
    print()
    
    try:
        # Fetch jobs
        jobs_df = fetch_and_save_jobs(app_id, app_key)
        
        if jobs_df is not None and not jobs_df.empty:
            print()
            print("=" * 60)
            print(f"✅ SUCCESS! Fetched {len(jobs_df)} jobs")
            print(f"   Companies: {jobs_df['company'].nunique()}")
            print(f"   Locations: {jobs_df['location'].nunique()}")
            print()
            print("Data saved to: data/jobs_<date>.csv")
            print()
            print("You can now run the app:")
            print("   streamlit run app.py")
            print("=" * 60)
        else:
            print()
            print("❌ Failed to fetch jobs")
            print("Check your API credentials and try again")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Please check:")
        print("1. Your API credentials are correct")
        print("2. You have internet connection")
        print("3. Adzuna API is accessible")
        logging.error(f"Error in quick start: {str(e)}")

if __name__ == "__main__":
    main()
