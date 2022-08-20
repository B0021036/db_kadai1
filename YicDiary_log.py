from multiprocessing import connection
from sqlite3 import connect
import pymysql.cursors
import tkinter as tk

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
        self.main.start(self.login_name)
        
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

app = tk.Tk()

# メインウィンドウのサイズ設定
app.geometry("600x400")

# アプリ本体のインスタンス生成
main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
login = Login(app, main)

app.mainloop()