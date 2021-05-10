import tkinter as tk
import tkinter.ttk as ttk
import feedparser
import webbrowser
import csv

def main():
    #ウィンドウ作成
    root = tk.Tk()
    root.title("tk_RSSreader")
    root.geometry("1200x600")

    #ノートブック作成
    nb=ttk.Notebook()
    nb.pack(fill='both',expand=1)

    #ホームタブ作成
    tab = tk.Frame(nb)
    nb.add(tab,text="ホーム", padding=3)
    
    #ホームタブ用フレーム
    frm=ttk.Frame(tab)
    frm.grid()

    #説明
    label = tk.Label(frm, text="RSS/RDFのURLを入力(本ソフト再起動後に反映されます)")
    label.grid(column=0,row=0)

    #RSS/RDFのURL入力用ボックス
    txtbox = tk.Entry(frm,width=100)
    txtbox.grid(column=0,row=1)

    #CSV書き込み用ボタン
    btn = tk.Button(frm, text='登録',command=lambda: csvwrite(txtbox.get()))
    btn.grid(column=1,row=1)
    
    #CSVファイル読み込み・ニュースタブ作成
    with open('csv/index.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            tab = tk.Frame(nb)
            nb.add(tab,text=row[1], padding=3)
            newstab(row, tab)

    root.mainloop()
    return 0

def csvwrite(rss_url): #入力されたURLをCSVに書き込み
    rss_dic = feedparser.parse(rss_url)
    tabtitle = rss_dic.feed.title #RSSの見出し
    tabtitle = ''.join(tabtitle.split()) #見出しの空白文字を削除
    with open('csv/index.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([rss_url, tabtitle])
    return 0

def newstab(row, tab): #RSSからニュース情報取得
    rss_url = row[0] #任意のRSS/RDF
    rss_dic = feedparser.parse(rss_url)
    newstxt = []
    newslink = []
    for entry in rss_dic.entries:
        title = entry.title
        link = entry.link
        newstxt.append(title)
        newslink.append(link)

    #ニュースのソース媒体名を表示
    news_source = ttk.Label(tab, text=rss_dic.feed.title + "からのニュース")
    news_source.grid(column=0, row=0)

    #リストボックス作成・設置
    txt = tk.StringVar(value=newstxt)
    lb = tk.Listbox(tab, listvariable=txt, height=48, width=192, selectmode="single")
    lb.grid(column=0, row=1)

    #選択したタイトルの記事をブラウザで開く
    def webopen(event):
        for i in lb.curselection():
            webbrowser.open(newslink[i])

    #リストボックスの中身を選択したらイベント実行
    lb.bind("<<ListboxSelect>>", webopen) 
    return 0

if __name__ == "__main__":
    main()