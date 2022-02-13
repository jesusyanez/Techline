import praw #reddit api library
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

#Calls up to the top 12 weekly submissions from r/technology
def scrape_submissions(reddit):
    sub_list = []
    # selects the subreddit technology.  This can be changed to any subreddit
    subreddit = reddit.subreddit('technology')
    # have it currently calling 15 submissions at a time, but can be any number between 1 and 1000
    for submission in subreddit.top('week', limit=15):
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

#writes dataframe(df) to csv file
def new_submissions(df):

    top10 = 'top10weekly.csv'

    # Creates new csv file
    with open(top10, 'w', newline='') as file:
        writer = csv.writer(file)
        #creates header columns
        writer.writerow(["", "id", "direction", "title"])
        writer.writerow(["", "", "", ""])



    # pulls full csv
    df_current = pd.read_csv('top10weekly.csv', index_col=0)

    # Checks for only the new rows in the df
    new_submission = df[~df['id'].isin(df_current['id'])]
    new_sub_list = new_submission.values.tolist()

    # Appends the new submissions to the current pandas df
    df_current = df_current.append(new_submission, sort=False)




    # saves new version of the csv
    df_current.to_csv('top10weekly.csv')



    return new_sub_list, new_submission, df_current




#takes top 5 data and appends list into html file
def to_html_list(df_current):
    #reads csv we just saved and stores as df
    df_current1 = pd.read_csv('top10weekly.csv', index_col=0)
    #create variable to store title and link for each row/article, later we will append these into html
    alink1 = df_current1.iloc[1, 1]
    akit1 = df_current1.iloc[1, 2]
    alink2 = df_current1.iloc[2, 1]
    akit2 = df_current1.iloc[2, 2]
    alink3 = df_current1.iloc[3, 1]
    akit3 = df_current1.iloc[3, 2]
    alink4 = df_current1.iloc[4, 1]
    akit4 = df_current1.iloc[4, 2]
    alink5 = df_current1.iloc[5, 1]
    akit5 = df_current1.iloc[5, 2]
    #close csv after we stored variables
    df_current1.to_csv('top10weekly.csv')

    #prepare to append/wrap variables to html
    kit_info = {
      'link1': alink1,
      'kit1': akit1,
      'link2': alink2,
      'kit2': akit2,
      'link3': alink3,
      'kit3': akit3,
      'link4': alink4,
      'kit4': akit4,
      'link5': alink5,
      'kit5': akit5,


    }

    #wrapper is the base html that will be unchanged and rewritten into html index
    wrapper ="""
    <!DOCTYPE html>
    <html lang="en">

    <head>

      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <meta name="description" content="">
      <meta name="author" content="">

      <title>TechLine</title>
      <link rel="shortcut icon" href="favicons.ico" />

      <!-- Bootstrap core CSS -->
      <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
      <link href="custom.css" rel="stylesheet">

    </head>

    <body>

      <!-- Navigation -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-company-black static-top">
        <div class="container">
          <a class="navbar-brand" href="#">
            <img src="techlinelogo1.png" alt="">
          </a>
        </div>
      </nav>

      <!-- Page Content -->
      <div class="container">
        <div class="row">
          <div class="col-md-9 text-center">
            <h1>Breaking Tech News</h1>

            <div class="embed-responsive embed-responsive-1by1">

            <iframe class="embed-responsive-item" style="border-style: none;" src="https://jesusyanez.github.io/Reddit-scraper-to-html-table/" height="1000" width="800" ></iframe>
			</div>
          </div>
          <div class="col-md-3 text-center">
          <br>
            <h2>
              <u>Weekly Scoop</u>
            </h2>
            <ol class="text-left">
              <li>
                <a href="{link1}" target="_blank">{kit1}</a>
              </li>
              <li>
                <a href="{link2}" target="_blank">{kit2}</a>
              </li>
              <li>
                <a href="{link3}" target="_blank">{kit3}</a>
              </li>
              <li>
                <a href="{link4}" target="_blank">{kit4}</a>
              </li>
              <li>
                <a href="{link5}" target="_blank">{kit5}</a>
              </li>
            </ol>

            <br/>


          </div>


          <div class="col-lg-12 text-center">


            <p class="lead">TechLine | Jesus Yanez</p>
            <ul class="list-unstyled">

            </ul>
          </div>
        </div>
      </div>

      <!-- Bootstrap core JavaScript -->
      <script src="vendor/jquery/jquery.slim.min.js"></script>
      <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    </body>

    </html>"""

    #creates new html text with stored variables
    new_html = wrapper.format(**kit_info)

    #opens/creates index file and writes it
    with open("index.html", "w", encoding='utf-8') as file:
        file.write(new_html)



    return df_current1

def main():
    reddit = reddit_object()
    df = scrape_submissions(reddit)
    new_sub_list, new_submission, df_current = new_submissions(df)
    df_current1 = to_html_list(df_current)
    print("new submissions: ", new_submission.shape)
    print("Current Dataframe: ", df_current.shape)


main()
