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
