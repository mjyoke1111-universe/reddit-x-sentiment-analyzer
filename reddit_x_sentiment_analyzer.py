#!/usr/bin/env python3
"""
Reddit/X Sentiment Analyzer

A tool to scrape comments/replies from Reddit threads or X posts using
Comet browser automation, analyze sentiment via Perplexity's free web interface,
and log results to CSV.

Dependencies:
- selenium
- beautifulsoup4
- requests
- csv (built-in)
- time (built-in)
- datetime (built-in)
- re (built-in)
- urllib.parse (built-in)
"""

import csv
import time
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests


class SentimentAnalyzer:
    def __init__(self):
        self.setup_driver()
        self.csv_filename = f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.init_csv()
    
    def setup_driver(self):
        """Initialize Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
    
    def init_csv(self):
        """Initialize CSV file with headers"""
        with open(self.csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'timestamp', 'platform', 'url', 'comment_text', 
                'sentiment', 'confidence', 'ai_reasoning'
            ])
    
    def log_to_csv(self, platform, url, comment_text, sentiment, confidence, reasoning):
        """Log analysis results to CSV"""
        timestamp = datetime.now().isoformat()
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, platform, url, comment_text[:500],  # Truncate long comments
                sentiment, confidence, reasoning
            ])
    
    def detect_platform(self, url):
        """Detect if URL is from Reddit or X/Twitter"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if 'reddit.com' in domain:
            return 'reddit'
        elif 'twitter.com' in domain or 'x.com' in domain:
            return 'x'
        else:
            raise ValueError(f"Unsupported platform: {domain}")
    
    def scrape_reddit_comments(self, url):
        """Scrape comments from Reddit thread"""
        print(f"Scraping Reddit thread: {url}")
        self.driver.get(url)
        time.sleep(3)
        
        comments = []
        
        try:
            # Wait for comments to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='comment']")))
            
            # Scroll to load more comments
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 10
            
            while scroll_attempts < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
            
            # Extract comment text
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='comment'] p")
            
            for element in comment_elements:
                text = element.text.strip()
                if text and len(text) > 10:  # Filter out very short comments
                    comments.append(text)
            
            print(f"Found {len(comments)} comments")
            
        except Exception as e:
            print(f"Error scraping Reddit comments: {e}")
        
        return comments
    
    def scrape_x_replies(self, url):
        """Scrape replies from X/Twitter post"""
        print(f"Scraping X post: {url}")
        self.driver.get(url)
        time.sleep(3)
        
        replies = []
        
        try:
            # Wait for tweets to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweet']")))
            
            # Scroll to load more replies
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 10
            
            while scroll_attempts < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
            
            # Extract reply text
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='tweet'] [data-testid='tweetText']")
            
            for element in tweet_elements:
                text = element.text.strip()
                if text and len(text) > 10:  # Filter out very short replies
                    replies.append(text)
            
            print(f"Found {len(replies)} replies")
            
        except Exception as e:
            print(f"Error scraping X replies: {e}")
        
        return replies
    
    def analyze_sentiment_with_perplexity(self, text):
        """Analyze sentiment using Perplexity's free web interface"""
        try:
            # Navigate to Perplexity
            self.driver.get("https://www.perplexity.ai")
            time.sleep(2)
            
            # Find the search/input box
            search_box = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "textarea, input[type='text'], [contenteditable='true']"
            )))
            
            # Create sentiment analysis prompt
            prompt = f"""Analyze the sentiment of this text and provide:
1. Sentiment (positive/negative/neutral)
2. Confidence score (0-1)
3. Brief reasoning

Text: "{text[:300]}..."

Respond in this exact format:
Sentiment: [sentiment]
Confidence: [score]
Reasoning: [brief explanation]"""
            
            search_box.clear()
            search_box.send_keys(prompt)
            time.sleep(1)
            
            # Submit the query
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], [aria-label*='submit'], [aria-label*='Send']")
            submit_button.click()
            
            # Wait for response
            time.sleep(5)
            
            # Extract response
            response_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='response'], .response, .answer")
            
            if response_elements:
                response_text = response_elements[-1].text
                return self.parse_sentiment_response(response_text)
            else:
                return "neutral", 0.5, "Unable to get response from Perplexity"
        
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "neutral", 0.5, f"Error: {str(e)}"
    
    def parse_sentiment_response(self, response):
        """Parse sentiment analysis response from Perplexity"""
        sentiment = "neutral"
        confidence = 0.5
        reasoning = "Unable to parse response"
        
        try:
            # Extract sentiment
            sentiment_match = re.search(r'Sentiment:\s*(\w+)', response, re.IGNORECASE)
            if sentiment_match:
                sentiment = sentiment_match.group(1).lower()
            
            # Extract confidence
            confidence_match = re.search(r'Confidence:\s*([0-9.]+)', response, re.IGNORECASE)
            if confidence_match:
                confidence = float(confidence_match.group(1))
            
            # Extract reasoning
            reasoning_match = re.search(r'Reasoning:\s*(.+)', response, re.IGNORECASE | re.DOTALL)
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()[:200]  # Limit length
        
        except Exception as e:
            print(f"Error parsing response: {e}")
        
        return sentiment, confidence, reasoning
    
    def analyze_url(self, url):
        """Main method to analyze sentiment for a given URL"""
        platform = self.detect_platform(url)
        
        # Scrape comments/replies
        if platform == 'reddit':
            texts = self.scrape_reddit_comments(url)
        elif platform == 'x':
            texts = self.scrape_x_replies(url)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        
        print(f"Analyzing sentiment for {len(texts)} {platform} comments/replies...")
        
        # Analyze each comment/reply
        for i, text in enumerate(texts):
            print(f"Analyzing {i+1}/{len(texts)}...")
            
            sentiment, confidence, reasoning = self.analyze_sentiment_with_perplexity(text)
            
            # Log results
            self.log_to_csv(platform, url, text, sentiment, confidence, reasoning)
            
            # Rate limiting - wait between requests
            time.sleep(3)
        
        print(f"Analysis complete. Results saved to {self.csv_filename}")
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            self.driver.quit()


def main():
    """Main function"""
    print("Reddit/X Sentiment Analyzer")
    print("===========================\n")
    
    analyzer = SentimentAnalyzer()
    
    try:
        # Get URL from user
        url = input("Enter Reddit thread URL or X post URL: ").strip()
        
        if not url:
            print("No URL provided.")
            return
        
        # Validate URL
        try:
            analyzer.detect_platform(url)
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        # Analyze the URL
        analyzer.analyze_url(url)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
