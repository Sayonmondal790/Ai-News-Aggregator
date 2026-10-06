import { useState, useEffect } from 'react';
import './App.css';
import Lightfall from './Lightfall.jsx';

const API_BASE = "https://ai-news-aggregator-fjwn.onrender.com";

export default function App() {
  const [articles, setArticles] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [classifications, setClassifications] = useState({});
  const [loadingAction, setLoadingAction] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false); // Controls the popup

  useEffect(() => {
    fetch(`${API_BASE}/api/news`)
      .then(res => res.json())
      .then(data => setArticles(data))
      .catch(err => console.error("Error fetching news:", err));
  }, []);

  const handleClassify = async (articleId) => {
    setLoadingAction(`classify-${articleId}`);
    try {
      const res = await fetch(`${API_BASE}/api/classify/${articleId}`);
      const data = await res.json();
      setClassifications(prev => ({
        ...prev,
        [articleId]: data.classification
      }));
    } catch (err) {
      console.error("Classification error:", err);
    } finally {
      setLoadingAction(null);
    }
  };

  const handleRecommend = async (article) => {
    setSelectedArticle(article);
    setLoadingAction(`rec-${article.id}`);
    try {
      const res = await fetch(`${API_BASE}/api/recommend/${article.id}`);
      const data = await res.json();
      setRecommendations(data);
      setIsModalOpen(true); // Open the popup when data arrives
    } catch (err) {
      console.error("Recommendation error:", err);
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <>
      {/* 1. The WebGL background layer goes here */}
      <div className="background-layer">
        <Lightfall
          colors={['#60a5fa', '#c084fc', '#3b82f6']}
          backgroundColor="#09090b"
          speed={0.6}
          streakCount={3}
          mouseInteraction={true}
        />
      </div>

      {/* 2. Your existing container stays exactly the same */}
      <div className="container">
        <header className="header">
          <h1>AI News Aggregator</h1>
          <p>Curated feed powered by TF-IDF similarity and zero-shot NLP</p>
        </header>

        <main className="layout">
          <section className="feed-column">
            <h2 className="section-title">Top Stories</h2>
            
            {articles.length === 0 ? (
              <p>Loading news stream...</p>
            ) : (
              <div className="news-grid">
                {articles.map(article => (
                  <article key={article.id} className="news-card">
                    <div className="card-meta">
                      <span className="source-tag">{article.source || "BBC News"}</span>
                      <span className="reading-time">{article.reading_time_min || 5} min read</span>
                    </div>
                    <h3>{article.title}</h3>
                    <p className="summary">{article.summary || article.full_text?.slice(0, 100) + "..."}</p>

                    <div className="card-actions">
                      <button 
                        onClick={() => handleClassify(article.id)} 
                        disabled={loadingAction === `classify-${article.id}`}
                      >
                        {loadingAction === `classify-${article.id}` ? "Analyzing..." : "Fact / Opinion"}
                      </button>
                      <button 
                        onClick={() => handleRecommend(article)}
                        disabled={loadingAction === `rec-${article.id}`}
                        className="secondary"
                      >
                        {loadingAction === `rec-${article.id}` ? "Searching..." : "Related Stories"}
                      </button>
                    </div>

                    {classifications[article.id] && (
                      <div className={`badge ${classifications[article.id]?.label.toLowerCase()}`}>
                        <strong>{classifications[article.id].label}</strong> ({(classifications[article.id].confidence * 100).toFixed(1)}%)
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </section>
        </main>

        {/* Popup Modal for Recommendations */}
        {isModalOpen && (
          <div className="modal-overlay" onClick={() => setIsModalOpen(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <button className="close-button" onClick={() => setIsModalOpen(false)}>×</button>
              <h2>Recommendations</h2>
              <p className="sidebar-hint">Similar to: <em>"{selectedArticle.title}"</em></p>
              
              {recommendations.length === 0 ? (
                <p>No related stories found.</p>
              ) : (
                recommendations.map(rec => (
                  <div key={rec.id} className="rec-card">
                    <h4>{rec.title}</h4>
                    <span className="score-tag">
                      Match: {(rec.similarity_score * 100).toFixed(1)}%
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
}