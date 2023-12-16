<template>
  <!--登录表单的容器-->
  <div class="login_container">
    <div class="title">
      <span>疲劳驾驶监控中心</span>
    </div>
    <!--登录区域-->
    <div class="login_box" style="margin-top: 50px">
      <!--头像-->
      <div class="avatar_box">
        <img src="../assets/img/img_1.png">
      </div>
      <!--表单-->
      <el-form :model="loginForm" :rules="loginRules" ref="loginForm" label- width="0px" class="login_form">
        <el-form-item prop="account">
          <el-input v-model="loginForm.account" placeholder="请输入帐户用户名" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="请输入登录密码"
            prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item prop="verifyCode">
          <div class="verifyCode_box">
            <el-input v-model="loginForm.verifyCode" placeholder="请输入计算结果" prefix-icon="el-icon-mobile"
              class="verifyCode"></el-input>
            <img src="../assets/img/mskKPg.png" alt="" class="verifyCode_img">
          </div>
        </el-form-item>


        <el-form-item class="login_btn" style="white-space: pre;">
          <el-button type="primary" @click="submitForm('loginForm')">登录</el-button>
          <el-button @click="resetForm('loginForm')">重置</el-button>
          {{ ' '.repeat(2) }}
          <router-link to="/register" class="tip-color">没有账号？去注册（默认司机）</router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
// 从 admin API 文件中导入 accountLogin 方法，用于登录请求
import { accountLogin } from '@/api/admin'

export default {
  name: 'Login',  // 组件名称
  data() {
    return {
      // 登录表单的数据模型
      loginForm: {
        account: '',     // 用户账号
        password: '',    // 登录密码
        verifyCode: '',  // 验证码
        sessionid: null, // 会话ID
      },
      // 登录表单的验证规则
      loginRules: {
        admin: [
          { required: true, message: '请输入登录用户名', trigger: 'blur' },
          { min: 1, max: 12, message: '请输入1-12位', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { min: 6, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur' }
        ],
        verifyCode: [
          { required: true, message: '请输入计算结果', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 提交登录表单的方法
    submitForm(loginForm) {
      // 使用Element UI的表单验证
      this.$refs[loginForm].validate(valid => {
        if (!valid) {
          // 表单验证未通过时的提示信息
          this.$message({
            message: '请完整输入',
            type: 'warning',
            duration: 1200
          })
          return false
        }
      })
      // 调用登录请求方法
      this.getadminLogin()
    },
    // 重置登录表单的方法
    resetForm(formName) {
      // 重置表单字段
      this.$refs[formName].resetFields()
    },
    // 异步方法，执行登录请求
    async getadminLogin() {
      // 发送登录请求，等待结果
      const { data } = await accountLogin(this.loginForm.account, this.loginForm.password)
      // 打印响应数据
      console.log(data)
      // 将token、shop数据和sessionid存储到Vuex
      this.$store.commit('getToken', data.data.token)
      this.$store.commit('getData', data.data.shop)
      this.$store.commit('getId', data.data.sessionid)
      // 打印存储到Vuex的数据
      console.log(this.$store.state.token)
      console.log(this.$store.state.data)
      console.log(this.$store.state.sessionid)
      // 根据响应数据判断登录状态，并显示对应的提示消息
      if (data.code === 4001) {
        this.$message({
          message: '用户名不存在',
          type: 'warning',
          duration: 2000,
        })
      } else if (data.code === 4002) {
        this.$message({
          message: '用户名对应密码错误',
          type: 'warning',
          duration: 2000
        })
      } else if (data.code === 20000 && data.data.type === 0) {
        // 管理员登录成功，跳转到管理员主界面
        this.$message({
          message: '登录成功',
          type: 'success',
          duration: 2000,
          onClose: () => {
            this.$router.push('/Adminmain')
          }
        })
      } else if (data.code === 20000 && data.data.type === 1) {
        // 普通用户登录成功，跳转到用户主界面
        this.$message({
          message: '登录成功',
          type: 'success',
          duration: 2000,
          onClose: () => {
            this.$router.push('/Usermain')
          }
        })
      }
    }
  }
}
</script>


<style lang="less" scoped>
.title {
  color: dimgray;
  -webkit-text-stroke: 1px black;
  letter-spacing: 0.04em;
  background-color: #FFFFFF;
  font-size: 50px;
  font-weight: bold;
  text-shadow: 1px -1px black, 2px -2px white;
  text-align: center;
  opacity: 0.45;
}

.login_container {
  height: 100%;
  background-color: #708090;
}

.login_box {
  width: 450px;
  height: 400px;
  background-color: #FFFFFF;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  .avatar_box {
    width: 130px;
    height: 130px;
    border: 1px solid #EEEEEE;
    border-radius: 50%;
    padding: 10px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    margin: -65px auto;
    background-color: #FFFFFF;

    img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #EEEEEE;
    }
  }

  .login_form {
    position: absolute;
    bottom: 0px;
    width: 100%;
    padding: 0px 20px;
    box-sizing: border-box;

    .login_btn {
      display: flex;
      justify-content: flex-end;
    }

    .tip-color {
      color: #708090;
    }

    .tip-color:hover {
      color: red;
    }

    .tip-color:active {
      color: green;
    }

    .verifyCode_box {
      display: flex;

      .verifyCode {
        width: 70%;
        justify-content: left;
      }

      .verifyCode_img {
        width: 30%;
        height: 45px;
        justify-content: flex-end;
      }
    }
  }
}

.login_container {
  background: url(../assets/img/img_3.png) no-repeat;
  background-size: 100% 770px;
  overflow: hidden;
  height: 100%;
}
</style>
