from fastapi import FastAPI

# FastAPI クラスのインスタンスを作成。このオブジェクトは API アプリケーションを表す
app = FastAPI(debug=True)

# api モジュールをインポートし、読み込み時にビュー関数を登録できるようにする
from orders.api import api