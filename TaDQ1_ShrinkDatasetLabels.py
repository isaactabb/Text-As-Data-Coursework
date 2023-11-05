# Note: While splitting the set, the datasets contain three sets of labels
#       Team, Date, and Follower. In the end, I decided to use the Team label.
#       You will see in the following code that I also extracted the other labels
#       as well though.

# TaD Pre-Processing
import pandas as pd
import string
import random

# read the file
dataset = pd.read_csv("NBATweets.csv")

# original length of dataset
print(len(dataset))

# filter out data to only the four teams that made the conference finals
dataset_teams = dataset[dataset.group_name.isin(['DenverNuggets', 'LosAngelesLakers', 
                                                 'MiamiHeat', 'BostonCeltics'])]

# change the date_range so it only ranges from the day of the first conference finals game
# until the day of the last finals game
date_range = (dataset_teams['created_at'] >= '2020-09-15 00:00') & (dataset_teams['created_at'] <= '2020-10-11 23:59')
dataset_teams2 = dataset_teams.loc[date_range]
# reset the index
dataset_teams2 = dataset_teams2.reset_index(drop=True)

texts = []
teams = []
dates = []
followers = []
# reduce to a random 10000 data points
for i in range(10000):
    random.seed()
    index = random.randint(0, len(dataset_teams2)-1)
    texts.append(dataset_teams2.at[index, 'text'])
    teams.append(dataset_teams2.at[index, 'group_name'])
    dates.append(dataset_teams2.at[index, 'created_at'])
    followers.append(dataset_teams2.at[index, 'followers'])
    dataset_teams2 = dataset_teams2.drop(index)
    dataset_teams2 = dataset_teams2.reset_index(drop=True)

# create the new dataframe
nba_tweets_dct = {
    'text': texts,
    'team': teams,
    'date': dates,
    'followers': followers
} 
nba_tweets = pd.DataFrame(nba_tweets_dct)

# function to create a date label based on which of three 9-day periods post is from
def date_label(row):
    if (row['date'] <= '2020-09-23 23:59'):
        return 'period1'
    elif (row['date'] > '2020-09-23 23:59') and (row['date'] <= '2020-10-02 23:59'):
        return 'period2'
    else:
        return 'period3'
    
# apply the date label to the dataframe
nba_tweets['date_label'] = nba_tweets.apply(lambda row: date_label(row), axis=1)

# function to create a follower label based on how many followers the account has
def follower_label(row):
    if (row['followers'] <= 100):
        return 'small'
    elif (row['followers'] > 100) and (row['followers'] <= 1000):
        return 'medium'
    else:
        return 'large'

# apply the follower label to data frame
nba_tweets['follower_label'] = nba_tweets.apply(lambda row: follower_label(row), axis=1)

# write the new data frame to a csv
nba_tweets.to_csv("NBATweets_processed.csv")
