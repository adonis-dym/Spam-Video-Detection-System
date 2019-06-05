import pandas as pd
import requests
from sklearn.utils import shuffle
from PIL import Image
import os
from tomorrow import threads
from io import BytesIO as Bytes2Data


width = 224
height = 224
# start=6400
# length = 50000
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
}

picdata = pd.read_csv('./test_info.csv')
# picdata = pd.read_csv('/project/jzhuang_03/yiming.dong/final_data.csv')
# picdata = shuffle(picdata)
for i in range(1000):
    id, loc, label = picdata.iloc[i]
    img_raw = requests.get(loc, headers=headers)
    img = Image.open(Bytes2Data(img_raw.content))
    img = img.resize((width, height), Image.ANTIALIAS)
    # if i < length * 0.8:
    #     kind = '/train/'
    # elif i < length * 0.9:
    #     kind = '/validation/'
    # else:
    #     kind = '/test/'
    # file_out = '/project/jzhuang_03/yiming.dong' + kind + str(id) + '_' + str(label) + '.jpg'
    file_out = './testset_pic/' + str(id) + '_' + str(label) + '.jpg'
    if len(img.split()) == 4:
        # prevent IOError: cannot write mode RGBA as BMP
        r, g, b, a = img.split()
        img = Image.merge("RGB", (r, g, b))
        img.save(file_out)
    else:
        img.save(file_out)

    if i % 100 == 0:
        print("Successfully crawled {} pictures".format(i))
