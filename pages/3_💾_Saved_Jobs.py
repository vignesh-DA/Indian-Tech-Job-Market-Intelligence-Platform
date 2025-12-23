"""
Saved Jobs & User Profile Page
Manage saved jobs and user profile
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from src.logger import logging
from src.exception import CustomException


# Page configuration
st.set_page_config(
    page_title="Saved Jobs",
    page_icon="💾",
    layout="wide"
)

# Initialize session state
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'skills': [],
        'role': 'Software Engineer',
        'experience': '0-2 years',
        'location': 'Bangalore',
        'preferred_locations': []
    }


def display_saved_job(job, index):
    """Display a saved job card"""
    with st.container():
        col1, col2, col3 = st.columns([4, 2, 1])
        
        with col1:
            st.markdown(f"### {job['title']}")
            st.markdown(f"**{job['company']}** • {job['location']}")
        
        with col2:
            if job.get('match_score'):
                st.metric("Match Score", f"{job['match_score']}%")
        
        with col3:
            if st.button("🗑️ Remove", key=f"remove_{index}"):
                return True
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Experience**")
            st.write(job.get('experience', 'N/A'))
        
        with col2:
            st.markdown("**Salary**")
            salary = job.get('salary', 'Not specified')
            if salary != "Not specified" and job.get('salary_min', 0) > 0:
                min_sal = job['salary_min'] / 100000
                max_sal = job['salary_max'] / 100000
                st.write(f"₹{min_sal:.1f}L - ₹{max_sal:.1f}L")
            else:
                st.write("Not specified")
        
        with col3:
            st.markdown("**Skills**")
            skills = job.get('skills', '')
            if skills:
                skills_list = [s.strip() for s in str(skills).split(',')]
                st.write(', '.join(skills_list[:3]) + '...' if len(skills_list) > 3 else ', '.join(skills_list))
            else:
                st.write("N/A")
        
        # Description
        if job.get('description'):
            with st.expander("📄 Job Description"):
                st.write(job['description'])
        
        # Skills analysis if available
        if job.get('matched_skills') or job.get('missing_skills'):
            col1, col2 = st.columns(2)
            
            with col1:
                if job.get('matched_skills'):
                    st.markdown("**✅ Your Matching Skills**")
                    st.write(job['matched_skills'])
            
            with col2:
                if job.get('missing_skills'):
                    st.markdown("**📚 Skills to Learn**")
                    st.write(job['missing_skills'])
        
        # Apply button
        if job.get('url'):
            st.link_button("🔗 Apply Now", job['url'], use_container_width=False)
        
        st.divider()
        
        return False


def export_saved_jobs():
    """Export saved jobs to CSV"""
    if not st.session_state.saved_jobs:
        return None
    
    df = pd.DataFrame(st.session_state.saved_jobs)
    return df.to_csv(index=False).encode('utf-8')


def main():
    """Main page function"""
    try:
        st.title("💾 Saved Jobs & Profile")
        st.markdown("Manage your saved jobs and profile settings")
        
        # Tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Saved Jobs", "User Profile", "Application Tracker"])
        
        # Tab 1: Saved Jobs
        with tab1:
            st.subheader("📑 Your Saved Jobs")
            
            if not st.session_state.saved_jobs:
                st.info("""
                📌 **No saved jobs yet!**
                
                Start saving jobs from the Job Recommendations page to keep track of 
                opportunities you're interested in.
                """)
            else:
                # Stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Saved", len(st.session_state.saved_jobs))
                
                with col2:
                    companies = len(set(job['company'] for job in st.session_state.saved_jobs))
                    st.metric("Companies", companies)
                
                with col3:
                    locations = len(set(job['location'] for job in st.session_state.saved_jobs))
                    st.metric("Locations", locations)
                
                with col4:
                    avg_score = sum(job.get('match_score', 0) for job in st.session_state.saved_jobs) / len(st.session_state.saved_jobs)
                    st.metric("Avg Match", f"{avg_score:.1f}%")
                
                st.divider()
                
                # Filter options
                col1, col2, col3 = st.columns([2, 2, 6])
                
                with col1:
                    companies = ['All'] + sorted(list(set(job['company'] for job in st.session_state.saved_jobs)))
                    filter_company = st.selectbox("Company", companies)
                
                with col2:
                    locations = ['All'] + sorted(list(set(job['location'] for job in st.session_state.saved_jobs)))
                    filter_location = st.selectbox("Location", locations)
                
                # Sort option
                sort_by = st.radio(
                    "Sort by",
                    ["Match Score (High to Low)", "Match Score (Low to High)", "Company (A-Z)", "Recently Added"],
                    horizontal=True
                )
                
                # Apply filters and sorting
                filtered_jobs = st.session_state.saved_jobs.copy()
                
                if filter_company != 'All':
                    filtered_jobs = [job for job in filtered_jobs if job['company'] == filter_company]
                
                if filter_location != 'All':
                    filtered_jobs = [job for job in filtered_jobs if job['location'] == filter_location]
                
                # Sort
                if sort_by == "Match Score (High to Low)":
                    filtered_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
                elif sort_by == "Match Score (Low to High)":
                    filtered_jobs.sort(key=lambda x: x.get('match_score', 0))
                elif sort_by == "Company (A-Z)":
                    filtered_jobs.sort(key=lambda x: x['company'])
                # Recently added is default order
                
                st.markdown(f"### Showing {len(filtered_jobs)} Jobs")
                
                # Display jobs
                jobs_to_remove = []
                for idx, job in enumerate(filtered_jobs):
                    should_remove = display_saved_job(job, idx)
                    if should_remove:
                        jobs_to_remove.append(job['job_id'])
                
                # Remove jobs marked for deletion
                if jobs_to_remove:
                    st.session_state.saved_jobs = [
                        job for job in st.session_state.saved_jobs 
                        if job['job_id'] not in jobs_to_remove
                    ]
                    st.rerun()
                
                # Export and clear options
                st.divider()
                col1, col2, col3 = st.columns([2, 2, 6])
                
                with col1:
                    csv_data = export_saved_jobs()
                    if csv_data:
                        st.download_button(
                            label="📥 Export to CSV",
                            data=csv_data,
                            file_name=f"saved_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("🗑️ Clear All", type="secondary"):
                        if st.checkbox("Are you sure?"):
                            st.session_state.saved_jobs = []
                            st.rerun()
        
        # Tab 2: User Profile
        with tab2:
            st.subheader("👤 Your Profile")
            
            profile = st.session_state.user_profile
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Current Profile")
                st.markdown(f"**Desired Role:** {profile['role']}")
                st.markdown(f"**Experience Level:** {profile['experience']}")
                st.markdown(f"**Preferred Location:** {profile['location']}")
                
                if profile['skills']:
                    st.markdown(f"**Skills ({len(profile['skills'])}):**")
                    for skill in profile['skills']:
                        st.markdown(f"- {skill}")
                else:
                    st.markdown("**Skills:** None selected")
            
            with col2:
                st.markdown("### Update Profile")
                st.info("💡 Update your profile in the Job Recommendations page sidebar")
                
                # Display stats
                st.markdown("### Profile Completeness")
                
                completeness = 0
                if profile['role']:
                    completeness += 25
                if profile['experience']:
                    completeness += 25
                if profile['location']:
                    completeness += 25
                if profile['skills']:
                    completeness += 25
                
                st.progress(completeness / 100)
                st.write(f"{completeness}% Complete")
                
                if completeness < 100:
                    st.warning("Complete your profile to get better recommendations!")
        
        # Tab 3: Application Tracker
        with tab3:
            st.subheader("📋 Application Tracker")
            
            st.info("""
            **Coming Soon!**
            
            Track your job applications with:
            - Application status (Applied, Interview, Rejected, Offer)
            - Application dates
            - Follow-up reminders
            - Notes and feedback
            - Interview preparation resources
            """)
            
            # Placeholder for application tracker
            if 'applications' not in st.session_state:
                st.session_state.applications = []
            
            st.markdown("### Add Application")
            
            with st.form("add_application"):
                col1, col2 = st.columns(2)
                
                with col1:
                    app_company = st.text_input("Company Name")
                    app_position = st.text_input("Position")
                    app_date = st.date_input("Application Date", datetime.now())
                
                with col2:
                    app_status = st.selectbox(
                        "Status",
                        ["Applied", "Screening", "Interview", "Offer", "Rejected"]
                    )
                    app_url = st.text_input("Job URL (optional)")
                    app_notes = st.text_area("Notes (optional)")
                
                submitted = st.form_submit_button("Add Application")
                
                if submitted and app_company and app_position:
                    new_app = {
                        'company': app_company,
                        'position': app_position,
                        'date': app_date,
                        'status': app_status,
                        'url': app_url,
                        'notes': app_notes
                    }
                    st.session_state.applications.append(new_app)
                    st.success("Application added!")
                    st.rerun()
            
            # Display applications
            if st.session_state.applications:
                st.markdown("### Your Applications")
                
                df = pd.DataFrame(st.session_state.applications)
                st.dataframe(df, use_container_width=True)
                
                # Stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Applied", len(st.session_state.applications))
                
                with col2:
                    interviews = len([a for a in st.session_state.applications if a['status'] == 'Interview'])
                    st.metric("Interviews", interviews)
                
                with col3:
                    offers = len([a for a in st.session_state.applications if a['status'] == 'Offer'])
                    st.metric("Offers", offers)
                
                with col4:
                    if len(st.session_state.applications) > 0:
                        success_rate = (offers / len(st.session_state.applications)) * 100
                        st.metric("Success Rate", f"{success_rate:.1f}%")
        
    except Exception as e:
        logging.error(f"Error in saved jobs page: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
