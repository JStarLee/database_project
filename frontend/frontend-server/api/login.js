import request from '@/utils/request'

export default{

    //会员登录
    submitLogin(userInfo){
        return request({
            url: '/users/login/',
            method: 'post',
            data: userInfo
        })
    },

    //根据token获取会员信息
    getMemberInfo(token){
        return request({
            url: '/users/info/',
            method: 'get',
            params: { token }
        })
    }
}