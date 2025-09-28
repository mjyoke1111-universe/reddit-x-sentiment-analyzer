# Reddit & X Sentiment Analyzer - Free MVP

Automated sentiment analysis for Reddit threads & comments and X (Twitter) posts using AI-powered, no-cost deployment with evidence logging.

## 🚀 Free MVP Features

- **Reddit Analysis**: Analyze sentiment of threads and all comments
- **X (Twitter) Analysis**: Analyze sentiment of posts and replies
- **AI-Powered**: Uses Perplexity AI for advanced sentiment detection
- **Evidence Logging**: Automatically logs all analysis results with timestamps
- **Zero Cost**: Built entirely with free tools and services
- **No Authentication Required**: Works without API keys or paid subscriptions

## 🛠️ How It Works (Using Only Free Tools)

### Core Technology Stack
- **Comet Browser**: Free web automation for data collection
- **Perplexity AI**: Free tier for sentiment analysis
- **GitHub**: Free hosting and version control
- **Local Storage**: Free evidence logging to local files

### Step-by-Step Process

1. **Data Collection**
   - Use Comet browser automation to scrape Reddit threads/comments
   - Extract X (Twitter) posts and replies via web scraping
   - No API keys required - direct web interface access

2. **Sentiment Analysis**
   - Send collected text to Perplexity AI (free tier)
   - Get sentiment scores: Positive, Negative, Neutral
   - Include confidence levels and reasoning

3. **Evidence Logging**
   - Timestamp all analyses
   - Save original text, sentiment scores, and AI reasoning
   - Export results to CSV/JSON for further analysis
   - Store locally - no cloud costs

### Workflow Example

```
Input: Reddit thread URL or X post URL
↓
Comet scrapes all comments/replies
↓
Text sent to Perplexity for sentiment analysis
↓
Results logged with evidence:
- Original text
- Sentiment score
- Confidence level
- Timestamp
- Source URL
↓
Export comprehensive report
```

## 🎯 Use Cases

- **Brand Monitoring**: Track sentiment around products/services
- **Social Research**: Analyze public opinion on topics
- **Content Strategy**: Understand audience reactions
- **Market Research**: Gauge customer sentiment
- **Academic Research**: Study social media discourse

## 📊 Output Format

Each analysis generates:
- **Summary Report**: Overall sentiment distribution
- **Detailed Log**: Individual comment/post analysis
- **Evidence File**: Original text + analysis for verification
- **Timestamp Tracking**: When analysis was performed

## 🆓 Why This MVP is Completely Free

1. **Comet Browser**: Free web automation tool
2. **Perplexity AI**: Free tier provides sentiment analysis
3. **GitHub**: Free hosting and code management
4. **Local Storage**: No cloud storage fees
5. **Web Scraping**: Direct access, no API costs

## 🚦 Getting Started

1. Clone this repository
2. Open Comet browser
3. Load the analyzer script
4. Enter Reddit thread or X post URL
5. Watch automated analysis begin
6. Review generated evidence logs

## 🔍 Evidence Logging Details

Every analysis includes:
- **Source Verification**: Original URL and timestamp
- **Text Preservation**: Exact comment/post content
- **AI Reasoning**: Why the sentiment was classified
- **Confidence Metrics**: How certain the AI is
- **Audit Trail**: Complete processing history

## ⚡ Quick Demo

1. Input: `https://reddit.com/r/technology/comments/example`
2. Comet automatically:
   - Scrapes main post + all comments
   - Sends each to Perplexity for analysis
   - Logs results with evidence
   - Generates summary report
3. Output: Complete sentiment analysis with proof

## 📈 Scalability

While this is a free MVP, it can handle:
- Reddit threads with 100+ comments
- X conversations with multiple replies
- Batch processing of multiple URLs
- Historical analysis of past discussions

## 🤖 AI Prompt Engineering

Optimized prompts for Perplexity ensure:
- Accurate sentiment classification
- Contextual understanding
- Confidence scoring
- Detailed reasoning
- Bias detection

## 📋 Evidence Report Sample

```json
{
  "analysis_id": "reddit_tech_001",
  "timestamp": "2025-09-28T10:57:00Z",
  "source_url": "https://reddit.com/r/technology/comments/example",
  "total_comments": 45,
  "sentiment_summary": {
    "positive": 62%,
    "neutral": 28%,
    "negative": 10%
  },
  "evidence_log": "evidence_reddit_tech_001.csv",
  "processing_time": "2.3 minutes"
}
```

## 🎓 Learn More

- [Comet Browser Documentation](https://comet.perplexity.ai)
- [Perplexity AI Guide](https://perplexity.ai)
- [Sentiment Analysis Best Practices](https://github.com/)

---

**Built with ❤️ using only free tools: Comet + Perplexity + GitHub**

*No API keys, no subscriptions, no hidden costs - just powerful sentiment analysis.*
