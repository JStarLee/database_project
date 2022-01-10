<template>
  <div class="app-container">
     <el-form label-width="120px" ref="classroom" :model="classroom" :rules="rules">    
     <el-form-item label="教室名" prop="name">
        <el-input v-model="classroom.name"/>
      </el-form-item>
      <el-form-item label="教室地址" prop="address">
        <el-input v-model="classroom.address"/>
      </el-form-item>

      <el-form-item>
        <el-button :disabled="saveBtnDisabled" type="primary" @click="saveOrUpdate">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import classroomApi from "@/api/edu/classroom";
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'

export default {
  components: {ImageCropper,PanThumb},
    data(){
        const classroomIsNotExist = (rule, value, callback)=>{
        if(value==null||value==undefined||value==''){
          callback(new Error('教室地址不为空'))
        }  
        for (var i=0;i<this.allClassroom.length;i++){
          if(value == this.allClassroom[i]['address']&&!this.classroom.classroom_id){
            callback(new Error('教室地址不能重复！'))
          }
        }
        callback()
      }
        return{
            classroom: {
                name: '',
                address: ''
            },
            rules: {
                name:[
                    {required:true,message:'教室名不能为空 ',trigger:'blur'},
                    {min:2,max:10,message:'教室名长度应介于2和10之间',trigger:'blur'},
                ],
                address: [
                    {required:true,message:'地址不能为空',trigger:'blur'},
                    {min:1,max:30,message:'地址长度不超过30',trigger:'blur'},
                    {validator: classroomIsNotExist,message:'教室地址不能重复！',trigger:'blur'},
                ],
           },

            // 保存按钮是否禁用
            saveBtnDisabled: false
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
        getAllClassroom(){
          classroomApi.getAllClassroom()
              .then(response => {
                  this.allClassroom = response.data.classroom
              })
        },
        // 根据id查询教室
        getClassroomById(classroom_id){
            classroomApi.getClassroomInfo(classroom_id)
                .then(response => {
                    this.classroom = response.data.classroom;
                })
        },
        saveOrUpdate(){
            // 判断修改还是添加 根据classroom是否有classroom_id
            this.$refs['classroom'].validate((valid) => {
              if (valid) { 
                if(!this.classroom.classroom_id){
                    this.saveClassroom()
                }else{
                    this.updateClassroomById(this.classroom.classroom_id)
                }
              } else {
                console.log('error submit!!')
                return false
              }
            })
                         
        },
        // 修改教室的方法
        updateClassroomById(classroom_id){
            classroomApi.updateClassroom(classroom_id,this.classroom)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/classroom/table'})
                })
        },
        saveClassroom(){
            classroomApi.addClassroom(this.classroom)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '添加成功！'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/classroom/table'})
                      })
        },
        init(){
            // console.log(this.$route.params.classroom_id)
             // 页面渲染之前执行
            this.getAllClassroom()
            if(this.$route.params && this.$route.params.classroom_id){
                // 从路径中获取classroom_id的值
                const classroom_id = this.$route.params.classroom_id
                // 调用根据classroom_id查询的方法
                this.getClassroomById(classroom_id)
            }else{
                //路径没有classroom_id值，是添加操作
                //清空表单
                this.classroom = {}
            }
        }
    }
}
</script>