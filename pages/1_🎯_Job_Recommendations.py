"""
Job Recommendations Page
ML-powered job matching with skills analysis
"""
import streamlit as st
import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException
from src.data_loader import load_recent_jobs, load_all_jobs_for_training, get_unique_skills
from src.recommendation_engine import JobRecommendationEngine, get_learning_suggestions


# Page configuration
st.set_page_config(
    page_title="Job Recommendations",
    page_icon="🎯",
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


def initialize_engine():
    """Initialize and train recommendation engine"""
    try:
        if 'recommendation_engine' not in st.session_state:
            engine = JobRecommendationEngine()
            
            # Try to load saved model
            if not engine.load_model():
                # Train new model
                with st.spinner("Training recommendation engine..."):
                    jobs_df = load_all_jobs_for_training()
                    if not jobs_df.empty:
                        engine.train(jobs_df)
                        engine.save_model()
            
            st.session_state.recommendation_engine = engine
        
        return st.session_state.recommendation_engine
        
    except Exception as e:
        logging.error(f"Error initializing engine: {str(e)}")
        return None


def display_job_card(job, rank):
    """Display a job recommendation card"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### #{rank} {job['title']}")
            st.markdown(f"**{job['company']}** • {job['location']}")
        
        with col2:
            st.metric("Match Score", f"{job['match_score']}%")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Experience Required**")
            st.write(job['experience'])
        
        with col2:
            st.markdown("**Salary**")
            salary_display = job['salary']
            if salary_display != "Not specified" and job.get('salary_min', 0) > 0:
                min_sal = job['salary_min'] / 100000
                max_sal = job['salary_max'] / 100000
                st.write(f"₹{min_sal:.1f}L - ₹{max_sal:.1f}L")
            else:
                st.write("Not specified")
        
        with col3:
            st.markdown("**Posted Date**")
            if pd.notna(job.get('posted_date')):
                posted_date = pd.to_datetime(job['posted_date'])
                # Make timezone-aware comparison
                now = pd.Timestamp.now(tz='UTC') if posted_date.tz else pd.Timestamp.now()
                days_ago = (now - posted_date).days
                st.write(f"{days_ago} days ago")
            else:
                st.write("Recently")
        
        # Skills analysis
        col1, col2 = st.columns(2)
        
        with col1:
            matched_skills = job.get('matched_skills', '')
            if matched_skills:
                st.markdown("**✅ Your Matching Skills**")
                skills_list = [s.strip() for s in matched_skills.split(',')]
                st.write(", ".join(skills_list))
            else:
                st.markdown("**✅ Your Matching Skills**")
                st.write("General match")
        
        with col2:
            missing_skills = job.get('missing_skills', '')
            if missing_skills:
                st.markdown("**📚 Skills to Learn**")
                skills_list = [s.strip() for s in missing_skills.split(',')]
                st.write(", ".join(skills_list[:3]))  # Show top 3
        
        # Description preview
        if job.get('description'):
            with st.expander("📄 Job Description"):
                st.write(job['description'])
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 2, 6])
        
        with col1:
            if st.button("💾 Save Job", key=f"save_{job['job_id']}"):
                if job['job_id'] not in [j['job_id'] for j in st.session_state.saved_jobs]:
                    st.session_state.saved_jobs.append(job.to_dict())
                    st.success("Job saved!")
                else:
                    st.info("Already saved")
        
        with col2:
            if job.get('url'):
                st.link_button("🔗 Apply Now", job['url'])
        
        st.divider()


def main():
    """Main page function"""
    try:
        st.title("🎯 AI-Powered Job Recommendations")
        st.markdown("Get personalized job matches based on your skills and preferences")
        
        # Load jobs data
        jobs_df = load_recent_jobs(days=30)
        
        if jobs_df.empty:
            st.warning("⚠️ No job data available. Please fetch jobs from the home page first.")
            return
        
        # Initialize recommendation engine
        engine = initialize_engine()
        
        if engine is None:
            st.error("Failed to initialize recommendation engine")
            return
        
        # Retrain engine with latest data if needed
        if engine.jobs_df is None or len(engine.jobs_df) == 0:
            with st.spinner("Training recommendation engine..."):
                engine.train(jobs_df)
        
        # Sidebar - User Profile Input
        st.sidebar.header("Your Profile")
        
        # Get available skills from data
        all_skills = get_unique_skills(jobs_df)
        if not all_skills:
            all_skills = [
                'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'Angular',
                'Django', 'Flask', 'AWS', 'Docker', 'Kubernetes', 'SQL',
                'MongoDB', 'Machine Learning', 'Data Science', 'DevOps'
            ]
        
        # User inputs
        selected_skills = st.sidebar.multiselect(
            "Select Your Skills",
            options=all_skills,
            default=st.session_state.user_profile.get('skills', []),
            help="Select all skills you have"
        )
        
        role = st.sidebar.text_input(
            "Desired Role",
            value=st.session_state.user_profile.get('role', 'Software Engineer'),
            help="e.g., Software Engineer, Data Scientist"
        )
        
        experience_options = ['0-2 years', '2-5 years', '5-10 years', '10+ years']
        experience = st.sidebar.selectbox(
            "Your Experience",
            options=experience_options,
            index=experience_options.index(st.session_state.user_profile.get('experience', '0-2 years'))
        )
        
        # Get unique locations
        locations = ['Any'] + sorted(jobs_df['location'].dropna().unique().tolist())
        current_location = st.session_state.user_profile.get('location', 'Bangalore')
        location_index = locations.index(current_location) if current_location in locations else 0
        
        location = st.sidebar.selectbox(
            "Preferred Location",
            options=locations,
            index=location_index
        )
        
        num_results = st.sidebar.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=20,
            value=10
        )
        
        # Update user profile in session state
        st.session_state.user_profile = {
            'skills': selected_skills,
            'role': role,
            'experience': experience,
            'location': location
        }
        
        # Get recommendations button
        if st.sidebar.button("🔍 Find Matching Jobs", type="primary"):
            if not selected_skills:
                st.warning("⚠️ Please select at least one skill to get recommendations")
            else:
                with st.spinner("Finding the best matches for you..."):
                    # Get recommendations
                    recommendations = engine.calculate_match(
                        st.session_state.user_profile,
                        top_n=num_results
                    )
                    
                    if not recommendations.empty:
                        st.session_state.recommendations = recommendations
                        st.success(f"✅ Found {len(recommendations)} matching jobs!")
                    else:
                        st.error("No matching jobs found. Try adjusting your filters.")
        
        # Display recommendations
        if 'recommendations' in st.session_state and not st.session_state.recommendations.empty:
            recommendations = st.session_state.recommendations
            
            st.divider()
            
            # Summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Top Matches", len(recommendations))
            
            with col2:
                avg_score = recommendations['match_score'].mean()
                st.metric("Avg Match Score", f"{avg_score:.1f}%")
            
            with col3:
                companies = recommendations['company'].nunique()
                st.metric("Companies", companies)
            
            with col4:
                locations_count = recommendations['location'].nunique()
                st.metric("Locations", locations_count)
            
            st.divider()
            
            # Filters for results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_score = st.slider(
                    "Minimum Match Score",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=5
                )
            
            with col2:
                result_locations = ['All'] + sorted(recommendations['location'].unique().tolist())
                filter_location = st.selectbox("Filter by Location", result_locations)
            
            with col3:
                result_companies = ['All'] + sorted(recommendations['company'].unique().tolist())
                filter_company = st.selectbox("Filter by Company", result_companies)
            
            # Apply filters
            filtered_recs = recommendations[recommendations['match_score'] >= min_score]
            
            if filter_location != 'All':
                filtered_recs = filtered_recs[filtered_recs['location'] == filter_location]
            
            if filter_company != 'All':
                filtered_recs = filtered_recs[filtered_recs['company'] == filter_company]
            
            st.markdown(f"### Showing {len(filtered_recs)} Jobs")
            
            # Display each job
            for idx, (_, job) in enumerate(filtered_recs.iterrows(), 1):
                display_job_card(job, idx)
            
            # Learning suggestions
            if not filtered_recs.empty:
                st.divider()
                st.subheader("📚 Skills Development Suggestions")
                
                # Get most common missing skills
                all_missing = []
                for missing in filtered_recs['missing_skills'].dropna():
                    if missing:
                        all_missing.extend([s.strip() for s in missing.split(',')])
                
                if all_missing:
                    from collections import Counter
                    top_missing = Counter(all_missing).most_common(5)
                    
                    st.markdown("**Most In-Demand Skills You Should Learn:**")
                    
                    for skill, count in top_missing:
                        st.markdown(f"- **{skill}** (Required by {count} jobs)")
                    
                    # Get learning suggestions
                    missing_skills_str = ', '.join([skill for skill, _ in top_missing[:3]])
                    suggestions = get_learning_suggestions(missing_skills_str)
                    
                    if suggestions:
                        st.markdown("**Recommended Learning Resources:**")
                        for suggestion in suggestions:
                            st.markdown(f"- {suggestion}")
        
        else:
            # No recommendations yet
            st.info("""
            👈 **Get Started:**
            1. Select your skills from the sidebar
            2. Enter your desired role and experience
            3. Choose your preferred location
            4. Click "Find Matching Jobs"
            
            Our AI will analyze thousands of jobs and find the perfect matches for you!
            """)
            
            # Show some stats
            st.divider()
            st.subheader("📊 Available Opportunities")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Jobs", len(jobs_df))
            
            with col2:
                st.metric("Companies", jobs_df['company'].nunique())
            
            with col3:
                st.metric("Locations", jobs_df['location'].nunique())
        
    except Exception as e:
        logging.error(f"Error in recommendations page: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
