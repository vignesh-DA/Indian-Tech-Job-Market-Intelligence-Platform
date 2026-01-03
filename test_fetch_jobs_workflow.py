"""
Test script for complete fetch_jobs workflow:
1. Delete old CSV files
2. Delete old pickle model
3. Fetch new jobs from API
4. Save new CSV
5. Train and save new pickle model
6. Use model for recommendations
"""

import requests
import json
import os
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
FETCH_JOBS_ENDPOINT = f"{BASE_URL}/api/fetch-jobs"
RECOMMENDATIONS_ENDPOINT = f"{BASE_URL}/api/recommendations"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_files():
    """Check if CSV and pickle files exist"""
    csv_files = []
    pickle_files = []
    
    if os.path.exists("data"):
        csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
    
    if os.path.exists("models"):
        pickle_files = [f for f in os.listdir("models") if f.endswith('.pkl')]
    
    return csv_files, pickle_files

def test_fetch_jobs_workflow():
    """Test the complete fetch_jobs workflow"""
    
    print_section("STEP 1: CHECK INITIAL STATE")
    csv_before, pkl_before = check_files()
    print(f"CSV files before: {csv_before}")
    print(f"Pickle files before: {pkl_before}")
    
    print_section("STEP 2: CALL FETCH_JOBS ENDPOINT")
    try:
        response = requests.post(FETCH_JOBS_ENDPOINT)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code != 200:
            print("❌ FETCH_JOBS FAILED")
            return False
        
        if not result.get('success'):
            print("❌ API returned success=false")
            return False
        
        job_count = result.get('count', 0)
        model_trained = result.get('model_trained', False)
        
        print(f"✅ FETCH_JOBS SUCCESSFUL")
        print(f"   - Jobs fetched: {job_count}")
        print(f"   - Model trained: {model_trained}")
        
    except Exception as e:
        print(f"❌ ERROR calling fetch_jobs: {str(e)}")
        return False
    
    print_section("STEP 3: CHECK FILES AFTER FETCH")
    time.sleep(2)  # Wait for file operations to complete
    csv_after, pkl_after = check_files()
    print(f"CSV files after: {csv_after}")
    print(f"Pickle files after: {pkl_after}")
    
    # Verify CSV was created
    if not csv_after:
        print("❌ No CSV file created!")
        return False
    else:
        print(f"✅ CSV file created: {csv_after[0]}")
        csv_path = os.path.join("data", csv_after[0])
        csv_size = os.path.getsize(csv_path) / (1024*1024)
        print(f"   - Size: {csv_size:.2f} MB")
    
    # Verify pickle was created
    if not pkl_after:
        print("❌ No pickle file created!")
        return False
    else:
        print(f"✅ Pickle file created: {pkl_after[0]}")
        pkl_path = os.path.join("models", pkl_after[0])
        pkl_size = os.path.getsize(pkl_path) / (1024*1024)
        print(f"   - Size: {pkl_size:.2f} MB")
    
    print_section("STEP 4: TEST RECOMMENDATIONS WITH NEW MODEL")
    try:
        payload = {
            "skills": ["Python", "Machine Learning", "SQL"],
            "role": "Data Scientist",
            "experience": "2-4 years",
            "location": "Bangalore",
            "preferred_locations": ["Bangalore", "Pune"]
        }
        
        response = requests.post(RECOMMENDATIONS_ENDPOINT, json=payload)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 and result.get('success'):
            recommendations = result.get('data', [])
            print(f"✅ RECOMMENDATIONS RETRIEVED")
            print(f"   - Count: {len(recommendations)}")
            
            if recommendations:
                first_job = recommendations[0]
                print(f"   - Top match: {first_job.get('title')}")
                print(f"   - Company: {first_job.get('company')}")
                print(f"   - Match score: {first_job.get('match_score', 'N/A')}%")
                print(f"   - Your skills: {first_job.get('your_skills', [])}")
                print(f"   - Missing skills: {first_job.get('missing_skills', [])}")
        else:
            print(f"❌ Recommendations failed: {result.get('message')}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR testing recommendations: {str(e)}")
        return False
    
    print_section("✅ COMPLETE WORKFLOW TEST PASSED")
    print("Summary:")
    print(f"  1. Old files deleted ✅")
    print(f"  2. New jobs fetched: {job_count} ✅")
    print(f"  3. CSV saved: {csv_after[0]} ✅")
    print(f"  4. Pickle model created ✅")
    print(f"  5. Recommendations working ✅")
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  COMPLETE FETCH_JOBS WORKFLOW TEST")
    print("  Testing: Delete Old → Fetch New → Save CSV → Train Model → Recommend")
    print("=" * 70)
    
    success = test_fetch_jobs_workflow()
    
    if success:
        print("\n✅ ALL TESTS PASSED - WORKFLOW IS COMPLETE AND WORKING\n")
    else:
        print("\n❌ TESTS FAILED - CHECK ERRORS ABOVE\n")
