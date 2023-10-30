import os
from time import time, sleep
from tkinter import filedialog, messagebox
import imageio
import jieba
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from wordcloud import WordCloud, STOPWORDS
import threading

window = ttk.Window(title='词云生成器1.0', themename='sandstone', size=(800, 600), position=None, alpha=0.9,
                    resizable=(False, False))
window.place_window_center()
# 选择文件主区域
select_area = ttk.Frame(window, width=700, height=400, bootstyle='default')
select_area.pack_propagate(False)
select_area.pack()
# 文件选择区域
labF = ttk.Labelframe(select_area, text='选择文本文件', width=320,
                      height=400, borderwidth=10, bootstyle='secondary')
labF.pack_propagate(False)
labF.pack(side='left')

# 图片选择区域
labF1 = ttk.Labelframe(select_area, text='选择图片文件', width=320,
                       height=400, borderwidth=10, bootstyle='warning')
labF1.pack_propagate(False)
labF1.pack(side='right')
pgbar = ttk.Progressbar(select_area, length=400, maximum=100,
                        value=0, orient='vertical', bootstyle='success')
pgbar.pack()

file_path = ''  # 文件路径全局变量
imag_path = ''  # 图片路径全局变量
t = ''  # 保存的图片名称全局变量


def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path.endswith('.txt'):
        lab_tip = ttk.Label(labF, text=file_path)
        lab_tip.pack()
    else:
        messagebox.showwarning('注意', '您选择的不是文本文件')


def select_imag():
    global imag_path
    imag_path = filedialog.askopenfilename()
    if imag_path.endswith('.png'):
        lab_tip = ttk.Label(labF1, text=imag_path)
        lab_tip.pack()
    else:
        messagebox.showwarning('注意', '您选择的不是png格式的图片')


#   预览页图片全局变量
photo = ''
#   存储路径文件，用于修改存储路径
if os.path.exists('url.txt'):
    pass
else:
    with open('url.txt', 'w', encoding='utf-8') as f:
        f.write('D:/词云图')
#   读取存储路径文件作为变量
file = open('url.txt', 'r', encoding='utf-8')
urlR = file.read()
#   停用词变量
stopw = STOPWORDS


#   文件判断、词云生成、预览页展示
def wc():
    if file_path == '':
        messagebox.showwarning('注意', '没有选择文本文件')
    elif imag_path == '':
        messagebox.showwarning('注意', '没有选择图片文件')
    pgbar['value'] = 0
    pgbar.update()
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    txt = jieba.lcut(txt)
    newTxet = ''.join(txt)
    #   加载进度条，词云图生成期间会在控制台输出成功信息，会有几毫秒空白期，用进度条增加可视化体验
    for i in range(80):
        sleep(0.01)
        pgbar['value'] = i
        pgbar.update()
    wordcloud = WordCloud(font_path='myexe/方正粗黑宋简体.ttf',
                          width=2000,
                          height=1000,
                          background_color='white',
                          mask=imageio.v3.imread(imag_path),
                          stopwords=stopw
                          ).generate(newTxet)
    global t, urlR
    t = time()
    t = '{:.0f}'.format(t)
    #   词云图保存为文件
    wordcloud.to_file(f'{urlR}/{t}.png')

    #   图片生成后进度条拉满
    def progressbar():
        for j in range(80, 100):
            sleep(0.01)
            pgbar['value'] = j
            pgbar.update()

    pgbar['value'] = 0
    pgbar.configure(bootstyle='light')
    pgbar.update()

    t1 = threading.Thread(target=progressbar)
    t1.start()
    #   新窗口用来展示生成的词云图效果
    win = ttk.Toplevel(title='词云图预览', size=(1000, 500))
    win.position_center()
    lab_tip = ttk.Label(win, text=f'文件已经保存到{urlR}/{t}.png', font='宋体,32')
    lab_tip.pack()
    imag = Image.open(f'{urlR}/{t}.png')
    global photo
    photo = ImageTk.PhotoImage(image=imag)
    lab_img = ttk.Label(win, image=photo, justify='center')
    lab_img.pack()


# 文件选择按钮
button = ttk.Button(labF, text='+', bootstyle=(INFO, OUTLINE),
                    command=select_file, width=10)
button.pack(pady=150)
# 图片选择按钮
button1 = ttk.Button(labF1, text='+', bootstyle=(INFO, OUTLINE), command=select_imag, width=10)
button1.pack(pady=150)
#   生成执行按钮
bu_ok = ttk.Button(window, width=20, text='一键生成',
                   bootstyle=(SUCCESS, OUTLINE), command=wc)
bu_ok.pack(pady=50)


#   修改文件存储路径的函数
def add_path():
    with open('url.txt', 'w', encoding='utf-8') as fa:
        new_path = filedialog.askdirectory()
        fa.write(f'{new_path}')
        lab_url.config(text=urlR)


#   标签显示当前文件的存储路径
file_url = ttk.Frame(window)
file_url.pack(side='right', padx=20)
lab_url = ttk.Label(file_url, text=f'{urlR}')
lab_url.pack()
# 修改存储路径的按钮
bu_url = ttk.Button(file_url, text='修改存储路径', bootstyle='secondary-outline', command=add_path)
bu_url.pack()
#   作者信息
lab_who = ttk.Label(window, text='@By祥云万里凝')
lab_who.pack(side='left')

if __name__ == '__main__':
    window.mainloop()
    file.close()  # 文件在最后关闭，为了避免图片被回收而导致预览页不显示图片的问题
