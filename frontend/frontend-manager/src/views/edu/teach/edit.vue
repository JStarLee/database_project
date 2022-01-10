<template>
  <div class="app-container">
     <el-form label-width="120px" ref="teach" :model="teach" :rules="rules">    
      <el-form-item label="开课号">
        <el-input v-model="teach.section"/>
      </el-form-item>
      <el-form-item label="教师号">
        <el-input v-model="teach.Teacher" />
      </el-form-item>
      <el-form-item label="状态">
        <el-input v-model="teach.status" />
      </el-form-item>
      <el-form-item>
        <el-button :disabled="saveBtnDisabled" type="primary" @click="saveOrUpdate">保存</el-button>
      </el-form-item>
    </el-form>
     

  </div>
</template>
<script>
import teachApi from "@/api/edu/teach";

export default {
    data(){
        return{
            teach: {
                Teacher:'',
                section:'',
                status:'',
            },
            rules: {
           },
            // 保存按钮是否禁用
            saveBtnDisabled: false,

        }
    },
    
    created(){
            this.init()     
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
        getTeachById(id){
            teachApi.getTeachInfo(id)
                .then(response => {
                    this.teach = response.data.teach;
                })
        },
        saveOrUpdate(){
            // 判断修改还是添加 根据teach是否有id
            console.log(this.teach.id)
            if(!this.teach.id){
                 //添加
                this.saveTeach()
            }else{
                 this.updateTeachById(this.teach.id)
            }

              
        },
        // 修改课程的方法
        updateTeachById(id){
            teachApi.updateTeach(id,this.teach)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/teach/table'})
                })
        },
        saveTeach(){
            teachApi.addTeach(this.teach)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '添加成功！'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/teach/table'})
                      })
        },
        init(){
            // console.log(this.$route.params.id)
             // 页面渲染之前执行
            if(this.$route.params && this.$route.params.id){
                // 从路径中获取id的值
                const id = this.$route.params.id
                // 调用根据id查询的方法
                this.getTeachById(id)
            }else{
                //路径没有id值，是添加操作
                //清空表单
                this.teach = {}
            }
        }
    }
}
</script>