# NetatmoAPIClient

このPythonクライアントは、Netatmo Weather APIにアクセスするためのものです。アクセストークンの取得と更新、およびNetatmoデバイスからの気象データの取得が可能です。

## 使用方法
1. [netatmo_api_client.py](https://github.com/shinking02/NetatmoAPIClient/blob/main/netatmo_api_client.py)を自身のプロジェクトのルートディレクトリ（.envなどがあるフォルダ）にダウンロードしてください。
2. .envファイルが存在しない場合は、[.env.example](https://github.com/shinking02/NetatmoAPIClient/blob/main/.env.example)を参考に作成し、すでに存在している場合は既存の.envファイルに下記内容を追記してください。（`YOUR_`から始まる箇所は書き換えてください）

```
CLIENT_ID=YOUR_CLIENT_ID
CLIENT_SECRET=YOUR_CLIENT_SECRET
INITIAL_REFRESH_TOKEN=YOUR__REFRESH_TOKEN
```
> [!WARNING]
> `INITIAL_REFRESH_TOKEN`に記載するリフレッシュトークンは一度しか使用できません。すでに使用済みのリフレッシュトークンではエラーになるため注意してください。

3. .envへの記載が完了後、下記のようにして実行することができます。[参考(example.py)](https://github.com/shinking02/NetatmoAPIClient/blob/main/example.py)
```python
from netatmo_api_client import NetatmoAPIClient

# NetatmoClientクラスのインスタンス化
client = NetatmoAPIClient()

# ステーションデータを取得して表示
stations_data = client.get_stations_data()
print("Stations Data:", stations_data)

```


## オプション
NetatmoAPIClientではリフレッシュトークンを用いて取得したアクセストークンを`netatmo_api_client.py`と同一階層の`token_info.json`に保存します。
`token_info.json`を他のディレクトリに保存したい場合や、別のファイル名を使用したい場合はクライアントの初期化時に保存先を指定することができます。
```python
from netatmo_api_client import NetatmoAPIClient
client = NetatmoApiClient(token_file="path/to/your/custom_token_info.json")
```
