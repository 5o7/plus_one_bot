# Import tools

import praw
import time

# Credentials and website access

creds = {"client_id": "xxxxxxxxxxxxxxxx",
         "client_secret": "xxxxxxxxxxxxxxxx",
         "password": "xxxxxxxxxxxxxxxx",
         "user_agent": "xxxxxxxxxxxxxxxx",
         "username": "xxxxxxxxxxxxxxxx"}

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

# a list of ways to comment "good rec"

good_recs = ["good rec", "great rec", "this is the one", "win", "solved"]
sub_name = "xxxxxxxxxxxxxxxx"

# The following code runs once every 15 minutes

while True:
         
    # Get the newest 50 submissions

    for submission in reddit.subreddit(sub_name).new(limit=50):
        submission.comments.replace_more(limit=None)

        # Only give out one point per submission

        comments = submission.comments.list()
        task_complete = False
        for comment in comments:
            try:
                if str(comment.author) == "xxxxxxxxxxxxxxxx":
                    task_complete = True
                    break
            except:
                pass

        # Scan second level comments for "good rec" or something similar

        if not task_complete:
            for top_level_comment in submission.comments:
                for second_level_comment in top_level_comment.replies:
                    if submission.author == second_level_comment.author:
                        for i in range(0, len(good_recs)):
                            if good_recs[i] in second_level_comment.body.lower():

                                # We have a winner. Top comment author's flair has 4 conditions
                                # Add one point to the the top level comment author

                                if top_level_comment.author_flair_text == None:
                                    reddit.subreddit(sub_name).flair.set(top_level_comment.author, "1")
                                elif top_level_comment.author_flair_text == "Quality Poster 👍":
                                    reddit.subreddit(sub_name).flair.set(top_level_comment.author, "Quality Poster 👍 1")
                                elif len(top_level_comment.author_flair_text) < 5:
                                    new_flair = str(int(top_level_comment.author_flair_text) + 1)
                                    reddit.subreddit(sub_name).flair.set(top_level_comment.author, new_flair)
                                else:
                                    new_flair = str(int(top_level_comment.author_flair_text[17:]) + 1)
                                    new_flair = "Quality Poster 👍 " + new_flair
                                    reddit.subreddit(sub_name).flair.set(top_level_comment.author, new_flair)

                                # Add a comment to mark the submission task complete

                                second_level_comment.reply("You've successfully awarded a user one 'good taste point'. Thanks for getting back with them!")


    # Take a nap

    time.sleep(900)



