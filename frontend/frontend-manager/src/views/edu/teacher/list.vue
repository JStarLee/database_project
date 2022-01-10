<template>
  <div class="app-container">
    <!--查询表单-->
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="teacherQuery.name" placeholder="教师名" />
      </el-form-item>
      <el-form-item>
        <el-select v-model="teacherQuery.sex" clearable placeholder="性别">
          <el-option :value="'1'" label="男" />
          <el-option :value="'2'" label="女" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="teacherQuery.be_good_at" clearable placeholder="擅长字体">
          <el-option :value="'1'" label="楷书" />
          <el-option :value="'2'" label="行书" />
        </el-select>
      </el-form-item>
      <el-button type="primary" icon="el-icon-search" @click="getList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

    <!-- 数据列表 -->
    <el-table :data="list" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="70">
        <template slot-scope="scope">{{(page-1) * size + scope.$index + 1}}</template>
      </el-table-column>

      <el-table-column prop="tid" label="教师号" width="80" />

      <el-table-column prop="name" label="教师名" width="80" />

      <el-table-column align="center" label="擅长字体" width="80">
        <template slot-scope="scope">{{{'':'','1':'楷书','2':'行书'}[scope.row.be_good_at]}}</template>
      </el-table-column  >

      <el-table-column align="center" label="性别" width="80">
        <template slot-scope="scope">{{{'':'','1':'男','2':'女'}[scope.row.sex]}}</template>      
      </el-table-column  >

      <el-table-column prop="intro" label="介绍" />

      <el-table-column prop="admission_time" label="添加时间" width="160" />

      <el-table-column label="操作" width="200">
        <template slot-scope="scope">
        <router-link :to=" '/teacher/edit/'+scope.row.tid">
            <el-button type="primary" size="mini" icon="el-icon-edit">修改</el-button>
        </router-link>
          <el-button    type="danger" size="mini" icon="el-icon-delete" @click="removeDataById(scope.row.tid)" >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      :currentPage="page"
      :page-size="size"
      :total="total"
      style="padding: 30px 0; text-align: center;"
      layout="total, prev, pager, next, jumper"
      @current-change="getList"
    />
  </div>
</template>


<script>
//第一步，引入调用teacher.js文件

import teacher from "@/api/edu/teacher";
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
      teacherQuery: {} //条件封装对象
    };
  },

  created() {
    //页面渲染之前执行，一般是调用methods定义的方法
    //调用
    this.getList();
  },

  methods: {
    //创建具体的方法，调用teacher.js定义方法
    // 教师列表的方法
    //默认查第一页
    getList(page = 1) {
      this.page = page;
      teacher
        .getTeacherListPage(this.page, this.size, this.teacherQuery)
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
      this.teacherQuery = {};

      //查询所有教师数据
      this.getList();
    },

    // 删除教师的方法
    removeDataById(tid) {
      this.$confirm("此操作将永久删除教师记录, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        // 点击确定，执行then
        .then(() => {
          // 调用删除的方法
          teacher.deleteByTeacherId(tid)
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