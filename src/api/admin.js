import request from '../utils/request'

/**
 * 管理员登录
 * @param adminName
 * @param adminPwd
 * @returns {AxiosPromise}
 */
export const adminLogin = (adminName, adminPwd) => {
  return request({
    url: '/Admin/AdminLogin',
    method: 'post',
    headers: {
      'Content-Type': 'application/json', // 明确设置 Content-Type
    },
    data: { // 使用 data 而不是 param 发送请求体
      adminName,
      adminPwd
    }
  })
}

// export const adminLogin = (adminName, adminPwd) => {
//   return request({
//     url: '/Admin/AdminLogin',
//     method: 'post',
//     param: {
//       adminName,
//       adminPwd
//     }
//   })
// }
