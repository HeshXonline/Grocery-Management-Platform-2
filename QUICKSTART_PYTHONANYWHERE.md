# Quick Start Guide for PythonAnywhere

## 🎯 **5-Minute Deployment to PythonAnywhere**

### **Step 1: Sign Up (1 minute)**
1. Go to https://www.pythonanywhere.com/
2. Click "Start running Python online in less than a minute!"
3. Create FREE account

### **Step 2: Clone Your Repository (1 minute)**
1. Open **"Bash" console** from Dashboard
2. Run these commands:
```bash
git clone https://github.com/HeshXonline/Grocery-Management-Platform-2.git
cd Grocery-Management-Platform-2
```

### **Step 3: Set Up Environment (2 minutes)**
Still in the Bash console:
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python sample_data.py
```

### **Step 4: Create Web App (1 minute)**
1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**
5. Click **"Next"** → Click **"Next"** (keep defaults)

### **Step 5: Configure WSGI File (30 seconds)**
1. On the Web tab, find **"Code"** section
2. Click on the **WSGI configuration file** link (looks like `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **DELETE ALL** existing content
4. **COPY AND PASTE** this (replace YOUR_USERNAME with your actual username):

```python
import sys
import os

project_home = '/home/YOUR_USERNAME/Grocery-Management-Platform-2'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as file:
        exec(file.read(), {'__file__': activate_this})

from main import app as application
```

5. Click **"Save"** (top right)

### **Step 6: Set Up Static Files (30 seconds)**
Still on the Web tab, scroll to **"Static files"** section:

1. Click **"Enter URL"** → Type: `/static/`
2. Click **"Enter path"** → Type: `/home/YOUR_USERNAME/Grocery-Management-Platform-2/static`
3. Click the **✓** (checkmark) to save

(Replace YOUR_USERNAME with your actual username)

### **Step 7: Reload and Launch! (10 seconds)**
1. Scroll to top of Web tab
2. Click big green **"Reload YOUR_USERNAME.pythonanywhere.com"** button
3. Wait for "✓ Reload successful"
4. Click the link: **YOUR_USERNAME.pythonanywhere.com**

---

## 🎉 **You're Live!**

Your grocery management system is now running at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

### **Pages:**
- 🏠 **Dashboard:** `https://YOUR_USERNAME.pythonanywhere.com/`
- 💰 **Billing:** `https://YOUR_USERNAME.pythonanywhere.com/billing.html`
- 📦 **Products:** `https://YOUR_USERNAME.pythonanywhere.com/products.html`
- 📊 **Reports:** `https://YOUR_USERNAME.pythonanywhere.com/reports.html`
- 📖 **API Docs:** `https://YOUR_USERNAME.pythonanywhere.com/docs`

---

## ⚠️ **Troubleshooting**

**Problem: "Something went wrong" error**
- Go to Web tab → Click "Error log" link
- Check what the error says
- Common fix: Make sure you replaced YOUR_USERNAME in WSGI file

**Problem: "Page not found"**
- Make sure web app is reloaded
- Check static files path is correct

**Problem: "Import Error"**
- Make sure you activated venv before pip install
- Re-run: `source venv/bin/activate` then `pip install -r requirements.txt`

---

## 📝 **Default Login**
No login required! Just start using it.

⚠️ **Security Note:** Anyone with the URL can access your shop data. Only share with trusted users.

---

## 🔄 **Updating Your App**

When you make changes to your code:

```bash
# In PythonAnywhere Bash console:
cd ~/Grocery-Management-Platform-2
git pull origin main
source venv/bin/activate
# Then go to Web tab and click Reload
```

---

## 💾 **Database Location**
Your SQLite database file: `/home/YOUR_USERNAME/Grocery-Management-Platform-2/grocery.db`

To backup:
```bash
cp ~/Grocery-Management-Platform-2/grocery.db ~/grocery_backup.db
```

---

**Need help?** Check full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
