<template>
  <div class="main" style="background-color:rgba(0,0,0,0.3)">
    <div class="title">
      <a class="active" href="/login">登录</a>
      <span>·</span>
      <a href="/register">注册</a>
    </div>

    <div class="sign-up-container">
      <el-form  ref="userForm" :model="user">

        <el-form-item style="margin-bottom: 30px" class="input-prepend restyle te" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <!-- <div > -->
            <el-input type="text" placeholder="用户名" v-model="user.username"/>
            <i class="iconfont icon-phone" />
          <!-- </div> -->
        </el-form-item>

        <el-form-item class="input-prepend te" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <div>
            <el-input type="password" placeholder="密码" v-model="user.password"/>
            <i class="iconfont icon-password"/>
          </div>
        </el-form-item>

        <div class="btn">
          <input type="button" class="sign-in-button" value="登录" @click="submitLogin()">
          
        </div>
      </el-form>
    </div>

  </div>
</template>

<script>
  import '../assets/css/sign.css'
  import '../assets/css/iconfont.css'

  import cookie from 'js-cookie'
  import loginApi from '@/api/login'

  export default {
    layout: 'sign',

    data () {
      return {
        //封装登录手机号和密码对象
        user:{
          username:'',
          password:''
        },
        //用户信息
        loginInfo:{}
      }
    },

    methods: {
      // 登录的方法
      submitLogin() {
        //第一步 调用接口进行登录，返回token字符串
        loginApi.submitLogin(this.user) 
           .then(response => {
             //第二步 获取token字符串放到cookie里面
             //第一个参数cookie名称，第二个参数值，第三个参数作用范围
            cookie.set('my_token',response.data.data.token,{domain: 'localhost'})
            console.log("#####  "+response.data.data.token)
              //第四步 调用接口 根据token获取用户信息，为了首页面显示
              loginApi.getMemberInfo(response.data.data.token)
                .then(response => {
                  // &&&&&&&&&&&&&&&&&&&&&&&&&&
                  // this.loginInfo.roles = response.data.data.roles
                  this.loginInfo = response.data.data

                  //获取返回用户信息，放到cookie里面
                  // &&&&&&&&&&&&&&&&&&&&&&&&&&
                  cookie.set('my_ucenter_username',this.loginInfo.username,{domain: 'localhost'})
                  cookie.set('my_ucenter_roles',this.loginInfo.roles,{domain: 'localhost'})
                  cookie.set('my_ucenter_avatar',this.loginInfo.avatar,{domain: 'localhost'})
                  cookie.set('my_ucenter_uid',this.loginInfo.uid,{domain: 'localhost'})


                  //跳转页面
                  window.location.href = "/";
                })
           })
      },
      checkId (rule, value, callback) {
        //debugger
        if (!(/^1[34578]\d{9}$/.test(value))) {
          return callback(new Error('手机号码格式不正确'))
        }
        return callback()
      }
    }
  }
</script>
<style>
   .el-form-item__error{
    z-index: 9999999;
  }
</style>

<style scoped>
.te{
  background-color: rgba(0, 0, 0, 0.6);
}
.te >>> input
{
  color: white;  
}
</style>