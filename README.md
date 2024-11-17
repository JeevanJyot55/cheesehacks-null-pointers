# cheesehacks-null-pointers
# OptiStocks

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
   Backend Setup:

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   Running the Application
4. **Start the Backend:**
   ```bash
   python stockSelectorFunction.py
5. **Start the Frontend:**
   ```bash
   npm run dev
