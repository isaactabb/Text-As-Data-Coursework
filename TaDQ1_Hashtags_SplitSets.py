# Note: While splitting the set, the datasets contain three sets of labels
#       Team, Date, and Follower. In the end, I decided to use the Team label.
#       You will see in the following code that I also extracted the other labels
#       as well though.

# TaD Pre-Processing
import pandas as pd
import string
import random

# read the file
nba_tweets = pd.read_csv("NBATweets_processed.csv")

# for each index in the data frame
for index in nba_tweets.index:
    # hashtag status holds if it is part of hashtag
    hashtag_status = False
    # will hold final text
    no_hashtag_text = ''
    # for each character in each text
    for c in nba_tweets['text'][index]:
        # if character is hashtag, will start hashtag chain
        if c == '#':
            hashtag_status = True
        # hashtag chain ends at space or punctuation
        elif c == ' ' or (c in string.punctuation):
            hashtag_status = False

        # if not part of a hashtag, added to final text
        if hashtag_status == False:
            no_hashtag_text += c

    # reset tweet at index to updated text with no hashtags
    nba_tweets.at[index, 'text'] = no_hashtag_text

# the following lists will hold the text and labels for each subset
# training, validation, test
train_text = []
train_team = []
train_date = []
train_follower = []
valid_text = []
valid_team = []
valid_date = []
valid_follower = []
test_text = []
test_team = []
test_date = []
test_follower = []
train_set_count = 0
valid_set_count = 0
test_set_count = 0

# iterates through the nba tweets
for i in nba_tweets.index:
    # sets random seed
    random.seed()
    # random index
    index = random.randint(0, len(nba_tweets)-1)
    # if the training set is not full yet (6000 is 60% of 10000)
    if train_set_count < 6000:
        # add the tweet text, team, date, and follower at random index to lists
        train_text.append(nba_tweets.at[index, 'text'])
        train_team.append(nba_tweets.at[index, 'team'])
        train_date.append(nba_tweets.at[index, 'date_label'])
        train_follower.append(nba_tweets.at[index, 'follower_label'])
        # drop that index from the nba tweets dataframe
        nba_tweets = nba_tweets.drop(index)
        # increment count
        train_set_count += 1
    # the following conditionals are same as last but for validation/test sets
    elif valid_set_count < 2000:
        valid_text.append(nba_tweets.at[index, 'text'])
        valid_team.append(nba_tweets.at[index, 'team'])
        valid_date.append(nba_tweets.at[index, 'date_label'])
        valid_follower.append(nba_tweets.at[index, 'follower_label'])
        nba_tweets = nba_tweets.drop(index)
        valid_set_count +=1
    elif test_set_count < 2000:
        test_text.append(nba_tweets.at[index, 'text'])
        test_team.append(nba_tweets.at[index, 'team'])
        test_date.append(nba_tweets.at[index, 'date_label'])
        test_follower.append(nba_tweets.at[index, 'follower_label'])
        nba_tweets = nba_tweets.drop(index)
        test_set_count +=1

    # reset the index after each iteration
    nba_tweets = nba_tweets.reset_index(drop=True)

# create set data frames and write to csvs
train_dct = {
    'text': train_text,
    'team': train_team,
    'date_label': train_date,
    'follower_label': train_follower
} 
training_set = pd.DataFrame(train_dct)
training_set.to_csv("training_set.csv")
    
valid_dct = {
    'text': valid_text,
    'team': valid_team,
    'date_label': valid_date,
    'follower_label': valid_follower
} 
valid_set = pd.DataFrame(valid_dct)
valid_set.to_csv("validation_set.csv")

test_dct = {
    'text': test_text,
    'team': test_team,
    'date_label': test_date,
    'follower_label': test_follower
} 
test_set = pd.DataFrame(test_dct)
test_set.to_csv("test_set.csv")