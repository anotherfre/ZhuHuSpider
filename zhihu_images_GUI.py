# -*- coding: utf-8 -*-
from tkinter import *
import threading
from tkinter.filedialog import askdirectory
from zhihu_images import *


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


class App:
    def __init__(self):
        root = Tk()
        root.title("知乎图片下载")
        self.path = StringVar()
        self._flag = threading.Event()
        self._flag.clear()
        self.url = StringVar()

        _label = Label(root, text='路径:').grid(row=0, column=0)
        _entry = Entry(root, textvariable=self.path).grid(row=0, column=1)
        self._button_choose = Button(root, text='选择路径', command=self.select_path).grid(row=0, column=2)
        _label_image = Label(root, text=' 图片链接：').grid(row=1, column=0)
        self._entry_image = Entry(root, textvariable=self.url).grid(row=1, column=1)
        self._button_start = Button(root, text='开始下载', command=lambda: thread_it(self.start_app)).grid(row=1, column=2)

        self.display_text = Text(root, width=40, height=10)
        self.display_text.grid(row=2, columnspan=3)
        self.display_text.config(state=DISABLED)
        root.mainloop()

    def select_path(self):
        """
        选择程序路径
        :return:
        """
        _path = askdirectory()
        self.path.set(_path)

    def start_app(self):
        if not self.url.get() or not self.path.get():
            self.display_text.config(state=NORMAL)
            self.display_text.insert("insert", "图片链接或者选择路径为空 \n")
            self.display_text.config(state=DISABLED)

        else:
            self.display_text.config(state=NORMAL)
            self.display_text.insert("insert", "正在获取... \n")
            self.display_text.config(state=DISABLED)
            _spider = ZhiHuSpider(self.url.get(), self.path.get())
            images = _spider.get_cont()
            clear_items = _spider.clear_cont(images)
            result = _spider.download_cont(clear_items)
            if result == "success":
                self.display_text.config(state=NORMAL)
                self.display_text.insert("insert", "完成！！！ \n")
                self.display_text.config(state=DISABLED)


if __name__ == '__main__':
    """
    pyinstaller 打包指令
    pyinstaller -D -w -F zhihu_images_GUI.py --hidden-import zhihu_images --name=ZhuHuSpider
    """
    app = App()
