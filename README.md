# 🔮 Threads Fortune Teller

A mystical personality quiz that reveals your content creator DNA through AI-powered analysis of your Threads posts. Generate shareable creator portraits that people love to post on social media!

## ✨ Features

- **🎭 Creator Personality Quiz**: Discover your mystical content creator archetype
- **🧬 Content DNA Analysis**: AI-powered breakdown of your posting patterns
- **📱 One-Click Sharing**: Share to Threads, Instagram Stories, or copy text
- **🎨 Generated Images**: Beautiful, shareable creator portrait graphics
- **🔮 Mystical Experience**: Fortune teller theme with cosmic animations
- **💰 Cost-Controlled**: Cached analysis and smart API usage limits

## 🌟 Creator Archetypes

Your mystical reading reveals one of these creator personalities:
- 📚 **The Authentic Storyteller** - Shares personal experiences and vulnerable moments
- 🔥 **The Trendsetter** - Always ahead of the curve with fresh content
- 🤝 **The Community Builder** - Brings people together through engagement
- 🎓 **The Knowledge Sharer** - Educates and empowers their audience
- 💬 **The Conversation Starter** - Sparks meaningful discussions
- 🎨 **The Visual Artist** - Creates stunning visual content
- 🎬 **The Behind-the-Scenes Creator** - Shows the real process
- 💪 **The Motivational Voice** - Inspires and uplifts others

## 🚀 Quick Start

1. **Clone and Setup**
```bash
git clone https://github.com/Ninacheng222/threads_analytics.git
cd threads_analytics
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys:
# - THREADS_ACCESS_TOKEN
# - THREADS_USER_ID  
# - OPENAI_API_KEY
```

3. **Run Locally**
```bash
python app.py
```

4. **Visit the Fortune Teller**
Open http://localhost:8000 and begin your mystical reading! 🔮

## 🔑 Getting API Access

### Threads API Setup
1. Visit [Meta Developer Console](https://developers.facebook.com)
2. Create new app with "Threads API" use case
3. Generate access token and get your user ID
4. Add to `.env` file

### OpenAI API Key
1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Add `OPENAI_API_KEY` to `.env` file

## 🎯 How It Works

1. **🔗 Connect**: User authorizes Threads account access
2. **✨ Analyze**: AI analyzes posting patterns, content themes, engagement
3. **🎭 Generate**: Creates mystical creator portrait with archetype
4. **📱 Share**: One-click sharing to social platforms

## 📊 What Gets Analyzed

- **Content Themes**: Personal vs Educational vs Entertainment ratios
- **Posting Patterns**: Frequency, timing, consistency
- **Engagement Metrics**: Views, likes, replies, reposts, shares
- **Creator Personality**: Communication style and audience connection

## 🎨 Shareable Content

### Instagram Stories Format
- 1080x1920 cosmic gradient background
- Creator archetype with mystical styling
- Content DNA breakdown with percentages
- Shareable quote and app branding

### Threads Post Format
```
🔮 Just discovered my Creator DNA! ✨

✨ Your content resonates with the frequency of authenticity ✨

My digital aura reveals:
🎭 Archetype: The Authentic Storyteller
📱 Content DNA: 45% Personal
🌙 Posting Spirit: Night Owl Creator

What's YOUR creator personality? 
threadsfortune.app
```

## 🚀 Deployment

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

## 💰 Cost Control

- **Analysis Limit**: Max 50 posts per user reading
- **Cache System**: Results cached for 30 days to avoid re-analysis
- **GPT-3.5-Turbo**: Cost-effective model choice
- **Smart Batching**: Efficient API usage patterns

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🔮 Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **Frontend**: Alpine.js + Tailwind CSS + Cosmic animations
- **AI**: OpenAI GPT-3.5-turbo for personality analysis
- **Images**: Pillow for dynamic content generation
- **Deployment**: Railway, Heroku, or any Python hosting

## 🌟 Future Features

### Phase 2: Viral Mechanics
- **Friend Comparisons**: "Tag a Trendsetter friend"
- **Seasonal Readings**: "Your Winter Creator Energy"
- **Achievement System**: Unlock new archetypes
- **Waiting List**: Build anticipation for new features

### Phase 3: Advanced Sharing
- **TikTok Integration**: Share to TikTok with video format
- **Twitter/X Support**: Auto-thread generation
- **WhatsApp Stories**: Direct sharing to WhatsApp Status
- **Custom Branding**: White-label for agencies

### Phase 4: Business Model
- **Premium Archetypes**: Exclusive creator personalities
- **Team Features**: Brand team personality analysis
- **API Access**: Third-party integrations
- **Analytics Dashboard**: Track viral performance

## 🎭 Sample Creator Portraits

```json
{
  "archetype": "The Authentic Storyteller",
  "content_dna": {"personal": 45, "educational": 30, "entertainment": 25},
  "posting_spirit": "Night Owl Creator",
  "engagement_insight": "Your audience craves your vulnerable authenticity",
  "creator_level": "Rising Star ⭐",
  "mystical_advice": "The universe rewards consistency over perfection",
  "shareable_quote": "✨ Your content resonates with the frequency of authenticity ✨"
}
```

## 🔗 Links

- **Live Demo**: [threadsfortune.app](https://threadsfortune.app) (coming soon)
- **GitHub**: [threads_analytics](https://github.com/Ninacheng222/threads_analytics)
- **API Docs**: `/docs` (when running locally)

## 📄 License

MIT License - Build amazing things! ✨

---

**Ready to discover your Creator DNA?** 🔮✨

*The digital universe is waiting to reveal your mystical creator personality...*