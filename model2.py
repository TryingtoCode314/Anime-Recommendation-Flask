import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import Dataset, Reader
import time
from surprise.prediction_algorithms import SVD
from Functions import SVD_Predict


path = os.path.join(os.getcwd(), 'anime_data')
anime_rec = pd.read_csv(os.path.join(path, 'anime_rec.csv'))
rating = pd.read_csv(os.path.join(path, 'rating.csv'))
anime_rec_2 = anime_rec[['anime_id','name']]
rating_withnames = pd.merge(rating, anime_rec_2, on = 'anime_id')
all_data = rating_withnames[rating_withnames['rating'] != -1]
#shuffle dataset adjust frac=0.1 for 10% of dataset,0.5 for 50%, 1 for 100% etc.
final_data = all_data.sample(frac=0.001).reset_index(drop=True) 
final_data = final_data.drop('name', axis=1)

reader = Reader(rating_scale=(1, 10))
from surprise.model_selection import train_test_split
data = Dataset.load_from_df(final_data, reader)
#train, test = train_test_split(data)
train = data.build_full_trainset()


#Where the actual code starts

algo = SVD()
algo.fit(train)


#anime_names_list = 19,57,64
#new_user_rating_list = 7,2,3
#your_ratings = list(zip(anime_names_list, new_user_rating_list))



def recommendation_function(your_ratings):
    predictions = SVD_Predict(algo, your_ratings)
    df = pd.DataFrame(predictions, columns=['anime_id', 'rating'])
    new_data = pd.merge(df.nlargest(3, 'rating'), anime_rec_2, left_on=['anime_id'], right_on=['anime_id'])
    new_data = new_data[['name', 'anime_id', 'rating']]
    new_data = new_data.to_dict("tight")
    new_data = {k: new_data[k] for k in ('index', 'data')}
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
#print(recommendation_function(your_ratings))