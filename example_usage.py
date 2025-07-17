"""
Example usage of the Instagram Follower Scraper
"""

from instagram_scraper import InstagramFollowerScraper

def example_basic_usage():
    """Example of basic usage without login."""
    scraper = InstagramFollowerScraper()

    # Get follower data for a public account
    username = "instagram"  # Official Instagram account
    follower_data = scraper.get_follower_count(username)

    if follower_data:
        scraper.display_follower_info(follower_data)
        scraper.save_to_file(follower_data)

def example_with_login():
    """Example usage with login for private accounts."""
    scraper = InstagramFollowerScraper()

    # Login first (credentials should be in .env file)
    if scraper.login():
        # Now you can access private accounts you follow
        username = "private_account_username"
        follower_data = scraper.get_follower_count(username)

        if follower_data:
            scraper.display_follower_info(follower_data)

def example_multiple_accounts():
    """Example of checking multiple accounts."""
    scraper = InstagramFollowerScraper()

    accounts = ["instagram", "nasa", "natgeo"]

    for account in accounts:
        print(f"\nProcessing @{account}...")
        follower_data = scraper.get_follower_count(account)

        if follower_data:
            print(f"@{account}: {follower_data['followers']:,} followers")

if __name__ == "__main__":
    # Run the basic example
    example_basic_usage()

    # Uncomment to test multiple accounts
    # example_multiple_accounts()
