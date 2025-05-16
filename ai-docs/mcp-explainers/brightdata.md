# Bright Data Tools Guide

This document provides an overview of Bright Data's capabilities through the Model Context Protocol (MCP) in VS Code. Bright Data specializes in web scraping, data extraction, and browser automation with the ability to bypass bot detection and access geo-restricted content.

## Web Scraping and Search Tools

### 1. Search Engine Scraping
**Question:** "What are the top search results for 'machine learning frameworks' on Google?"  
**Tool:** `f1e_search_engine`  
**Description:** Scrapes search results from Google, Bing, or Yandex, returning SERP results in markdown format (URL, title, description).

### 2. Webpage Scraping (Markdown)
**Question:** "Can you extract the content from this webpage that has anti-bot measures?"  
**Tool:** `f1e_scrape_as_markdown`  
**Description:** Scrapes a single webpage URL with advanced options for content extraction and returns the results in Markdown format. This tool can bypass bot detection or CAPTCHA systems.

### 3. Webpage Scraping (HTML)
**Question:** "I need the HTML structure of this webpage for detailed analysis."  
**Tool:** `f1e_scrape_as_html`  
**Description:** Similar to the markdown scraper but returns results in HTML format, preserving the structure for more technical analysis.

### 4. Session Statistics
**Question:** "How many web scraping operations have I performed in this session?"  
**Tool:** `f1e_session_stats`  
**Description:** Provides usage statistics for the current session, including the number and types of tools used.

## Structured Data Extraction

### E-commerce Data

#### 1. Amazon Product Data
**Question:** "Can you extract detailed information about this Amazon product?"  
**Tool:** `f1e_web_data_amazon_product`  
**Description:** Quickly retrieves structured Amazon product data from a valid product URL (containing `/dp/`). May use cached data when available for faster results.

#### 2. Amazon Product Reviews
**Question:** "What are people saying in the reviews for this Amazon product?"  
**Tool:** `f1e_web_data_amazon_product_reviews`  
**Description:** Extracts structured review data from Amazon product pages, including ratings, text, and metadata.

### Professional Networks Data

#### 1. LinkedIn Person Profile
**Question:** "Can you get information about this professional's LinkedIn profile?"  
**Tool:** `f1e_web_data_linkedin_person_profile`  
**Description:** Extracts structured data from LinkedIn personal profiles, including work history, skills, and education.

#### 2. LinkedIn Company Profile
**Question:** "What information is available about this company on LinkedIn?"  
**Tool:** `f1e_web_data_linkedin_company_profile`  
**Description:** Retrieves structured data from LinkedIn company profiles, including company size, industry, and description.

#### 3. ZoomInfo Company Profile
**Question:** "I need more detailed business information about this company from ZoomInfo."  
**Tool:** `f1e_web_data_zoominfo_company_profile`  
**Description:** Extracts structured company data from ZoomInfo, which often contains more comprehensive business intelligence than other platforms.

### Social Media Data

#### 1. Instagram Profiles
**Question:** "Can you extract data from this Instagram profile?"  
**Tool:** `f1e_web_data_instagram_profiles`  
**Description:** Retrieves structured data from Instagram profiles, including follower count, post count, and bio information.

#### 2. Instagram Posts
**Question:** "What information can you extract from this Instagram post?"  
**Tool:** `f1e_web_data_instagram_posts`  
**Description:** Extracts structured data from individual Instagram posts, including captions, likes, and comments count.

#### 3. Instagram Reels
**Question:** "Can you get the metadata for this Instagram reel?"  
**Tool:** `f1e_web_data_instagram_reels`  
**Description:** Retrieves structured data specific to Instagram reels, including view counts and engagement metrics.

#### 4. Instagram Comments
**Question:** "What are people commenting on this Instagram post?"  
**Tool:** `f1e_web_data_instagram_comments`  
**Description:** Extracts structured comment data from Instagram posts, including usernames and comment text.

#### 5. Facebook Posts
**Question:** "Can you extract the content and engagement metrics from this Facebook post?"  
**Tool:** `f1e_web_data_facebook_posts`  
**Description:** Retrieves structured data from Facebook posts, including text, reactions, and share counts.

#### 6. Facebook Marketplace Listings
**Question:** "What details can you extract from this Facebook Marketplace listing?"  
**Tool:** `f1e_web_data_facebook_marketplace_listings`  
**Description:** Extracts structured data from Facebook Marketplace listings, including price, description, and location.

#### 7. Facebook Company Reviews
**Question:** "What are customers saying in the reviews for this company on Facebook?"  
**Tool:** `f1e_web_data_facebook_company_reviews`  
**Description:** Retrieves structured review data from Facebook company pages, including ratings and review text.

#### 8. X (Twitter) Posts
**Question:** "Can you extract the content and engagement metrics from this tweet?"  
**Tool:** `f1e_web_data_x_posts`  
**Description:** Extracts structured data from X (formerly Twitter) posts, including text, like count, and repost count.

### Real Estate and Travel Data

#### 1. Zillow Properties Listing
**Question:** "What are the details of this home listing on Zillow?"  
**Tool:** `f1e_web_data_zillow_properties_listing`  
**Description:** Extracts structured data from Zillow property listings, including price, specifications, and property details.

#### 2. Booking Hotel Listings
**Question:** "Can you get the details for this hotel from Booking.com?"  
**Tool:** `f1e_web_data_booking_hotel_listings`  
**Description:** Retrieves structured data from Booking.com hotel listings, including pricing, amenities, and availability.

#### 3. YouTube Videos
**Question:** "What metadata can you extract from this YouTube video?"  
**Tool:** `f1e_web_data_youtube_videos`  
**Description:** Extracts structured data from YouTube videos, including title, description, view count, and engagement metrics.

## Browser Automation Tools
These tools require BROWSER_AUTH to be configured.

### 1. Browser Navigation
**Question:** "Navigate to this specific URL using the browser automation."  
**Tool:** `f1e_scraping_browser_navigate`  
**Description:** Navigates a scraping browser session to a specified URL, establishing a session that can be used with other browser automation tools.

### 2. Browser Back Navigation
**Question:** "Go back to the previous page in the browser session."  
**Tool:** `f1e_scraping_browser_go_back`  
**Description:** Navigates back to the previous page in the current browser session, similar to clicking the back button.

### 3. Browser Forward Navigation
**Question:** "Go forward to the next page in the browser session."  
**Tool:** `f1e_scraping_browser_go_forward`  
**Description:** Navigates forward to the next page in the current browser session, similar to clicking the forward button.

### 4. Element Clicking
**Question:** "Click on the 'Submit' button on this form."  
**Tool:** `f1e_scraping_browser_click`  
**Description:** Clicks on a specified element within the current webpage. Requires knowing the element selector.

### 5. Link Analysis
**Question:** "What links are available on the current page?"  
**Tool:** `f1e_scraping_browser_links`  
**Description:** Extracts all links on the current page along with their text and selectors, which is useful for identifying targets for the click tool.

### 6. Text Input

---

**Note:** This file has been automatically truncated to 150 lines maximum.
Full content was 258 lines. Last updated: 2025-05-17 00:39:42
