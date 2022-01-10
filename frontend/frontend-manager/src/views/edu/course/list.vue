<template>
  <div class="app-container">
    <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="courseQuery.cid" placeholder="课程号" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="courseQuery.name" placeholder="课程名" />
      </el-form-item>
      <el-form-item>
        <el-input v-model="courseQuery.fcourse" placeholder="先导课程号" />
      </el-form-item>

      <el-button type="primary" icon="el-icon-search" @click="getList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

    <!-- 数据列表 -->
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="70">
        <template slot-scope="scope">{{(page-1) * size + scope.$index + 1}}</template>
      </el-table-column>
      <el-table-column prop="cid" label="课程号" width="80" />
      <el-table-column prop="name" label="课程名" width="100" />
      <el-table-column prop="fcourse.cid" label="先导课程号" width="100" />
      <el-table-column prop="fcourse.name" label="先导课程名" width="100" />
      <el-table-column prop="choosed_sum" label="已选总人数" width="100"/>

      <el-table-column prop="intro" label="介绍" />

      <el-table-column prop="admission_time" label="添加时间" width="160" />

      <el-table-column label="操作" width="200">
        <template slot-scope="scope">
        <router-link :to=" '/course/edit/'+scope.row.cid">
            <el-button type="primary" size="mini" icon="el-icon-edit">修改</el-button>
        </router-link>
          <el-button    type="danger" size="mini" icon="el-icon-delete" @click="removeDataById(scope.row.cid)" >删除</el-button>
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
//第一步，引入调用course.js文件

import course from "@/api/edu/course";
export default {
  //写核心代码的位置

  data() {
    //定义变量和初始值
    return {
      list: null, //查询之后接口返回的数据
      page: 1, //当前页
      size: 5, //每页记录数
      total: 0, //总记录数
      courseQuery: {} //条件封装对象
    };
  },

  created() {
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    this.getList();
  },

  methods: {
    //创建具体的方法，调用course.js定义方法
    // 课程列表的方法
    //默认查第一页
    getList(page = 1) {
      this.page = page;
      course
        .getCourseListPage(this.page, this.size, this.courseQuery)
        .then(response => {
          //请求成功
          //response接口返回的数据
          //  console.log(reponse)

          // this.list = response.data.rows;
          this.list = response.data
          // this.total = response.data.total;
          this.total = response.lens;


            // console.log(this.list)
            // console.log(this.total)
        })
        .catch(error => {
          //请求失败
          console.log(error);
        });
    },

    // 清空的方法
    resetData() {
      //表单输入项数据清空
      this.courseQuery = {};

      //查询所有课程数据
      this.getList();
    },

    // 删除课程的方法
    removeDataById(cid) {
      this.$confirm("此操作将永久删除课程记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        // 点击确定，执行then
        .then(() => {
          // 调用删除的方法
          course.deleteByCourseId(cid)
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