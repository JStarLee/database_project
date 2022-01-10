import request from '@/utils/request'

export function login(data) {
  return request({
    // url: '/vue-admin-template/user/login',
    url: '/users/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: '/vue-admin-template/user/info',
    url: '/users/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    // url: '/vue-admin-template/user/logout',
    url: '/users/logout/',
    method: 'post'
  })
}
