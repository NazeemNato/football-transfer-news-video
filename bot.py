from help import *
import pyttsx3
import moviepy.editor as mpe
from bs4 import BeautifulSoup
import requests
from variables import *

print('---- bot started ----')
header ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
videos = []

tribal_article = []
tribal_img = []
url ='https://www.tribalfootball.com/transfers?page=1'
source = requests.get(url ,headers=header).text
soup = BeautifulSoup(source,'lxml')
find_container = soup.find('div',class_='switcher js-anchor list')
find_grid = find_container.find('div',class_='grid grid--narrow')
for news in find_grid.findAll('div',class_='grid__item palm-one-half desk-wide-one-third'):
    find_a = news.find('a',href=True)
    _url = 'https://www.tribalfootball.com'+find_a['href']
    _source = requests.get(_url ,headers=header).text
    _soup = BeautifulSoup(_source,'lxml')
    _find_container = _soup.find('section',class_='core__grid')
    _find_content = _find_container.find('article',class_='content')
    _find_img = _find_content.find('div',class_='article__hero')
    _imageTag = _find_img.find('img')
    _imageUrl = _imageTag['srcset']
    # hero image 
    if len(tribal_img) <= 20:
        tribal_img.append(_imageUrl)
    _ptags = []
    _find_art = _find_content.find('div',class_='articleBody')
    for para in _find_art.find_all('p'):
        if para.text != '':
            _ptags.append(para.text)
    article = ' '.join(_ptags)
    _ptags.clear()
    # articles
    if len(tribal_article) <= 20:
        tribal_article.append(article)
print('+ NEWS SCRAPPED SUCCESS')      
# append intro videos 
intro = mpe.VideoFileClip('assets/intro.mp4')
videos.append(intro)
print('+ INTRO VIDEO ADDED')      

for i in range(10):
    # image downloadinng
    downloadImage(tribal_img[i],i)
    # david voice
    engine = pyttsx3.init("sapi5")
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    # text to sound
    engine.save_to_file(tribal_article[i], SOUND_NAME.format(i))
    engine.runAndWait()
    # create video and save it in memory
    video_oo = imageToVideo(PHOTO_NAME.format(i),SOUND_NAME.format(i))
    videos.append(video_oo)

print('+ 10 VIDEOS ADDED')  
outro = mpe.VideoFileClip('assets/outro.mp4')
videos.append(outro)
print('+ OUTRO VIDEO ADDED')    

final_video = mpe.concatenate_videoclips(videos)
print('+ VIDEO CONCATENATED') 

final_video.write_videofile('result/final.mp4',fps=25)
print('+ FINISHED')