# -*- coding:utf-8 -*-
# 作者：dong
# 时间：2021.11.15
from urllib import request

dic = {
    '玫瑰': 1,
    '蔷薇': 2, '海棠': 3, '蓝色妖姬': 4, '百合': 5, '郁金香': 6, '康乃馨': 7, '风信子': 8, '紫罗兰': 9, '勿忘我': 10, '四叶草': 11, '满天星': 12, '曼陀罗': 13,
    '鸢尾花': 14, '雏菊': 15, '水仙花': 16, '樱花': 17, '薰衣草': 18, '三色堇': 19, '茉莉花': 20, '睡莲': 21, '牵牛花': 22, '合欢花': 23, '海棠花': 24
}


i = 0
with open('./flower_url.txt', 'r', encoding='UTF-8-sig') as f:
    for readline in f.readlines():
        i = i + 1

        data = readline.split()

        flower_name = str(dic[data[0]])
        img_url = data[1]

        # 将远程图片下载到本地，第二个参数就是要保存到本地的文件名
        #print('D:/flower_data/' + flower_name + "/" + str(i) + ".jpg")
        request.urlretrieve(img_url, '../flower_data/' + flower_name + "/" + str(i) + ".jpg")
