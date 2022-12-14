※競技関係者以外への流出は控えて下さい！！！！

# 使い方
以下の5つのエンドポイントが実装されています。
- 試合情報の取得 ( GET /match )
- 問題情報の取得 ( GET /problem )
- 取得する分割データの指定 ( POST /problem/chunks )
- wavの取得 ( GET /problem/chunks/:filename)
- 問題への回答 ( POST /problem )


# 共通事項
## トークン
全てのリクエストには下記のリクエストヘッダ、もしくはクエリパラメーターのどちらかが必要です。

### リクエストヘッダの場合
Keyとしてprocon-token, Valueとして各高専のtokenを設定してください。
- procon-token: xxxxxxxxxxxx
### クエリパラメーターの場合
Keyとしてtoken, Valueとして各高専のtokenを設定してください。
- /match?token=xxxxxxx

## unix time
Unix epochからの経過秒数です。
1656601200 は 日本時間の2022年7月1日0時0分0秒を示します。

## 試合情報設定前
すべてのエンドポイントがAccessTimeErrorになります。

# 試合情報の取得 ( GET /match )
/match にGETリクエストを送ることで試合の情報を取得できます。

## レスポンス
### 成功した場合
下記のプロパティを含むjsonが返ります。
- problems 試合中の問題数。整数
- bonus_factor: 使用した分割数に対するボーナス係数の配列。n番目がn個利用場合のボーナス係数です。実数の配列
- penalty: 変更札に適用される係数。整数

```
{
    "problems": 3,
    "bonus_factor": [1.0],
    "penalty": 1
}
```
### 失敗した場合
status code 400の場合下記の可能性があります。
- `InvalidToken`: トークンが正しくない
- `AccessTimeError`: 試合の時間外


# 問題情報の取得 ( GET /problem )
/problem にGETリクエストを送ることで試合の情報を取得できます。

## レスポンス
### 成功した場合
下記のプロパティを含むjsonが返ります。
- id: 問題ID
- chunks: 分割数。整数
- start_at: 開始時間のunixtime
- time_limit: 制限時間。単位は秒。整数
- data: 重ね合わせ数。整数
```
{
    "id": "qual-1-1",
    "chunks": 2,
    "starts_at": 1655302266,
    "time_limit": 1000,
    "data": 3
}
```
### 失敗した場合
status code 400の場合下記の可能性があります。
- `InvalidToken`: トークンが正しくない
- `AccessTimeError`: 問題の回答時間外

# 取得する分割データの指定 ( POST /problem/chunks )
/problem/chunks にPOSTリクエストを送ることで取得する分割データの数を指定できます。

## リクエスト
クエリパラメータに取得する分割数nを指定してください。
例 /problem/chunks?n=2

## レスポンス
### 成功した場合
下記のプロパティを含むjsonが返ります。
chunks: 各分割データのファイル名の配列が返ります。
次に説明する /problem/chunks/ファイル名 にGETリクエストを送ることで分割データを取得できます。

```
{
    "chunks": [
        "problem3_31c6b25b1810f0c5b87a30a1ea17dcd2a5b9f832.wav",
        "problem1_75012769dcc8b201e17816927628dab234d5451b.wav",
    ]
}
```
### 失敗した場合
status code 400の場合下記の可能性があります。
- `InvalidToken`: トークンが正しくない
- `AccessTimeError`: 問題の回答時間外
- `FormatError`: フォーマットが正しくない
- `FormatError`: 問題に設定されているchunkの数をこえている

# wavの取得 ( GET /problem/chunks/:filename )
/problem/chunks/:filenameにGETリクエストを送ることで分割データを取得することができます。
_で区切られたファイル名の左側が分割前の順番で右側がdigestです。

## レスポンス
### 成功した場合
wavファイル
### 失敗した場合
status code 400の場合下記の可能性があります。
- `InvalidToken`: トークンが正しくない
- `AccessTimeError`: 問題の回答時間外
- `NotFound`: ファイルが存在しない

# 問題への回答 ( POST /problem )
/problem にPOSTリクエストを送ることで試合への回答を送信できます。

## リクエスト
リクエストヘッダーに下記を指定してください。
Content-Type: application/json


また、下記のプロパティを含むjsonをbodyに含めてください。
- problem_id: 問題ID
- answers: 回答するの絵札のIDを文字列の配列で設定してください。各絵札のIDは配布された音声の0埋めされた2桁の数字の部分です。
```
{
    "problem_id": "qual-1-1",    
    "answers": ["01", "02"]
}
```
## レスポンス
### 成功した場合
下記のプロパティを含むjsonが返ります。
- problem_id: 問題ID
- answers: 解凍された絵札のIDの配列
- accepted_at: 回答を受信した日時のunix time
```
{
    "problem_id": "qual-1-1",    
    "answers": ["01", "02"],
    "accepted_at": 1656601200,
}
```

### 失敗した場合
status code 400の場合下記の可能性があります。
- `InvalidToken`: トークンが正しくない
- `TooLargeRequestError`: bodyのサイズが1024byteをこえている
- `FormatError`: フォーマットが正しくない
- `FormatError`: 問題IDが指定されていない
- `FormatError`: answersの配列のサイズが0
- `FormatError`: answersの配列のサイズが問題の読み札数をこえている
- `AccessTimeError`: 指定された問題IDの回答時間外