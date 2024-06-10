import os
import sys
import argparse
import getpass
import json  # Import json module
from twitter_scraper import Twitter_Scraper
import selenium

# Load environment variables if .env file is present
try:
    from dotenv import load_dotenv
    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)

def main():
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from Twitter without using Twitter's API.",
        )

        # Adding arguments for mail, username, password, and number of tweets
        parser.add_argument(
            "--mail",
            type=str,
            default=os.getenv("TWITTER_MAIL"),
            help="Your Twitter mail.",
        )

        parser.add_argument(
            "--user",
            type=str,
            default=os.getenv("TWITTER_USERNAME"),
            help="Your Twitter username.",
        )

        parser.add_argument(
            "--password",
            type=str,
            default=os.getenv("TWITTER_PASSWORD"),
            help="Your Twitter password.",
        )

        parser.add_argument(
            "-t",
            "--tweets",
            type=int,
            default=10,
            help="Number of tweets to scrape (default: 10)",  # Changed default to 10
        )

        parser.add_argument(
            "-u",
            "--username",
            type=str,
            nargs='+',  # Allow multiple usernames
            default=["ETMarkets", "Breakoutrade94", "Trading4Bucks"],  # Default to the three specified usernames
            help="Twitter username(s). Scrape tweets from user profiles.",
        )

        parser.add_argument(
            "-ht",
            "--hashtag",
            type=str,
            default=None,
            help="Twitter hashtag. Scrape tweets from a hashtag.",
        )

        parser.add_argument(
            "-ntl",
            "--no_tweets_limit",
            nargs='?',
            default=False,
            help="Set no limit to the number of tweets to scrape (will scrape until no more tweets are available).",
        )

        parser.add_argument(
            "-q",
            "--query",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-a",
            "--add",
            type=str,
            default="",
            help="Additional data to scrape and save in the .csv file.",
        )

        parser.add_argument(
            "--latest",
            action="store_true",
            help="Scrape latest tweets",
        )

        parser.add_argument(
            "--top",
            action="store_true",
            help="Scrape top tweets",
        )

        args = parser.parse_args()

        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PASSWORD = args.password

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        print()

        additional_data = args.add.split(",")

        if (args.username is not None) + (args.hashtag is not None) + (args.query is not None) > 1:
            print("Please specify only one of --username, --hashtag, or --query.")
            sys.exit(1)

        if args.latest and args.top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(
                mail=USER_MAIL,
                username=USER_UNAME,
                password=USER_PASSWORD,
            )
            scraper.login()

            if args.username is not None:
                for username in args.username:
                    scraper.scrape_tweets(
                        max_tweets=args.tweets,
                        no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                        scrape_username=username,
                        scrape_hashtag=args.hashtag,
                        scrape_query=args.query,
                        scrape_latest=args.latest,
                        scrape_top=args.top,
                        scrape_poster_details="pd" in additional_data,
                    )
                    scraper.save_to_csv()
                    scraper.save_to_json()  # Save to JSON file
            else:
                scraper.scrape_tweets(
                    max_tweets=args.tweets,
                    no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                    scrape_username=args.username,
                    scrape_hashtag=args.hashtag,
                    scrape_query=args.query,
                    scrape_latest=args.latest,
                    scrape_top=args.top,
                    scrape_poster_details="pd" in additional_data,
                )
                scraper.save_to_csv()
                scraper.save_to_json()  # Save to JSON file

            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print(
                "Missing Twitter username or password environment variables. Please check your .env file."
            )
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    sys.exit(1)

if __name__ == "__main__":
    main()
