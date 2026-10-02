# Weather App – Real-Time Weather Information System

A beginner-friendly Flask web application that finds a city with the Open-Meteo Geocoding API and retrieves its current weather from Open-Meteo. It requires an internet connection but no API key. Searches happen in the background, so the page does not need to reload.

## Features

- Search for a city and view its country and current weather
- Temperature and feels-like temperature in Celsius
- Weather condition and a matching weather icon
- Humidity, wind speed, and atmospheric pressure
- Loading feedback and helpful messages for empty input, unknown cities, and service/network errors
- Responsive layout for desktop and mobile
- No API key or `.env` configuration required

## Technologies

- Python and Flask
- HTML, CSS, and JavaScript
- Open-Meteo Geocoding API and Forecast API
- Requests

## Project structure

```text
Weather-App/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Setup and installation

1. Install Python 3.10 or newer.
2. Open this project folder in VS Code and open a terminal in the folder.
3. Create and activate a virtual environment in PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

4. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the application

From the project folder, with the virtual environment activated, run:

```powershell
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

Enter a city such as Nandyal, Hyderabad, Bangalore, Delhi, or Mumbai and select **Search weather**. The app first looks up the city coordinates, then requests current conditions for those coordinates. An existing `.env` file from an older version is ignored by this app and is not needed.