<template>
  <div class="app-container">
<!-- &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& -->
<!--查询表单-->
    <el-form :inline="true" class="demo-form-inline" ref="sectionQuery" :model="sectionQuery" :rules="rules">
      <el-form-item label="选课人：" prop='sid'>
        <el-input v-model="sectionQuery.sid" placeholder="学号" />
      </el-form-item>
      <el-form-item label="筛选条件：" >
        <el-input v-model="sectionQuery.Course_name" placeholder="课程名" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="sectionQuery.Teacher_name" placeholder="教师名" />
      </el-form-item>
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
      <el-button type="primary" icon="el-icon-search" @click="getListControl()">查询</el-button>
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
  </div>
</template>
<script>
import takeApi from "@/api/edu/take";
import section from "@/api/edu/section";
import studentApi from "@/api/edu/student";
export default {
    data(){
        const isExist = (rule, value, callback)=>{
          if(value==null||value==undefined||value==''){
            callback()
          }
          for (var i=0;i<this.allStudent.length;i++){
            if(value == this.allStudent[i]['sid']){
              callback()
            }
          }
          callback(new Error('输入的学生号不存在'))
        }
        return{
            take: {
                Student:'',
                section:'',
                status:'',
            },
          allStudent:{},
            sectionQuery: {}, //条件封装对象
            rules: {
              sid:[
                {required:true,message:'须指定选课人',trigger:'blur'},
                {validator: isExist ,trigger:'blur'}
              ]
           },
            // 保存按钮是否禁用
            saveBtnDisabled: false,
            // 
            list: null, //查询之后接口返回的数据
            page: 1, //当前页
            size: 5, //每页记录数
            total: 0, //总记录数
        }
    },
    
    created(){
            this.init()     
            this.$alert('请指定选课人进行查询以获取可选课程', '提示', {
              confirmButtonText: '确定',
              callback: action => {

              }
            });
            this.getList();
    },

    //监听路由变化
    watch: {
        //路由变化的方式  路由发生变化，方法就会执行
        $route(to,from){
            this.init()
        }
    },
    methods: {
        // 根据id查询课程
        getTakeById(id){
            takeApi.getTakeInfo(id)
                .then(response => {
                    this.take = response.data.take;
                    this.teach = response.data.teach;
                })
        },
        getAllStudent(){
            studentApi.getAllStudent()
                .then(response => {
                    this.allStudent = response.data.allStudent;
                })
        },
        saveOrUpdate(){
            // 判断修改还是添加 根据take是否有id
            console.log(this.take.id)
            if(!this.take.id){
                 //添加
                this.saveTake()
            }else{
                 this.updateTakeById(this.take.id)
            }

              
        },
        // 修改课程的方法
        updateTakeById(id){
            takeApi.updateTake(id,this.take)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/take/table'})
                })
        },
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
                         this.$router.push({path:'/take/table'})
                      })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });          
            });

        },
        init(){
            // console.log(this.$route.params.id)
             // 页面渲染之前执行
            this.getAllStudent()
            if(this.$route.params && this.$route.params.id){
                // 从路径中获取id的值
                const id = this.$route.params.id
                // 调用根据id查询的方法
                this.getTakeById(id)
            }else{
                //路径没有id值，是添加操作
                //清空表单
                this.take = {}
            }
        },


        // &&&&&&&&&&&&&&&&&&&&&&&&&&
        //创建具体的方法，调用section.js定义方法
        // 开课列表的方法
        //默认查第一页
        getListControl(){
             // 判断修改还是添加 根据course是否有cid
            this.$refs['sectionQuery'].validate((valid) => {
              if (valid) {
                this.getList()
              } else {
                console.log('error submit!!')
                return false
              }
            })
        },
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
              this.list = response.data
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
}
</script>