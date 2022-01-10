<template>
  <div id="aCoursesList" class="bg-fa of">
    <section style="padding: 20px; width: 1500px;margin-left:auto;margin-right:auto;">
    <el-form :inline="true" class="demo-form-inline" ref="sectionQuery" :model="sectionQuery">
      <el-form-item label="筛选条件：" >
        <el-input v-model="sectionQuery.Course_name" placeholder="课程名" />
      </el-form-item>
      <el-form-item style="width:100px;"></el-form-item>
      <el-form-item>
        <el-input v-model="sectionQuery.Teacher_name" placeholder="教师名" />
      </el-form-item>
      <el-form-item style="width:100px;"></el-form-item>
      <el-form-item prop='start_end'>
        <el-date-picker
          v-model="sectionQuery.start_end"
          type="datetimerange"
          range-separator="To"
          start-placeholder="开课时间"
          end-placeholder="结课时间"
          value-format="yyyy-MM-dd"
        >
        </el-date-picker>
      </el-form-item>
      <el-button type="primary" icon="el-icon-search" @click="getList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

    <!-- 数据列表 -->
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="60">
        <template slot-scope="scope">{{(page-1) * size + scope.$index + 1}}</template>
      </el-table-column>
      <el-table-column prop="sec_id" label="开课号" width="80" />

      <el-table-column prop="Course.cid" label="课程号" width="80" />
      <el-table-column prop="Course.name" label="课程名" width="100" />
      <el-table-column prop="choosed" label="已选人数" width="100" />
      <el-table-column prop="capacity" label="课容量" width="100" />
      <el-table-column prop="start" label="开课时间" width="180" />
      <el-table-column prop="end" label="结课时间" width="180" />
      <el-table-column prop="classroom.address" label="教室" width="200" />
      <el-table-column label="上课时段">
        <template slot-scope="scope">
          <span v-for="item in scope.row.time_slot" :key="item.time_slot_id">{{item.time_slot_id}} ({{item.day}} {{item.start}}-{{item.end}}) <br></span>  
        </template>
      </el-table-column> />

      <el-table-column label="操作" width="200">
        <template slot-scope="scope">
        <!-- scope.row.sec_id -->
            <el-button type="primary" size="mini" icon="el-icon-circle-plus-outline" @click="select(scope.row.sec_id,sectionQuery.sid)">选课</el-button>
        </template>
      </el-table-column>
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
import takeApi from '@/api/take'

export default {
  data() {
    return {
      
      page:1, //当前页
      // data:{},  //课程列表
      take: {
          Student:'',
          section:'',
          status:'',
      },
    
      sectionQuery: {}, //条件封装对象

      list: [], //查询之后接口返回的数据
      page: 1, //当前页
      size: 5, //每页记录数
      total: 0, //总记录数
    }
  },
  created() {
    this.token = this.getToken()
    console.log(this.token)
    if(this.token) {//判断是否有token值
      //  this.hasLogin()
      this.init()
    }
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
        saveOrUpdate(){
            // 判断修改还是添加 根据take是否有id
            console.log(this.take.id)
                this.saveTake()


              
        },
        // 修改课程的方法
        saveTake(){
            this.$confirm('确定选择选择该课程', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
            takeApi.addTake(this.take)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '选课成功'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/ucenter'})
                      })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '未成功'
              });          
            });

        },
        init(){
            // console.log(this.$route.params.id)
             // 页面渲染之前执行
            var userStr_uid = cookie.get('my_ucenter_uid')
            console.log("sijdadoh___"+cookie.get('my_ucenter_uid'))
            if(this.$route.params && this.$route.params.id){
                // 从路径中获取id的值
                const id = this.$route.params.id
                // 调用根据id查询的方法
                if (id.length==5){
                  this.sectionQuery['Course_id']=id
                }else if(id.length==6){
                  this.sectionQuery['sec_id']=id
                }
                if(userStr_uid.substr(0,1)=='s'){
                  this.$set(this.sectionQuery,'sid',userStr_uid)
                }
                  
            }else{
                this.sectionQuery = {}
            }
            this.getList()
        },
            // &&&&&&&&&&&&&&&&&&&&&&&&&&

        getList(page = 1) {
          if(this.sectionQuery['sid']=='' || this.sectionQuery['sid']==undefined ||this.sectionQuery['sid'] ==null){
                      // 清空数据
            this.list = []
            this.total = 0;
            return;
          }
          this.page = page;
          section
              .getTakeSectionListPage(this.page, this.size, this.sectionQuery)
              .then(response => {
              //请求成功
              //response接口返回的数据
              this.list = response.data.data
              console.log(this.list)
              this.total = response.lens;
              })
              .catch(error => {
              //请求失败
                console.log(error);
              });
        },

        // 清空的方法
        resetData() {
        //表单输入项数据清空
        this.sectionQuery = {};

        //查询所有开课数据
        this.getList();
        },
        select(sec_id,sid){
          this.take.section=sec_id
          this.take.Student=sid
          this.take.status='ing'
          this.saveOrUpdate()
        }

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