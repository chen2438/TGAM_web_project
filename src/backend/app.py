from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

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

# 模拟管理员数据
ADMIN_USERS = {"admin": "password123"}

cars = [
    {
        "carId": 1,
        "carPlates": "ABC123",
        "carStyle": "小型车",
        "userName": "User1",
        "userPhone": "1234567890",
        "carCity": "City1",
        "userAddress": "Address1",
    },
    # ... 其他车辆数据
]
users = [
    {
        "userId": 1,
        "userName": "User1",
        "userPhone": "1234567890",
        "userTime": "2023-01-01",
        "userCity": "City1",
        "userAddress": "Address1",
    },
    # ... 其他用户数据
]


@app.route("/Admin/AdminLogin", methods=["POST"])
def admin_login():
    # 从请求中提取管理员用户名和密码
    admin_name = request.json.get("adminName")
    admin_pwd = request.json.get("adminPwd")

    # 检查管理员用户名是否存在以及密码是否匹配
    if admin_name in ADMIN_USERS and ADMIN_USERS[admin_name] == admin_pwd:
        # 登录成功
        response = {
            "code": 20000,
            "message": "登录成功",
            "data": {
                "token": "fake-jwt-token-for-demo",  # 示例用的假JWT令牌
                "shop": "ShopName",  # 示例用的商店名称
            },
        }
    elif admin_name not in ADMIN_USERS:
        # 管理员用户名不存在
        response = {"code": 4001, "message": "本管理员用户名不存在"}
    else:
        # 密码不匹配
        response = {"code": 4002, "message": "管理员用户名对应密码错误"}

    return jsonify(response)


@app.route("/Car/findCarCityAndCount", methods=["GET"])
def find_car_city_and_count():
    # 生成假数据
    data = [{"carCity": "City1", "cityCount": 5}, {"carCity": "City2", "cityCount": 3}]
    return jsonify({"code": 20000, "data": {"carCityAndCount": data}})


@app.route("/Car/queryCarList", methods=["GET"])
def query_car_list():
    # 这里可以添加筛选逻辑，根据请求参数过滤cars
    # 例如: city = request.args.get('carCity')
    return jsonify({"code": 20000, "data": {"records": cars, "total": len(cars)}})


@app.route("/User/common/findUserList", methods=["GET"])
def find_user_list():
    # 添加分页和过滤逻辑
    return jsonify({"code": 20000, "data": {"records": users, "total": len(users)}})


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


@app.route("/User/common/deleteUser", methods=["GET"])
def delete_user():
    # 这里应该是DELETE请求，用于删除用户
    # 在这里只返回成功信息
    return jsonify({"code": 20000, "message": "用户删除成功"})


@app.route("/User/common/findCarsAndUser", methods=["GET"])
def find_cars_and_user():
    # 生成假数据
    data = {
        "startedCarNum": random.randint(1, 10),
        "stoppedCarNum": random.randint(1, 10),
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
    stopped_cars = [
        # 填写您的模拟车辆数据
        {
            "carId": 1,
            "carPlates": "ABC123",
            "userName": "User1",
            "userPhone": "1234567890",
            "carStyle": "小型车",
            "carTude": "120.1,30.2",
        },
        # 其他车辆数据...
    ]
    return jsonify({"code": 20000, "data": {"stoppedCarList": stopped_cars}})


@app.route("/Car/findStartedCars", methods=["GET"])
def find_started_cars():
    # 模拟已启动车辆数据
    started_cars = [
        # 填写您的模拟车辆数据
        {
            "carId": 2,
            "carPlates": "XYZ789",
            "userName": "User2",
            "userPhone": "0987654321",
            "carStyle": "大型车",
            "carTude": "120.2,30.3",
            "userNow": 0,
        },
        # 其他车辆数据...
    ]
    return jsonify({"code": 20000, "data": {"startedCarList": started_cars}})


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    socketio.run(app, debug=True, port=8000)
