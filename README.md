## Setup Guide

1 **Create a Virtual Environment**

    python -m venv myenv
   
2 **Install Dependencies**

    pip install -r requirements.txt

3 **Update Twitter Credentials in .env File**

TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password


4 **Update Twitter Usernames**
In the __main__.py file, update the list of default usernames to the Twitter accounts whose data you want to scrape:
# Default to the three specified usernames
default_usernames = ["ETMarkets", "Breakoutrade94", "Trading4Bucks"]


5 **Run the Script**

python __main__.py


**Access Scraped Tweets**

Scraped tweets will be saved to the tweets folder in real-time.








