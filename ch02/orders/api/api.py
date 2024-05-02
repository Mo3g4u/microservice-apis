from datetime import datetime
from uuid import UUID

from starlette.responses import Response
from starlette import status

from orders.app import app

# pydantic モデルをインポートし、検証に使えるようにする
from orders.api.schemas import CreateOrderSchema

# レスポンスで返す注文オブジェクトを定義
orders = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': "delivered",
    'created': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quanttity': 1
        }
    ]
}

# /orders URL パスの GET エンドポイントを登録
@app.get('/orders')
def get_orders():
    return {'orders': [orders]}

# レスポンスのステータスコートが 201 (Created) であることを指定
@app.post('/orders', status_code=status.HTTP_201_CREATED)
# ペイロードを関数のパラメータとして宣言することでインターセプトし、型ヒントを使って検証
def create_order(order_details: CreateOrderSchema):
    return orders

# order_id などの URL パラメータを波かっこで囲んで定義
@app.get('/orders/{order_id}')
def get_order(order_id: UUID): # URL パラメータを関数の引数として取得
    return orders

@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return orders

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    # HTTPStatus.NO_CONTENT.value を使って空のレスポンスを返す
    return Response(status_code=status.HTTP_204_NO_CONTENT.value)

@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    return orders

@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    return orders
