// 引入 Vue 框架
import Vue from 'vue'
// 引入 Element UI 组件库
import ElementUI from 'element-ui'
// 引入 Element UI 的 CSS 样式
import 'element-ui/lib/theme-chalk/index.css'
// 引入根组件 App.vue
import App from './App.vue'
// 引入 Vue 路由配置
import router from './router'
// 引入 Vuex 状态管理配置
import store from './store'
// 引入全局 CSS 样式文件
import './assets/css/global.css'
// 引入 Vue AMap（高德地图）插件
import VueAMap from 'vue-amap'
// 注册 Vue AMap 插件
Vue.use(VueAMap)
// 注册 Element UI 组件库
Vue.use(ElementUI)

// 初始化 Vue AMap 插件配置
VueAMap.initAMapApiLoader({
  // 设置高德地图 API 密钥
  key: '241c26aea06ed390a44598314eefd604',
  // 指定需要加载的高德地图插件
  plugin: ['AMap.Geolocation', 'AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  // 设置高德地图 SDK 版本
  v: '1.4.4',
  // 设置 UI 库版本
  uiVersion: '1.0.11'
})

// 设置 Vue 在生产环境下不显示提示信息
Vue.config.productionTip = false

// 创建 Vue 实例，挂载到 #app 元素上
new Vue({
  router,  // 使用路由
  store,   // 使用 Vuex 状态管理
  render: h => h(App)  // 渲染根组件
}).$mount('#app')
