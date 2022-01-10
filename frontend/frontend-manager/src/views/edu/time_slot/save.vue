<template>
  <div class="app-container">
     <el-form label-width="120px">    
     <!-- <el-form label-width="120px">     -->
        <el-form-item label="课段一" style="margin-right:8px" >
            <el-time-select
                v-model="time_slot[0].start"
                placeholder="Start time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00', 
                    maxTime: time_slot[0].end
                }"
            >
            </el-time-select>
            <el-time-select
                v-model="time_slot[0].end"
                placeholder="End time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00',
                    minTime: time_slot[0].start,
                    maxTime: time_slot[1].start
                }"
            >
            </el-time-select>
        </el-form-item>
        
        <el-form-item label="课段二" style="margin-right:8px">
            <el-time-select
                v-model="time_slot[1].start"
                placeholder="Start time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00', 
                    minTime: time_slot[0].end,
                    maxTime: time_slot[1].end
                }"
            >
            </el-time-select>
            <el-time-select
                v-model="time_slot[1].end"
                placeholder="End time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00',
                    minTime: time_slot[1].start,
                    maxTime: time_slot[2].start
                }"
            >
            </el-time-select>
        </el-form-item>
        <el-form-item label="课段三" style="margin-right:8px"> 
            <el-time-select
                v-model="time_slot[2].start"
                placeholder="Start time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00', 
                    minTime: time_slot[1].end,                    
                    maxTime: time_slot[2].end
                }"
            >
            </el-time-select>
            <el-time-select
                v-model="time_slot[2].end"
                placeholder="End time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00',
                    minTime: time_slot[2].start,
                    maxTime: time_slot[3].start
                }"
            >
            </el-time-select>
        </el-form-item>

        <el-form-item label="课段四" style="margin-right:8px">
            <el-time-select
                v-model="time_slot[3].start"
                placeholder="Start time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00', 
                    minTime: time_slot[2].end,
                    maxTime: time_slot[3].end
                }"
            >
            </el-time-select>
            <el-time-select
                v-model="time_slot[3].end"
                placeholder="End time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00',
                    minTime: time_slot[3].start,
                    maxTime: time_slot[4].start
                }"
            >
            </el-time-select>
        </el-form-item>

        <el-form-item label="课段五" style="margin-right:8px">
            <el-time-select
                v-model="time_slot[4].start"
                placeholder="Start time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00', 
                    minTime: time_slot[3].end,
                    maxTime: time_slot[4].end
                }"
            >
            </el-time-select>
            <el-time-select
                v-model="time_slot[4].end"
                placeholder="End time"
                :picker-options="{
                    start:'08:00',
                    step:'00:15',
                    end:'21:00',
                    minTime: time_slot[4].start,
                }"
            >
            </el-time-select>
        </el-form-item>

      <el-form-item>
        <el-button :disabled="saveBtnDisabled" type="primary" @click="updateTime_slot">保存</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>


<script>
import time_slotApi from "@/api/edu/time_slot";

export default {
    data(){

        return{
            startTime:'',endTime:'',
            time_slot: [
                {start:'',end:''},
                {start:'',end:''},
                {start:'',end:''},
                {start:'',end:''},
                {start:'',end:''},
            ],
            rules:{
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

        // 根据查询所有时间段
        getAllTime_slot(){
            time_slotApi.getAllTime_slot()
                .then(response => {
                    this.time_slot = response.data.time_slot;
                    console.log(this.time_slot[0])

                    console.log(this.time_slot[0]['start'])
                })
        },

        // 修改开课时间段的方法
        updateTime_slot(){
            console.log(this.time_slot)
            for(let i=0;i<this.time_slot.length;i=i+1){
                console.log(this.time_slot[i])
                if(this.time_slot[i]['start']==''||this.time_slot[i]['start']==null||this.time_slot[i]['start']==undefined
                ||this.time_slot[i]['end']==''||this.time_slot[i]['end']==null||this.time_slot[i]['end']==undefined
                ){
                    
                    this.$message.error('时间不能为空')
                    return;
                }
            }
            time_slotApi.updateTime_slot(this.time_slot)
                //添加成功
                .then(response => {
                    //提示成功
                this.$message({
                    type: 'success',
                    message: '修改成功！'
                })
                    //回到列表页面  路由跳转
                    this.$router.push({path:'/time_slot/table'})
                })
        },

        init(){
            // 页面渲染之前执行
            this.getAllTime_slot()
            console.log('jjjjjjjjafiuj')

        }
    }
}
</script>