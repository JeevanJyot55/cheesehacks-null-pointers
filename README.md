## OptiStocks- Where Money Meets Strategy

## Overview

Investment Advisor is a web-based tool designed for hackathons. It helps users allocate their budget across diversified stocks based on risk tolerance using real-time stock data.

## Features

- Budget allocation across mid-cap and S&P 500 stocks
- Dynamic risk slider
- Real-time stock data retrieval via Yahoo Finance
- Backend: Flask API
- Frontend: React with TypeScript

## Tech Stack

- **Backend**: Flask, Flask-CORS, yfinance, pandas
- **Frontend**: React, TypeScript, Tailwind CSS

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>

2. **Backend Setup:**
   ```bash
   cd cheesybackend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip3 install Flask flask-cors yfinance pandas tqdm

3. **Frontend Setup:**
   ```bash
   cd cheesyfrontend
   npm install

4. **Start the Backend:**
   ```bash
   python3 stockSelectorFunction.py

5. **Start the Frontend:**
   ```bash
   npm run dev

Note: The python file and the frontend should be running at the same time.
