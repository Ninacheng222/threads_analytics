# Threads Analytics MVP

A simple, interactive dashboard to analyze your personal Threads account performance with AI-powered content insights.

## Features

- **Interactive Dashboard**: Sort, filter, and analyze your Threads posts
- **Performance Metrics**: Engagement rates, views, likes, replies, reposts, shares
- **AI Content Analysis**: OpenAI-powered insights on post performance
- **Cost-Controlled**: Cached analysis and configurable limits
- **Simple Deployment**: SQLite database, minimal dependencies

## Quick Start

1. **Clone and Setup**
```bash
git clone <my-threads-analytics-repo>
cd threads_analytics
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run Locally**
```bash
python app.py
```

4. **Access Dashboard**
Open http://localhost:8000

## Getting API Access

### Threads API Token
1. Go to [Meta Developer Console](https://developers.facebook.com)
2. Create a new app with "Threads API" use case
3. Generate access token and user ID
4. Add to `.env` file

### OpenAI API Key
1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Add to `.env` file

## Deployment

### Railway (Recommended - $5/month)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Environment Variables for Production
```
THREADS_ACCESS_TOKEN=your_token
THREADS_USER_ID=your_user_id
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://... (Railway provides this)
```

## Usage

1. **Sync Data**: Click "Sync Data" to fetch your latest posts
2. **Sort & Filter**: Click column headers to sort posts
3. **Select Posts**: Use checkboxes to select posts for analysis
4. **Analyze Content**: Click "Analyze Selected" for AI insights
5. **View Trends**: Switch between engagement, views, and likes charts

## Cost Control

- Analysis limited to 10 posts per request
- Results cached for 30 days
- Uses GPT-3.5-turbo for cost efficiency
- SQLite for free local development

## Next Phase Features

- Multi-user support with OAuth
- Advanced NLP analytics
- Real-time webhooks
- Export functionality
- Mobile optimization

## Architecture

```
Frontend (Alpine.js + Tailwind) → FastAPI → Threads API
                                      ↓
                               SQLite/PostgreSQL
                                      ↓
                                OpenAI API (Analysis)
```