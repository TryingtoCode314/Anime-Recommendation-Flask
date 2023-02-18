import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import Dataset
from surprise import Reader
import tqdm
import time

def merge_user_data(tuple_list, training_set, all_data):
    '''
    tuple_list follows the form [(anime_id, rating), (anime_id, rating)...]
    all_data is the entire dataset
    '''
    anime_ids = [i for i, r in tuple_list]
    is_anime_inList = all([i in training_set['anime_id'].unique() for i in anime_ids])
    if is_anime_inList:
        tups = [(all_data['user_id'].max() + 1, item, rating) for item, rating in tuple_list]
        tups = pd.DataFrame(data=tups, columns=['user_id','anime_id','rating'])
        return pd.concat([training_set, tups])
    else:
        print('anime_id not found in database')

path = os.path.join(os.getcwd(), 'anime_data')
anime_rec = pd.read_csv(os.path.join(path, 'anime_rec.csv'))
rating = pd.read_csv(os.path.join(path, 'rating.csv'))
anime_rec_2 = anime_rec[['anime_id','name']]
rating_withnames = pd.merge(rating, anime_rec_2, on = 'anime_id')
all_data = rating_withnames[rating_withnames['rating'] != -1]
#shuffle dataset adjust frac=0.1 for 10% of dataset,0.5 for 50%, 1 for 100% etc.
final_data = all_data.sample(frac=0.001).reset_index(drop=True) 
final_data =final_data.drop('name', axis=1)

reader = Reader(rating_scale=(1, 10))

from surprise import SVD
algo = SVD()

#put your ratings here: the first number is the anime id, the second is the rating
#your_ratings = [(1, 7),(5, 2)]
anime_names_list = 19,57,64
new_user_rating_list = 7,2,3
your_ratings = list(zip(anime_names_list, new_user_rating_list))
#your_ratings = list(tuple(map(int,input().split())) for r in range(2))#range(int(input('Enter # of animes : ')))) 


merged_data = merge_user_data(your_ratings, final_data, all_data)

data = Dataset.load_from_df(merged_data, reader)
train = data.build_full_trainset()

#change the 1 to any anime id for it to generate a rating prediction
algo.fit(train)

iid = list(set(final_data['anime_id']))
uid = [all_data['user_id'].max() + 1] * len(iid)
filler_rating = [-1000] * len(iid)
data = list(zip(uid, iid, filler_rating))

predictions = algo.test(data)
a = pd.DataFrame(predictions)

#print(a.nlargest(3, 'est'))

new_data = pd.merge(a.nlargest(3, 'est'), anime_rec_2, left_on=['iid'], right_on=['anime_id'])
new_data = new_data[['name', 'anime_id', 'est']]
new_data = new_data.to_dict("tight")
new_data = {k: new_data[k] for k in ('index', 'data')}
def recommendation_function(your_ratings):
    return (new_data)

#print(new_data)

def tuple_creator(anime_names_list, new_user_rating_list):
    #anime_names_list = list(map(float, anime_names_list.split(',')))
    #new_user_rating_list = list(map(float, new_user_rating_list.split(',')))
    anime_tuple = list(zip(anime_names_list, new_user_rating_list))
    return (anime_tuple)

def anime_id_list_creator(anime_names_list):
# input comma separated elements as string 
    anime_names_list=str(anime_names_list)
    list = anime_names_list.split(",")
    list[0] = list[0].replace("(","")
    list[-1] = list[-1].replace(")","")
    li = []
    for i in list:
        li.append(int(i))
    return li


def user_rating_list_creator(new_user_rating_list):
# input comma separated elements as string 
    new_user_rating_list=str(new_user_rating_list)
    list = new_user_rating_list.split(",")
    list[0] = list[0].replace("(","")
    list[-1] = list[-1].replace(")","")
    li = []
    for i in list:
        li.append(int(i))
    return li

#print(user_rating_list_creator(new_user_rating_list))
#print(tuple_creator(anime_names_list, new_user_rating_list))
print(recommendation_function(your_ratings))