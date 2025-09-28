#!/usr/bin/env python3
"""
Automated Daily Sentiment Reporter

This enhanced version automatically:
1. Finds trending Reddit threads and X posts
2. Analyzes sentiment using Perplexity AI via Comet Browser
3. Generates comprehensive daily sentiment reports
4. Posts reports to both Reddit and X
5. Logs evidence and commits to GitHub
6. Schedules recurring automation

Designed for full automation via Comet Assistant.
"""

import json
import csv
import time
from datetime import datetime, timedelta
import re
import os
from pathlib import Path

# This will be executed via Comet Browser automation
class AutomatedSentimentReporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_date = datetime.now().strftime('%Y-%m-%d')
        self.evidence_dir = Path(f"evidence_{self.report_date}")
        self.evidence_dir.mkdir(exist_ok=True)
        
    def find_trending_reddit_threads(self):
        """
        Navigate to Reddit trending/popular sections and collect URLs
        This will be executed by Comet Browser automation
        """
        trending_urls = [
            "https://www.reddit.com/r/all/top/?t=day",
            "https://www.reddit.com/r/technology/hot/",
            "https://www.reddit.com/r/worldnews/hot/", 
            "https://www.reddit.com/r/politics/hot/",
            "https://www.reddit.com/r/AskReddit/hot/"
        ]
        return trending_urls
    
    def find_trending_x_posts(self):
        """
        Navigate to X trending sections and collect URLs
        This will be executed by Comet Browser automation
        """
        trending_urls = [
            "https://x.com/explore/tabs/trending",
            "https://x.com/search?q=%23trending&src=trend_click&vertical=trends"
        ]
        return trending_urls
    
    def analyze_sentiment_with_perplexity(self, text_batch):
        """
        Send batch of text to Perplexity for sentiment analysis
        Enhanced prompt for better accuracy
        """
        prompt = f"""
        Analyze sentiment for this batch of social media content. For each text, provide:
        1. Sentiment: positive/negative/neutral 
        2. Intensity: low/medium/high
        3. Confidence: 0.0-1.0
        4. Key emotional indicators
        
        Texts to analyze:
        {json.dumps(text_batch, indent=2)}
        
        Respond in JSON format:
        {{
          "analysis": [
            {{
              "text_id": 0,
              "sentiment": "positive/negative/neutral",
              "intensity": "low/medium/high", 
              "confidence": 0.85,
              "emotional_indicators": ["excitement", "optimism"],
              "reasoning": "Brief explanation"
            }}
          ],
          "batch_summary": {{
            "positive_pct": 45,
            "negative_pct": 25,
            "neutral_pct": 30,
            "dominant_emotions": ["anger", "hope"],
            "key_topics": ["technology", "economy"]
          }}
        }}
        """
        
        # This will be executed via Comet navigation to Perplexity
        return prompt
    
    def generate_daily_report(self, reddit_data, x_data):
        """
        Generate comprehensive daily sentiment report
        """
        report = {
            "report_date": self.report_date,
            "timestamp": self.timestamp,
            "summary": {
                "total_posts_analyzed": len(reddit_data) + len(x_data),
                "reddit_posts": len(reddit_data),
                "x_posts": len(x_data)
            },
            "sentiment_breakdown": {
                "reddit": self.calculate_sentiment_stats(reddit_data),
                "x": self.calculate_sentiment_stats(x_data),
                "overall": self.calculate_overall_stats(reddit_data, x_data)
            },
            "trending_topics": self.extract_trending_topics(reddit_data, x_data),
            "hot_takes": self.identify_hot_takes(reddit_data, x_data),
            "evidence_files": [
                f"reddit_analysis_{self.timestamp}.csv",
                f"x_analysis_{self.timestamp}.csv",
                f"daily_report_{self.timestamp}.json"
            ]
        }
        
        return report
    
    def calculate_sentiment_stats(self, data):
        """Calculate sentiment statistics for a dataset"""
        if not data:
            return {"positive": 0, "negative": 0, "neutral": 0, "count": 0}
        
        total = len(data)
        positive = sum(1 for item in data if item.get('sentiment') == 'positive')
        negative = sum(1 for item in data if item.get('sentiment') == 'negative') 
        neutral = total - positive - negative
        
        return {
            "positive": round(positive/total*100, 1),
            "negative": round(negative/total*100, 1), 
            "neutral": round(neutral/total*100, 1),
            "count": total
        }
    
    def calculate_overall_stats(self, reddit_data, x_data):
        """Calculate combined sentiment statistics"""
        all_data = reddit_data + x_data
        return self.calculate_sentiment_stats(all_data)
    
    def extract_trending_topics(self, reddit_data, x_data):
        """Extract and rank trending topics from analysis"""
        # This would analyze the most frequently mentioned topics
        # For now, return placeholder structure
        return [
            {"topic": "AI Technology", "mentions": 156, "sentiment": "positive"},
            {"topic": "Economic Policy", "mentions": 89, "sentiment": "negative"},
            {"topic": "Climate Change", "mentions": 67, "sentiment": "neutral"}
        ]
    
    def identify_hot_takes(self, reddit_data, x_data):
        """Identify controversial or highly emotional posts"""
        hot_takes = []
        all_data = reddit_data + x_data
        
        for item in all_data:
            if (item.get('confidence', 0) > 0.8 and 
                item.get('intensity') == 'high'):
                hot_takes.append({
                    "platform": item.get('platform'),
                    "text_preview": item.get('text', '')[:100] + "...",
                    "sentiment": item.get('sentiment'),
                    "intensity": item.get('intensity'),
                    "url": item.get('source_url')
                })
        
        return hot_takes[:5]  # Top 5 hot takes
    
    def compose_social_report(self, report_data):
        """
        Compose social media post for the daily report
        """
        overall = report_data['sentiment_breakdown']['overall']
        trending = report_data['trending_topics'][:3]
        
        post_text = f"""🤖 Daily Sentiment Report - {self.report_date}

📊 Today's Social Sentiment:
✅ Positive: {overall['positive']}%
❌ Negative: {overall['negative']}% 
⚖️ Neutral: {overall['neutral']}%

🔥 Trending Topics:
{chr(10).join([f"• {t['topic']}: {t['sentiment']} sentiment" for t in trending])}

📈 Analysis: {overall['count']} posts from Reddit & X
🔍 Full evidence & methodology: [GitHub repo link]

#SentimentAnalysis #DataScience #SocialTrends #AI

Generated automatically by Comet + Perplexity 🚀"""
        
        return post_text
    
    def save_evidence_files(self, reddit_data, x_data, report_data):
        """Save all evidence and analysis files"""
        # Save Reddit analysis CSV
        reddit_file = self.evidence_dir / f"reddit_analysis_{self.timestamp}.csv"
        self.save_csv(reddit_data, reddit_file)
        
        # Save X analysis CSV  
        x_file = self.evidence_dir / f"x_analysis_{self.timestamp}.csv"
        self.save_csv(x_data, x_file)
        
        # Save daily report JSON
        report_file = self.evidence_dir / f"daily_report_{self.timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
            
        return [str(reddit_file), str(x_file), str(report_file)]
    
    def save_csv(self, data, filename):
        """Save data to CSV with proper headers"""
        if not data:
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'platform', 'source_url', 'text_preview',
                'sentiment', 'intensity', 'confidence', 'emotional_indicators',
                'reasoning'
            ])
            
            for item in data:
                writer.writerow([
                    item.get('timestamp', ''),
                    item.get('platform', ''),
                    item.get('source_url', ''),
                    item.get('text', '')[:200],  # Preview only
                    item.get('sentiment', ''),
                    item.get('intensity', ''),
                    item.get('confidence', ''),
                    json.dumps(item.get('emotional_indicators', [])),
                    item.get('reasoning', '')
                ])

# Comet Automation Instructions
"""
COMET EXECUTION PLAN:

1. TRENDING CONTENT DISCOVERY:
   - Navigate to reddit.com/r/all/top/?t=day
   - Scroll and collect top 10 thread URLs
   - Navigate to x.com/explore/tabs/trending 
   - Collect top 10 trending post URLs
   
2. SENTIMENT ANALYSIS:
   - For each URL, navigate and scrape comments/replies
   - Batch text into groups of 10 for efficiency
   - Navigate to perplexity.ai for each batch
   - Submit analysis prompt and extract JSON response
   
3. REPORT GENERATION:
   - Aggregate all sentiment data
   - Generate daily report with trends and hot-takes
   - Create social media post text
   
4. SOCIAL POSTING:
   - Navigate to reddit.com and post to r/datascience or r/analytics
   - Navigate to x.com and post daily report
   - Include transparent methodology and evidence links
   
5. EVIDENCE LOGGING:
   - Save all CSV and JSON files locally
   - Navigate to GitHub repo
   - Upload/commit all evidence files
   - Update README with latest report link
   
6. AUTOMATION SETUP:
   - Create Comet scheduled task for 12-hour intervals
   - Morning report: 8 AM analysis of overnight trends
   - Evening report: 8 PM analysis of daily trends

ERROR HANDLING:
   - Skip failed URLs, continue with available data
   - If Perplexity fails, use backup prompting
   - Always save partial results before social posting
   - Log all errors to error.log file

RATE LIMITING:
   - 2-3 second delays between major operations
   - Respect platform rate limits
   - Use random delays to avoid detection

QUALITY ASSURANCE:
   - Minimum 20 posts analyzed per platform
   - Skip posts with <10 words
   - Validate sentiment JSON responses
   - Include confidence thresholds in reporting
"""

def main():
    """Main execution function for Comet automation"""
    reporter = AutomatedSentimentReporter()
    print(f"Starting Daily Sentiment Report - {reporter.report_date}")
    
    # This would be executed by Comet Browser automation:
    # 1. Find trending content
    # 2. Analyze sentiment
    # 3. Generate and post reports
    # 4. Save evidence and commit to GitHub
    
    print("Automated Daily Sentiment Reporter initialized")
    print("Ready for Comet Browser automation execution")
    
if __name__ == "__main__":
    main()
