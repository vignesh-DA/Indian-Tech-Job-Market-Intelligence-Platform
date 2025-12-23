"""
Data Loader Module
Loads job data from CSV files and caches for performance
"""
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import os
import sys
from src.logger import logging
from src.exception import CustomException

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_recent_jobs(days=30):
    """
    Load jobs from the last N days
    
    Args:
        days: Number of days to look back
        
    Returns:
        DataFrame with recent jobs
    """
    try:
        logging.info(f"Loading jobs from last {days} days")
        data_dir = "data"
        
        if not os.path.exists(data_dir):
            logging.warning("Data directory not found")
            return pd.DataFrame()
        
        # Get all CSV files in data directory
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            logging.warning("No CSV files found in data directory")
            return pd.DataFrame()
        
        # Load and combine all CSV files
        dfs = []
        for file in csv_files:
            file_path = os.path.join(data_dir, file)
            try:
                df = pd.read_csv(file_path)
                dfs.append(df)
            except Exception as e:
                logging.error(f"Error loading {file}: {str(e)}")
                continue
        
        if not dfs:
            return pd.DataFrame()
        
        # Combine all dataframes
        all_jobs = pd.concat(dfs, ignore_index=True)
        
        # Convert posted_date to datetime with UTC timezone
        all_jobs['posted_date'] = pd.to_datetime(all_jobs['posted_date'], errors='coerce', utc=True)
        
        # Filter for recent jobs (make cutoff_date timezone-aware)
        cutoff_date = pd.Timestamp(datetime.now() - timedelta(days=days)).tz_localize('UTC')
        recent_jobs = all_jobs[all_jobs['posted_date'] >= cutoff_date]
        
        # Remove duplicates based on job_id
        recent_jobs = recent_jobs.drop_duplicates(subset=['job_id'], keep='last')
        
        logging.info(f"Loaded {len(recent_jobs)} recent jobs")
        return recent_jobs
        
    except Exception as e:
        logging.error(f"Error in load_recent_jobs: {str(e)}")
        raise CustomException(e, sys)


@st.cache_data(ttl=3600)
def load_all_jobs_for_training():
    """
    Load all historical job data for ML model training
    
    Returns:
        DataFrame with all job data
    """
    try:
        logging.info("Loading all jobs for training")
        data_dir = "data"
        
        if not os.path.exists(data_dir):
            logging.warning("Data directory not found")
            return pd.DataFrame()
        
        # Get all CSV files
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            return pd.DataFrame()
        
        # Load and combine all CSV files
        dfs = []
        for file in csv_files:
            file_path = os.path.join(data_dir, file)
            try:
                df = pd.read_csv(file_path)
                dfs.append(df)
            except Exception as e:
                logging.error(f"Error loading {file}: {str(e)}")
                continue
        
        if not dfs:
            return pd.DataFrame()
        
        all_jobs = pd.concat(dfs, ignore_index=True)
        
        # Remove duplicates
        all_jobs = all_jobs.drop_duplicates(subset=['job_id'], keep='last')
        
        logging.info(f"Loaded {len(all_jobs)} total jobs for training")
        return all_jobs
        
    except Exception as e:
        logging.error(f"Error in load_all_jobs_for_training: {str(e)}")
        raise CustomException(e, sys)


def save_jobs_to_csv(jobs_df):
    """
    Save jobs dataframe to CSV with today's date
    
    Args:
        jobs_df: DataFrame with job data
    """
    try:
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        today = datetime.now().strftime("%Y_%m_%d")
        filename = f"jobs_{today}.csv"
        filepath = os.path.join(data_dir, filename)
        
        jobs_df.to_csv(filepath, index=False)
        logging.info(f"Saved {len(jobs_df)} jobs to {filepath}")
        
    except Exception as e:
        logging.error(f"Error saving jobs to CSV: {str(e)}")
        raise CustomException(e, sys)


def get_unique_skills(jobs_df):
    """
    Extract unique skills from all jobs
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        List of unique skills
    """
    try:
        if jobs_df.empty or 'skills' not in jobs_df.columns:
            return []
        
        all_skills = set()
        for skills_str in jobs_df['skills'].dropna():
            if isinstance(skills_str, str):
                skills = [s.strip() for s in skills_str.split(',')]
                all_skills.update(skills)
        
        return sorted(list(all_skills))
        
    except Exception as e:
        logging.error(f"Error extracting skills: {str(e)}")
        return []


def get_unique_locations(jobs_df):
    """
    Get unique job locations
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        List of unique locations
    """
    try:
        if jobs_df.empty or 'location' not in jobs_df.columns:
            return []
        
        locations = jobs_df['location'].dropna().unique().tolist()
        return sorted(locations)
        
    except Exception as e:
        logging.error(f"Error extracting locations: {str(e)}")
        return []


def get_unique_companies(jobs_df):
    """
    Get unique company names
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        List of unique companies
    """
    try:
        if jobs_df.empty or 'company' not in jobs_df.columns:
            return []
        
        companies = jobs_df['company'].dropna().unique().tolist()
        return sorted(companies)
        
    except Exception as e:
        logging.error(f"Error extracting companies: {str(e)}")
        return []
