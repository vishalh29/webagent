# Browser Automation with Streamlit

A Streamlit application that automates browser interactions using the Gemini API.

## Requirements
- Python 3.11 or higher
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Application

1. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. The app will open in your default browser. You can:
   - Enter your Gemini API key
   - Adjust browser window size
   - Enter your task
   - Click "Run Task" to execute
   - View saved prompts in the "Saved Prompts" tab

## Files
- `streamlit_app.py`: Main Streamlit application
- `test_browser.py`: Test file for browser automation
- `browser_use/`: Core package for browser automation
- `.env`: Environment variables file 