<template>
  <div class="app-container">
    <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="takeQuery.section_id" placeholder="开课号" />
    </el-form-item>
          <el-form-item>
      <el-input v-model="takeQuery.student_id" placeholder="学号" />
    </el-form-item>
      <!-- <el-form-item label="添加时间">
        <el-date-picker
          v-model="takeQuery.begin"
          type="datetime"
          placeholder="选择开始时间"
          value-format="yyyy-MM-dd HH:mm:ss"
          default-time="00:00:00"
        />
      </el-form-item>
      <el-form-item>
        <el-date-picker
          v-model="takeQuery.end"
          type="datetime"
          placeholder="选择截止时间"
          value-format="yyyy-MM-dd HH:mm:ss"
          default-time="00:00:00"
        />
      </el-form-item> -->

      <el-button type="primary" icon="el-icon-search" @click="getList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

    <!-- 数据列表 -->
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="100">
        <template slot-scope="scope">{{(page-1) * size + scope.$index + 1}}</template>
      </el-table-column>
      <el-table-column prop="section.sec_id" label="开课号" width="200" />
      <el-table-column prop="section.Course.cid" label="课程号" width="200" />
      <el-table-column prop="section.Course.name" label="课程名" width="200" />
      
      <el-table-column prop="Student.sid" label="学号" width="200" />
      <el-table-column prop="Student.name" label="姓名" width="200" />

      <el-table-column prop="status" label="状态"/>

      <el-table-column label="操作" width="300">
        <template slot-scope="scope">
        <!-- <router-link :to=" '/take/edit/'+scope.row.id"> -->
            <el-button type="primary" size="mini" icon="el-icon-edit" disabled>修改</el-button>
        <!-- </router-link> -->
          <el-button    type="danger" size="mini" icon="el-icon-delete" @click="removeDataById(scope.row.id)" >删除</el-button>
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
//第一步，引入调用take.js文件

import take from "@/api/edu/take";
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
      takeQuery: {} //条件封装对象
    };
  },

  created() {
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    this.getList();
  },

  methods: {
    //创建具体的方法，调用take.js定义方法
    // 选课列表的方法
    //默认查第一页
    getList(page = 1) {
      this.page = page;
      take
        .getTakeListPage(this.page, this.size, this.takeQuery)
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
      this.takeQuery = {};

      //查询所有选课数据
      this.getList();
    },

    // 删除选课的方法
    removeDataById(id) {
      this.$confirm("此操作将永久删除选课记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        // 点击确定，执行then
        .then(() => {
          // 调用删除的方法
          take.deleteByTakeId(id)
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