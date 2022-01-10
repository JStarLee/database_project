<template>
  <div class="app-container">
     <el-form label-width="120px" ref="course" :model="course" :rules="rules">    
      <el-form-item label="课程名称" prop='name'>
        <el-input v-model="course.name"/>
      </el-form-item>
      <el-form-item label="先导课程" prop='fcourse'>
        <el-autocomplete
          v-model="course.fcourse"
          :fetch-suggestions="querySearchCourse"
          class="inline-input"
          placeholder="请输入课程号或名称"
          @select="handleSelect"
          >
          <template #default="{ item }">
            <span>{{ item.value }}</span>
            <span>——</span>
            <span >{{ item.link }}</span>
          </template>
        </el-autocomplete>
      </el-form-item>

      <el-form-item label="课程简介" prop='intro'>
        <el-input v-model="course.intro" :rows="10" type="textarea"/>
      </el-form-item>

      <!-- 课程头像：TODO -->

        <!-- 课程头像 -->
      <el-form-item label="课程图片">
        <!-- 头衔缩略图 -->
        <pan-thumb :image="course.photo"/>
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
import courseApi from "@/api/edu/course";
import ImageCropper from '@/components/ImageCropper'
import PanThumb from '@/components/PanThumb'

export default {

  components: {ImageCropper,PanThumb},
    data(){
        const isExist = (rule, value, callback)=>{
          if(value==null||value==undefined||value==''){
            callback()
          }
          for (var i=0;i<this.allCourse.length;i++){
            if(value == this.allCourse[i]['cid']){
              callback()
            }
          }
          callback(new Error('输入的课序号不存在'))
        }
        return{
            course: {
                cid: '',
                name: '',
                fcourse:'',
                intro: '',
                photo: ''
            },
            allCourse:{},
            rules: {
              name:[
                {required:true,message:'课程名不能为空 ',trigger:'blur'},
                {min:2,max:10,message:'课程名长度应介于2和10之间',trigger:'blur'},
              ],
              fcourse:[
                {min:5, max:5,message:'课序号长度应为五位',trigger:'blur'},
                {validator: isExist ,trigger:'blur'}
              ],
              intro: [
                {required:true,message:'课程介绍不能为空',trigger:'blur'},
                {min:1,max:200,message:'介绍长度不超过200字',trigger:'blur'},
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
          this.course.photo = data.url
          //每次上传成功后，key变化
          this.imagecropperKey = this.imagecropperKey + 1
        },

        // 根据id查询课程
        getCourseById(cid){
            courseApi.getCourseInfo(cid)
                .then(response => {
                    this.course = response.data.course;
                })
        },
        getAllCourse(){
            courseApi.getAllCourse()
                .then(response => {
                    this.allCourse = response.data.allCourse;
                })
        },

        saveOrUpdate(){
            // 判断修改还是添加 根据course是否有cid
            this.$refs['course'].validate((valid) => {
              if (valid) {
                if(!this.course.cid){
                    //添加
                    this.saveCourse()
                }else{
                    this.updateCourseById(this.course.cid)
                } 
              } else {
                console.log('error submit!!')
                return false
              }
            })
              
        },

        // 修改课程的方法
        updateCourseById(cid){
            courseApi.updateCourse(cid,this.course)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/course/table'})
                })
        },

        saveCourse(){
            courseApi.addCourse(this.course)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '添加成功！'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/course/table'})
                      })
        },

        init(){
            // console.log(this.$route.params.cid)
             // 页面渲染之前执行
            this.getAllCourse()
            if(this.$route.params && this.$route.params.cid){
                // 从路径中获取cid的值
                const cid = this.$route.params.cid
                // 调用根据cid查询的方法
                this.getCourseById(cid)
            }else{
                //路径没有cid值，是添加操作
                //清空表单
                this.course = {intro:'精品书法课程'}
            }
        },

        //################################################
        //所有的方法都要写在methods里面
        querySearchCourse(queryString, cb) {
        //在这里为这个数组中每一个对象加一个value字段, 因为autocomplete只识别value字段并在下拉列中显示，所以我从新封装了

          let programs = this.allCourse;
          let programList = [];
          for(let i=0;i<programs.length;i++){
            programList.push({'Truevalue':programs[i].cid +' '+'-'+' '+programs[i].name,'value':programs[i].cid,'link':programs[i].name})

          }
            console.log(queryString)
            let results = queryString ? programList.filter(this.createStateFilter(queryString)) : programList;
        //基本思路就是实现一个过滤器，过滤存在你输入字段的所有数据。
          clearTimeout(this.timeout);
              this.timeout = setTimeout(() => {
                cb(results);
              }, 1000 * Math.random());
          },
          createStateFilter(queryString) {
            return (program) => {
              return (program.Truevalue.toLowerCase().indexOf(queryString.toLowerCase()) !== -1);
            };
          },
          handleSelect(item) {
            // this.event.programCode = item.value
            console.log('this.event.programCode')
          }
          //hangdleSelect你选中那行，item就就是那那条数据，直接赋值v-modal就实现回显了。
    }
}
</script>