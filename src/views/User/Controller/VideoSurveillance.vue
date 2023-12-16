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
        <video ref="videoElement" autoplay style="display: none;"></video>
        <img :src="imageSrc" />
        <div>
            <p>Fatigue Count: {{ fatigueCount }}</p>
            <p>Status: {{ status }}</p>
        </div>
    </div>
</template>
  
<script>
import io from 'socket.io-client';

export default {
    name: 'UserFatigueDetection',
    data() {
        return {
            videoElement: null,
            outputElement: null,
            imageSrc: '',
            fatigueCount: 0,
            status: 'Normal',
            socket: io('http://localhost:8000') // Replace with your server URL and port
        };
    },
    mounted() {
        this.videoElement = this.$refs.videoElement;
        this.outputElement = this.$refs.outputElement;

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
                this.videoElement.srcObject = stream;
                this.videoElement.play();

                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');

                setInterval(() => {
                    context.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
                    const dataURL = canvas.toDataURL('image/jpeg');
                    this.socket.emit('frame', dataURL.split(',')[1]); // Send the frame to the server
                }, 100); // Send frames every 100ms
            });
        }

        this.socket.on('response', (data) => {
            this.imageSrc = 'data:image/jpeg;base64,' + data.data; // Update the image source
            this.fatigueCount = data.count;
            this.status = data.status;
        });
    },
    beforeDestroy() {
        this.socket.disconnect();
    }
};
</script>
  
<style>
img {
    width: 80%;
    max-width: 720px;
    height: auto;
}
</style>
