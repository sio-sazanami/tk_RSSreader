import tkinter as tk
from tkinter import ttk
import feedparser
import webbrowser

#RSSからニュース情報取得
rss_url = "https://kahoku.news/rss/general/%E5%AE%AE%E5%9F%8E" #任意のRSS/RDF
rss_dic = feedparser.parse(rss_url)
newstxt = []
newslink = []
for entry in rss_dic.entries:
    title = entry.title
    link = entry.link
    newstxt.append(title)
    newslink.append(link)

#ウィンドウ作成
root = tk.Tk()
root.title("今日のニュース")

#リストボックス収納用フレーム作成
frame = tk.Frame()
frame.grid(row=0)

#ニュースのソース媒体名を表示
news_source = ttk.Label(frame, text=rss_dic.feed.title + "からのニュース")
news_source.grid(column=0, row=0)

#リストボックス作成・設置
txt = tk.StringVar(value=newstxt)
lb = tk.Listbox(frame, listvariable=txt, height=16, width=55, selectmode="single",)
lb.grid(column=0, row=1)

#選択したタイトルの記事をブラウザで開く
def webopen(event):
    for i in lb.curselection():
        webbrowser.open(newslink[i])

#リストボックスの中身を選択したらイベント実行
lb.bind("<<ListboxSelect>>", webopen) 

root.mainloop()