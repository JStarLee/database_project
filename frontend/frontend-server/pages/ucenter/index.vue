<template>
  <div id="aCoursesList" class="bg-fa of">
    <section style="padding: 20px; width: 1500px;margin-left:auto;margin-right:auto;">
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="50">
        <template slot-scope="scope">{{(page-1) * size + scope.$index + 1}}</template>
      </el-table-column>
      <el-table-column prop="section.sec_id" label="开课号" width="100" />
      <el-table-column prop="section.Course.cid" label="课程号" width="100" />
      <el-table-column prop="section.Course.name" label="课程名" width="200" />
      
      <el-table-column prop="section.start" label="开课时间" width="180" />
      <el-table-column prop="section.end" label="结课时间" width="180" />
      <el-table-column prop="section.classroom.address" label="教室" width="200" />
      <el-table-column label="上课时段">
        <template slot-scope="scope">
          <span v-for="item in scope.row.section.time_slot" :key="item.time_slot_id">{{item.time_slot_id}} ({{item.day}} {{item.start.substr(11,5)}}-{{item.end.substr(11,5)}}) <br></span>  
        </template>
      </el-table-column> />

      <el-table-column prop="status" label="状态"/>

    </el-table>

    <!-- 分页 -->
    <el-pagination
      :current-page="page"
      :page-size="size"
      :total="total"
      style="padding: 30px 0; text-align: center;"
      layout="total, prev, pager, next, jumper"
      @current-change="getList"
    />
    </section>
  </div>

</template>
<script>
import section from '@/api/section'
import cookie from 'js-cookie'
import loginApi from '@/api/login'
import take from '@/api/take'

export default {
  data() {
    //定义变量和初始值
    return {
      list: null, //查询之后接口返回的数据
      page: 1, //当前页
      size: 5, //每页记录数
      total: 0, //总记录数
      takeQuery: {} //条件封装对象
    };
  },
  created() {
    this.token = this.getToken()
    console.log(this.token)
    if(this.token) {//判断是否有token值
      //  this.hasLogin()
      this.init()
    }
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    
  },
  watch: {
      //路由变化的方式  路由发生变化，方法就会执行
      $route(to,from){
          this.init()
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
          //  this.loginInfo.roles = response.data.data.roles
          //  this.flag= response.data.data.roles
          //  cookie.set('my_ucenter',this.loginInfo,{domain: 'localhost'})
        })
      return token;
    },
 
        // 修改课程的方法

        init(){
            // console.log(this.$route.params.id)
             // 页面渲染之前执行
            var userStr_uid = cookie.get('my_ucenter_uid')
            console.log("sijdadoh___"+cookie.get('my_ucenter_uid'))
            if(userStr_uid.substr(0,1)=='s'){
                  console.log("sijdadoh___"+cookie.get('my_ucenter_uid'))
                  this.$set(this.takeQuery,'Student_id',userStr_uid)
                }else{
                this.takeQuery = {}
            }
            this.getList()
        },
            // &&&&&&&&&&&&&&&&&&&&&&&&&&

        // getList(page = 1) {
        //   if(this.takeQuery['take_self__Student_id']=='' || this.takeQuery['take_self__Student_id']==undefined ||this.takeQuery['take_self__Student_id'] ==null){
        //               // 清空数据
        //     this.list = []
        //     this.total = 0;
        //     return;
        //   }
        //   this.page = page;
        //   section
        //       .getTakeSectionListPage(this.page, this.size, this.takeQuery)
        //       .then(response => {
        //       //请求成功
        //       //response接口返回的数据
        //       this.list = response.data.data
        //       console.log(this.list)
        //       this.total = response.lens;
        //       })
        //       .catch(error => {
        //       //请求失败
        //         console.log(error);
        //       });
        // },
        getList(page = 1) {
          this.page = page;
          take
            .getTakeListPage(this.page, this.size, this.takeQuery)
            .then(response => {
              //请求成功
              //response接口返回的数据
              this.list = response.data.data
              this.total = response.lens;

            })
            .catch(error => {
              //请求失败
              console.log(error);
            });
    },
  }
};
</script>
<style scoped>
  .active {
    background: #bdbdbd;
  }
  .hide {
    display: none;
  }
  .show {
    display: block;
  }
</style>