# scrape_isbn_publisher
ISBNの出版者情報を抽出する

# ISBN
[日本図書コード管理センター](https://isbn.jpo.or.jp/)で発行される本のコード。ISBNは国際標準図書番号。

# ISBNの出版者コード
```
978 - 4 - xxxxxx - yy - z
```
- 全体は13桁(ISBN-13)。以前は"978"がない10桁(ISBN-10)だったが枯渇し、"978"をつけた13桁になった。さらに枯渇したら979になることが決まっている。
- 978: 固定。
- 4: 国記号。日本は4。
- xxxxxx: 出版者記号。
  - 桁数は先頭の数字によって決まっている。（使わない数字がそこそこある）
    - ２桁：00～19
    - ３桁：250～699
    - ４桁：7500～8499
    - ５桁：86000～89999
    - ６桁：900000～949999
    - ７桁：9900000～9999999
- yy: 書名記号
  - 出版者内の書籍の番号。
  - `len(出版者記号) + len(署名記号) == 8`の制限がある。
- z: チェック数字
  - モジュラス10
  - 13桁の数字に対し、先頭から見て奇数桁は`x1`、偶数行は`x3`を掛け、すべて足す。その１の位を10から引いた値。10の場合は0。
    - 978 - 4 - 04 - 895048 - ? の場合
      - 9 + 7*3 + 8 + 4*3 + 0 + 4*3 + 8 + 9*3 + 5 + 0*3 + 4 + 8*3 = 130
      - 10 - 0 = 10（10の場合は0）

