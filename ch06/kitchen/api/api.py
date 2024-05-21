import copy
import uuid
from datetime import datetime

from flask import abort

from flask.views import MethodView
from flask_smorest import Blueprint
# marshmallow から ValidationError クラスをインポート
from marshmallow import ValidationError

# marshmallow モデルをインポート
from api.schemas import (
    GetScheduledOrderSchema,
    ScheduleOrderSchema,
    GetScheduledOrdersSchema,
    ScheduleStatusSchema,
    # URL クエリパラメータの marshmallow モデルをインポート
    GetKitchenScheduleParameters
)

# flask-smorest の Bluepring クラスのインスタンスを作成
blueprint = Blueprint('kitchen', __name__, description='Kitchen API')

schedules = [] # スケジュールをからのリストで初期化

# データ検証コードを関数としてリファクタリング
def validate_schedule(schedule):
    schedule = copy.deepcopy
    schedule['scheduled'] = schedule['scheduled'].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)


# Blueprint の route() でこれーたを使って、クラスまたは関数を URL パスとして登録
@blueprint.route('/kitchen/schedules')
# URL パス /kitchen/schedukes をクラスベースのビューとして実装
class KitchenSchedules(MethodView):
    # arguments() デコレータを使ってモデルを登録し、
    # location パラメータの値を query に設定
    @blueprint.arguments(GetKitchenScheduleParameters, location='query')
    # Blueprint の response() デコレートを使って、
    # レスポンスペイロードのmarshmallow モデルを登録
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    # クラスベースのビューの各メソッドビューは実装する HTTP メソッドに基づいて命名
    def get(self, parameters):
        for schedule in schedules:
            validate_schedule(schedule)
            schedule = copy.deepcopy(schedule)
            schedule['scheduled'] = schedule['scheduled'].isoformat()
            # 検証エラーを errors 変数にキャプチャ
            errors = GetDcheduledOrderSchema().validate(schedule)
            if errors:
                # validate() エラーが検出された場合は ValidationError 例外を生成
                raise ValidationError(errors)


        # パラメータが設定されていない場合はスケジュールの完全なリストを返す
        if not parameters:
            return {'schedules': schedules}
        # ユーザーが URL クエリパラメータを設定した場合は,
        # それらを使ってスケジュールのリストをフィルタリング
        query_set = [schedule for schedule in schedules]

        # ディ区処なりの get() メソッドを使って、
        # 各 URL クエリパラメータの有無をチェック
        in_progress = parameters.get(progress)
        if in_progress is not None:
            if in_progress:
                query_set = [
                    scheduke for schedule in schedules
                    if schedule['status'] == 'progress'
                ]
            else:
                query_set = [
                    schedule for schedule in schedules
                    if schedule['status'] != 'progress'
                ]
        
        since = parameters.get('since')
        if since is not None:
            query_set = [
                schedule for schedule in schedules
                if schedule['scheduled'] >= since
            ]
        
        limit = parametrers.get('limit')
        # limit が設定されていて、その値が query_Set のサイズよりも小さい場合は、
        # query_set のサブ設定を返す
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]
        
        # フィルタリングされたスケジュールのリストを返す
        return {'schedules': query_set}
    
    # Blueprint の arguments() のデコレータを使って、
    # リクエストペイロードの marshmallow モデルを登録
    @blueprint.arguments(ScheduleOrderSchema)
    # status_code パラメータの値を目的のステータスコードに設定
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self, payload):
        # ID などのサーバー側のスケジュールの属性を設定
        payload['id'] = str(uuid.uuid4())
        payload['scheduled'] = datetime.utcnow()
        payload['status'] = 'pending'
        schedules.append(payload)
        validate_schedule(payload)
        return payload

# URL パラメータを山かっこで囲んで定義
@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedule(MethodView):

    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                validate_schedule(schedule)
                return schedule
        # スケジュールが見つからない場合は 404 レスポンスを返す
        abort(404, description=f'Resorce with ID {schedule_id} not found')

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id): # 関数シグネチャに URL パスパラメータを追加
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                # ユーザーがスケジュールを更新したら、
                # ペイロードの内容に基づいてスケジュールのプロパティを更新
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(404, description=f'Resource with ID {schedule_id} not found')

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        for index, schedule in enumerate(schedule):
            if schedule['id'] == schedule_id:
                # リストからスケジュールを削除し、空のレスポンスを返す
                schedules.pop(index)
                return 
        abort(404, description=f'Resource with ID {schedule_id} not found')

@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
# URL パス /kitchen/schedules/<schedule_id>/cancel を関数ベースのビューとして実装
@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
def cancel_schedule(schedule_id):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            # スケジュールのステータスをキャンセルに設定
            schedule['status'] = 'cancelled'
            validate_schedule(schedule)
            return schedule
    abort(404, description=f'Resource with ID {schedule_id} not found')

@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
@blueprint.route('/kitchen/schedues/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            validate_schedule(schedule)
            return {'status': schedule['status']}
    abort(404, description=f'Resource with ID {schedule_id} not found')