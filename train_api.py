"""
train_api.py

Handles external API requests to the IRCTC RapidAPI for live train statuses.
"""
import requests
import json
import logging

def get_train_status(train_number, departure_date):
    """
    Fetches the live status for a specified train and date.
    
    Args:
        train_number (str): The train ID (e.g., '12051')
        departure_date (str): Expected in 'YYYYMMDD' format (e.g., '20250717')
        
    Returns:
        dict: The parsed JSON response, or an error dictionary.
    """
    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"
    
    querystring = {
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web",
        "deviceIdentifier": "Mozilla Firefox-138.0.0.0",
        "train_number": train_number
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-rapid-api": "rapid-api-database",
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapidapi-key": "5c145dbc7amsh38d1d617a4f328cp1dcbf0jsn9efdea3c60c2"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API Request Error: {e}")
        # Return generic error payload reflecting what the API throws
        try:
             # If error payload exists, try to return it
             return response.json()
        except Exception:
             return {"error": str(e), "status": {"result": "failure"}}
