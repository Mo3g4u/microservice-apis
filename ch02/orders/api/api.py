import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app

# pydantic モデルをインポートし、検証に使えるようにする
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
)


ORDERS = [] # インメモリの注文リストを Python リストとして表現

# /orders URL パスの GET エンドポイントを登録
@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return {'orders': ORDERS}

# レスポンスのステータスコートが 201 (Created) であることを指定
@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
# ペイロードを関数のパラメータとして宣言することでインターセプトし、型ヒントを使って検証
def create_order(order_details: CreateOrderSchema):
    # 各注文をディクショナリに変換
    order = order_details.dict()
    # ID などのサーバー側の属性で order オブジェクトを拡張
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    # 注文を作成するには、その注文をリストに追加
    ORDERS.append(order)
    # 注文をリストに追加した後、その注文を返す
    return order

# order_id などの URL パラメータを波かっこで囲んで定義
@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID): # URL パラメータを関数の引数として取得
    # 注文を ID で検索するたけに、ORDERS リストを順番に処理して ID をチェック
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    # 注文が見つからない場合は、status_code を 404 に設定した上で
    # HTTPException を生成し、 404 レスポンスを返す
    raise HTTPException(
        status_code=404,
        detail=f'Order wiith ID {order_id} not found'
        )

@app.put('/orders/{order_id, response_model=GetOrderSchema}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(
        status_code=404,
        detail=f'Order wiith ID {order_id} not found'
        )
        

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_order(order_id: UUID):
    # list.pop() メソッドを使ってリストから注文を削除
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return 
    raise HTTPException(
        status_code=404,
        detail=f'Order wiith ID {order_id} not found'
        )

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException(
        status_code=404,
        detail=f'Order wiith ID {order_id} not found'
        )


@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404,
        detail=f'Order wiith ID {order_id} not found'
        )
