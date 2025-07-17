"""
Posts Analytics - Simplified Version

A cleaner version focused on getting likes and comments from recent posts.
"""

from instagram_scraper import InstagramFollowerScraper
import instaloader
import sys
from datetime import datetime

def get_basic_profile_data(profile):
    """Extract basic profile information."""
    return {
        'username': profile.username,
        'full_name': profile.full_name,
        'followers': profile.followers,
        'following': profile.followees,
        'total_posts': profile.mediacount,
        'is_private': profile.is_private,
        'is_verified': profile.is_verified,
        'timestamp': datetime.now().isoformat()
    }

def analyze_single_post(post, post_number):
    """Analyze a single Instagram post."""
    return {
        'post_number': post_number,
        'shortcode': post.shortcode,
        'url': f"https://www.instagram.com/p/{post.shortcode}/",
        'date': post.date.isoformat()[:10],  # Just the date part
        'likes': post.likes,
        'comments': post.comments,
        'is_video': post.is_video,
        'caption_preview': post.caption[:100] + "..." if post.caption and len(post.caption) > 100 else (post.caption or "")
    }

def calculate_engagement_stats(posts_data, followers):
    """Calculate engagement statistics."""
    if not posts_data:
        return {}

    total_likes = sum(post['likes'] for post in posts_data)
    total_comments = sum(post['comments'] for post in posts_data)
    post_count = len(posts_data)

    avg_likes = total_likes / post_count
    avg_comments = total_comments / post_count

    # Calculate engagement rate (likes + comments) / followers
    engagement_rate = 0
    if followers > 0:
        total_engagement = total_likes + total_comments
        engagement_rate = (total_engagement / post_count) / followers * 100

    return {
        'total_likes': total_likes,
        'total_comments': total_comments,
        'average_likes': round(avg_likes, 1),
        'average_comments': round(avg_comments, 1),
        'engagement_rate': round(engagement_rate, 2)
    }

def scrape_posts_analytics(username, num_posts=3):
    """
    Main function to scrape Instagram posts analytics.

    Args:
        username (str): Instagram username
        num_posts (int): Number of recent posts to analyze

    Returns:
        dict: Complete analytics data
    """
    try:
        # Initialize scraper
        scraper = InstagramFollowerScraper()
        loader = scraper.loader

        # Get profile
        print(f"📊 Getting profile data for @{username}...")
        profile = instaloader.Profile.from_username(loader.context, username)

        # Basic profile data
        profile_data = get_basic_profile_data(profile)

        if profile.is_private:
            print("⚠️  This is a private account. Post data may be limited.")
            return {**profile_data, 'posts': [], 'engagement_stats': {}}

        # Get recent posts
        print(f"📱 Analyzing {num_posts} recent posts...")
        posts = profile.get_posts()
        posts_data = []

        for i, post in enumerate(posts):
            if i >= num_posts:
                break

            print(f"  ⏳ Post {i+1}/{num_posts}...")
            post_data = analyze_single_post(post, i + 1)
            posts_data.append(post_data)

        # Calculate engagement statistics
        engagement_stats = calculate_engagement_stats(posts_data, profile.followers)

        return {
            **profile_data,
            'posts': posts_data,
            'engagement_stats': engagement_stats
        }

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"❌ Profile '{username}' not found")
        return None
    except instaloader.exceptions.LoginRequiredException:
        print("❌ Login required for this profile")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_results(data):
    """Display the analytics results in a clean format."""
    if not data:
        return

    print("\n" + "="*50)
    print(f"📊 ANALYTICS: @{data['username']}")
    print("="*50)

    # Profile info
    print(f"👤 {data['full_name']}")
    print(f"👥 Followers: {data['followers']:,}")
    print(f"📸 Total Posts: {data['total_posts']:,}")
    print(f"✅ Verified: {'Yes' if data['is_verified'] else 'No'}")

    # Engagement stats
    if data['engagement_stats']:
        stats = data['engagement_stats']
        print("\n📈 ENGAGEMENT STATS:")
        print(f"💝 Avg Likes: {stats['average_likes']:,}")
        print(f"💬 Avg Comments: {stats['average_comments']:,}")
        print(f"🎯 Engagement Rate: {stats['engagement_rate']}%")

    # Recent posts
    if data['posts']:
        print("\n📱 RECENT POSTS:")
        for post in data['posts']:
            print(f"\n  Post #{post['post_number']} ({post['date']})")
            print(f"  ❤️  {post['likes']:,} likes")
            print(f"  💬 {post['comments']:,} comments")
            print(f"  🎥 {'Video' if post['is_video'] else 'Photo'}")
            if post['caption_preview']:
                print(f"  📝 {post['caption_preview']}")

    print("\n" + "="*50)

def save_simple_report(data, filename=None):
    """Save a simple text report."""
    if not data:
        return

    if not filename:
        filename = f"{data['username']}_report.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Instagram Analytics Report\n")
            f.write(f"Profile: @{data['username']}\n")
            f.write(f"Generated: {data['timestamp']}\n\n")

            f.write("PROFILE SUMMARY:\n")
            f.write(f"Full Name: {data['full_name']}\n")
            f.write(f"Followers: {data['followers']:,}\n")
            f.write(f"Total Posts: {data['total_posts']:,}\n\n")

            if data['engagement_stats']:
                stats = data['engagement_stats']
                f.write("ENGAGEMENT STATS:\n")
                f.write(f"Average Likes: {stats['average_likes']:,}\n")
                f.write(f"Average Comments: {stats['average_comments']:,}\n")
                f.write(f"Engagement Rate: {stats['engagement_rate']}%\n\n")

            if data['posts']:
                f.write("RECENT POSTS:\n")
                for post in data['posts']:
                    f.write(f"\nPost #{post['post_number']} - {post['date']}\n")
                    f.write(f"Likes: {post['likes']:,}\n")
                    f.write(f"Comments: {post['comments']:,}\n")
                    f.write(f"URL: {post['url']}\n")

        print(f"💾 Report saved: {filename}")

    except Exception as e:
        print(f"❌ Error saving report: {e}")

def main():
    """Main function."""
    print("Instagram Posts Analytics")
    print("="*30)
    print("Get likes & comments for recent posts\n")

    # Get username
    if len(sys.argv) > 1:
        username = sys.argv[1].lstrip('@')
    else:
        username = input("Enter username: ").strip().lstrip('@')
        if not username:
            print("No username provided.")
            sys.exit(1)

    # Get number of posts
    try:
        num_posts = input("Posts to analyze (1-10, default 3): ").strip()
        num_posts = int(num_posts) if num_posts else 3
        num_posts = max(1, min(10, num_posts))  # Clamp between 1-10
    except ValueError:
        num_posts = 3

    # Scrape data
    print(f"\n🔍 Analyzing @{username}...")
    data = scrape_posts_analytics(username, num_posts)

    if data:
        display_results(data)

        # Save report
        save_choice = input("\nSave report? (y/n): ").lower().strip()
        if save_choice == 'y':
            save_simple_report(data)
    else:
        print("❌ Failed to get data. Try a different username.")

if __name__ == "__main__":
    main()
