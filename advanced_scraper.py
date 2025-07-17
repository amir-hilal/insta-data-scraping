"""
Advanced Instagram Scraper - Posts Analytics

A Python script that fetches follower count plus detailed analytics
for the last 3 posts including likes and comments count.
"""

from instagram_scraper import InstagramFollowerScraper
import instaloader
import sys
from datetime import datetime
import json

class AdvancedInstagramScraper(InstagramFollowerScraper):
    def __init__(self):
        """Initialize the advanced Instagram scraper."""
        super().__init__()

        # Configure for minimal data download but enable post metadata
        self.loader.save_metadata = True
        self.loader.compress_json = False

    def get_post_analytics(self, username, post_count=3):
        """
        Get analytics for the last N posts of a user.

        Args:
            username (str): Instagram username (without @)
            post_count (int): Number of recent posts to analyze (default: 3)

        Returns:
            dict: Dictionary containing profile data and post analytics
        """
        try:
            # Get profile first
            profile = instaloader.Profile.from_username(self.loader.context, username)

            # Basic profile data
            profile_data = {
                'username': profile.username,
                'full_name': profile.full_name,
                'followers': profile.followers,
                'following': profile.followees,
                'total_posts': profile.mediacount,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'biography': profile.biography,
                'external_url': profile.external_url,
                'timestamp': datetime.now().isoformat(),
                'posts_analyzed': [],
                'analytics_summary': {}
            }

            if profile.is_private:
                print(f"⚠️  Profile @{username} is private. Post analytics may be limited.")
                return profile_data

            print(f"📊 Analyzing last {post_count} posts...")

            # Get recent posts
            posts = profile.get_posts()
            analyzed_posts = []
            total_likes = 0
            total_comments = 0

            for i, post in enumerate(posts):
                if i >= post_count:
                    break

                print(f"  📱 Analyzing post {i+1}/{post_count}...")

                post_data = {
                    'post_number': i + 1,
                    'shortcode': post.shortcode,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'date': post.date.isoformat(),
                    'likes': post.likes,
                    'comments': post.comments,
                    'is_video': post.is_video,
                    'caption': post.caption[:200] + "..." if post.caption and len(post.caption) > 200 else post.caption,
                    'caption_hashtags': post.caption_hashtags if hasattr(post, 'caption_hashtags') else [],
                    'location': post.location.name if post.location else None
                }

                analyzed_posts.append(post_data)
                total_likes += post.likes
                total_comments += post.comments

            # Calculate analytics summary
            if analyzed_posts:
                avg_likes = total_likes / len(analyzed_posts)
                avg_comments = total_comments / len(analyzed_posts)
                engagement_rate = ((total_likes + total_comments) / len(analyzed_posts)) / profile.followers * 100 if profile.followers > 0 else 0

                profile_data['analytics_summary'] = {
                    'total_likes': total_likes,
                    'total_comments': total_comments,
                    'average_likes_per_post': round(avg_likes, 2),
                    'average_comments_per_post': round(avg_comments, 2),
                    'engagement_rate_percentage': round(engagement_rate, 2),
                    'posts_analyzed_count': len(analyzed_posts)
                }

            profile_data['posts_analyzed'] = analyzed_posts

            return profile_data

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"❌ Error: Profile '{username}' does not exist")
            return None
        except instaloader.exceptions.LoginRequiredException:
            print("❌ Error: Login required to access this profile's posts")
            return None
        except Exception as e:
            print(f"❌ Error getting post analytics: {e}")
            return None

    def display_analytics(self, data):
        """
        Display comprehensive analytics in a formatted way.

        Args:
            data (dict): Analytics data dictionary
        """
        if not data:
            return

        print("\n" + "="*60)
        print(f"📊 INSTAGRAM ANALYTICS: @{data['username']}")
        print("="*60)

        # Profile overview
        print("👤 PROFILE OVERVIEW:")
        print(f"   Full Name: {data['full_name']}")
        print(f"   Followers: {data['followers']:,}")
        print(f"   Following: {data['following']:,}")
        print(f"   Total Posts: {data['total_posts']:,}")
        print(f"   Verified: {'✓' if data['is_verified'] else '✗'}")
        print(f"   Private: {'Yes' if data['is_private'] else 'No'}")

        # Analytics summary
        if data['analytics_summary']:
            summary = data['analytics_summary']
            print(f"\n📈 ENGAGEMENT ANALYTICS ({summary['posts_analyzed_count']} recent posts):")
            print(f"   Total Likes: {summary['total_likes']:,}")
            print(f"   Total Comments: {summary['total_comments']:,}")
            print(f"   Avg Likes/Post: {summary['average_likes_per_post']:,.1f}")
            print(f"   Avg Comments/Post: {summary['average_comments_per_post']:,.1f}")
            print(f"   Engagement Rate: {summary['engagement_rate_percentage']:.2f}%")

        # Individual posts
        if data['posts_analyzed']:
            print("\n📱 RECENT POSTS BREAKDOWN:")
            for post in data['posts_analyzed']:
                print(f"\n   Post #{post['post_number']} ({post['date'][:10]})")
                print(f"   ❤️  Likes: {post['likes']:,}")
                print(f"   💬 Comments: {post['comments']:,}")
                print(f"   🎥 Type: {'Video' if post['is_video'] else 'Photo'}")
                if post['location']:
                    print(f"   📍 Location: {post['location']}")
                if post['caption']:
                    print(f"   📝 Caption: {post['caption'][:100]}...")
                print(f"   🔗 URL: {post['url']}")

        print(f"\n⏰ Data retrieved: {data['timestamp']}")
        print("="*60)

    def save_analytics_to_json(self, data, filename=None):
        """
        Save analytics data to a JSON file.

        Args:
            data (dict): Analytics data dictionary
            filename (str): Optional filename (default: username_analytics.json)
        """
        if not data:
            return

        if not filename:
            filename = f"{data['username']}_analytics.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"📄 Analytics data saved to: {filename}")

        except Exception as e:
            print(f"❌ Error saving analytics to file: {e}")

    def save_analytics_to_text(self, data, filename=None):
        """
        Save analytics data to a readable text file.

        Args:
            data (dict): Analytics data dictionary
            filename (str): Optional filename (default: username_analytics.txt)
        """
        if not data:
            return

        if not filename:
            filename = f"{data['username']}_analytics.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Instagram Analytics Report\n")
                f.write(f"Generated: {data['timestamp']}\n")
                f.write("="*50 + "\n\n")

                f.write(f"PROFILE: @{data['username']}\n")
                f.write(f"Full Name: {data['full_name']}\n")
                f.write(f"Followers: {data['followers']:,}\n")
                f.write(f"Following: {data['following']:,}\n")
                f.write(f"Total Posts: {data['total_posts']:,}\n")
                f.write(f"Verified: {'Yes' if data['is_verified'] else 'No'}\n")
                f.write(f"Private: {'Yes' if data['is_private'] else 'No'}\n\n")

                if data['analytics_summary']:
                    summary = data['analytics_summary']
                    f.write(f"ENGAGEMENT SUMMARY ({summary['posts_analyzed_count']} posts):\n")
                    f.write(f"Total Likes: {summary['total_likes']:,}\n")
                    f.write(f"Total Comments: {summary['total_comments']:,}\n")
                    f.write(f"Average Likes per Post: {summary['average_likes_per_post']:,.1f}\n")
                    f.write(f"Average Comments per Post: {summary['average_comments_per_post']:,.1f}\n")
                    f.write(f"Engagement Rate: {summary['engagement_rate_percentage']:.2f}%\n\n")

                if data['posts_analyzed']:
                    f.write("RECENT POSTS:\n")
                    for post in data['posts_analyzed']:
                        f.write(f"\nPost #{post['post_number']} - {post['date'][:10]}\n")
                        f.write(f"Likes: {post['likes']:,}\n")
                        f.write(f"Comments: {post['comments']:,}\n")
                        f.write(f"Type: {'Video' if post['is_video'] else 'Photo'}\n")
                        f.write(f"URL: {post['url']}\n")
                        if post['location']:
                            f.write(f"Location: {post['location']}\n")
                        if post['caption']:
                            f.write(f"Caption: {post['caption']}\n")

            print(f"📄 Analytics report saved to: {filename}")

        except Exception as e:
            print(f"❌ Error saving analytics report: {e}")


def main():
    """Main function for advanced Instagram analytics."""
    print("Advanced Instagram Analytics")
    print("="*40)
    print("Fetches profile data + likes/comments for recent posts")
    print("Note: Works best with public profiles\n")

    # Get username
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter Instagram username: ").strip()
        if not username:
            print("No username provided. Exiting.")
            sys.exit(1)

    # Get number of posts to analyze
    try:
        post_count = input("Number of recent posts to analyze (default: 3): ").strip()
        post_count = int(post_count) if post_count else 3
        if post_count < 1 or post_count > 10:
            print("Setting to 3 posts (valid range: 1-10)")
            post_count = 3
    except ValueError:
        print("Invalid input. Using default: 3 posts")
        post_count = 3

    # Remove @ if present
    username = username.lstrip('@')

    # Initialize advanced scraper
    scraper = AdvancedInstagramScraper()

    print(f"\n🔍 Analyzing @{username}...")
    print("This may take a moment as we fetch post data...\n")

    # Get analytics data
    analytics_data = scraper.get_post_analytics(username, post_count)

    if analytics_data:
        # Display analytics
        scraper.display_analytics(analytics_data)

        # Ask about saving data
        print("\n💾 Save options:")
        save_choice = input("Save data? (t=text, j=json, b=both, n=no): ").lower().strip()

        if save_choice in ['t', 'text', 'b', 'both']:
            scraper.save_analytics_to_text(analytics_data)

        if save_choice in ['j', 'json', 'b', 'both']:
            scraper.save_analytics_to_json(analytics_data)
    else:
        print("❌ Failed to retrieve analytics data.")
        print("\nPossible solutions:")
        print("- Verify the username is correct")
        print("- Try with a public account")
        print("- Check your internet connection")


if __name__ == "__main__":
    main()
