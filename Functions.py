import pandas as pd 
import os 
import numpy as np
def merge_user_data(tuple_list, training_set, all_data):
    anime_ids = [i for i, r in tuple_list]
    is_anime_inList = all([i in training_set['anime_id'].unique() for i in anime_ids])
    if is_anime_inList:
        tups = [(all_data['user_id'].max() + 1, item, rating) for item, rating in tuple_list]
        tups = pd.DataFrame(data=tups, columns=['user_id','anime_id','rating'])
        return pd.concat([training_set, tups])
    else:
        print('anime_id not found in database')

def SVD_Predict(algo, user_input, epoch=20):
    pu = np.random.normal(algo.init_mean, algo.init_std_dev, algo.n_factors)
    bu = np.zeros(1)
    
    #SDG
    for current_epoch in range(epoch):
         for i, r in user_input:
            #convert iid to corresponding index of qi
            i = algo.trainset.to_inner_iid(i)

            # compute current error
            dot = 0  # <q_i, p_u>
            for f in range(algo.n_factors):
                dot += algo.qi[i, f] * pu[f]
            err = r - (algo.trainset.global_mean + bu + algo.bi[i] + dot)

            # update biases
            bu += algo.lr_bu * (err - algo.reg_bu * bu)
            

            # update factors
            for f in range(algo.n_factors):
                puf = pu[f]
                qif = algo.qi[i, f]
                pu[f] += algo.lr_pu * (err * qif - algo.reg_pu * puf)

    dots = np.dot(algo.qi, pu) 
    predictions = [(algo.trainset.to_raw_iid(i), float(algo.trainset.global_mean + bu + 
    algo.bi[i] + dots[i])) for i in algo.trainset.all_items()]

    


    return predictions


    
