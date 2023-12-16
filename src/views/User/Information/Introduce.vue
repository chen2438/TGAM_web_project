<template>
  <div class="page">
      <div class="nav">
          <div class="nav-item">
              <!-- <img src="../assets/gshx-nav.png" /> -->
              <button @click="change(0)" :class="{ newStyle: 0 === number }">高山滑雪</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/hylb-nav.png" /> -->
              <button @click="change(1)" :class="{ newStyle: 1 === number }">花样滑冰</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/ddsh-nav.png" /> -->
              <button @click="change(2)" :class="{ newStyle: 2 === number }">短道速滑</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/xq.png" /> -->
              <button @click="change(3)" :class="{ newStyle: 3 === number }">钢架雪车</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/djlx.png" /> -->
              <button @click="change(4)" :class="{ newStyle: 4 === number }">冬季两项</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/xqiao.png" /> -->
              <button @click="change(4)" :class="{ newStyle: 4 === number }">雪橇</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/dbhx.png" /> -->
              <button @click="change(4)" :class="{ newStyle: 4 === number }">单板滑雪</button>
          </div>
          <div class="nav-item">
              <!-- <img src="../assets/dbhx.png" /> -->
              <button @click="change(4)" :class="{ newStyle: 4 === number }">...</button>
          </div>



      </div>
      <div class="content">
          <div class="item" v-show="0 === number">
              <div class="title">
                  高山滑雪
              </div>
              <div class="details">
                  <div class="text">
                      <div class="sub">
                          <!-- <img src="../assets/gshx.png" /> -->
                          <span>项目介绍</span>
                      </div>
                      <p>高山滑雪（Alpine Skiing）是以滑雪板、雪鞋、固定器和滑雪杖为主要用具，从山上向山下，沿着旗门设定的赛道滑下的雪上竞速运动项目。奥运会高山滑雪设男子项目、女子项目、混合项目。其中，男子项目和女子项目各设滑降、回转、大回转、超级大回转、全能5个小项，混合项目则为混合团体赛。其中，滑降和超级大回转属速度项目，按一次滑行成绩决出名次。回转和大回转属技术项目，以两次滑行成绩合计计算。</p>
                      <div class="sub">
                          <!-- <img src="../assets/gshx.png" /> -->
                          <span>项目规则</span>
                      </div>
                      <p>在高山滑雪比赛中，选手滑行速度可以超过130公里/小时，不同项目起点与终点的垂直高度差亦有不同：速降男子800-1100米，女子500-800米；回转男子180-220米，女子140-200米；大回转男子250-450米，女子250-400米；超大回转男子500-650米，女子400-600米。</p>
                      <p>这些垂直高度差让比赛更加艰难，因为选手在滑下来的同时需要穿越设置在滑行路线上的一系列的旗门，如果有选手错过了一个旗门，那么他就必须回去重新穿越这个错过的旗门，否则他就丧失比赛资格。</p>
                      <p>高山滑雪的每个项目比赛均采用单人出发，出发的顺序通过抽签决定，但有的项目需要滑两次，第二次出发的顺序由由第一次比赛的成绩确定。出发的间隔一般为60秒，只有回转项目采用不等时出发。出发时，运动员必须身穿经正式铅封标志的运动服（即经裁判员检查并认可的服装），佩戴出发号码布，头戴护盔，脚穿滑雪板，手持滑雪杖，同时必须使用脱离式固定器。</p>
                  </div>
                  <div class="image">
                      <!-- <img style="border: 3px solid #3889a8 ;border-radius: 20px;" src="../assets/gshx01.png" /> -->
                  </div>
              </div>
          </div>
          <div class="item" v-show="1 === number">
              <div class="title">
                  <h1>花样滑冰</h1>
              </div>
              <div class="details">
                  <div class="text">
                      <div class="sub">
                          <!-- <img src="../assets/hyhb.png" /> -->
                          <span>项目介绍</span>
                      </div>
                      <p>花样滑冰（Figure Skating）是冰上运动项目之一。运动员通过冰刀在冰面上划出图形，并表演跳跃、旋转等高难度动作。花样滑冰的裁判会按照动作的质量与艺术性表现进行综合评分，最高为6分。</p>
                      <div class="sub">
                          <!-- <img src="../assets/hyhb.png" /> -->
                          <span>项目规则</span>
                      </div>
                      <p>冬奥会和世界锦标赛参赛名额由上一年度世界锦标赛的成绩根据国际滑联的相关规定进行计算确定，但每个国家和地区每项最多可参加3人（对）。所有项目必须分别进行。男、女单人和双人各包括有短节目，自由滑和表演自由滑3项内容，冬奥会和世界锦标赛只规定有短节目和自由滑。每项内容各进行1天，短节目在先。</p>
                      <p>短节目由规定的3种不同跳跃、3种不同旋转和2种不同步法共8个动作和连接步组成。运动员自选音乐，根据要求编排一套不超过2分40秒的节目。评分包括规定动作分和表演分。裁判员依据动作质量，难度和完成情况先评出规定动作分，然后根据内容编排的均衡性和音乐的一致性、速度、姿势以及音乐特点表达等再出示第二个分——表演分。</p>
                      <p>自由滑是由跳跃、旋转、步法和各种姿势组成。运动员自选音乐，根据规则编排一套均衡内容的节目。自由滑比赛的时间男子单人和双人为4分30秒，女子单人4分钟。自由滑评分包括技术水平分和表演分。</p>
                      <p>表演自由滑是由规定数量的跳跃﹑旋转和步法组成。节目主要突出音乐的表达和艺术表演。其评分包括滑行技术分和表演分。比赛时间为3分30秒至4分30秒。</p>
                      <p>冰上舞蹈比赛由规定舞、创编舞、自由舞和表演舞4项内容组成。冬奥会和世界锦标赛只进行3项，分别在3天进行。第1天为规定舞，第2天创编舞。规定舞是根据规定的音乐、图案、步法和重复次数进行比赛。规定舞共有22种，每次比赛滑其中的2种。冰上舞蹈的评分包括技术分和节奏/表演分。</p>
                  </div>
                  <div class="image">
                      <!-- <img style="border: 3px solid #3889a8 ;border-radius: 20px;" src="../assets/hyhb01.png" /> -->
                  </div>
              </div>
          </div>
          <div class="item" v-show="2 === number">
              <div class="title">
                  <h1>短道速滑</h1>
              </div>
              <div class="details">
                  <div class="text">
                      <div class="sub">
                          <!-- <img src="../assets/sdhb.png" /> -->
                          <span>项目介绍</span>
                      </div>
                      <p>高山滑雪（Alpine Skiing）是以滑雪板、雪鞋、固定器和滑雪杖为主要用具，从山上向山下，沿着旗门设定的赛道滑下的雪上竞速运动项目。奥运会高山滑雪设男子项目、女子项目、混合项目。其中，男子项目和女子项目各设滑降、回转、大回转、超级大回转、全能5个小项，混合项目则为混合团体赛。其中，滑降和超级大回转属速度项目，按一次滑行成绩决出名次。回转和大回转属技术项目，以两次滑行成绩合计计算。</p>
                      <div class="sub">
                          <!-- <img src="../assets/sdhb.png" /> -->
                          <span>项目规则</span>
                      </div>
                      <p>在高山滑雪比赛中，选手滑行速度可以超过130公里/小时，不同项目起点与终点的垂直高度差亦有不同：速降男子800-1100米，女子500-800米；回转男子180-220米，女子140-200米；大回转男子250-450米，女子250-400米；超大回转男子500-650米，女子400-600米。</p>
                      <p>这些垂直高度差让比赛更加艰难，因为选手在滑下来的同时需要穿越设置在滑行路线上的一系列的旗门，如果有选手错过了一个旗门，那么他就必须回去重新穿越这个错过的旗门，否则他就丧失比赛资格。</p>
                      <p>高山滑雪的每个项目比赛均采用单人出发，出发的顺序通过抽签决定，但有的项目需要滑两次，第二次出发的顺序由由第一次比赛的成绩确定。出发的间隔一般为60秒，只有回转项目采用不等时出发。出发时，运动员必须身穿经正式铅封标志的运动服（即经裁判员检查并认可的服装），佩戴出发号码布，头戴护盔，脚穿滑雪板，手持滑雪杖，同时必须使用脱离式固定器。</p>
                  </div>
                  <div class="image">
                      <!-- <img style="border: 3px solid #3889a8 ;border-radius: 20px;" src="../assets/sdhb01.png" /> -->
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>
<script>
export default {
  name: 'Introduce',
  data() {
      return {
          number: 0,
      }
  },
  methods: {
      change: function (index) {
          this.number = index;
      },
  },

}
</script>
<style scoped>
.page {
  padding: 0 2px;
  display: flex;
  margin-top: 20px;
  width: 100%;
  font-size: 20px;
}
.nav {
  width: 10%;
  height: 400px;
  display: inline-block;
  margin: 20px 0 0 40px;
  font-size: 25px;
}
.nav-item {
  width: 140px;
  height: 80px;
  padding: 2px;
  display: flex;
  border: 2px #c0c4cc solid;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.nav-item img {
  width: 70px;
  height: 70px;
}
.nav-item button {
  margin: 0;
  padding: 0;
  border: 1px solid transparent;
  outline: none;
  background-color: #fff;
  font-size: 15px;
  color: grey;
}
.nav-item button:focus {
  color: black;
}
.title {
  left: 20px;
  font-size: 35px;
}
.item {
  width: 90%;
  display: flex;
  flex-direction: column;
}
.details {
  width: 100%;
  display: flex;
  flex-direction: row;
  margin: 10px 10px 10px 10px;
}
.text {
  width: 85%;
  height: 500px;
  border: 5px solid #3889a8;
  border-radius: 11px;
  overflow: auto;
  margin-right: 40px;
}
.text .sub {
  width: 30%;
  height: 30px;
  font-size: 15px;
  color: #3889a8;
  padding: 20px;
}
p {
  text-align: justify;
  text-indent: 2rem;
}
.sub img {
  width: 30px;
  height: 30px;
}
.content .item .image > img{
  width: 400px;
  height: 500px;
  padding: 5px;

}
</style>
