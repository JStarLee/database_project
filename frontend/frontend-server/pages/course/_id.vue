<template>
  <div id="aCoursesList" class="bg-fa of">
    <!-- /课程详情 开始 -->
    <section class="container">
      <section class="path-wrap txtOf hLh30">
        <!-- <a href="#" title class="c-999 fsize14">首页</a> -->
        <a href="#" title class="c-999 fsize14">课程</a>

        <!-- \
        <a href="#" title class="c-999 fsize14">{{course.subjectLevelOne}}</a>
        \
        <span class="c-333 fsize14">{{course.subjectLevelTwo}}</span> -->
      </section>
      <div>
        <article class="c-v-pic-wrap" style="height: 357px;">
          <section class="p-h-video-box" id="videoPlay">
            <img height="357px" :src="course.photo" :alt="course.name" class="dis c-v-pic">
          </section>
        </article>
        <aside class="c-attr-wrap">
          <section class="ml20 mr15">
            <h2 class="hLh30 txtOf mt15">
              <span class="c-fff fsize24">{{course.name}}</span>
            </h2>
            <div class="hLh30 txtOf mt15">
              <span class="c-fff fsize16">课程号：{{course.cid}}</span>
            </div>
            <div class="hLh30 txtOf mt15">
              <span class="c-fff fsize16">先导课程号：{{course.fcourse==null?'无':course.fcourse}}</span>
            </div>
            <section class="c-attr-mt c-attr-undis" v-if="sectionList.length==0">
              <span class="c-fff fsize14">暂无开课&nbsp;&nbsp;&nbsp;</span>
            </section>
            <!-- <section class="c-attr-mt c-attr-undis" v-if="sectionList.length!=0">
              <span class="c-fff fsize14">开课情况：&nbsp;&nbsp;&nbsp;</span>
            </section>
            <section class="c-attr-mt of" v-if="sectionList.length!=0">
              <div class="ml10 vam" v-for="item in sectionList" :key="item.sec_id">
                <em class="icon18 scIcon"></em>
                <a class="c-fff vam" title="开课" :href="'/section/'+item.sec_id" >开课：{{item.sec_id}}</a>
              </div>
            </section> -->
            <br>
            <br>
            <br>
            <br>
            <section  class="c-attr-mt" v-if="sectionList.length!=0">
              <a :href="'/section/'+course.cid" title="进入选课" class="comm-btn c-btn-3">立即选课</a>
            </section> 
          </section>
        </aside>
        <aside class="thr-attr-box">
          <!--   <ol class="thr-attr-ol clearfix"> -->
          <ol class="thr-attr-ol ">
            <li>
              <p>&nbsp;</p>
              <aside>
                <span class="c-fff f-fM">选课总人数</span>
                <br>
                <h6 class="c-fff f-fM mt10">{{course.choosed_sum}}</h6>
              </aside>
            </li>
            <li>
              <p>&nbsp;</p>
              <aside>
                <span class="c-fff f-fM">热度指数</span>
                <br>
                <h6 class="c-fff f-fM mt10">{{hotIndex}}</h6>
              </aside>
            </li>
            <!-- <li>
              <p>&nbsp;</p>
              <aside>
                <span class="c-fff f-fM">浏览数</span>
                <br>
                <h6 class="c-fff f-fM mt10">501</h6>
              </aside>
            </li> -->
          </ol>
        </aside>
        <div class="clear"></div>
      </div>
      <!-- /课程封面介绍 -->
      <div class="mt20 c-infor-box">
        <article class="fl col-7">
          <section class="mr30">
            <div class="i-box">
              <div>
                <section id="c-i-tabTitle" class="c-infor-tabTitle c-tab-title">
                  <a name="c-i" class="current" title="课程详情">课程详情</a>
                </section>
              </div>
              <article class="ml10 mr10 pt20">
                <div>
                  <h6 class="c-i-content c-infor-title">
                    <span>课程介绍</span>
                  </h6>
                  <div class="course-txt-body-wrap">
                    <section class="course-txt-body">
                      <p>{{course.intro}}</p>
                    </section>
                  </div>
                </div>
                <!-- /课程介绍 -->

              </article>
            </div>
          </section>
        </article>
        <div class="clear"></div>
      </div>
    </section>
    <!-- /课程详情 结束 -->
  </div>
</template>

<script>
import courseApi from '@/api/course'
import orderApi from '@/api/orders'
export default {
   asyncData({ params, error }) {
    return {courseId:params.id}
   },

   data(){
     return {
       course: {},
       sectionList: [],
       hotIndex:''
     }
   },

  //在页面渲染之前执行
  created(){
      this.initCourseInfo()
  },

  methods:{
      initCourseInfo(){
         courseApi.getFrontCourseInfo(this.courseId)
            .then(response =>{
              this.course = response.data.data.course
              this.sectionList = response.data.data.sectionList
              this.hotIndex = response.data.data.hotIndex

            })
      }
  }
};
</script>
