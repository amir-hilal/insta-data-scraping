"""
Instagram Follower Counter

A Python script that uses instaloader to fetch the number of followers
for a specified Instagram account.
"""

import instaloader
import os
from dotenv import load_dotenv
import sys
from datetime import datetime

class InstagramFollowerScraper:
    def __init__(self):
        """Initialize the Instagram scraper with instaloader."""
        self.loader = instaloader.Instaloader()

        # Load environment variables
        load_dotenv()

        # Optional: Login credentials for accessing private accounts
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')

        # Configure instaloader settings
        self.loader.download_pictures = False
        self.loader.download_videos = False
        self.loader.download_video_thumbnails = False
        self.loader.download_geotags = False
        self.loader.download_comments = False
        self.loader.save_metadata = False

    def login(self):
        """
        Login to Instagram (optional - only needed for private accounts).

        Returns:
            bool: True if login successful, False otherwise
        """
        if not self.username or not self.password:
            print("No credentials provided. Running without login (public accounts only).")
            return False

        try:
            self.loader.login(self.username, self.password)
            print(f"Successfully logged in as {self.username}")
            return True
        except instaloader.exceptions.BadCredentialsException:
            print("Error: Invalid username or password")
            return False
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("Error: Two-factor authentication required")
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def get_follower_count(self, username):
        """
        Get the follower count for a specific Instagram account.

        Args:
            username (str): Instagram username (without @)

        Returns:
            dict: Dictionary containing follower data and metadata
        """
        try:
            # Get profile
            profile = instaloader.Profile.from_username(self.loader.context, username)

            # Extract follower information
            follower_data = {
                'username': profile.username,
                'full_name': profile.full_name,
                'followers': profile.followers,
                'following': profile.followees,
                'posts': profile.mediacount,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'biography': profile.biography,
                'external_url': profile.external_url,
                'timestamp': datetime.now().isoformat()
            }

            return follower_data

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Error: Profile '{username}' does not exist")
            return None
        except instaloader.exceptions.LoginRequiredException:
            print("Error: Login required to access this profile (private account)")
            return None
        except Exception as e:
            print(f"Error getting follower count: {e}")
            return None

    def display_follower_info(self, follower_data):
        """
        Display follower information in a formatted way.

        Args:
            follower_data (dict): Follower data dictionary
        """
        if not follower_data:
            return

        print("\n" + "="*50)
        print(f"INSTAGRAM PROFILE: @{follower_data['username']}")
        print("="*50)
        print(f"Full Name: {follower_data['full_name']}")
        print(f"Followers: {follower_data['followers']:,}")
        print(f"Following: {follower_data['following']:,}")
        print(f"Posts: {follower_data['posts']:,}")
        print(f"Private Account: {'Yes' if follower_data['is_private'] else 'No'}")
        print(f"Verified: {'Yes' if follower_data['is_verified'] else 'No'}")
        print(f"Bio: {follower_data['biography'][:100]}{'...' if len(follower_data['biography']) > 100 else ''}")
        if follower_data['external_url']:
            print(f"Website: {follower_data['external_url']}")
        print(f"Data retrieved: {follower_data['timestamp']}")
        print("="*50)

    def save_to_file(self, follower_data, filename=None):
        """
        Save follower data to a text file.

        Args:
            follower_data (dict): Follower data dictionary
            filename (str): Optional filename (default: username_followers.txt)
        """
        if not follower_data:
            return

        if not filename:
            filename = f"{follower_data['username']}_followers.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Instagram Profile Data\n")
                f.write(f"Generated: {follower_data['timestamp']}\n\n")
                f.write(f"Username: @{follower_data['username']}\n")
                f.write(f"Full Name: {follower_data['full_name']}\n")
                f.write(f"Followers: {follower_data['followers']:,}\n")
                f.write(f"Following: {follower_data['following']:,}\n")
                f.write(f"Posts: {follower_data['posts']:,}\n")
                f.write(f"Private Account: {'Yes' if follower_data['is_private'] else 'No'}\n")
                f.write(f"Verified: {'Yes' if follower_data['is_verified'] else 'No'}\n")
                f.write(f"Biography: {follower_data['biography']}\n")
                if follower_data['external_url']:
                    f.write(f"Website: {follower_data['external_url']}\n")

            print(f"Data saved to: {filename}")

        except Exception as e:
            print(f"Error saving to file: {e}")


def main():
    """Main function to run the Instagram follower scraper."""
    print("Instagram Follower Counter")
    print("-" * 30)
    print("Note: This tool can access public profiles without login.")
    print("Login is only required for private accounts.\n")

    # Initialize scraper
    scraper = InstagramFollowerScraper()

    # Get target account from environment or user input
    target_account = os.getenv('TARGET_ACCOUNT')

    if not target_account:
        target_account = input("Enter Instagram username to analyze: ").strip()
        if not target_account:
            print("No username provided. Exiting.")
            sys.exit(1)

    # Remove @ if present
    target_account = target_account.lstrip('@')

    print(f"\nFetching data for @{target_account}...")

    # First, try to get follower data without login (for public accounts)
    follower_data = scraper.get_follower_count(target_account)

    # If login is required (private account), offer to login
    if not follower_data:
        print("Unable to access this profile without login.")
        login_choice = input("Do you want to login to Instagram to try accessing this account? (y/n): ").lower().strip()

        if login_choice == 'y':
            if scraper.login():
                print(f"Retrying data fetch for @{target_account}...")
                follower_data = scraper.get_follower_count(target_account)
            else:
                print("Login failed. Cannot access private account.")

    if follower_data:
        # Display information
        scraper.display_follower_info(follower_data)

        # Ask if user wants to save to file
        save_choice = input("\nSave data to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            scraper.save_to_file(follower_data)
    else:
        print("Failed to retrieve follower data.")


if __name__ == "__main__":
    main()
