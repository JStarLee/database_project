<template>
  <div id="aCoursesList" class="bg-fa of">
    <!-- 讲师列表 开始 -->
    <section class="container">
      <header class="comm-title all-teacher-title">
        <!-- <h2 class="fl tac">
          <span class="c-333">全部讲师</span>
        </h2>
        <section class="c-tab-title">
          <a id="subjectAll" title="全部" href="#">全部</a>
          <c:forEach var="subject" items="${subjectList }">
                            <a id="${subject.subjectId}" title="${subject.subjectName }" href="javascript:void(0)" onclick="submitForm(${subject.subjectId})">${subject.subjectName }</a>
          </c:forEach>
        </section> -->
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
          <el-button type="primary" icon="el-icon-search" @click="gotoPage(1)">查询</el-button>
          <el-button type="default" @click="resetData()">清空</el-button>
        </el-form>
      </header>
      <section class="c-sort-box unBr">
        <div>
          <!-- /无数据提示 开始-->
          <section class="no-data-wrap" v-if="data.lens==0">
            <em class="icon30 no-data-ico">&nbsp;</em>
            <span class="c-666 fsize14 ml10 vam">没有相关数据，小编正在努力整理中...</span>
          </section>
          <!-- /无数据提示 结束-->
          <article v-if="data.lens>0" class="i-teacher-list">
            <ul class="of">
              <li v-for="teacher in data.data" :key="teacher.tid">
                <section class="i-teach-wrap">
                  <div class="i-teach-pic">
                    <a :href="'/teacher/'+teacher.tid" :title="teacher.name" target="_blank">
                      <img :src="teacher.photo" :alt="teacher.name">
                    </a>
                  </div>
                  <div class="mt10 hLh30 txtOf tac">
                    <a :href="'/teacher/'+teacher.tid" :title="teacher.name" target="_blank" class="fsize18 c-666">{{teacher.name}}</a>
                  </div>
                  <div class="mt10 hLh30 txtOf tac">
                    <span class="fsize14 c-999">擅长：{{{'':'','1':'楷书','2':'行书'}[teacher.be_good_at]}}</span>
                  </div>
                  <div class="hLh30 txtOf tac">
                    <span class="fsize14 c-999">{{teacher.intro}}</span>
                  </div>
                  <!-- <div class="mt15 i-q-txt">
                    <p class="c-999 f-fA">{{teacher.career}}</p>
                  </div> -->
                </section>
              </li>
              
            </ul>
            <div class="clear"></div>
          </article>
        </div>
        <!-- 公共分页 开始 -->
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
      <!-- 公共分页 结束 -->
        <!-- 公共分页 结束 -->
      </section>
    </section>
    <!-- /讲师列表 结束 -->
  </div>
</template>
<script>

import teacherApi from '@/api/teacher'
export default {
    //使用异步调用
     //异步调用，调用一次
  //params: 相当于之前 this.$route.params.id  等价  params.id
    // asyncData({params,error}){
    //   return teacherApi.getTeacherList(1,8,{})
    //       .then(response => {
    //         //this.data = response.data.data
    //         console.log(response.data.data.page)
    //          return  {data: response.data.data.page}
    //       })
    // },

    //异步调用，调用一次
  //params: 相当于之前 this.$route.params.id  等价  params.id
  // asyncData({ params, error }) {
  //   return teacherApi.getTeacherList(1,8,{}).then(response => {
  //         //this.data = response.data.data
  //         return { data: response }
  //      })
  // },
      data() {
        return {
          page:1, //当前页
          data:{},  //列表
          teacherQuery:{}
        }
      },
  created() {
    //课程第一次查询
    this.initTeacherFirst()
  },
    methods: {
      //分页切换的方法
    //参数是页码数
        //1 查询第一页数据
    initTeacherFirst() {
      teacherApi.getTeacherList(1,8,this.teacherQuery).then(response => {
        this.data = response.data
        console.log(this.data)
      })
    },

    gotoPage(page) {
        teacherApi.getTeacherList(page,8,this.teacherQuery)
          .then(response => {
            this.data = response.data
          })
      },
      resetData() {
      //表单输入项数据清空
      this.teacherQuery = {}

      //查询所有教师数据
      this.gotoPage(1)
    }
  },
    

};
</script>