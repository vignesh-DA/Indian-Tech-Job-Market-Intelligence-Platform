"""
Market Intelligence Dashboard
Real-time analytics and insights on Indian tech job market
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from src.logger import logging
from src.exception import CustomException
from src.data_loader import load_recent_jobs
from src.analytics import (
    calculate_salary_trends,
    get_top_skills,
    get_top_companies,
    calculate_location_stats,
    get_posting_trends,
    get_experience_distribution,
    get_role_distribution,
    calculate_summary_stats
)


# Page configuration
st.set_page_config(
    page_title="Market Dashboard",
    page_icon="📊",
    layout="wide"
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


def create_salary_chart(salary_df, group_by):
    """Create salary trends chart"""
    if salary_df.empty:
        return None
    
    fig = px.bar(
        salary_df.head(10),
        x=group_by,
        y='mean',
        title=f"Average Salary by {group_by.title()}",
        labels={'mean': 'Average Salary (₹)', group_by: group_by.title()},
        color='mean',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    return fig


def create_skills_chart(skills_df):
    """Create top skills chart"""
    if skills_df.empty:
        return None
    
    fig = px.bar(
        skills_df.head(15),
        x='count',
        y='skill',
        orientation='h',
        title="Top In-Demand Skills",
        labels={'count': 'Number of Job Postings', 'skill': 'Skill'},
        color='count',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_companies_chart(companies_df):
    """Create top companies chart"""
    if companies_df.empty:
        return None
    
    fig = px.bar(
        companies_df.head(10),
        x='company',
        y='job_count',
        title="Top Hiring Companies",
        labels={'job_count': 'Number of Jobs', 'company': 'Company'},
        color='job_count',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    
    return fig


def create_location_chart(location_df):
    """Create location statistics chart"""
    if location_df.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=location_df['location'].head(10),
        y=location_df['job_count'].head(10),
        name='Job Count',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Jobs by Location",
        xaxis_title="Location",
        yaxis_title="Number of Jobs",
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


def create_trend_chart(trend_df):
    """Create posting trends over time chart"""
    if trend_df.empty:
        return None
    
    fig = px.line(
        trend_df,
        x='date',
        y='count',
        title="Job Posting Trends (Last 30 Days)",
        labels={'count': 'Number of Jobs', 'date': 'Date'}
    )
    
    fig.update_traces(line_color='#667eea', line_width=3)
    fig.update_layout(height=400)
    
    return fig


def create_experience_chart(exp_df):
    """Create experience distribution chart"""
    if exp_df.empty:
        return None
    
    fig = px.pie(
        exp_df,
        values='count',
        names='experience_level',
        title="Experience Level Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_role_chart(role_df):
    """Create role distribution chart"""
    if role_df.empty:
        return None
    
    fig = px.treemap(
        role_df,
        path=['role'],
        values='count',
        title="Job Roles Distribution",
        color='count',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(height=400)
    
    return fig


def main():
    """Main dashboard function"""
    try:
        st.title("📊 Tech Job Market Intelligence Dashboard")
        st.markdown("Real-time insights and analytics on the Indian tech job market")
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        days_filter = st.sidebar.slider(
            "Data Range (Days)",
            min_value=7,
            max_value=90,
            value=30,
            help="Filter jobs from last N days"
        )
        
        # Load data
        with st.spinner("Loading market data..."):
            jobs_df = load_recent_jobs(days=days_filter)
        
        if jobs_df.empty:
            st.warning("⚠️ No job data available. Please fetch jobs from the home page first.")
            return
        
        # Calculate summary stats
        stats = calculate_summary_stats(jobs_df)
        
        # Display summary metrics
        st.subheader("📈 Market Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Jobs", f"{stats.get('total_jobs', 0):,}")
        
        with col2:
            st.metric("Companies", f"{stats.get('total_companies', 0):,}")
        
        with col3:
            st.metric("Locations", f"{stats.get('total_locations', 0)}")
        
        with col4:
            avg_salary = stats.get('avg_salary', 0)
            if avg_salary > 0:
                st.metric("Avg Salary", f"₹{avg_salary/100000:.1f}L")
            else:
                st.metric("Avg Salary", "N/A")
        
        with col5:
            st.metric("Jobs This Week", f"{stats.get('jobs_this_week', 0)}")
        
        st.divider()
        
        # Additional filters
        col1, col2 = st.columns(2)
        
        with col1:
            locations = ['All'] + sorted(jobs_df['location'].dropna().unique().tolist())
            selected_location = st.selectbox("Filter by Location", locations)
        
        with col2:
            categories = ['All'] + sorted(jobs_df['category'].dropna().unique().tolist()) if 'category' in jobs_df.columns else ['All']
            selected_category = st.selectbox("Filter by Category", categories)
        
        # Apply filters
        filtered_df = jobs_df.copy()
        
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['location'] == selected_location]
        
        if selected_category != 'All' and 'category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        if filtered_df.empty:
            st.warning("No jobs found with selected filters")
            return
        
        st.info(f"Showing {len(filtered_df)} jobs based on filters")
        
        st.divider()
        
        # Row 1: Salary and Skills
        st.subheader("💰 Salary & Skills Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Salary trends by location
            salary_by_location = calculate_salary_trends(filtered_df, group_by='location')
            if not salary_by_location.empty:
                fig = create_salary_chart(salary_by_location, 'location')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough salary data available")
        
        with col2:
            # Top skills
            top_skills = get_top_skills(filtered_df, top_n=15)
            if not top_skills.empty:
                fig = create_skills_chart(top_skills)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Skills data not available")
        
        st.divider()
        
        # Row 2: Companies and Locations
        st.subheader("🏢 Companies & Locations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top companies
            top_companies = get_top_companies(filtered_df, top_n=10)
            if not top_companies.empty:
                fig = create_companies_chart(top_companies)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Company data not available")
        
        with col2:
            # Location stats
            location_stats = calculate_location_stats(filtered_df)
            if not location_stats.empty:
                fig = create_location_chart(location_stats)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Location data not available")
        
        st.divider()
        
        # Row 3: Trends and Distribution
        st.subheader("📅 Trends & Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Posting trends
            posting_trends = get_posting_trends(filtered_df, days=days_filter)
            if not posting_trends.empty:
                fig = create_trend_chart(posting_trends)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Trend data not available")
        
        with col2:
            # Experience distribution
            exp_dist = get_experience_distribution(filtered_df)
            if not exp_dist.empty:
                fig = create_experience_chart(exp_dist)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Experience data not available")
        
        st.divider()
        
        # Row 4: Role Distribution
        st.subheader("👔 Job Roles")
        
        role_dist = get_role_distribution(filtered_df, top_n=10)
        if not role_dist.empty:
            fig = create_role_chart(role_dist)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Role data not available")
        
        st.divider()
        
        # Detailed tables
        st.subheader("📋 Detailed Data Tables")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Salary Stats", "Top Skills", "Top Companies", "Locations"])
        
        with tab1:
            salary_by_location = calculate_salary_trends(filtered_df, group_by='location')
            if not salary_by_location.empty:
                st.dataframe(
                    salary_by_location.style.format({
                        'mean': '₹{:,.0f}',
                        'median': '₹{:,.0f}',
                        'min': '₹{:,.0f}',
                        'max': '₹{:,.0f}'
                    }),
                    use_container_width=True
                )
            else:
                st.info("No salary data")
        
        with tab2:
            top_skills = get_top_skills(filtered_df, top_n=30)
            if not top_skills.empty:
                st.dataframe(top_skills, use_container_width=True)
            else:
                st.info("No skills data")
        
        with tab3:
            top_companies = get_top_companies(filtered_df, top_n=30)
            if not top_companies.empty:
                st.dataframe(top_companies, use_container_width=True)
            else:
                st.info("No company data")
        
        with tab4:
            location_stats = calculate_location_stats(filtered_df)
            if not location_stats.empty:
                st.dataframe(
                    location_stats.style.format({
                        'avg_salary': '₹{:,.0f}',
                        'avg_salary_min': '₹{:,.0f}',
                        'avg_salary_max': '₹{:,.0f}'
                    }),
                    use_container_width=True
                )
            else:
                st.info("No location data")
        
        # Export option
        st.divider()
        st.subheader("💾 Export Data")
        
        col1, col2, col3 = st.columns([2, 2, 6])
        
        with col1:
            # Export filtered jobs
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Jobs CSV",
                data=csv,
                file_name=f"jobs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export salary stats
            salary_stats = calculate_salary_trends(filtered_df, group_by='location')
            if not salary_stats.empty:
                salary_csv = salary_stats.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Salary Stats",
                    data=salary_csv,
                    file_name=f"salary_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
    except Exception as e:
        logging.error(f"Error in dashboard: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
