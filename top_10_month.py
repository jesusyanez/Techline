import praw
import pandas as pd
import config
import time
import datetime
import csv

# connects to reddit praw object using the reddit application api client id and client secret
def reddit_object():

    reddit = praw.Reddit(client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent,
                        username = config.username,
                        password = config.password)

    return reddit

#Calls up to the last 12 submissions from technology
def scrape_submissions(reddit):
    sub_list = []
    # selects the subreddit technology.  This can be changed to any subreddit
    subreddit = reddit.subreddit('technology')
    # have it currently calling 15 submissions at a time, but can be any number between 1 and 1000
    for submission in subreddit.top('month', limit=15):
        # different submission attributes I choose to pull are below
        # look at the praw documentation for other submission attributes

        title = submission.title
        pk = submission.id
        direction = submission.url

        sub_list.append([pk, title, direction])
    df = pd.DataFrame(sub_list, columns=['id', 'title', 'direction'])
    # removes reddit links in direction column
    df = df[~df.direction.str.contains("reddit.com")]

    return df

#writes the first csv database file
def new_submissions(df):

    top10 = 'top10monthly.csv'

    # Creates new csv file
    with open(top10, 'w', newline='') as file:
        writer = csv.writer(file)
        #creates header columns
        writer.writerow(["", "id", "direction", "title"])
        writer.writerow(["", "", "", ""])


    # pulls full csv
    df_current = pd.read_csv('top10monthly.csv', index_col=0)

    # Checks for only the new rows in the df
    new_submission = df[~df['id'].isin(df_current['id'])]
    new_sub_list = new_submission.values.tolist()

    # Appends the new submissions to the current pandas df
    df_current = df_current.append(new_submission, sort=False)




    # saves new version of the csv
    df_current.to_csv('top10monthly.csv')



    return new_sub_list, new_submission, df_current






def main():
    reddit = reddit_object()
    df = scrape_submissions(reddit)
    new_sub_list, new_submission, df_current = new_submissions(df)
    print("new submissions: ", new_submission.shape)
    print("Current Dataframe: ", df_current.shape)


main()
