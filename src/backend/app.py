from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)
sessionid = 0  # (=carId=userId)标识符,不同司机登录账号后，后后端传参作为标识符标识司机

# analyze.py
from analyze import socketio

app.config["SECRET_KEY"] = "secret!"
socketio.init_app(app, cors_allowed_origins="*")

# db.py
from db import setup_db

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data.db')}"
setup_db(app)

# 模拟数据

cars = [
    {
        "carId": 1,
        "carState": 0,  # 0未启动，1启动
        "carPlates": "浙A3N809",
        "carStyle": "小型车",
        "carCity": "City1",
        "carTude": "120.1,30.2",
        "userName": "张伟",
        "userId": 1,
        "userPhone": "13158375930",
        "userAddress": "浙江理工大学学生生活2区",
        "userNow": 0,  # 0疲劳驾驶,1正常
        "userTime": "2023-01-01",
        "userScore": 8,  # 司机驾驶分
        "userAccount": "driver",
        "userPassword": "driver123456",
        "type": 1,  # 司机
        "tiredSituation": "频繁",
        "times": 2,
        "reminded": 38,
        "alltimes": 1800,
    },
    {
        "carId": 2,
        "carState": 1,  # 0未启动，1启动
        "carPlates": "浙B8GJ65",
        "carStyle": "大型车",
        "carCity": "City2",
        "carTude": "120.2,30.3",
        "userName": "李明",
        "userId": 2,
        "userPhone": "13285836284",
        "userTime": "2023-03-15",
        "userAddress": "Address2",
        "userScore": 12,  # 司机驾驶分
        "userAccount": "driver2",
        "userPassword": "driver123666",
        "type": 1,  # 司机
        "userNow": 0,
        "tiredSituation": "偶尔",
        "times": 1,
        "reminded": 2,
        "alltimes": 500,
    },
    {
        "carId": 3,
        "carState": 1,  # 0未启动，1启动
        "carPlates": "浙C6H975",
        "carStyle": "中型车",
        "carTude": "120.3,30.1",
        "carCity": "City3",
        "userName": "陈晨",
        "userId": 3,
        "userScore": 12,
        "userPhone": "13019273638",
        "userAddress": "ADMIN",
        "userNow": 1,
        "userAccount": "admin",
        "userPassword": "admin123456",
        "type": 0,  # 管理员
        "tiredSituation": "偶尔",
        "times": 3,
        "reminded": 5,
        "alltimes": 800,
    },
    # ... 其他车辆数据
]
users = cars
tired = cars
events = [
    {"eventTime": "2023-4-2 20:46", "event": "过度疲劳，被警示，扣2分"},
    {"eventTime": "2023-5-2 18:45", "event": "过度疲劳，被警示，扣2分"},
]


@app.route("/Account/AccountLogin", methods=["POST"])
def account_login():
    # 从请求中提取管理员用户名和密码
    name = request.json.get("Name")
    pwd = request.json.get("Pwd")
    print(f"{name}, {pwd}")
    # 遍历登录信息列表，检查用户名和密码是否匹配
    for login in users:
        if login["userAccount"] == name and login["userPassword"] == pwd:
            sessionid = login["userId"]
            # 登录成功，返回对应的用户类型
            response = {
                "code": 20000,
                "message": "登录成功",
                "data": {
                    "token": "fake-jwt-token-for-demo",  # 示例用的假JWT令牌
                    "type": login["type"],  # 返回用户类型
                    "sessionid": sessionid,
                },
            }
            return jsonify(response)
        if login["userAccount"] == name and login["userPassword"] != pwd:
            # 密码不匹配
            response = {"code": 4002, "message": "管理员用户名对应密码错误"}
            return jsonify(response)
    # 管理员用户名不存在
    response = {"code": 4001, "message": "本管理员用户名不存在"}
    return jsonify(response)


# 注册
@app.route("/Account/AccountRegister", methods=["POST"])
def admin_register():
    data = request.get_json()
    print("data", data)
    name = data.get("admin")
    password = data.get("password")
    type = 1  # 这里新增用户默认是司机
    try:
        if name != "" and password != "":
            userId = len(users)  # 默认只有一个管理员
            new_user = {
                "userId": userId,
                "userName": "",
                "userPhone": "",
                "userTime": datetime.now().date().strftime("%Y-%-m-%-d"),
                "userScore": 12,
                "userAddress": "",
                "userAccount": name,
                "userPassword": password,
                "type": 1,
            }
            users.append(new_user)
            response = {
                "code": 20000,
                "message": "register success",
                "data": {
                    "token": "fake-jwt-token-for-demo",  # 示例用的假JWT令牌
                },
            }
            return jsonify(response)
    except Exception as e:
        print("register failed: ", e)
        response = {"code": 4001, "message": "register failed"}
        return jsonify(response)


@app.route("/Car/findCarCityAndCount", methods=["GET"])
def find_car_city_and_count():
    # 生成假数据
    data = [{"carCity": "City1", "cityCount": 5}, {"carCity": "City2", "cityCount": 3}]
    return jsonify({"code": 20000, "data": {"carCityAndCount": data}})


@app.route("/Car/queryCarList", methods=["GET"])
def query_car_list(city=None, plates=None, style=None):
    # 这里可以添加筛选逻辑，根据请求参数过滤cars
    # 例如: city = request.args.get('carCity')
    city = request.args.get("carCity")
    plates = request.args.get("carPlates")
    style = request.args.get("carStyle")
    filtered_car = cars
    if city:
        filtered_car = [item for item in filtered_car if item["carCity"] == city]
    if plates:
        filtered_car = [
            item for item in filtered_car if item["carPlates"].find(plates) != -1
        ]
    if style:
        filtered_car = [item for item in filtered_car if item["carStyle"] == style]
    print("filtered_car", filtered_car)
    return jsonify(
        {"code": 20000, "data": {"records": filtered_car, "total": len(cars)}}
    )


@app.route("/User/common/findUserList", methods=["GET"])
def find_user_list():
    # 添加分页和过滤逻辑
    return jsonify({"code": 20000, "data": {"records": users, "total": len(users)}})


@app.route("/Head/findUserTired", methods=["GET"])
def find_user_tired():
    # 添加分页和过滤逻辑
    return jsonify({"code": 20000, "data": {"UserAll": tired, "total": len(tired)}})


@app.route("/User/common/getUserById", methods=["GET"])
def get_user_by_id():
    user_id = request.args.get("userId")
    user = next((u for u in users if u["userId"] == int(user_id)), None)
    return jsonify({"code": 20000, "data": {"user": user}})


@app.route("/User/common/editUser", methods=["GET"])
def edit_user():
    # 这里应该是POST请求，用于更新用户信息
    # 在这里只返回成功信息
    return jsonify({"code": 20000, "message": "用户信息更新成功"})


@app.route("/User/common/deleteUser", methods=["POST"])
def delete_user():
    global users  # 引入全局变量
    userId_to_delete = request.json.get("userId")
    # 使用列表推导式创建一个新的列表，仅保留 userId 不等于要删除的值的数据项
    users = [user for user in users if user["userId"] != userId_to_delete]
    return jsonify({"code": 20000, "message": "用户删除成功"})


@app.route("/User/common/findCarsAndUser", methods=["GET"])
def find_cars_and_user():
    # 生成假数据
    data = {
        "startedCarNum": len([car for car in cars if car["carState"] == 1]),
        "stoppedCarNum": len([car for car in cars if car["carState"] == 0]),
        "userNum": len(users),
    }
    return jsonify({"code": 20000, "data": data})


@app.route("/User/common/warningAllTiredUser", methods=["POST"])
def warning_all_tired_user():
    # 生成警告信息
    return jsonify({"code": 20000, "message": "所有疲劳驾驶用户已警告"})


@app.route("/User/common/warningtiredUserById", methods=["POST"])
def warning_tired_user_by_id():
    # 根据用户ID生成警告
    user_id = request.args.get("userId")
    # 在这里只返回成功信息
    return jsonify({"code": 20000, "message": f"用户 {user_id} 已被警告"})


@app.route("/Car/findStoppedCars", methods=["GET"])
def find_stopped_cars():
    # 模拟未启动车辆数据
    stopped_cars = [car for car in cars if car["carState"] == 0]
    return jsonify({"code": 20000, "data": {"stoppedCarList": stopped_cars}})


@app.route("/Car/findStartedCars", methods=["GET"])
def find_started_cars():
    # 模拟已启动车辆数据
    started_cars = [car for car in cars if car["carState"] == 1]
    return jsonify({"code": 20000, "data": {"startedCarList": started_cars}})


@app.route("/User/userInfo", methods=["GET"])
def userInfo():
    return jsonify({"code": 20000, "res": users[0], "events": events})


@app.route("/User/updateuser", methods=["GET"])
def updateUser():
    temp_user = request.args.get("userId")
    return jsonify({"code": 20000, "message": "用户修改成功"})


from gevent import pywsgi

if __name__ == "__main__":
    server = pywsgi.WSGIServer(("0.0.0.0", 8000), app)
    server.serve_forever()
    # socketio.run(app, debug=True, port=8000)
