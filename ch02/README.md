# 第２章

## piipenv が入って無かったら

```
brew install pipenv
```

## 仮装環境の作成と依存ファイルのインストール

```
pipenv --three # これはエラーが出た この次のコマンドから実行
pipenv install fastapi uvicorn # FastAPI と Uvicorn をインストール
pipenv shell # 仮装環境をアクティブ化
```

## アプリケーションを実行してみる

仮装環境をアクティブ化したところで以下を実行

```
uvicorn orders.app:app --reload
```
