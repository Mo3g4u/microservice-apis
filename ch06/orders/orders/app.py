from fastapi import FastAPI
from pathlib import Path
import yaml

# FastAPI クラスのインスタンスを作成。このオブジェクトは API アプリケーションを表す
app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

# PyYAML を使って API 仕様書をロード
oas_doc = yaml.safe_load(
    (Path(__file__).parent / '../oas.yaml').read_text()
)

# FastAPI の openapi プロパティを上書きし、API 仕様書を返すようにする
app.openapi = lambda: oas_doc

# api モジュールをインポートし、読み込み時にビュー関数を登録できるようにする
from orders.api import api