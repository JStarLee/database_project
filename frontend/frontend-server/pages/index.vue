<template>
  <div>
    <!-- 幻灯片 开始 -->
    <div class="swiper">
      <swiper ref="mySwiper" :options="swiperOptions"  style="background: #040B1B">
        <swiper-slide><img src="../assets/img/pic/banner2.jpg" alt=" "></swiper-slide>
        <swiper-slide><img src="../assets/img/pic/banner3.jpg" alt=" "></swiper-slide>
        <swiper-slide><img src="../assets/img/pic/banner1.jpg" alt=" "></swiper-slide>
        <div class="swiper-pagination " slot="pagination"></div>
        <div
          class="swiper-button-prev swiper-button-white"
          slot="button-prev"
        ></div>
        <div
          class="swiper-button-next swiper-button-white"
          slot="button-next"
        ></div>
      </swiper>
    </div>
    <!-- 幻灯片 结束 -->
    <div id="aCoursesList">
      <!-- 网校课程 开始 -->
      <div>
        <section class="container">
          <header class="comm-title">
            <h2 class="tac">
              <span class="c-333">热门课程</span>
            </h2>
          </header>
          <div>
            <article class="comm-course-list">
              <ul class="of" id="bna">
                <li v-for="course in courseList" :key="course.cid">
                  <div class="cc-l-wrap">
                    <section class="course-img">
                      <img
                        :src="course.photo"
                        class="img-responsive"
                        :alt="course.name"
                      />
                      <div class="cc-mask">
                        <a
                          :href="'/course/' + course.cid"
                          title="开始学习"
                          class="comm-btn c-btn-1"
                          >开始学习</a
                        >
                      </div>
                    </section>
                    <h3 class="hLh30 txtOf mt10">
                      <a
                        :href="'/course/' + course.cid"
                        :title="course.name"
                        class="course-title fsize18 c-333"
                        >{{ course.name }}</a
                      >
                    </h3>
                    <section class="mt10 hLh20 of">
                      <span
                        class="fr jgTag bg-green"
                        v-if="Number(course.price) === 0"
                      >
                        <i class="c-fff fsize12 f-fA">免费</i>
                      </span>
                      <span class="fl jgAttr c-ccc f-fA">
                        <i class="c-999 f-fA">{{ course.choosed_sum }}人学习</i>
                        <!-- |
                        <i class="c-999 f-fA">{{ course.viewCount }}评论</i> -->
                      </span>
                    </section>
                  </div>
                </li>
              </ul>
              <div class="clear"></div>
            </article>
            <section class="tac pt20">
              <a href="/course" title="全部课程" class="comm-btn c-btn-2">全部课程</a>
            </section>
          </div>
        </section>
      </div>
      <!-- /网校课程 结束 -->
      <!-- 网校名师 开始 -->
      <div>
        <section class="container">
          <header class="comm-title">
            <h2 class="tac">
              <span class="c-333">名师大咖</span>
            </h2>
          </header>
          <div>
            <article class="i-teacher-list">
              <ul class="of">
                <li v-for="teacher in teacherList" :key="teacher.tid">
                  <section class="i-teach-wrap">
                    <div class="i-teach-pic">
                      <a :href="'/teacher/' + teacher.tid" :title="teacher.name">
                        <img :alt="teacher.name" :src="teacher.photo" />
                      </a>
                    </div>
                    <div class="mt10 hLh30 txtOf tac">
                      <a :href="'/teacher/' + teacher.tid" :title="teacher.name" class="fsize18 c-666">{{ teacher.name }}</a>
                    </div>
                    <div class="hLh30 txtOf tac">
                      <span class="fsize14 c-999">{{ teacher.career }}</span>
                    </div>
                    <div class="mt15 i-q-txt">
                      <p class="c-999 f-fA">{{ teacher.intro }}</p>
                    </div>
                  </section>
                </li>
              </ul>
              <div class="clear"></div>
            </article>
            <section class="tac pt20">
              <a href="/teacher" title="全部讲师" class="comm-btn c-btn-2">全部讲师</a>
            </section>
          </div>
        </section>
      </div>
      <!-- /网校名师 结束 -->
    </div>
  </div>
</template>

<script>
// import banner from '@/api/banner'
import index from '@/api/index'
export default {
  data () {
    return {

      swiperOptions: {
        spaceBetween: 30,
        loop: true,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        },
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        autoplay: {
          delay: 5000
        }
      },

      // swiperList代码
      swiperList: [

      ],
      // banner数组
      bannerList: [

      ],
      courseList: [

      ],
      teacherList: [

      ]
    }
  },
  created() {
  //调用查询banner的方法
    // this.getBannerList()
    //调用查询热门课程和名师的方法
    this.getHotCourseTeacher()
  },
  methods:{
    //查询热门课程和名师
    getHotCourseTeacher() {
      index.getIndexData()
        .then(response => {
          this.courseList = response.data.data.courseList
          this.teacherList = response.data.data.teacherList
        })
    },
    //查询banner数据
    // getBannerList() {
    //   banner.getListBanner()
    //     .then(response => {
    //       this.bannerList = response.data.data.list
    //     })
    // }
  }
}
</script>
