# controller

环境: 
```
node v16.20.2
npm 8.19.4
python 3.11.5
```

Debian 12 安装 node 16
```
# Using Debian, as root
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
VERSION=node_16.x
DISTRO="$(lsb_release -s -c)"
echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | tee /etc/apt/sources.list.d/nodesource.list
echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | tee -a /etc/apt/sources.list.d/nodesource.list
```

手动选择特定版本

```
apt-cache madison nodejs
sudo apt-get install -y nodejs=<版本号>
```

Python 依赖

```
git clone https://github.com/chen2438/TGAM_web_project.git
cd TGAM_web_project

python3 -m venv myenv
source myenv/bin/activate
pip install flask_socketio flask_cors opencv-python dlib scipy imutils flask_sqlalchemy gevent
# deactivate
```

登录账号: 

admin: admin123456

driver: driver123456

## Project setup

```
npm install
```

### 启动本地服务器

```
npm run serve
```

### 启动后端

```
python3 src/backend/app.py
```

### 构建

后端仍需手动启动

注意修改`.env.production`

```
npm run build
```
