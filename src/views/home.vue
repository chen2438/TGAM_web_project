<template>
  <div class="home">
    <img src="../assets/img/scai.png" alt="" style="position: fixed; left:25%; top: 10%;" />
    <el-row :gutter="0">
      <el-col :span="3" :offset="22" class="top" style="margin-top: 11px">
        <el-button :span="3" type="primary" @click="gotologin">登录</el-button>

      </el-col>
    </el-row>
    <el-row style="margin-top: 300px;margin-left: 300px">
      <el-col :span="8" class="t1">
        <div class="text text1">{{ startedCarNum }}</div>
        <div class="textt tt1">正在使用</div>
      </el-col>
      <el-col :span="8" class="t2">
        <div class="text text2">{{ carNum }}</div>
        <div class="textt tt2">车辆数目</div>
      </el-col>
      <el-col :span="8" class="t3">
        <div class="text text3">{{ userNum }}</div>
        <div class="textt tt3">注册用户
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
// 从 driver API 文件中导入 findCarsAndUser 方法
import { findCarsAndUser } from '@/api/driver'

export default {
  name: 'home',  // 组件名为 'home'
  components: {},  // 组件依赖的子组件列表（当前为空）

  // 组件的本地状态数据
  data() {
    return {
      startedCarNum: 111,  // 正在使用的车辆数初始值
      carNum: 2222,        // 车辆总数的初始值
      userNum: 33333       // 注册用户数的初始值
    }
  },

  // 组件创建后的生命周期钩子
  created() {
    // 组件创建后立即调用 getCarsAndUser 方法获取数据
    this.getCarsAndUser()
  },

  // 定义组件方法
  methods: {
    // 异步方法，用于从 API 获取车辆和用户信息
    async getCarsAndUser() {
      // 等待 findCarsAndUser 方法的结果
      const { data } = await findCarsAndUser()
      // 更新正在使用的车辆数
      this.startedCarNum = data.data.startedCarNum
      // 更新停用的车辆数（未在模板中显示）
      this.stoppedCarNum = data.data.stoppedCarNum
      // 计算并更新总车辆数
      this.carNum = this.startedCarNum + this.stoppedCarNum
      // 更新用户数
      this.userNum = data.data.userNum
    },

    // 方法，用于处理登录按钮的点击事件
    gotologin() {
      // 导航到登录页面
      this.$router.push('/login')
    },

    // 方法，用于处理访客进入的操作
    guestEnter() {
      // 导航到主机页面
      this.$router.push('/host')
    }
  }
}
</script>

<style>
.home {
  background: url(../assets/img/img_3.png) no-repeat;
  background-size: 100% 770px;
  overflow: hidden;
  height: 100%;
}

.text,
.textt {
  font-size: 1.5rem;
  color: #fff;
}
</style>
