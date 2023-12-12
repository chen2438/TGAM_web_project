from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

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


from flask_socketio import SocketIO, emit
import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import base64

app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

# 加载dlib的人脸检测器和形状预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("src/backend/shape_predictor_68_face_landmarks.dat")

# 定义闭眼阈值和帧计数
EYE_AR_THRESH = 0.15
EYE_AR_CONSEC_FRAMES = 15

# 初始化帧计数器和闭眼计数器
COUNTER = 0
TOTAL = 0


def eye_aspect_ratio(eye):
    # 计算两组垂直眼标志之间的欧氏距离
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # 计算水平眼标志之间的欧氏距离
    C = dist.euclidean(eye[0], eye[3])

    # 计算眼睛的纵横比
    ear = (A + B) / (2.0 * C)
    return ear


@socketio.on("frame")
def handle_frame(data):
    global COUNTER, TOTAL
    # 解码图像
    img_data = base64.b64decode(data)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 水平翻转图像
    frame = cv2.flip(frame, 1)

    # 调整帧的大小以加快处理速度
    # frame = cv2.resize(frame, (960, 540))

    # 将帧转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测灰度图像中的人脸
    faces = detector(gray)

    # 假设状态为正常
    text = "Normal"

    for face in faces:
        # 绘制人脸识别框
        (x, y, w, h) = face_utils.rect_to_bb(face)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 获取人脸的形状
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # 绘制面部特征点
        for x, y in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        # 提取左眼和右眼的坐标
        left_eye = shape[42:48]
        right_eye = shape[36:42]

        # 计算左眼和右眼的纵横比
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # 计算双眼纵横比的平均值
        ear = (left_ear + right_ear) / 2.0

        # 检查纵横比是否低于阈值
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            text = "Fatigue"
        else:
            # 纵横比高于阈值时，如果连续帧计数大于等于阈值，则疲劳驾驶计数加1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL += 1

            # 重置帧计数器
            COUNTER = 0

    # 将处理后的帧编码为JPEG，然后转换为Base64字符串
    _, buffer = cv2.imencode(".jpg", frame)
    response = base64.b64encode(buffer).decode("utf-8")

    # 发送响应到客户端
    emit("response", {"data": response, "count": TOTAL, "status": text})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
