<template>
  <div class="app-container">
     <el-form label-width="120px" ref="student" :model="student" :rules="rules">
      <el-form-item label="学生名称" prop='name'>
        <el-input v-model="student.name"/>
      </el-form-item>

      <el-form-item label="性别" prop='sex'>
        <el-select v-model="student.sex" clearable placeholder="请选择">
          <el-option :value="'1'" label="男"/>
          <el-option :value="'2'" label="女"/>
        </el-select>
      </el-form-item>

      <el-form-item label="学生简介" prop='intro'>
        <el-input v-model="student.intro" :rows="10" type="textarea"/>
      </el-form-item>

      <!-- 学生头像：TODO -->

        <!-- 学生头像 -->
      <el-form-item label="学生照片">

          <!-- 头衔缩略图 -->
          <pan-thumb :image="student.photo"/>
          <!-- 文件上传按钮 -->
          <el-button type="primary" icon="el-icon-upload" @click="imagecropperShow=true">更换头像
          </el-button>

          <!--
            v-show：是否显示上传组件
            :key：类似于id，如果一个页面多个图片上传控件，可以做区分
            :url：后台上传的url地址
            @close：关闭上传组件
            @crop-upload-success：上传成功后的回调 
              <input type="file" name="file"/>
          -->
          <image-cropper
            v-show="imagecropperShow"
            :width="500"
            :height="500"
            :key="imagecropperKey"  
            :url="BASE_API+'/edu/photo'"
            field="file"
            @close="close"
            @crop-upload-success="cropSuccess"
          />
      </el-form-item>

      <el-form-item>
        <el-button :disabled="saveBtnDisabled" type="primary" @click="saveOrUpdate">保存</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>


<script>
import studentApi from "@/api/edu/student";
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'

export default {

  components: {ImageCropper,PanThumb},
    data(){
        return{
            student: {
                name: '',
                sex:'',
                be_good_at:'',
                intro: '',
                photo:''
            },
            rules: {
              name:[
                {required:true,message:'学生名不能为空 ',trigger:'blur'},
                {min:2,max:10,message:'学生名长度应介于2和10之间',trigger:'blur'},
              ],
              sex:[
                {required:true,message:'性别不能为空',trigger:'change'}
              ],
              intro: [
                {required:true,message:'学生介绍不能为空',trigger:'blur'},
                {min:1,max:200,message:'介绍长度不超过200',trigger:'blur'},
              ],
              photo: []
            },
            imagecropperShow: false,
            //上传组件的唯一标识
            imagecropperKey: 0, 
            // 保存按钮是否禁用
            saveBtnDisabled: false,
            // 获取BASE_API的值
            BASE_API: process.env.VUE_APP_BASE_API,
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
    }
    ,

    methods: {
      // 关闭上传弹窗的方法
          close(){
            this.imagecropperShow = false

            //上传组件初始化
            this.imagecropperKey = this.imagecropperKey + 1
          },
        // 上传成功的方法
        cropSuccess(data){

          //关闭弹框
          this.imagecropperShow = false;
          // 上传之后接口返回的图片地址
          this.student.photo = data.url
          //每次上传成功后，key变化
          this.imagecropperKey = this.imagecropperKey + 1
        },

        // 根据id查询学生
        getStudentById(sid){
            studentApi.getStudentInfo(sid)
                .then(response => {
                    // console.log("hhhhh")
                    // console.log(response.data.student)
                    this.student = response.data.student;
                })
        },

        saveOrUpdate(){
            // 判断修改还是添加 根据student是否有sid
            // console.log(this.student.sid)
            this.$refs['student'].validate((valid) => {
              if (valid) {
                if(!this.student.sid){
                    //添加
                    this.saveStudent()
                }else{
                    this.updateStudentById(this.student.sid)
                } 
              } else {
                console.log('error submit!!')
                return false
              }
            })
   
        },

        // 修改学生的方法
        updateStudentById(sid){
            studentApi.updateStudent(sid,this.student)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/student/table'})
                })
        },

      
    

        saveStudent(){
            studentApi.addStudent(this.student)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '添加成功！'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/student/table'})
                      })
        },

        init(){
             // 页面渲染之前执行
            if(this.$route.params && this.$route.params.sid){
                // 从路径中获取sid的值
                const sid = this.$route.params.sid
                // 调用根据sid查询的方法
                this.getStudentById(sid)
            }else{
                //路径没有sid值，是添加操作
                //清空表单
                this.student = {intro:'书法爱好者一名~'}
            }
        }
    }
}
</script>