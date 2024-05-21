from pathlib import Path
import yaml
from apispec import APISpec

from flask import Flask
from flask_smorest import Api

# 先ほど定義して Blueprint をインポート
from api.api import blueprint

# 先ほど定義した BaseConfig クラスをインポート
from config import BaseConfig

# Flask アプリケーションオブジェクトのインスタンスを作成
app = Flask(__name__)

# from_object メソッドを使って、クラスから設定を読み込む
app.config.from_object(BaseConfig)

# flask-smorest の　Api オブジェクトのインスタンスを作成
kitchen_api = Api(app)

# Blueprint を厨房 API オブジェクトに登録
kitchen_api.register_blueprint(blueprint)

api_spec = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())
spec = APISpec(
    title=api_spec['info']['title'],
    version=api_spec['info']['version'],
    openapi_version=api_spec['openapi']
)
spec.to_dict = lambda: api_spec
kitchen_api.spec = spec