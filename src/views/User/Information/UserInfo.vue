<template>
  <div>
    <!--面包屑-->
    <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-left: 10px;padding-bottom: 10px;font-size: 12px">
      <el-breadcrumb-item :to="{ path: '/usermain' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>基础信息</el-breadcrumb-item>
      <el-breadcrumb-item>个人中心</el-breadcrumb-item>
    </el-breadcrumb>
    <div>
        <el-card>
          <el-descriptions class="margin-top" title="简介" :column="2" border>
            <template slot="extra">
              <el-button type="primary" size="small" @click="edit">操作</el-button>
            </template>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-picture-outline"></i>
                头像
              </template>
              <img class="img" src="../../../assets/img/timg.jpg" alt="" />
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-user"></i>
                姓名
              </template>
              {{ user.userName }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-s-custom"></i>
                账号
              </template>
              {{ user.userAccount }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-odometer"></i>
                密码
              </template>
              {{ user.userPassword }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-mobile-phone"></i>
                手机号码
              </template>
              {{ user.userPhone }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-location-outline"></i>
                家庭地址
              </template>
              {{ user.userAddress }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-magic-stick"></i>
                驾照分数
              </template>
              {{ user.userScore }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label">
                <i class="el-icon-date"></i>
                注册日期
              </template>
              {{ user.userTime }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
        <el-dialog  title="修改个人信息" :visible.sync="dialogFormVisible" width="60%" @close="handleClose">
            <el-form :model="user"  ref="updateuser" label-width="150px">
                <div class="updateinfo">
                    <div class="left">
                        <el-form-item label="头像" prop="avatar">
                            <img style="width:150px;height:200px" src="../../../assets/img/timg.jpg"/>
                        </el-form-item>
                        <el-form-item label="密码" prop="password">
                            <el-input v-model="user.userPassword"></el-input>
                        </el-form-item>
                        <el-form-item label="姓名" prop="name">
                            <el-input v-model="user.userName" disabled></el-input>
                        </el-form-item>
                        <!-- <el-form-item label="性别" prop="sex">
                            <el-switch v-model="updateuser.sex" active-color="#13ce66" inactive-color="#ff4949" 
                            active-text="男" inactive-text="女" :active-value="1" :inactive-value="0">
                            </el-switch>
                        </el-form-item> -->

                    </div>
                    <div class="right">
                        <el-form-item label="用户编号" prop="id">
                            <el-input v-model="user.userId" disabled></el-input>
                        </el-form-item>
                        <el-form-item label="账号" prop="account">
                            <el-input v-model="user.userAccount" disabled></el-input>
                        </el-form-item>
                        <el-form-item label="驾照分" prop="score">
                            <el-input v-model="user.userScore" disabled></el-input>
                        </el-form-item>
                        <el-form-item label="家庭地址" prop="area">
                            <el-input v-model="user.userAddress"></el-input>
                        </el-form-item>
                        <el-form-item label="手机号" prop="phone">
                            <el-input v-model="user.userPhone"></el-input>
                        </el-form-item>
                        <el-form-item label="注册时间" prop="time">
                            <el-input v-model="user.userTime"></el-input>
                        </el-form-item>
                    </div>
                </div>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="submit">提 交</el-button>
            </span>
        </el-dialog>
    </div>
    <div>
      <div class="block" >
        <el-timeline reverse="true"> 
          <el-timeline-item v-for="(item,index) in events" :key="index" :timestamp="item.eventTime" placement="top" color=rgb(11,223,32) size="large" icon="el-icon-warning">
            <el-card>
              <h4>{{ item.event }}</h4>
              <p>{{ item.eventTime }} 请勿疲劳驾驶：道路千万条，安全第一条，行车不规范，亲人两行泪</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </div>
</template>

<script>
import { userInfo ,updateUser } from "@/api/driver.js";
export default {
  name: "Info",
  data() {
    return {
      user:{
        type: Number,
        userId: Number,
        userName: String,
        userAccount: String,
        userPassword: String,
        userPhone: String,
        userAddress: String,
        userScore: Number,
        userTime: String
      },
      dialogFormVisible : false,
      events:[{
          eventTime:"2018/4/2 20:46",
          event:"过度疲劳，被警示，扣2分"
        },
        {
          eventTime:"2018/5/2 18:45",
          event:"过度疲劳，被警示，扣2分"
        }
      ],
      websocket:null
    };
  },
  mounted() {
    this.load();
  },
  created() {
    // 创建WebSocket连接
    const ws = new WebSocket('ws://127.0.0.1:8000/User/userInfo'); // 替换为WebSocket服务器地址
    // 监听WebSocket的状态变化
    ws.onopen = function () {
      console.log('WebSocket连接已建立');
    };
    // 监听WebSocket消息
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // 处理接收到的数据
      
    };
  },
  methods: {
    async load() {
      const response = await userInfo(this.$store.state.sessionid);
      const { code, res, events } = response.data;
      this.user = res
      this.events = events
      console.log(res)
      console.log(this.user)
    },
    edit(){
      this.dialogFormVisible = true;
    },
    // 监听弹窗的关闭事件
    handleClose () {
    // eslint-disable-next-line no-unused-expressions
      this.$refs.updateuser.resetFields()
    },
    // 修改司机信息并提交
    submit () {
      // eslint-disable-next-line no-unused-expressions
      this.$refs.updateuser.validate(async valid => {
        // eslint-disable-next-line no-useless-return
        if (!valid) return
        // 发起修改信息的数据申请
        // eslint-disable-next-line no-unused-vars
        const { data } = await updateUser(this.user.userId, this.user.userAddress,this.user.userPassword,this.user.userTime,this.user.userPhone)
        console.log(data.data)
        if (data.code !== 20000) {
          return this.$message.error('更新司机信息失败')
        }
        this.load()
        this.dialogFormVisible = false
        this.$message.success('更新司机信息成功')
      })
    },
    open2() {
        this.$notify({
          title: '警告',
          message: '警告，注意驾驶分数是否变动！',
          type: 'warning'
        });
      }
  },
  //深层监听
  watch:{
    'user.userScore':{
      handler:function(newval, oldval){
        if(newval != this.user.userScore || oldval != 0)
          this.open2()
      }
    }
  }
};
</script>

<style scoped>
.img {
  width: 80px;
  height: 80px;
}
.updateinfo {
  height: 350px;
  overflow: auto;
}
.left {
  /* width: 330px; */
  float: left;
}
.right {
  overflow: hidden;
}
.block{
  padding-top: 30px;
  margin-right: 50px;
}
</style>
