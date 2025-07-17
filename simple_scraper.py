"""
Simple Instagram Follower Counter - Public Profiles Only

A minimal script that demonstrates scraping public Instagram profiles
without any login requirements.
"""

from instagram_scraper import InstagramFollowerScraper
import sys

def simple_scrape(username):
    """
    Simple function to get follower count for public profiles only.

    Args:
        username (str): Instagram username (without @)

    Returns:
        dict or None: Follower data if successful, None otherwise
    """
    # Remove @ if present
    username = username.lstrip('@')

    print(f"Fetching data for @{username}...")
    print("(Public profiles only - no login required)\n")

    # Initialize scraper (no login)
    scraper = InstagramFollowerScraper()

    # Get follower data
    follower_data = scraper.get_follower_count(username)

    if follower_data:
        # Display just the essential info
        print("✅ SUCCESS!")
        print(f"@{follower_data['username']}: {follower_data['followers']:,} followers")
        print(f"Following: {follower_data['following']:,}")
        print(f"Posts: {follower_data['posts']:,}")
        print(f"Verified: {'✓' if follower_data['is_verified'] else '✗'}")

        if follower_data['is_private']:
            print("⚠️  Note: This is a private account, some data may be limited.")

        return follower_data
    else:
        print("❌ Failed to retrieve data.")
        print("This could be because:")
        print("  - The account doesn't exist")
        print("  - The account is private and requires login")
        print("  - Rate limiting by Instagram")
        return None

def main():
    """Main function for simple public profile scraping."""
    print("Simple Instagram Follower Counter")
    print("=" * 40)
    print("Public profiles only - No login required\n")

    if len(sys.argv) > 1:
        # Username provided as command line argument
        username = sys.argv[1]
    else:
        # Ask for username
        username = input("Enter Instagram username: ").strip()
        if not username:
            print("No username provided. Exiting.")
            sys.exit(1)

    # Try to scrape the profile
    follower_data = simple_scrape(username)

    if follower_data:
        # Offer to save data
        save = input("\nSave data to file? (y/n): ").lower().strip()
        if save == 'y':
            scraper = InstagramFollowerScraper()
            scraper.save_to_file(follower_data)

if __name__ == "__main__":
    main()
