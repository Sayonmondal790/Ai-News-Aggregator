# AI-Powered News Aggregator

![Live on Vercel](https://img.shields.io/badge/Deployed-Vercel-black?style=flat&logo=vercel)
![Live on Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat&logo=render)

A full-stack web application that automatically curates, classifies, and recommends real-time news articles. Built with a React frontend and a FastAPI backend, this project leverages machine learning to provide users with an intelligent, distraction-free reading experience by distinguishing between factual reporting and opinion pieces.

**Live Demo:** [ai-news-aggregator-eosin.vercel.app](https://ai-news-aggregator-eosin.vercel.app/)

## ✨ Key Features

*   **Automated Content Pipeline:** Ingests live RSS feeds (currently configured for Times of India) across multiple categories, cleaning and standardizing the text automatically.
*   **Zero-Shot NLP Classification:** Integrates the Hugging Face Inference API (`facebook/bart-large-mnli`) to instantly classify any article's tone strictly as "Fact" or "Opinion".
*   **Semantic Recommendations:** Utilizes TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to calculate cosine similarity between articles, generating a highly accurate "Related Stories" feed based on context rather than tags.
*   **High Fault Tolerance:** Engineered with robust error handling to maintain UI stability. The system gracefully catches API network timeouts, missing dataframe entries, and JSON serialization errors to prevent application crashes.
*   **Dynamic UI:** Features a responsive CSS grid layout with an interactive WebGL background.

## 🛠️ Tech Stack

**Frontend**
*   React.js (Vite)
*   CSS3 & WebGL (`Lightfall.jsx`)
*   Deployed on Vercel

**Backend**
*   FastAPI (Python)
*   Pandas (Data manipulation and caching)
*   Deployed on Render

**Machine Learning**
*   Hugging Face API (Zero-shot text classification)
*   Scikit-learn (TF-IDF and Cosine Similarity)

## 🚀 Running Locally

To run this project on your local machine, you will need two terminal windows to start the frontend and backend separately.

### 1. Backend Setup

cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

# (Optional) Fetch fresh news data
python ingestion.py

# Start the FastAPI server
uvicorn main:app --reload --port 10000

### 2. Frontend Setup
cd frontend
npm install

# Start the Vite development server
npm run dev
