<template>
    <div>
    <div>
      <!--面包屑-->
      <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-left: 10px;padding-bottom: 10px;font-size: 12px">
        <el-breadcrumb-item :to="{ path: '/usermain' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>监控中心</el-breadcrumb-item>
        <el-breadcrumb-item>视频监控</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div style="margin-bottom: 30px;">
        <img src="../../User/camera.png" style="width: 80px;margin-left: 370px;">
        <span style="font-size: 80px;color:rgb(106, 165, 190);"> 摄   像  检  测</span>
    </div>

    <el-container>
  <el-aside width="600px" style="margin-left: 40px;">

    <video ref="videoElement" autoplay style="display: none;"></video>
    <img :src="imageSrc" />

  </el-aside>
  <el-main>
    <el-table :data="tableData" class="img-styled" style="margin-top: 30px;">
            <el-table-column prop="label" label="项目"></el-table-column>
            <el-table-column prop="value" label="数据"></el-table-column>
    </el-table>
  </el-main>
</el-container>
<div>
        <audio controls="controls"  src="../alarm_music/1级.mp3" ref="audio"></audio>
        <audio controls="controls" src="../alarm_music/2级.mp3"  ref="audio"></audio>
        <audio controls="controls" src="../alarm_music/3级.mp3"  ref="audio"></audio>
        <audio controls="controls" src="../alarm_music/大哥清醒一下.mp3"  ref="audio"></audio> <!--测试mountd函数加载后音乐器是否播放-->
        <audio controls="controls"></audio>

</div>

</div>
</template>
  
<script>
import io from 'socket.io-client';
import { updateVideo } from '../../../api/data';
export default {
    name: 'UserFatigueDetection',
    data() {
        return {
            videoElement: null,
            outputElement: null,
            imageSrc: '',
            eye_count: 0,
            temp_eye:0,
            eye_text: '',
            mouth_count: 0,
            temp_mouth:0,
            mouth_text: '',
            fatigueCount: 0,
            status: {},
            socket: io('http://localhost:8000'), // Replace with your server URL and port
            tableData: [
                { label: '眯眼计数', value: '' },
                { label: '眼部状态', value: '' },
                { label: '打哈欠计数', value: '' },
                { label: '嘴部状态', value: '' }
            ],
            reminded:0,
            count:0,
            audioSrc:''
        };

    },
    methods: {
        updateTableData() {
            this.tableData = [
                { label: '眯眼计数', value: this.eye_count },
                { label: '眼部状态', value: this.eye_text },
                { label: '打哈欠计数', value: this.mouth_count },
                { label: '嘴部状态', value: this.mouth_text }
            ];
        },
        async updateVideo(){
            console.log("updateVideo前的status" + this.status)
            const response = await updateVideo(this.status)
            if (response.code === 20000) console.log("更新数据成功")
        },
        checkFatigue() {
            const eyeCount = this.eye_count;
            const yawnCount = this.mouth_count;
            if (eyeCount <= 5 && yawnCount <= 1) {
                // 不疲劳
                this.audioSrc = '';
            } else if (
                (eyeCount > 5 && eyeCount <= 10) || (yawnCount > 2 && yawnCount <= 4)) {
                // 轻度疲劳
                this.audioSrc = '../alarm_music/大哥清醒一下.mp3';
            } else if ((eyeCount > 10 && eyeCount <= 15) || (yawnCount > 4 && yawnCount <= 6)) {
                // 重度疲劳
                this.audioSrc = '../alarm_music/1级.mp3';
                this.fatigueCount++;
            } else if (eyeCount > 15 || yawnCount > 6) {
                // 极度疲劳
                this.audioSrc = '../alarm_music/大哥清醒一下.mp3,../alarm_music/3级.mp3';
                this.fatigueCount++;
            }
            },
        playAudio(audioSrc) {
            const audio = new Audio(audioSrc);
            audio.play();
            this.reminded++;
            },
        startplay() {
            this.$refs.audio.currentTime = 0; // 从头开始播放提示音
            this.$refs.audio.play(); // 播放
            console.log('播放');
            },
    },
    mounted() {
        this.videoElement = this.$refs.videoElement;
        this.outputElement = this.$refs.outputElement;
        this.startplay()//测试音乐器能否播放
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
                this.videoElement.srcObject = stream;
                this.videoElement.play();

                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');

                canvas.width = 600; // 设置宽度为1280像素
                canvas.height = 400; // 设置高度为720像素

                setInterval(() => {
                    context.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
                    const dataURL = canvas.toDataURL('image/jpeg');
                    this.socket.emit('frame', dataURL.split(',')[1]); // Send the frame to the server
                }, 100); // Send frames every 100ms
            });
        }
        console.log("***********************************************")
                    // 每30秒执行一次判断
        setInterval(() => {
            this.count++;
            this.checkFatigue();
            if (this.audioSrc) { this.playAudio(this.audioSrc.trim());}
            this.audioSrc = ''
            this.temp_eye += this.eye_count;
            this.temp_mouth + this.mouth_count;
            if (this.count === 4) {
                this.status = {
                    time: new Date().toLocaleTimeString().strftime("%Y-%m-%d %H:%M"),
                    fatigue: this.fatigueCount,
                    situation: `眯眼${this.temp_eye}次, 打哈欠${this.temp_mouth}次`,
                    reminded:this.reminded,
                    userId:this.$cookies.get("userId"),
                    userName:this.$cookies.get("userName"),
                    carPlates:this.$cookies.get("carPlates")
                },
                this.temp_eye = 0;
                this.temp_mouth = 0;
                this.reminded = 0;
                this.fatigueCount = 0;
                this.count = 0;
                this.updateVideo();
            }
        },30000);
        console.log("***********************************************")


        this.socket.on('response', (data) => {
            this.imageSrc = 'data:image/jpeg;base64,' + data.data; // Update the image source
            this.eye_count = data.eye_count;
            this.eye_text = data.eye_text;
            this.mouth_count = data.mouth_count;
            this.mouth_text = data.mouth_text;
            this.updateTableData(); // 更新表格数据
        });
    },
    beforeDestroy() {
        this.socket.disconnect();
        clearInterval(this.timer)
    }

};
</script>
  
<style>
.img-styled {
    border: 4px solid #ddd;
    /* 添加边框 */
    border-radius: 10px;
    /* 圆角边框 */
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    /* 添加阴影 */
    width: 80%;
    /* 调整图片宽度 */
    max-width: 500px;
    /* 最大宽度 */
    height: auto;
    /* 高度自适应 */
    display: block;
    /* 居中显示 */
    margin: 10px auto;
    /* 上下外边距 */
}
</style>
