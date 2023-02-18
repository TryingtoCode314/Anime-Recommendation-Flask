from flask import Flask, render_template, jsonify, request
import model2
from model2 import recommendation_function, tuple_creator, anime_id_list_creator, user_rating_list_creator

app = Flask(__name__)


#@app.route('/')
#def hello():
   # return recommendation_function()


def my_function(input_data):
    # Do something with input_data
    anime_results = recommendation_function(input_data)
    return anime_results

@app.route("/")
def index():
    return render_template("index.html")



@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        #result = my_function(user_input)
        result = request.form["Anime_ID List"]
        result2 = request.form["Anime Rating List"]
        result_modified = anime_id_list_creator(result)
        result2_modified = user_rating_list_creator(result2)
        anime_tuple = tuple_creator(result_modified, result2_modified)
        anime_results = recommendation_function(anime_tuple)
    return render_template("result.html", result = result, result2 = result2, anime_results=anime_results, result_modified = result_modified, result2_modified = result2_modified, anime_tuple = anime_tuple)


 
if __name__ == "__main__":
    app.run()
