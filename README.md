# Instagram Data Scraping Project

A Python script that uses the `instaloader` library to fetch follower counts and basic profile information from Instagram accounts.

## Features

- **Get follower count for any public Instagram account (no login required)**
- **Advanced post analytics: likes, comments, engagement rates**
- **Analyze recent posts (1-10 posts) with detailed metrics**
- **Support for private accounts (with login)**
- Display detailed profile information
- Save data to text files and JSON
- Environment variable configuration
- Error handling for common issues

## Scripts Available

### 1. `simple_scraper.py` - Basic Profile Info
- Quick follower count lookup
- No login required for public profiles
- Minimal output, fast execution

### 2. `posts_analytics.py` - Posts Engagement Analysis
- **NEW!** Analyzes likes and comments on recent posts
- Calculates engagement rates and averages
- Clean, focused output
- Best for content creators and marketers

### 3. `instagram_scraper.py` - Full Featured
- Complete profile analysis
- Optional login support
- Detailed output with all profile information

### 4. `advanced_scraper.py` - Comprehensive Analytics
- Most detailed analysis including post metadata
- JSON export capabilities
- Advanced engagement metrics

## Quick Start Examples

### Basic Follower Count (Public Profiles)
```bash
python simple_scraper.py instagram
```

### Posts Analytics (Likes & Comments)
```bash
python posts_analytics.py nasa
```

### Full Profile Analysis
```bash
python instagram_scraper.py
```

## Advanced Setup (Private Profiles)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables (optional):**
   - Copy `.env.example` to `.env`
   - Fill in your Instagram credentials (only needed for private accounts)
   - Set a default target account if desired

3. **Run the script:**
   ```bash
   python instagram_scraper.py
   ```

## Usage

### Basic Usage
Run the script and enter an Instagram username when prompted:
```bash
python instagram_scraper.py
```

### With Environment Variables
Set up your `.env` file with:
```
TARGET_ACCOUNT=username_to_analyze
INSTAGRAM_USERNAME=your_username  # Optional
INSTAGRAM_PASSWORD=your_password  # Optional
```

### Features Available

- **Public Accounts**: No login required
- **Private Accounts**: Requires Instagram login
- **Data Export**: Save results to text files
- **Detailed Info**: Followers, following, posts, verification status, bio, etc.

## Output Information

The script provides:
- Username and full name
- Follower count
- Following count
- Number of posts
- Account verification status
- Privacy status
- Biography
- External website URL
- Timestamp of data retrieval

## Important Notes

⚠️ **Rate Limiting**: Instagram has rate limits. Don't make too many requests in a short time.

⚠️ **Login Requirements**: Some profiles require login to view follower counts.

⚠️ **Terms of Service**: Make sure to comply with Instagram's Terms of Service when using this tool.

⚠️ **Two-Factor Authentication**: If you have 2FA enabled, you may need to generate an app-specific password.

## Example Output

```
==================================================
INSTAGRAM PROFILE: @example_user
==================================================
Full Name: Example User
Followers: 1,234,567
Following: 456
Posts: 123
Private Account: No
Verified: Yes
Bio: This is an example biography...
Website: https://example.com
Data retrieved: 2025-07-17T10:30:45.123456
==================================================
```

## File Structure

```
insta-data-scraping/
├── simple_scraper.py       # Basic follower count (public profiles)
├── posts_analytics.py      # NEW! Posts likes/comments analysis
├── instagram_scraper.py    # Full featured scraper (public + private)
├── advanced_scraper.py     # Comprehensive analytics with JSON export
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your environment variables (create this)
├── example_usage.py       # Example usage patterns
└── README.md              # This file
```

## Troubleshooting

**Profile not found**: Verify the username is correct and the account exists.

**Login required**: The account is private. Set up login credentials in `.env`.

**Bad credentials**: Check your username/password in the `.env` file.

**Rate limited**: Wait before making more requests to Instagram.

## Dependencies

- `instaloader`: Instagram data downloading library
- `python-dotenv`: Environment variable management
