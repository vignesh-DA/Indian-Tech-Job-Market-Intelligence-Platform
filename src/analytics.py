"""
Analytics Module
Calculate market intelligence metrics for dashboard
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from src.logger import logging
from src.exception import CustomException
from src.data_loader import normalize_location


def filter_jobs_by_location(jobs_df, location):
    """
    Filter jobs by normalized location
    
    Args:
        jobs_df: DataFrame with job data
        location: Location to filter by (normalized city name)
        
    Returns:
        Filtered DataFrame
    """
    if not location or location == 'All':
        return jobs_df
    
    filtered = []
    location_lower = location.lower()
    
    for idx, row in jobs_df.iterrows():
        normalized = normalize_location(row.get('location', '')).lower()
        if normalized == location_lower or normalized == 'remote':
            filtered.append(idx)
    
    return jobs_df.loc[filtered].copy() if filtered else pd.DataFrame()


def calculate_salary_trends(jobs_df, group_by='location'):
    """
    Calculate salary trends by location or role
    
    Args:
        jobs_df: DataFrame with job data
        group_by: Column to group by ('location', 'title', etc.)
        
    Returns:
        DataFrame with salary statistics
    """
    try:
        if jobs_df.empty or 'salary_min' not in jobs_df.columns:
            return pd.DataFrame()
        
        # Filter valid salaries
        valid_salaries = jobs_df[
            (jobs_df['salary_min'] > 0) & 
            (jobs_df['salary_max'] > 0)
        ].copy()
        
        if valid_salaries.empty:
            return pd.DataFrame()
        
        # Calculate average salary
        valid_salaries['avg_salary'] = (
            valid_salaries['salary_min'] + valid_salaries['salary_max']
        ) / 2
        
        # Group and calculate stats
        salary_stats = valid_salaries.groupby(group_by).agg({
            'avg_salary': ['mean', 'median', 'min', 'max', 'count']
        }).round(0)
        
        salary_stats.columns = ['Average Salary', 'Typical Salary', 'Lowest Salary', 'Highest Salary', 'Number of Jobs']
        salary_stats = salary_stats.reset_index()
        salary_stats = salary_stats.sort_values('Average Salary', ascending=False)
        
        logging.info(f"Calculated salary trends for {len(salary_stats)} groups")
        return salary_stats
        
    except Exception as e:
        logging.error(f"Error calculating salary trends: {str(e)}")
        raise CustomException(e, sys)


def get_top_skills(jobs_df, top_n=20):
    """
    Get most in-demand skills from jobs
    
    Args:
        jobs_df: DataFrame with job data
        top_n: Number of top skills to return
        
    Returns:
        DataFrame with skill counts
    """
    try:
        if jobs_df.empty or 'skills' not in jobs_df.columns:
            return pd.DataFrame()
        
        # Count skill occurrences
        skill_counts = {}
        
        for skills_str in jobs_df['skills'].dropna():
            if isinstance(skills_str, str):
                skills = [s.strip() for s in skills_str.split(',')]
                for skill in skills:
                    if skill:
                        skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Convert to dataframe
        skills_df = pd.DataFrame(
            list(skill_counts.items()),
            columns=['skill', 'count']
        )
        
        skills_df = skills_df.sort_values('count', ascending=False).head(top_n)
        
        logging.info(f"Found {len(skills_df)} top skills")
        return skills_df
        
    except Exception as e:
        logging.error(f"Error getting top skills: {str(e)}")
        return pd.DataFrame()


def get_top_companies(jobs_df, top_n=15):
    """
    Get companies with most job postings
    
    Args:
        jobs_df: DataFrame with job data
        top_n: Number of top companies to return
        
    Returns:
        DataFrame with company job counts
    """
    try:
        if jobs_df.empty or 'company' not in jobs_df.columns:
            return pd.DataFrame()
        
        company_counts = jobs_df['company'].value_counts().head(top_n)
        
        companies_df = pd.DataFrame({
            'company': company_counts.index,
            'job_count': company_counts.values
        })
        
        logging.info(f"Found {len(companies_df)} top companies")
        return companies_df
        
    except Exception as e:
        logging.error(f"Error getting top companies: {str(e)}")
        return pd.DataFrame()


def calculate_location_stats(jobs_df):
    """
    Calculate job statistics by location
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        DataFrame with location statistics
    """
    try:
        if jobs_df.empty or 'location' not in jobs_df.columns:
            return pd.DataFrame()
        
        location_stats = jobs_df.groupby('location').agg({
            'job_id': 'count',
            'salary_min': 'mean',
            'salary_max': 'mean'
        }).round(0)
        
        location_stats.columns = ['job_count', 'avg_salary_min', 'avg_salary_max']
        location_stats['avg_salary'] = (
            location_stats['avg_salary_min'] + location_stats['avg_salary_max']
        ) / 2
        
        location_stats = location_stats.reset_index()
        location_stats = location_stats.sort_values('job_count', ascending=False)
        
        logging.info(f"Calculated stats for {len(location_stats)} locations")
        return location_stats
        
    except Exception as e:
        logging.error(f"Error calculating location stats: {str(e)}")
        return pd.DataFrame()


def get_posting_trends(jobs_df, days=30):
    """
    Get job posting trends over time
    
    Args:
        jobs_df: DataFrame with job data
        days: Number of days to analyze
        
    Returns:
        DataFrame with daily job counts
    """
    try:
        if jobs_df.empty or 'posted_date' not in jobs_df.columns:
            return pd.DataFrame()
        
        # Ensure posted_date is datetime with UTC timezone
        jobs_df['posted_date'] = pd.to_datetime(jobs_df['posted_date'], errors='coerce', utc=True)
        
        # Filter recent posts (make cutoff_date timezone-aware)
        cutoff_date = pd.Timestamp(datetime.now() - timedelta(days=days)).tz_localize('UTC')
        recent_jobs = jobs_df[jobs_df['posted_date'] >= cutoff_date].copy()
        
        if recent_jobs.empty:
            return pd.DataFrame()
        
        # Extract date only
        recent_jobs['date'] = recent_jobs['posted_date'].dt.date
        
        # Count jobs per day
        daily_counts = recent_jobs.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        # Fill missing dates with 0
        date_range = pd.date_range(
            start=cutoff_date.date(),
            end=datetime.now().date(),
            freq='D'
        )
        
        full_range = pd.DataFrame({'date': date_range})
        daily_counts = full_range.merge(daily_counts, on='date', how='left')
        daily_counts['count'] = daily_counts['count'].fillna(0).astype(int)
        
        logging.info(f"Calculated posting trends for {len(daily_counts)} days")
        return daily_counts
        
    except Exception as e:
        logging.error(f"Error calculating posting trends: {str(e)}")
        return pd.DataFrame()


def get_experience_distribution(jobs_df):
    """
    Get distribution of experience requirements
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        DataFrame with experience level counts
    """
    try:
        if jobs_df.empty or 'experience' not in jobs_df.columns:
            return pd.DataFrame()
        
        exp_counts = jobs_df['experience'].value_counts()
        
        exp_df = pd.DataFrame({
            'experience_level': exp_counts.index,
            'count': exp_counts.values
        })
        
        logging.info(f"Calculated experience distribution")
        return exp_df
        
    except Exception as e:
        logging.error(f"Error calculating experience distribution: {str(e)}")
        return pd.DataFrame()


def get_role_distribution(jobs_df, top_n=10):
    """
    Get distribution of job roles
    
    Args:
        jobs_df: DataFrame with job data
        top_n: Number of top roles to return
        
    Returns:
        DataFrame with role counts
    """
    try:
        if jobs_df.empty or 'title' not in jobs_df.columns:
            return pd.DataFrame()
        
        # Simplify job titles by extracting key roles
        def extract_role(title):
            title_lower = str(title).lower()
            if 'data scientist' in title_lower:
                return 'Data Scientist'
            elif 'data engineer' in title_lower:
                return 'Data Engineer'
            elif 'data analyst' in title_lower:
                return 'Data Analyst'
            elif 'full stack' in title_lower:
                return 'Full Stack Developer'
            elif 'frontend' in title_lower or 'front end' in title_lower:
                return 'Frontend Developer'
            elif 'backend' in title_lower or 'back end' in title_lower:
                return 'Backend Developer'
            elif 'devops' in title_lower:
                return 'DevOps Engineer'
            elif 'machine learning' in title_lower or 'ml engineer' in title_lower:
                return 'ML Engineer'
            elif 'software engineer' in title_lower or 'software developer' in title_lower:
                return 'Software Engineer'
            elif 'qa' in title_lower or 'test' in title_lower:
                return 'QA Engineer'
            else:
                return 'Other'
        
        jobs_df['role'] = jobs_df['title'].apply(extract_role)
        
        role_counts = jobs_df['role'].value_counts().head(top_n)
        
        role_df = pd.DataFrame({
            'role': role_counts.index,
            'count': role_counts.values
        })
        
        logging.info(f"Calculated role distribution")
        return role_df
        
    except Exception as e:
        logging.error(f"Error calculating role distribution: {str(e)}")
        return pd.DataFrame()


def calculate_summary_stats(jobs_df):
    """
    Calculate overall summary statistics
    
    Args:
        jobs_df: DataFrame with job data
        
    Returns:
        Dictionary with summary stats
    """
    try:
        if jobs_df.empty:
            return {}
        
        stats = {
            'total_jobs': len(jobs_df),
            'total_companies': jobs_df['company'].nunique() if 'company' in jobs_df.columns else 0,
            'total_locations': jobs_df['location'].nunique() if 'location' in jobs_df.columns else 0,
            'avg_salary': 0,
            'jobs_today': 0,
            'jobs_this_week': 0
        }
        
        # Calculate average salary
        if 'salary_min' in jobs_df.columns and 'salary_max' in jobs_df.columns:
            valid_salaries = jobs_df[
                (jobs_df['salary_min'] > 0) & 
                (jobs_df['salary_max'] > 0)
            ]
            if not valid_salaries.empty:
                avg_sal = (valid_salaries['salary_min'] + valid_salaries['salary_max']) / 2
                stats['avg_salary'] = int(avg_sal.mean())
        
        # Calculate recent postings
        if 'posted_date' in jobs_df.columns:
            jobs_df['posted_date'] = pd.to_datetime(jobs_df['posted_date'], errors='coerce')
            today = datetime.now().date()
            week_ago = today - timedelta(days=7)
            
            stats['jobs_today'] = len(jobs_df[jobs_df['posted_date'].dt.date == today])
            stats['jobs_this_week'] = len(jobs_df[jobs_df['posted_date'].dt.date >= week_ago])
        
        logging.info("Calculated summary statistics")
        return stats
        
    except Exception as e:
        logging.error(f"Error calculating summary stats: {str(e)}")
        return {}
