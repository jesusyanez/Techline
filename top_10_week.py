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




#takes top 10 data and appends list into html file
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
    alink6 = df_current1.iloc[6, 1]
    akit6 = df_current1.iloc[6, 2]
    alink7 = df_current1.iloc[7, 1]
    akit7 = df_current1.iloc[7, 2]
    alink8 = df_current1.iloc[8, 1]
    akit8 = df_current1.iloc[8, 2]
    alink9 = df_current1.iloc[9, 1]
    akit9 = df_current1.iloc[9, 2]
    alink10 = df_current1.iloc[10, 1]
    akit10 = df_current1.iloc[10, 2]
    #close csv after we stored variables
    df_current1.to_csv('top10weekly.csv')
    #open up csv for month data
    df_current1 = pd.read_csv('top10monthly.csv', index_col=0)
    #store variables again from csv df
    blink1 = df_current1.iloc[1, 1]
    bkit1 = df_current1.iloc[1, 2]
    blink2 = df_current1.iloc[2, 1]
    bkit2 = df_current1.iloc[2, 2]
    blink3 = df_current1.iloc[3, 1]
    bkit3 = df_current1.iloc[3, 2]
    blink4 = df_current1.iloc[4, 1]
    bkit4 = df_current1.iloc[4, 2]
    blink5 = df_current1.iloc[5, 1]
    bkit5 = df_current1.iloc[5, 2]
    blink6 = df_current1.iloc[6, 1]
    bkit6 = df_current1.iloc[6, 2]
    blink7 = df_current1.iloc[7, 1]
    bkit7 = df_current1.iloc[7, 2]
    blink8 = df_current1.iloc[8, 1]
    bkit8 = df_current1.iloc[8, 2]
    blink9 = df_current1.iloc[9, 1]
    bkit9 = df_current1.iloc[9, 2]
    blink10 = df_current1.iloc[10, 1]
    bkit10 = df_current1.iloc[10, 2]
    #close csv
    df_current1.to_csv('top10monthly.csv')
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
      'link6':alink6,
      'kit6': akit6,
      'link7': alink7,
      'kit7': akit7,
      'link8': alink8,
      'kit8': akit8,
      'link9': alink9,
      'kit9': akit9,
      'link10': alink10,
      'kit10': akit10,

      'link11': blink1,
      'kit11': bkit1,
      'link12': blink2,
      'kit12': bkit2,
      'link13': blink3,
      'kit13': bkit3,
      'link14': blink4,
      'kit14': bkit4,
      'link15': blink5,
      'kit15': bkit5,
      'link16':blink6,
      'kit16': bkit6,
      'link17': blink7,
      'kit17': bkit7,
      'link18': blink8,
      'kit18': bkit8,
      'link19': blink9,
      'kit19': bkit9,
      'link20': blink10,
      'kit20': bkit10,

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

      <title>TechLine - Breaking Tech News</title>
      <link rel="shortcut icon" href="favicons.ico" />

      <!-- Bootstrap core CSS -->
      <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
      <link href="custom.css" rel="stylesheet">
      <!-- Global site tag (gtag.js) - Google Analytics -->
      <script async src="https://www.googletagmanager.com/gtag/js?id=UA-145008938-2"></script>
      <script>
         window.dataLayer = window.dataLayer || [];
         function gtag(){{dataLayer.push(arguments);}}
         gtag('js', new Date());

         gtag('config', 'UA-145008938-2');
      </script>


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
            <h1>Breaking News</h1>

            <div class="embed-responsive embed-responsive-1by1">

            <iframe class="embed-responsive-item" style="border-style: none;" src="http://localhost:8000/" height="1000" width="800" ></iframe>
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
              <li>
                <a href="{link6}" target="_blank">{kit6}</a>
              </li>
              <li>
                <a href="{link7}" target="_blank">{kit7}</a>
              </li>
              <li>
                <a href="{link8}" target="_blank">{kit8}</a>
              </li>
              <li>
                <a href="{link9}" target="_blank">{kit9}</a>
              </li>
              <li>
                <a href="{link10}" target="_blank">{kit10}</a>
              </li>
            </ol>

            <br/>
            <br>
            <h2>
              <u>Major This Month</u>
            </h2>
            <ol class="text-left">
              <li>
                <a href="{link11}" target="_blank">{kit11}</a>
              </li>
              <li>
                <a href="{link12}" target="_blank">{kit12}</a>
              </li>
              <li>
                <a href="{link13}" target="_blank">{kit13}</a>
              </li>
              <li>
                <a href="{link14}" target="_blank">{kit14}</a>
              </li>
              <li>
                <a href="{link15}" target="_blank">{kit15}</a>
              </li>
              <li>
                <a href="{link16}" target="_blank">{kit16}</a>
              </li>
              <li>
                <a href="{link17}" target="_blank">{kit17}</a>
              </li>
              <li>
                <a href="{link18}" target="_blank">{kit18}</a>
              </li>
              <li>
                <a href="{link19}" target="_blank">{kit19}</a>
              </li>
              <li>
                <a href="{link20}" target="_blank">{kit20}</a>
              </li>

            </ol>
          </div>


          <div class="col-lg-12 text-center">


            <p class="lead">TechLine | Jesus R. Yanez</p>
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
