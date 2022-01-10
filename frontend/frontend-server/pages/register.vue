<template>
  <div class="main" style="background-color:rgba(0,0,0,0.4)">
    <div class="title">
      <a href="/login">登录</a>
      <span>·</span>
      <a class="active" href="/register">注册</a>
    </div>

    <div class="sign-up-container">
      <el-form ref="userForm" :model="params">
        <el-form-item style="margin-bottom: 30px" class="input-prepend restyle no-radius te" prop="username" :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' },{mix: 2,max: 10 ,message: '姓名长度须在2~10之间',trigger: 'blur'}]">
          <div>
            <el-input type="text" placeholder="用户名" v-model="params.username"/>
            <i class="iconfont icon-phone"/>
          </div>
        </el-form-item>
        <el-form-item class="input-prepend te" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <div>
            <el-input type="password" placeholder="设置密码" v-model="params.password"/>
            <i class="iconfont icon-password"/>
          </div>
        </el-form-item>
        <el-form-item class="input-prepend te" prop="roles" :rules="[{ required: true, message: '请输入密码'}]">
          <div>
            <el-radio v-model="params.roles" label="2">学生</el-radio>
            <el-radio v-model="params.roles" label="1">教师</el-radio>
          </div>
        </el-form-item>
        <div class="btn">
          <input type="button" class="sign-up-button" value="注册" @click="submitRegister()">
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
  import '~/assets/css/sign.css'
  import '~/assets/css/iconfont.css'

  import registerApi from '@/api/register'
  export default {
    layout: 'sign',
    data() {
      return {
        params: { //封装注册输入数据
          username: '',
          password: '',
          roles:''
        }
      }
    },
    methods: {
      //注册提交的方法
      submitRegister() {
        console.log(this.params)
        registerApi.registerMember(this.params)
        .then(response => {
          //提示注册成功
            this.$message({
              type: 'success',
              message: "注册成功"
            })
          //跳转登录页面
          this.$router.push({path:'/login'})
        })
      },
      
    }
  }
</script>
<style scoped>
.te{
  background-color: rgba(0, 0, 0, 0.6);
}
.te >>> input
{
  color: white;  
}
</style>