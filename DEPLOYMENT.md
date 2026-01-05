# Grocery Management System - Deployment Guide

## 🚀 PythonAnywhere Deployment Instructions

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account
3. Go to your Dashboard

### Step 2: Upload Code
**Option A: Using Git (Recommended)**
```bash
cd ~
git clone https://github.com/HeshXonline/Grocery-Management-Platform-2.git
cd Grocery-Management-Platform-2
```

**Option B: Upload ZIP**
1. Download repository as ZIP from GitHub
2. Upload to PythonAnywhere Files tab
3. Extract in your home directory

### Step 3: Set Up Virtual Environment
Open a **Bash console** on PythonAnywhere:
```bash
cd ~/Grocery-Management-Platform-2
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
cd ~/Grocery-Management-Platform-2
source venv/bin/activate
python init_db.py
python sample_data.py
```

### Step 5: Configure Web App
1. Go to **Web** tab on PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click through to create the app

### Step 6: Configure WSGI File
1. Click on the **WSGI configuration file** link
2. Delete everything and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/Grocery-Management-Platform-2'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set up the virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Import the FastAPI app
from main import app as application
```

**Replace `YOUR_USERNAME` with your PythonAnywhere username**

### Step 7: Configure Static Files
In the **Web** tab, add static files mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/Grocery-Management-Platform-2/static` |

### Step 8: Set Environment Variables (Optional)
If you want to use MySQL instead of SQLite:
1. Go to **Files** tab
2. Edit `.env` file
3. Update `DATABASE_URL` with your MySQL connection string

### Step 9: Reload Web App
1. Go to **Web** tab
2. Click **Reload** button (big green button)
3. Wait for reload to complete

### Step 10: Access Your App
Your app will be available at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

## 📱 Access Pages:
- **Dashboard:** `https://YOUR_USERNAME.pythonanywhere.com/`
- **Billing:** `https://YOUR_USERNAME.pythonanywhere.com/billing.html`
- **Products:** `https://YOUR_USERNAME.pythonanywhere.com/products.html`
- **Reports:** `https://YOUR_USERNAME.pythonanywhere.com/reports.html`
- **API Docs:** `https://YOUR_USERNAME.pythonanywhere.com/docs`

## 🔧 Troubleshooting

### Check Error Logs
1. Go to **Web** tab
2. Click on **Error log** link
3. Check for any errors

### Common Issues:

**"Import Error"**
- Make sure virtual environment is activated when installing packages
- Check WSGI file paths are correct

**"Static files not loading"**
- Verify static files mapping in Web tab
- Make sure path is correct

**"Database locked"**
- SQLite may have issues with concurrent writes
- Restart web app

**"502 Bad Gateway"**
- Check error logs
- Make sure WSGI file is correct
- Reload web app

## 🗄️ Database Management

### View Database (SQLite)
```bash
cd ~/Grocery-Management-Platform-2
sqlite3 grocery.db
.tables
.schema products
SELECT * FROM products LIMIT 5;
.quit
```

### Backup Database
```bash
cp grocery.db grocery_backup_$(date +%Y%m%d).db
```

### Reset Database
```bash
rm grocery.db
python init_db.py
python sample_data.py
```

## 🔒 Security Notes

- The app has **no authentication** - anyone with the URL can access it
- Only share the URL with trusted users
- Consider adding authentication for production use
- PythonAnywhere free tier is for development/testing only

## 📊 Limitations on Free Plan

- SQLite database only (no MySQL)
- Limited CPU time
- App sleeps after inactivity
- One web app only
- Limited bandwidth

## 🎯 Local Development

To run locally for testing:
```bash
# Using SQLite
DATABASE_URL=sqlite:///./grocery.db uvicorn main:app --reload --port 8000

# Using MySQL (if available)
DATABASE_URL=mysql+pymysql://user:pass@localhost/db uvicorn main:app --reload --port 8000
```

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere forums
2. Review error logs
3. Verify all paths in WSGI configuration
4. Ensure virtual environment is properly set up

---

**Your Grocery Management System is now ready for the cloud! 🎉**
