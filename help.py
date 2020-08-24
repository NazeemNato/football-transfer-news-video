import moviepy.editor as mpe
import requests
from help import *
from variables import *

def imageToVideo(image,sound):
    voice = mpe.AudioFileClip(sound)
    img = mpe.ImageClip(image).set_duration(voice.duration)
    reimg = img.resize(SIZE)
    finalClip = reimg.set_audio(voice)
    return finalClip

def downloadImage(url,i):
    f = open(PHOTO_NAME.format(i),'wb')
    f.write(requests.get(url).content)
    f.close