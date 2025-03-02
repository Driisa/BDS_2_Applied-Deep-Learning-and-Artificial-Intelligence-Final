# **📌 Virtual Environment Guide for AI Trend Tracker**

> ⚠️ **IMPORTANT**: This project uses CrewAI and OpenAI which have specific dependency requirements. A proper virtual environment setup is **essential** to avoid conflicts with other Python installations or packages.

---

## **1️⃣ Creating the Virtual Environment**
Run this in **CMD (not PowerShell)**:
```cmd
cd "C:\path\to\AI-Trend-Tracker"
py -3.10 -m venv myenv
```
✅ This creates a virtual environment named **`myenv`** using Python 3.10, which is **required for compatibility** with CrewAI.

---

## **2️⃣ Activating the Virtual Environment**
After creating it, **activate** it:
```cmd
myenv\Scripts\activate.bat
```
✅ You should now see `(myenv)` at the start of the terminal.  
Example:
```
(myenv) C:\path\to\AI-Trend-Tracker>
```

> 🔴 **CRITICAL**: The AI Trend Tracker application **will not work correctly** unless run from within the virtual environment, as it requires specific versions of packages that may conflict with your system packages.

---

## **3️⃣ Checking If You're Inside the Virtual Environment**
Run this command:
```cmd
where python
```
- ✅ If you see **`myenv\Scripts\python.exe`**, you're **inside the virtual environment**.
- ❌ If you see **a system path like `Python310\python.exe`**, you are **not inside the virtual environment** and must activate it before proceeding.

---

## **4️⃣ Installing Project Dependencies**
First, clear old failed installs:
```cmd
pip cache purge
```

Make sure the virtual environment is activated **before installing**:
```cmd
pip install -r requirements.txt
```

> 📝 **NOTE**: The installation may take several minutes as CrewAI and its dependencies are complex packages. Be patient and watch for any error messages.

---

## **5️⃣ Setting Up API Keys**
After installing dependencies, create your `config.py` file:
```cmd
copy config.example.py config.py
```

Then edit the `config.py` file to add your API keys:
```python
# Configuration file for API keys and other settings
OPENAI_API_KEY = "your-openai-api-key-here"  # Required for summarization
PERIGON_API_KEY = "your-perigon-api-key-here"  # Required for news fetching
```

> ⚠️ **WARNING**: Without valid API keys, the application will throw errors when trying to fetch or analyze news.

---

## **6️⃣ Running the Application**
With the virtual environment activated and dependencies installed:
```cmd
streamlit run app.py
```

The application should open in your default web browser at `http://localhost:8501`.

---

## **7️⃣ Reactivating the Virtual Environment (After Restarting CMD)**
If you **restart CMD** or open a **new terminal**, reactivate the virtual environment before working:
```cmd
cd "C:\path\to\AI-Trend-Tracker"
myenv\Scripts\activate.bat
```
✅ `(myenv)` should appear again, confirming activation.

---

## **8️⃣ Deactivating the Virtual Environment**
To exit the virtual environment, type:
```cmd
deactivate
```
✅ This returns you to the system environment.

---

## **9️⃣ Troubleshooting Common Issues**

### Package Conflicts
If you see errors related to package versions:
```cmd
pip uninstall -y langchain langchain-openai crewai
pip install langchain==0.0.267 langchain-openai==0.0.2 crewai==0.28.0
```

### OpenAI API Errors
If you see "Invalid API key" or similar:
- Double-check your API key in `config.py`
- Ensure you're using an API key with sufficient credits
- Check that the model specified (e.g., `gpt-4o-mini`) is available on your OpenAI account

### CrewAI Errors
If you see validation errors from CrewAI:
- Ensure you're using `verbose=True` (boolean) instead of numeric values
- Check that your Task definitions follow the expected format

---

# **🔥 Summary Table**
| Action | Command |
|--------|---------|
| **Create Virtual Environment** | `py -3.10 -m venv myenv` |
| **Activate Virtual Environment** | `myenv\Scripts\activate.bat` |
| **Check If Active** | `(myenv)` appears in CMD |
| **Verify Python Path** | `where python` (should show `myenv\Scripts\python.exe`) |
| **Install Dependencies** | `pip install -r requirements.txt` |
| **Run Application** | `streamlit run app.py` |
| **Reactivate After Restart** | `myenv\Scripts\activate.bat` |
| **Deactivate Virtual Environment** | `deactivate` |

---

### **🚀 Now You're Ready to Track AI Trends!**
✅ Remember to always activate the virtual environment before running the application.