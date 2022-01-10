<template>
  <div class="in-wrap">
    <!-- 公共头引入 -->
    <header id="header">
      <section class="container">
        <h1 id="logo">
          <a href="#" title="墨文书法">
            <img src="../assets/img/logo.png" width="100%" alt="墨文书法">
          </a>
        </h1>
        <div class="h-r-nsl">
          <ul class="nav">
            <router-link to="/" tag="li" active-class="current" exact>
              <a>首页</a>
            </router-link>
            <router-link to="/course" tag="li" active-class="current">
              <a>课程</a>
            </router-link>
            <router-link to="/teacher" tag="li" active-class="current">
              <a>名师</a>
            </router-link>
            <!-- <router-link to="/article" tag="li" active-class="current">
              <a>作品</a>
            </router-link>
            <router-link to="/qa" tag="li" active-class="current">
              <a>问答</a>
            </router-link> -->
          </ul>
          <!-- / nav -->
           <!-- / nav -->
<ul class="h-r-login">
    <!-- <li v-if="!loginInfo.id" id="no-login"> -->

    <li v-if="!loginInfo.roles" id="no-login">
        
        <a href="/login" title="登录">
            <em class="icon18 login-icon">&nbsp;</em>
            <span class="vam ml5">登录</span>
        </a>
        <a href="/register" title="注册">
            <span class="vam ml5">注册</span>
        </a>
    </li>

    <!-- <li v-if="loginInfo.id" id="is-login-two" class="h-r-user"> -->
    <li v-if="loginInfo.roles" id="is-login-two" class="h-r-user">
        <span>欢迎您，{{ loginInfo.roles=='1'? "老师":"学生" }}</span>

        <a href="/ucenter" title>

            <span id="userName" class="vam disIb">{{ loginInfo.username }}</span>
            <img
                 :src="loginInfo.avatar"
                 width="30"
                 height="30"
                 class="vam picImg"
                 alt
                 >
        </a>
        <a href="javascript:void(0);" title="退出" @click="logout()" class="ml5"> | 退出</a>
    </li>
    
    <!-- /未登录显示第1 li；登录后显示第2，3 li -->
</ul>
          <!-- <aside class="h-r-search">
            <form action="#" method="post">
              <label class="h-r-s-box">
                <input type="text" placeholder="发现你想学的课程" name="queryCourse.courseName" value>
                <button type="submit" class="s-btn">
                  <em class="icon18">&nbsp;</em>
                </button>
              </label>
            </form>
          </aside> -->
        </div>
        <aside class="mw-nav-btn">
          <div class="mw-nav-icon"></div>
        </aside>
        <div class="clear"></div>
      </section>
    </header>
    <!-- /公共头引入 -->
    <nuxt/>

    <!-- 公共底引入 -->
    <footer id="footer">
      <section class="container">
        <div class>
          <h4 class="hLh30">
            <span class="fsize18 f-fM c-999">友情链接</span>
          </h4>
          <ul class="of flink-list">
            <li>
              <a href="#" title="..." target="_blank">...</a>
            </li>
          </ul>
          <div class="clear"></div>
        </div>
        <div class="b-foot">
          <section class="fl col-7">
            <section class="mr20">
              <section class="b-f-link">
                <a href="#" title="关于我们" target="_blank">关于我们</a>|
                <a href="#" title="联系我们" target="_blank">联系我们</a>|
                <a href="#" title="帮助中心" target="_blank">帮助中心</a>|
                <a href="#" title="资源下载" target="_blank">资源下载</a>|
                <!-- <span>服务热线：010-56253825(北京) 0755-85293825(深圳)</span> -->
                <span>Email：lixingshuo@mailsdu.edu.cn</span>
              </section>
              <!-- <section class="b-f-link mt10">
                <span>©2018课程版权均归谷粒学院所有 京ICP备17055252号</span>
              </section> -->
            </section>
          </section>
          <aside class="fl col-3 tac mt15">
            <section class="gf-tx">
              <span>
                <img src="../assets/img/wx-icon.png" alt>
              </span>
            </section>
            <section class="gf-tx">
              <span>
                <img src="../assets/img/wb-icon.png" alt>
              </span>
            </section>
          </aside>
          <div class="clear"></div>
        </div>
      </section>
    </footer>
    <!-- /公共底引入 -->
  </div>
</template>
<script>
import '../assets/css/reset.css'
import '../assets/css/theme.css'
import '../assets/css/global.css'
import '../assets/css/web.css'
import '../assets/css/base.css'
import '../assets/css/activity_tab.css'
import '../assets/css/bottom_rec.css'
import '../assets/css/nice_select.css'
import '../assets/css/order.css'
import '../assets/css/swiper-3.3.1.min.css'
import '../assets/css/pages-weixinpay.css'

import cookie from 'js-cookie'
import loginApi from '@/api/login'

export default {
  data() {
    return {
        token:'',
        flag:'',
        loginInfo: {
          id: '',
          avatar: '',
          username: '',
          sex: '',
          roles:''
        }
    }
  },
  created() {
    //获取路径里面token值
    // this.token = this.$route.query.token
    this.token = this.getToken()
    console.log(this.token)
    if(this.token) {//判断是否有token值
      //  this.hasLogin()
      this.showInfo()
    }

    
  },
  methods:{
    //创建方法，从cookie获取用户信息
    getToken() {
      //从cookie获取用户信息
      var token = cookie.get('my_token')

      // 把字符串转换json对象(js对象)
        loginApi.getMemberInfo(token)
        .then(response => {
          // console.log('################'+response.data.data.userInfo)
           this.loginInfo.roles = response.data.data.roles
          //  this.flag= response.data.data.roles
          //  cookie.set('my_ucenter',this.loginInfo,{domain: 'localhost'})
        })
      return token;
    },
    showInfo() {
      //从cookie获取用户信息
      var userStr_username = cookie.get('my_ucenter_username')
      var userStr_roles = cookie.get('my_ucenter_roles')
      var userStr_avatar = cookie.get('my_ucenter_avatar')
      var userStr_uid = cookie.get('my_ucenter_uid')
      
      console.log(cookie.get('my_ucenter_uid'))
      // 把字符串转换json对象(js对象)
      if(userStr_username) {
        this.$set(this.loginInfo,'username',userStr_username)
        this.$set(this.loginInfo,'avatar',userStr_avatar)
        this.$set(this.loginInfo,'roles',userStr_roles)
        this.$set(this.loginInfo,'uid',userStr_uid)
        console.log(this.loginInfo.uid)
      }
    },

    //退出
    logout() {
      //清空cookie值
      this.loginInfo=undefined
      cookie.set('my_token','',{domain: 'localhost'})
      cookie.set('my_ucenter_username','',{domain: 'localhost'})
      cookie.set('my_ucenter_avatar','',{domain: 'localhost'})
      cookie.set('my_ucenter_roles','',{domain: 'localhost'})
      
      //回到首页面
      window.location.href = "/";
    }

  }
}
</script>
