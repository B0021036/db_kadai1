import string
import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
from turtle import width
import pymysql.cursors
from tkinter import scrolledtext
from multiprocessing import connection
from sqlite3 import connect

class Login():
    '''ログインを制御するクラス'''

    def __init__(self, master, main):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
            body:アプリ本体のクラスのインスタンス
        '''

        self.master = master

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()


    def create_widgets(self):
        '''ウィジェットを作成・配置する'''

        # ユーザー名入力用のウィジェット
        self.name_label = tk.Label(
            self.master,
            text="ユーザー名"
        )
        self.name_label.grid(
            row=0,
            column=0
        )
        self.widgets.append(self.name_label)

        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(
            row=0,
            column=1
        )
        self.widgets.append(self.name_entry)

        # パスワード入力用のウィジェット
        self.pass_label = tk.Label(
            self.master,
            text="パスワード"
        )
        self.pass_label.grid(
            row=1,
            column=0
        )
        self.widgets.append(self.pass_label)

        self.pass_entry = tk.Entry(
            self.master,
            show="*"
        )
        self.pass_entry.grid(
            row=1,
            column=1
        )
        self.widgets.append(self.pass_entry)

        # ログインボタン
        self.login_button = tk.Button(
            self.master,
            text="ログイン",
            command=self.login
        )
        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.login_button)

        # 登録ボタン
        self.register_button = tk.Button(
            self.master,
            text="登録",
            command=self.register
        )
        self.register_button.grid(
            row=3,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.register_button)

        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tk.CENTER)

    def login(self):
        '''ログインを実行する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        if self.check(username, password):
            # ログインユーザー名を設定
            self.login_name = username

            self.success()
        else:
            self.fail()

    def check(self, username, password):
        '''
            入力されたユーザー情報が登録済みか確認する
            username:ユーザー名
            password:パスワード
            返却値:True(登録済み),False（未登録）
        '''

        # DB接続
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='',
                                     db='apr01',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            connection.begin()

            with connection.cursor() as cursor:
                sql = 'select * from users where name = %s and pass = %s'

                cursor.execute(sql, (username, password))

                # 取得したユーザー情報をリスト化
                user_list = cursor.fetchall()

                # ユーザー情報の有無をチェック
                if user_list:
                    ret = True
                else:
                    ret = False

        #except Exception as e:
            #print('error:', e)
            #connection.rellback()
        finally:
            connection.close()


        # ユーザー情報が登録されているかどうかを返却
        return ret

    def save(self, username, password):
        '''
            入力されたユーザー情報を登録する
            username:ユーザー名
            password:パスワード
        '''

        # DB接続
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='',
                                     db='apr01',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            connection.begin()

            with connection.cursor() as cursor:

                # 取得した情報をDBに追記
                sql = "INSERT INTO users(name, pass) VALUE(%s, %s)"
                cursor.execute(sql, (username, password))

                # DBを保存
                connection.commit()

        # DB接続をクローズ
        except Exception as e:
            print('error:', e)
            connection.rellback()
        finally:
            connection.close()


    def register(self):
        '''ユーザー名とパスワードを登録する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        self.save(username, password)

    def fail(self):
        '''ログイン失敗時の処理を行う'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tk.Label(
            self.master,
            text="ログインできませんでした",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tk.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):
        '''ログイン画面を再表示する'''

        # "ログインできませんでした"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()

    def success(self):
        '''ログイン成功時の処理を実行する'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tk.Label(
            self.master,
            text="ログインに成功しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tk.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start)

    def main_start(self):
        '''アプリ本体を起動する'''

        # "ログインに成功しました"メッセージを削除
        self.message.destroy()

        # アプリ本体を起動
        self.main.start(self.master)
        
class MainAppli():
    '''アプリ本体'''

    def __init__(self, master):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
        '''

        self.master = master

        # ログイン完了していないのでウィジェットは作成しない

    def start(self, login_name):
        '''アプリを起動する'''

        # ログインユーザー名を表示する
        self.message = tk.Label(
            self.master,
            font=("",40),
            text=login_name + "でログイン中"
        )
        self.message.pack()

        # 必要に応じてウィジェット作成やイベントの設定なども行う
WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class YicDiary:
  def __init__(self, root):
    root.title('予定管理アプリ')
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)


  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.scrolledText = scrolledtext.ScrolledText(rightFrame, width=30, height=10)
    self.scrolledText.grid(column=0, row=10, columnspan=3, sticky=tk.W + tk.E, pady=50, padx=30)


    self.schedule()


  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    self.scrolledText.delete([1.0], tk.END)

    click_days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(click_days)
    # データベースに予定の問い合わせを行う

    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='apr01',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
      connection.begin()
      with connection.cursor() as cursor:
          sql = ' \
                SELECT kinds_name, memo, day FROM schedule \
                inner join calendar on schedule.schedule_id = calendar.schedule_id \
                inner join kinds on schedule.kinds_id = kinds.kinds_id  \
                where day = %s \
                order by schedule.kinds_id DESC; \
                '

          cursor.execute(sql, click_days)

          results = cursor.fetchall()

          for i, row in enumerate(results):
            string1 = row['kinds_name']
            string2 = row['memo']
            #string3 = string1 + ' ' + string2
            string3 = '[' + string1 + ']' + ' ' + string2
            print(string3)
            self.scrolledText.insert([1.0], string3)

          #connection.commit()

    except Exception as e:
      print('error', e)
    finally:
      connection.close()

  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # データベースに新規予定を挿入する
    # 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(days)
    
    # 種別
    kinds = self.combo.get()
    print(kinds)

    kinds_dict= {'学校':1, '試験':2, '課題':3, '行事':4, '就活':5, 'アルバイト':6, '旅行':7}
    kinds_no = kinds_dict[kinds]

     # 予定詳細
    memo = self.text.get("1.0", "end")
    print(memo)


    # 別表にしている人は、外部キーとして呼び出す値を得る
    #　getKey() メソッドは(または関数)は自作すること
    #foreignKey = getKey(kinds) 
  
    
    # データベースに接続
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='apr01',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        #トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:
          # SQLの作成・定義
          sql = "INSERT INTO calendar(day) VALUES(%s)"
          # SQLの実行
          cursor.execute(sql, (days,))

          # SQLの作成・定義
          sql = "SELECT MAX(schedule_id) FROM calendar"
          # SQLの実行
          cursor.execute(sql)

          # 実行結果の受け取り（複数行の場合）
          results = cursor.fetchone()

          MAXID = results['MAX(schedule_id)']

          # SQLの作成・定義
          sql = "INSERT INTO schedule(schedule_id, kinds_id, memo) VALUE(%s, %s, %s)"
          # SQLの実行
          cursor.execute(sql, (MAXID, kinds_no, memo))


          connection.commit()
        
    except Exception as e:
      print('error:', e)
      connection.rollback()
    finally:
      connection.close()


    # この行に制御が移った時点で、DBとの接続は切れている
    self.sub_win.destroy()


  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day

      self.schedule()


app = tk.Tk()

# メインウィンドウのサイズ設定
app.geometry("600x400")

# アプリ本体のインスタンス生成
main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
login = Login(app, main)

app.mainloop()
