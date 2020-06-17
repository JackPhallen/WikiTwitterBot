import os
import sys
import smtplib
import time
from BotConfig import BotConfig

class TwitterBot:

    def __init__(self, config_file):
        # Set bot configurations
        self.config = BotConfig(config_file)

    def connect(self):
        '''
        Establish connections with SMTP server
        '''
        smtp_connection = smtplib.SMTP(self.config.emailserver, self.config.emailserverport)
        smtp_connection.starttls()
        smtp_connection.login(self.config.email, self.config.emailpassword)
        self.connection = smtp_connection

    def disconnect(self):
        '''
        End connection with SMTP server
        '''
        self.connection.quit()

    def send_tweet(self, body, subject, debug = False):
        '''
        Sends tweet
        :param body: Tweet text
        :param subject: trigger set in IFTTT (default #sendTweet)
        :return:
        '''
        tweet_string = self.config.tweetformat
        message = tweet_string.format(subject, body)
        if not debug:
            self.connect()
            self.connection.sendmail(self.config.email, self.config.triggeremail, message)
            print("\nSuccessfully Tweeted\n----------------\n{}\n----------------\n".format(body))
            self.disconnect()
        else:
            print("Debug:\n" + message)

    def get_tweets(self):
        tweet_list = []
        for key, getter in self.config.modules.items():
            fetched_tweets = getter()
            #Add if not empty
            if fetched_tweets:
                tweet_list.extend(fetched_tweets)
        return tweet_list

    def run(self):
        '''
        Loops through each tweet continuously unless loop is False
        :param tweets: list of tweets
        :param loop: continue after finishing list
        :return:
        '''
        trigger = self.config.triggerhashtag
        pause = int(self.config.freqmins) * 60
        loop = self.config.loop == "True"
        debug = self.config.debug == "True"
        if debug:
            print("Running in debug!")

        # Loops through tweets indefinitely unless loop is False
        while loop:
            tweets = self.get_tweets()
            # If empty list, continue
            if not tweets:
                continue
            for tweet in tweets:
                # If None, don't tweet
                if tweet:
                    try:
                        self.send_tweet(tweet, trigger, debug)
                    except Exception as ex:
                        print("Error Sending Tweet: {}".format(ex))
                        continue
                    time.sleep(pause)
                else:
                    print("Error: Module returned empty tweet")



if __name__ == "__main__":
    BASE = os.path.dirname(os.path.realpath(sys.argv[0]))
    RESOURCES = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "resources/")
    PROPS = os.path.join(RESOURCES, "properties.ini")

    props_path = os.path.join(BASE, PROPS)
    bot = TwitterBot(props_path)
    bot.run()
