import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
// 创建并导出一个新的 Vuex.Store 实例
export default new Vuex.Store({
  // state 定义了存储的初始状态
  state: {
    data: {},       // 用于存储数据对象
    token: '',      // 用于存储令牌字符串
    sessionid: null // 用于存储会话 ID
  },

  // mutations 是同步函数，用于更改存储的状态
  mutations: {
    // getToken mutation 用于设置 token 的值
    getToken: (state, token) => {
      state.token = token
    },
    // getData mutation 用于设置 data 对象
    getData: (state, data) => {
      state.data = data
    },
    // getId mutation 用于设置 sessionid 的值
    getId: (state, sessionid) => {
      state.sessionid = sessionid
    }
  },

  // actions 用于处理异步操作，可以调用 mutations
  actions: {
  },

  // modules 允许将 store 分割成模块，每个模块拥有自己的 state、mutations、actions 等
  modules: {
  }
})