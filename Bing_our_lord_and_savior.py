from bing_image_urls import bing_image_urls

a=1
b=2
c=3

def Bingify(anime_one, anime_two, anime_three):
    url = bing_image_urls(anime_one, limit=1)[0]
    url2 = bing_image_urls(anime_two, limit=1)[0]
    url3 = bing_image_urls(anime_three, limit=1)[0]

    url_list = [url, url2, url3]

    return url_list

#print(Bingify(a,b,c)[2])