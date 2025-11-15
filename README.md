# agent-builder-api

AI Agent Builder API

# Application Purpose

A backend API service to manage and interact with AI agents. Designed to be used in AI-powered tools or services that need customizable agent workflows.

# Preconditions

- Python 3.8 or higher

# Install Python

## Windows:
1. Download from: https://www.python.org/downloads/windows/
2. Run the installer
3. Check "Add Python to PATH" before installing

## macOS:
```brew install python```

## Ubuntu/Linux:
```sudo apt update```  
```sudo apt install python3 python3-pip```

# Run Local

## 1. Clone the repository
```git clone https://github.com/i-do-dev/agent-builder-api.git```   
```cd agent-builder-api```  

## 2. Create virtual environment
```python -m venv venv ```  
```source venv/bin/activate```  

On Windows:     
```venv\Scripts\activate```

## 3. Install dependencies
```pip install -r requirements.txt```

## 4. Run Database Migrations
```alembic upgrade head```  

Generate migration script:  
```alembic revision --autogenerate -m "your change message"```

## 5. Run server
```uvicorn main:app --reload``` 

# API Documentation (Swagger UI)
http://127.0.0.1:8000/docs
