<template>
  <div class="app-container">
     <el-form label-width="120px" ref="section" :model="section" :rules="rules">    

      <el-form-item label="课程号" prop='Course'>
        <el-input v-model="section.Course"/>
      </el-form-item>

      <el-form-item label="课容量" prop='capacity' :disabled="updateFlag">
        <el-input v-model="section.capacity" />
      </el-form-item>
      <el-form-item label="开课-结课时间" prop='start_end'>
        <el-date-picker
          v-model="section.start_end"
          type="datetimerange"
          range-starseparator="To"
          t-placeholder="Start date"
          end-placeholder="End date"
          value-format="yyyy-MM-dd"
        >
        </el-date-picker>
      </el-form-item>

      <el-form-item label="教室" prop='classroom'>
        <el-autocomplete
          v-model="section.classroom"
          :fetch-suggestions="querySearchAsync"
          class="inline-input"
          placeholder="请输入教室编号或地址"
          @select="handleSelect"
          >
          <template #default="{ item }">
            <span>{{ item.value }}</span>
            <span>——</span>
            <span >{{ item.link }}</span>
          </template>
        </el-autocomplete>
      </el-form-item>

      <el-form-item label="时间段" prop='time_slot'>
        <el-transfer
          style="text-align: left; display: inline-block"
          v-model="section.time_slot"
          filterable
          :titles="['Source', 'Target']"
          :button-texts="['到左边', '到右边']"
          :format="{
            noChecked: '${total}',
            hasChecked: '${checked}/${total}'
          }"
          @change="handleChange"
          :data="time_slot_select">
          <span slot-scope="{ option }">{{ option.key }}</span>
          <!-- <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>
          <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button> -->
        </el-transfer>
      </el-form-item>
         
      <el-form-item>
        <el-button :disabled="saveBtnDisabled" type="primary" @click="saveOrUpdate">保存</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>


<script>
import sectionApi from "@/api/edu/section";
import classroomApi from "@/api/edu/classroom";
import courseApi from "@/api/edu/course";
import time_slotApi from "@/api/edu/time_slot";



export default {
  
    data(){
       const courseIsExist = (rule, value, callback)=>{
        if(value==null||value==undefined||value==''){
          callback(new Error('课程号不为空'))
        }  
        for (var i=0;i<this.allCourse.length;i++){
          if(value == this.allCourse[i]['cid']){
            callback()
          }
        }
        callback(new Error('输入的课序号不存在'))
      }
      const classroomIsExist = (rule, value, callback)=>{
        if(value==null||value==undefined||value==''){
          callback(new Error('教室号不为空'))
        }  
        for (var i=0;i<this.allClassroom.length;i++){
          if(value == this.allClassroom[i]['classroom_id']){
            callback()
          }
        }
        callback(new Error('输入的教室号不存在'))
      }
        return{
            updateFlag:'',
            section: {
                sec_id:'',
                Course: '',
                classroom:'',
                choosed:'',
                capacity:'',
                start:'',
                end:'',
                start_end:'',
                time_slot:'',
            },
            time_slot_select: [],
            value4: [],
            section_time_slot_first:'',
            section_time_slot_second:'',
            allCourse:{},
            rules: {
                Course:[
                  {required:true,message:'课程号不为空 ',trigger:'blur'},
                  {min:5,max:5,message:'课程号必须为五位数字',trigger:'blur'},
                  {validator: courseIsExist ,message:'课程不存在',trigger:'blur'},
              ],
                capacity:[
                  {required:true,message:'课容量不为空 ',trigger:'blur'},
                ],
                start_end:[
                  {required:true,message:'开课时间不为空 ',trigger:'blur'},
                ],
                classroom:[
                  {required:true,message:'教室号不为空 ',trigger:'blur'},
                  {min:1,max:4,message:'教室号长度不超过4',trigger:'blur'},
                  {validator: classroomIsExist ,message:'教室不存在',trigger:'blur'},
                  //坑：保证这种
              ],
           },
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
    }
    ,

    methods: {
        getAllClassroom(){
          classroomApi.getAllClassroom()
              .then(response => {
                  this.allClassroom = response.data.classroom
              })
        },
        getAllTime_slot_select(){
          time_slotApi.getAllTime_slotSelect()
              .then(response => {
                  for (let i = 1; i <= (response.data.time_slot).length; i++) {
                    this.time_slot_select.push({
                      key: response.data.time_slot[i]["time_slot_id"],
                    });
                  }
              })
        },
        // 根据sec_id查询开课
        getSectionById(sec_id){
            sectionApi.getSectionInfo(sec_id)
                .then(response => {
                    // console.log("hhhhh")
                    // console.log(response.data.section)
                    this.section = response.data.section;
                    this.$set(this.section,'start_end',[this.section.start,this.section.end])
                })
        },
        getAllCourse(){
            courseApi.getAllCourse()
                .then(response => {
                    this.allCourse = response.data.allCourse;
                })
        },

        saveOrUpdate(){
            // 判断修改还是添加 根据section是否有sec_id

            this.$refs['section'].validate((valid) => {
              if (valid) { 
                if(!this.section.sec_id){
                    this.saveSection()
                }else{
                    this.updateSectionById(this.section.sec_id)
                }
              } else {
                console.log('error submit!!')
                return false
              }
            })                          
        },

        // 修改开课的方法
        updateSectionById(sec_id){
            sectionApi.updateSection(sec_id,this.section)
                .then(response => {
                    // 提示信息
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })

                     //回到列表页面  路由跳转
                    this.$router.push({path:'/section/table'})
                })
        },

        saveSection(){
            sectionApi.addSection(this.section)
                      //添加成功
                      .then(response => {
                          //提示成功
                        this.$message({
                            type: 'success',
                            message: '添加成功！'
                        })
                         //回到列表页面  路由跳转
                         this.$router.push({path:'/section/table'})
                      })
        },

        init(){
            // console.log(this.$route.params.sec_id)
             // 页面渲染之前执行
            this.getAllCourse();
            this.getAllClassroom();
            this.getAllTime_slot_select();
            console.log(this.allCourse)
            if(this.$route.params && this.$route.params.sec_id){
                // 从路径中获取tid的值
                const sec_id = this.$route.params.sec_id
                // 调用根据tid查询的方法
                this.getSectionById(sec_id)
                this.updateFlag=true
            }else{
                //路径没有tid值，是添加操作
                //清空表单
                this.section = {}
                this.updateFlag=false
            }
        },

        //所有的方法都要写在methods里面
        querySearchAsync(queryString, cb) {
        //在这里为这个数组中每一个对象加一个value字段, 因为autocomplete只识别value字段并在下拉列中显示，所以我从新封装了

          let programs = this.allClassroom;
          let programList = [];
          for(let i=0;i<programs.length;i++){
            // programList.push({'value':programs[i].classroom_id +' '+'-'+' '+programs[i].address})
            // programList.push({'value':programs[i].classroom_id ,'link':programs[i].address})
            programList.push({'Truevalue':programs[i].classroom_id +' '+'-'+' '+programs[i].address,'value':programs[i].classroom_id,'link':programs[i].address})

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
          },
          //hangdleSelect你选中那行，item就就是那那条数据，直接赋值v-modal就实现回显了。
          handleChange(value, direction, movedKeys) {
            // console.log(value, direction, movedKeys);
          }
    }
}
</script>

