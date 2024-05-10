# 第 6 章

## 初期設定

```
mkdir ch06
cp - ch02 ch06/orders
cd ch06/orders
pipenv install --dev && pipenv shell
uvicorn orders.app:app --reload
```

## API の設計書をロードするには PyYAML が必要

```
pipenv install pyyaml
```
