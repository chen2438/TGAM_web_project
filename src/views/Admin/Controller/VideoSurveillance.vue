<template>
    <div>
      <!--面包屑-->
      <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-left: 10px;padding-bottom: 10px;font-size: 12px">
        <el-breadcrumb-item :to="{ path: '/adminmain' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>监控中心</el-breadcrumb-item>
        <el-breadcrumb-item>视频监控</el-breadcrumb-item>
      </el-breadcrumb>
    
    <el-div class="allVideo">
      <div class="rowVideo">
        <div class="eachVideo">
            <video ref="videoElement" autoplay style="display: none;"></video>
            <img :src="imageSrc" />
            <div>
                <a>司机姓名：{{ driverName }}，司机车牌：{{ plate }}</a><br>
                <a>疲劳次数: {{ fatigueCount }}，当前疲劳等级：{{ status }}</a>
            </div>
        </div>
        <div class="eachVideo">
            <video ref="videoElement" autoplay style="display: none;"></video>
            <img :src="imageSrc" />
            <div>
                <a>司机姓名：{{ driverName }}，司机车牌：{{ plate }}</a><br>
                <a>疲劳次数: {{ fatigueCount }}，当前疲劳等级：{{ status }}</a>
            </div>
        </div>
      </div>
      <div class="rowVideo">
        <div class="eachVideo">
            <video ref="videoElement" autoplay style="display: none;"></video>
            <img :src="imageSrc" />
            <div>
                <a>司机姓名：{{ driverName }}，司机车牌：{{ plate }}</a><br>
                <a>疲劳次数: {{ fatigueCount }}，当前疲劳等级：{{ status }}</a>
            </div>
        </div>
        <div class="eachVideo">
            <video ref="videoElement" autoplay style="display: none;"></video>
            <img :src="imageSrc" />
            <div>
                <a>司机姓名：{{ driverName }}，司机车牌：{{ plate }}</a><br>
                <a>疲劳次数: {{ fatigueCount }}，当前疲劳等级：{{ status }}</a>
            </div>
        </div>
      </div>
    </el-div>
</div>
</template>
  
<script>
import io from 'socket.io-client';

export default {
    name: 'AdminFatigueDetection',
    data() {
        return {
            videoElement: null,
            outputElement: null,
            imageSrc: '',
            driverName:'',
            plate:'',
            fatigueCount: 0,
            status:[
                { value: 0,label: '正常' },
                { value: 1,label: '轻度疲劳' }, 
                { value: 2,label: '中度疲劳' }, 
                { value: 3,label: '重度疲劳' }, 
            ],
            status: 'Normal',
            socket: io('http://localhost:8000') // Replace with your server URL and port
        };
    },


    startStream() {
        const videoElement = this.$refs.video;
        const streamUrl = '/getVideo'; // 与后端路由对应

        if (window.MediaSource && MediaSource.isTypeSupported('video/mp4')) {
        const mediaSource = new MediaSource();
        videoElement.src = URL.createObjectURL(mediaSource);

        mediaSource.addEventListener('sourceopen', () => {
            const sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');

            const xhr = new XMLHttpRequest();
            xhr.open('GET', streamUrl);
            xhr.responseType = 'arraybuffer';
            xhr.onerror = () => console.log('Error loading video stream');
            xhr.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total * 100 | 0);
                    console.log(`Loading video stream ${percentComplete}%`);
                }
            };
            xhr.onload = () => {
                const uint8Array = new Uint8Array(xhr.response);
                let i = 0;

                (function readChunk() {
                    const length = ((uint8Array[i] << 24) | (uint8Array[i + 1] << 16) | (uint8Array[i + 2] << 8) | uint8Array[i + 3]) >>> 0;
                    i += 4;

                    if (length === 0) {
                        mediaSource.endOfStream();
                    } else {
                        const chunk = uint8Array.subarray(i, i + length);
                        i += length;

                        sourceBuffer.appendBuffer(chunk);
                        readChunk();
                    }
                })();
            };
            xhr.send();
        });
        } else {
            console.log('Unsupported MIME type or codec: video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
        }
    },

    // mounted() {
    //     this.videoElement = this.$refs.videoElement;
    //     this.outputElement = this.$refs.outputElement;

    //     if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    //         navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    //             this.videoElement.srcObject = stream;
    //             this.videoElement.play();

    //             const canvas = document.createElement('canvas');
    //             const context = canvas.getContext('2d');

    //             setInterval(() => {
    //                 context.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
    //                 const dataURL = canvas.toDataURL('image/jpeg');
    //                 this.socket.emit('frame', dataURL.split(',')[1]); // Send the frame to the server
    //             }, 100); // Send frames every 100ms
    //         });
    //     }

    //     this.socket.on('response', (data) => {
    //         this.imageSrc = 'data:image/jpeg;base64,' + data.data; // Update the image source
    //         this.driverName = data.driverName;
    //         this.plate = data.plate;
    //         this.fatigueCount = data.count;
    //         this.status = data.status;
    //     });
    // },
    // beforeDestroy() {
    //     this.socket.disconnect();
    // }
};
</script>
  
<style>
.allVideo{
    width:100%;
    height:100%;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: 40%,40%;
    grid-gap: 10px;
}
.rowVideo{
    height:100%;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: 50% 50%;
    grid-gap: 10px;
    justify-items: center;
    align-items: center;
}
.eachVideo{
    width:80%;
    height:auto;
    justify-items: center;
    align-items: center;
    border: 1px solid #ccc; /* 边框样式，可根据需求调整 */
    border-radius: 10px;
    padding: 10px; /* 内边距，可根据需求调整 */
}

img {
    width: 80%;
    max-width: 720px;
    height: auto;
    
}
</style>
