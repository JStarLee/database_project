<template>
  <div class="app-container">
    <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="sectionQuery.Course_name" placeholder="课程名" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="sectionQuery.Teacher_name" placeholder="教师名" />
      </el-form-item>
      <el-form-item>
        <el-date-picker
          v-model="sectionQuery.start_end"
          type="datetimerange"
          range-separator="To"
          start-placeholder="开课日期"
          end-placeholder="结课日期"
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
        <router-link :to=" '/section/edit/'+scope.row.sec_id">
            <el-button type="primary" size="mini" icon="el-icon-edit">修改</el-button>
        </router-link>
          <el-button    type="danger" size="mini" icon="el-icon-delete" @click="removeDataById(scope.row.sec_id)" >删除</el-button>
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
//第一步，引入调用section.js文件

import section from "@/api/edu/section";
export default {
  //写核心代码的位置

  //固定结构

  data() {
    //定义变量和初始值
    return {
      list: null, //查询之后接口返回的数据
      page: 1, //当前页
      size: 5, //每页记录数
      total: 0, //总记录数
      sectionQuery: {} //条件封装对象
    };
  },

  created() {
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    this.getList();
  },

  methods: {
    //创建具体的方法，调用section.js定义方法
    // 开课列表的方法
    //默认查第一页
    getList(page = 1) {
      this.page = page;
      section
        .getSectionListPage(this.page, this.size, this.sectionQuery)
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

    // 删除开课的方法
    removeDataById(sec_id) {
      this.$confirm("此操作将永久删除开课记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        // 点击确定，执行then
        .then(() => {
          // 调用删除的方法
          section.deleteBySectionId(sec_id)
            // 删除成功
            .then(response => {
              this.$message({
                type: "success",
                message: "删除成功!"
              });
              //回到列表页面
              this.getList();
            });
        });
    }
  }
};
</script>