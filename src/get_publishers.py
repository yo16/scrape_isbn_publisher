from get_one_publisher import get_one_publisher
import sqlite3
import time
import random


def get_publishers():
    pub_no_list = (
        {
            "keta": 2,
            "start": 0,
            "end": 19
        },
        {
            "keta": 3,
            "start": 250,
            "end": 699
        },
        {
            "keta": 4,
            "start": 7500,
            "end": 8499
        },
        {
            "keta": 5,
            "start": 86000,
            "end": 89999
        },
        {
            "keta": 6,
            "start": 900000,
            "end": 949999
        },
        {
            "keta": 7,
            "start": 9900000,
            "end": 9999999
        }
    )

    # DB接続
    with sqlite3.connect("pub_code.db", isolation_level=None) as conn:  # 自動commit
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pub(pub_code, pub_name)")

        for kse in pub_no_list:
            keta = kse["keta"]
            start = kse["start"]
            end = kse["end"]

            for n in range(start, end+1):   # endの最後の数字も使うから+1
                cur_pub_no = f"{n:0{keta}}"

                # DBにあるか確認
                cur.execute(
                    f"SELECT pub_code, pub_name FROM pub WHERE pub_code='{cur_pub_no}'"
                )
                rec = cur.fetchone()

                # なければ取得
                if rec is None:
                    # cur_pub_noに対応するpublisher名を取得
                    publisher = get_one_publisher(cur_pub_no)
                    print(f"{cur_pub_no}: {publisher}")

                    # ランダムで5～10秒待つ
                    time.sleep(
                        5.0 + 5*random.random()
                    )

                    # DBへ格納
                    cur.execute(
                        "INSERT INTO pub values(?,?)",
                        (cur_pub_no, publisher)
                    )
                
                else:
                    # あるなら表示
                    print(f"{rec[0]}: {rec[1]} (already exists)")

    return pub_no_list

