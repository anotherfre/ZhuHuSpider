# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time
import traceback


class ZhiHuSpider:
    def __init__(self, original_url, path):
        self.header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, sdch, br',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'max-age=0', 'Host': 'www.zhihu.com', 'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'

                            }
        self.original_url = original_url
        self.path = path

        images = self.get_cont()
        clear_items = self.clear_cont(images)
        self.download_cont(clear_items)

    def download_cont(self, imgs):
        """
        下载内容
        :return:
        """

        is_exists = os.path.exists(self.path)
        if not is_exists:
            os.mkdir(self.path)
            print("创建文件夹路径 ", self.path)

        for index, img in enumerate(imgs):
            try:
                r = requests.get(img['src'])
                if r.status_code == 200:
                    get_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                    with open(r"{}\\".format(self.path) + get_time + "_" + str(index) + '.' +
                              img["src"].split("?")[0].split(".")[-1], 'wb')as file:
                        file.write(r.content)
                        print('保存照片第 ' + str(index) + ' 张成功')
            except:
                print(traceback.format_exc())

    def clear_cont(self, items):

        """
        清洗数据
        :return:
        """
        clear_items = []
        count = 0
        for item in items:
            if count % 2 != 1:
                clear_items.append(item)
            count = count + 1
        return clear_items

    def get_cont(self):
        """
        爬取内容
        :return:
        """

        resp = requests.get(self.original_url, headers=self.header_data)

        soup = BeautifulSoup(resp.text, features="html.parser")
        images = soup.select("div.QuestionAnswer-content img.origin_image")
        return images


if __name__ == '__main__':
    """
    img_url: 下载图片的问题链接
    path：下载保存的路径
    """

    img_url = "https://www.zhihu.com/question/282345576/answer/789784852"
    path = r'D:\zhihu_images'
    _spider = ZhiHuSpider(original_url=img_url, path=path)
