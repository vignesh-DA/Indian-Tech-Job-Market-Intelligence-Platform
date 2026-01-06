# Deployment Checklist for Render

## ✅ Completed Items

### 1. Data Files
- [x] CSV data file (`data/jobs_2026_01_06.csv`) now included in git
- [x] Updated `.gitignore` to allow CSV files while excluding sensitive data
- [x] 12,550 jobs available in dataset

### 2. Environment Configuration
- [x] `runtime.txt` created (Python 3.11.8)
- [x] `.python-version` file created
- [x] `render.yaml` configuration file created
- [x] `Procfile` with gunicorn configuration
- [x] All environment variables configured in Render dashboard (11 variables)

### 3. Package Dependencies
- [x] `requirements.txt` updated for Python 3.13 compatibility
- [x] pandas==2.2.3, numpy==1.26.4, scikit-learn==1.5.2
- [x] gunicorn==21.2.0 included
- [x] All dependencies have pre-built wheels

### 4. Frontend Configuration
- [x] API URLs now dynamic (auto-detect localhost vs production)
- [x] `config.js` updated with environment detection
- [x] All hardcoded `localhost:5000` URLs replaced with `API_BASE_URL`
- [x] Dashboard.js updated (14 API calls fixed)

### 5. Authentication
- [x] Profile picture loading added to all pages
- [x] `main.js` has `checkAuth()` function
- [x] Profile dropdown functionality working
- [x] Logout button configured
- [x] Google OAuth redirect URIs configured for production

### 6. Code Quality
- [x] No secrets in repository
- [x] `.env` files excluded from git
- [x] All imports present
- [x] Data loader working (tested locally)

## 📝 Render Environment Variables Required

1. `ADZUNA_APP_ID` - Your Adzuna API app ID
2. `ADZUNA_APP_KEY` - Your Adzuna API key
3. `GEMINI_API_KEY` - Google Gemini API key
4. `GOOGLE_OAUTH_CLIENT_ID` - OAuth client ID
5. `GOOGLE_OAUTH_CLIENT_SECRET` - OAuth client secret
6. `GOOGLE_OAUTH_REDIRECT_URI` - https://your-app.onrender.com/api/auth/callback
7. `FLASK_SECRET_KEY` - Random secret key for sessions
8. `FLASK_ENV` - production
9. `DEBUG` - False
10. `ENVIRONMENT` - production
11. `RENDER` - true

## 🚀 Deployment Steps

1. **Push Latest Code**
   ```bash
   git push origin main
   ```

2. **Render Dashboard**
   - Go to https://dashboard.render.com
   - Select your service
   - Click "Manual Deploy" > "Deploy latest commit"

3. **Monitor Build Logs**
   - Watch for Python version (should be 3.11.8 or use 3.13.4 with new packages)
   - Verify all packages install successfully
   - Check for any import errors

4. **Verify Deployment**
   - Visit your deployed URL
   - Test Google OAuth login
   - Check if profile picture loads
   - Verify dashboard shows data (not dashes)
   - Test roles dropdown in recommendations page

## 🔍 Troubleshooting

### If roles dropdown is empty:
1. Check logs: `Load recent jobs` message
2. Verify CSV file exists in data/ directory
3. Test `/api/roles` endpoint directly

### If dashboard shows dashes:
1. Check browser console for API errors
2. Verify CORS is not blocking requests
3. Check if `/api/summary-stats` returns data

### If profile picture doesn't load:
1. Verify user is logged in via OAuth
2. Check `/api/auth/user` endpoint
3. Verify `checkAuth()` runs on page load

## 📊 Expected Results

After successful deployment:
- **Total Jobs**: ~12,550
- **Companies**: ~hundreds
- **Locations**: ~tens
- **Roles**: ~100 unique roles
- **Dashboard charts**: All populated
- **Recommendations**: Working with role selection

## 🎯 Post-Deployment Testing

1. [ ] Login with Google OAuth
2. [ ] Profile picture visible in navbar
3. [ ] Dashboard loads with actual data
4. [ ] Roles dropdown populated
5. [ ] Recommendations page working
6. [ ] Saved jobs functionality
7. [ ] Chatbot (if Gemini API key configured)

## 📞 Support

If issues persist:
- Check Render logs: `Logs` tab in dashboard
- Review browser console errors
- Verify all environment variables are set correctly
