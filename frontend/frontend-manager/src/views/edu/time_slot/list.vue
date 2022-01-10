<template>
  <div class="app-container">
    <span width="100" style="display:inline"></span>
    <el-table 
      :data="list.time_slot_id" border fit highlight-current-row  
      style="font-size:18px"
    >
      <el-table-column align="center" prop="0" label="时段"/>
      <el-table-column align="center" prop="1" :label=list.day[0] width="200" />
      <el-table-column align="center" prop="2" :label=list.day[1] width="200" />
      <el-table-column align="center" prop="3" :label=list.day[2] width="200" />
      <el-table-column align="center" prop="4" :label=list.day[3] width="200" />
      <el-table-column align="center" prop="5" :label=list.day[4] width="200" />
      <el-table-column align="center" prop="6" :label=list.day[5] width="200" />
      <el-table-column align="center" prop="7" :label=list.day[6] width="200" />

    </el-table>

  </div>
</template>


<script>
//第一步，引入调用time_slot.js文件

import time_slot from "@/api/edu/time_slot";
export default {
  //写核心代码的位置

  //固定结构

  data() {
    //定义变量和初始值
    return {
      list: null, //查询之后接口返回的数据
    };
  },

  created() {
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    this.getList();
  },

  methods: {
    //创建具体的方法，调用time_slot.js定义方法
    // 开课时间列表的方法
    getList() {
      time_slot
        .getTime_slotList()
        .then(response => {
          //请求成功
          this.list = response.data
        })
        .catch(error => {
          //请求失败
          console.log(error);
        });
    },
      arraySpanMethod({ row, column, rowIndex, columnIndex }) {
          if (columnIndex === 0&&rowIndex===0) {
            return [5, 1];
          }else if(columnIndex===0){
            return [0,0]
          }

      },
  }
};
</script>