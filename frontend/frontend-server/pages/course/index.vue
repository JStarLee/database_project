<template>
  <div id="aCoursesList" class="bg-fa of">
    <!-- /课程列表 开始 -->
    <section class="container">
      <header class="comm-title">
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

          <el-button type="primary" icon="el-icon-search" @click="gotoPage(1)">查询</el-button>
          <el-button type="default" @click="resetData()">清空</el-button>
        </el-form>
      </header>
      <section class="c-sort-box">
        <div class="mt40">
          <!-- /无数据提示 开始-->
          <section class="no-data-wrap" v-if="data.lens==0">
            <em class="icon30 no-data-ico">&nbsp;</em>
            <span class="c-666 fsize14 ml10 vam">没有相关数据，小编正在努力整理中...</span>
          </section>
          <!-- /无数据提示 结束-->
          <article  v-if="data.lens>0" class="comm-course-list">
            <ul class="of" id="bna">
              <li v-for="course in data.data" :key="course.cid">
                <div class="cc-l-wrap">
                  <section class="course-img">
                    <img :src="course.photo" class="img-responsive" :alt="course.name">
                    <div class="cc-mask">
                      <a :href="'/course/'+course.cid" name="开始学习" class="comm-btn c-btn-1">开始学习</a>
                    </div>
                  </section>
                  <h3 class="hLh30 txtOf mt10">
                    <a :href="'/course/'+course.cid" :title="course.name" class="course-title fsize18 c-333">{{course.name}}</a>
                  </h3>
                  <div class="hLh30 txtOf mt10">
                    <span class="course-title fsize14 c-333">课程号：{{course.cid}}&nbsp;&nbsp;&nbsp;</span>
                    <span class="course-title fsize14 c-333">先导课程号：{{course.fcourse==null?'无':course.fcourse.cid}}</span>
                  </div>
                  <section class="mt10 hLh20 of">
                    <span class="fl jgAttr c-ccc f-fA">
                      <i class="c-999 f-fA">{{course.choosed_sum}}人学习</i>
                      <!-- |
                      <i class="c-999 f-fA">{{course.viewCount}}评论</i> -->
                    </span>
                  </section>
                </div>
              </li>
              
            </ul>
            <div class="clear"></div>
          </article>
        </div>
        <!-- 公共分页 开始 -->
        <div>
      <div class="paging">
        <!-- undisable这个class是否存在，取决于数据属性hasPrevious -->
        <a
          :class="{undisable: !data.hasPrevious}"
          href="#"
          title="首页"
          @click.prevent="gotoPage(1)">首页</a>
        <a
          :class="{undisable: !data.hasPrevious}"
          href="#"
          title="前一页"
          @click.prevent="gotoPage(data.current-1)">&lt;</a>
        <a
          v-for="page in data.pages"
          :key="page"
          :class="{current: data.current == page, undisable: data.current == page}"
          :title="'第'+page+'页'"
          href="#"
          @click.prevent="gotoPage(page)">{{ page }}</a>
        <a
          :class="{undisable: !data.hasNext}"
          href="#"
          title="后一页"
          @click.prevent="gotoPage(parseInt(data.current)+1)">&gt;</a>
        <a
          :class="{undisable: !data.hasNext}"
          href="#"
          title="末页"
          @click.prevent="gotoPage(data.pages)">末页</a>
        <div class="clear"/>
      </div>
    </div>
      </section>
    </section>
    <!-- /课程列表 结束 -->
  </div>
</template>
<script>
import courseApi from '@/api/course'

export default {
  data() {
    return {
      page:1, //当前页
      data:{},  //课程列表
      subjectNestedList: [], // 一级分类列表
      subSubjectList: [], // 二级分类列表
      courseQuery:{}
      // oneIndex:-1,
      // twoIndex:-1,
      // buyCountSort:"",
      // gmtCreateSort:"",
      // priceSort:""
    }
  },
  created() {
    //课程第一次查询
    this.initCourseFirst()
    // //一级分类显示
    // this.initSubject()
  },
  methods:{
    //1 查询第一页数据
    initCourseFirst() {
      // courseApi.getFrontCourseList(1,8,this.searchObj).then(response => {
      courseApi.getFrontCourseList(1,8,this.courseQuery).then(response => {

        this.data = response.data
      })
    },
    //3 分页切换的方法
    gotoPage(page) {
      // courseApi.getFrontCourseList(page,8,this.searchObj).then(response => {
      courseApi.getFrontCourseList(page,8,this.courseQuery).then(response => {

        this.data = response.data
      })
    },

    // 清空的方法
    resetData() {
      //表单输入项数据清空
      this.courseQuery = {};

      //查询所有课程数据
      this.gotoPage(1);
    },

  }
};
</script>
<style scoped>
  .active {
    background: #bdbdbd;
  }
  .hide {
    display: none;
  }
  .show {
    display: block;
  }
</style>