# Text-to-PPT-Generation-Streamlit-App
This is an official repo for "idea to PPT Streamlit App". It generates PPT from your text using GPT-X Model and Python PPTX Library.

# Setup

This setup is for Ubuntu, windows may be different

## Create virtual python environment
```
python -m venv .venv
```

## Activate virtual python environment
```
.venv\Scripts\activate
```

## Install libs
```
pip install -r requirements.txt
```

# Config

Follow this [video](https://www.youtube.com/watch?v=6aj5a7qGcb4) to get Gemini API key.

Change the content of file `.env`
```
GOOGLE_API_KEY=<put-your-api-key-here>
```

# Run
```
python -m streamlit run app.py
```
