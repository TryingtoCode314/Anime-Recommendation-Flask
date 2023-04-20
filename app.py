from flask import Flask, render_template, jsonify, request
import model2
import os, pandas as pd
from model2 import recommendation_function, tuple_creator, anime_id_list_creator, user_rating_list_creator
from ast import literal_eval as make_tuple
from Bing_our_lord_and_savior import Bingify
app = Flask(__name__)
path = os.path.join(os.getcwd(), 'anime_data')
df = pd.read_csv(os.path.join(path, 'anime.csv'))

#@app.route('/')
#def hello():
   # return recommendation_function()


def my_function(input_data):
    # Do something with input_data
    anime_results = recommendation_function(input_data)
    return anime_results

@app.route("/")
def home():
    df2 = df[['MAL_ID','Name']]
    return render_template("home.html", df2=df2)



@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        #result = my_function(user_input)
        #result = request.form["Anime_ID List"]
        #result2 = request.form["Anime Rating List"]
        #result_modified = anime_id_list_creator(result)
        #result2_modified = user_rating_list_creator(result2)
        #anime_tuple = tuple_creator(result_modified, result2_modified)
        result = request.form['anime-list-input']
        anime_tuple = make_tuple(result)
        
        print(anime_tuple)
        if type(anime_tuple[0]) == int:
            result_int, result2_int = anime_tuple
            result = [result_int]
            result2 = [result2_int]
        else:
            result, result2 = list(zip(*anime_tuple))
            
        anime_results = recommendation_function(zip(result, result2))
        anime_images = Bingify(anime_results["data"][0][0], anime_results["data"][1][0], anime_results["data"][2][0])
        
    return render_template("result.html", result = result, result2 = result2, anime_results=anime_results, anime_tuple = anime_tuple, anime_images = anime_images)


 
if __name__ == "__main__":
    app.run()
