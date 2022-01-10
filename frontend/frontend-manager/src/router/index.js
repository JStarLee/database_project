import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import take from '@/api/edu/take'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },
    // 讲师管理
    {
      path: '/teacher',
      component: Layout,
      redirect: '/teacher/table',
      name: '讲师管理',
      meta: { title: '讲师管理', icon: 'teacher' },
      children: [
        {
          path: 'table',
          name: '讲师列表',
          component: () => import('@/views/edu/teacher/list'),
          meta: { title: '讲师列表', icon: 'table' }
        },
        {
          path: 'save',
          name: '添加讲师',  
          component: () => import('@/views/edu/teacher/save'),
          meta: { title: '添加讲师', icon: 'tree' }
        },
        {
          path: 'edit/:tid',   
          name: 'EduTeacherEdit',
          component: () => import('@/views/edu/teacher/save'),
          meta: { title: '编辑讲师', noCache: true },
          hidden: true
        }
      ]
    },
    // 学生管理
    {
      path: '/student',
      component: Layout,
      redirect: '/student/table',
      name: '学生管理',
      meta: { title: '学生管理', icon: 'student' },
      children: [
        {
          path: 'table',
          name: '学生列表',
          component: () => import('@/views/edu/student/list'),
          meta: { title: '学生列表', icon: 'table' }
        },
        {
          path: 'save',
          name: '添加学生',  
          component: () => import('@/views/edu/student/save'),
          meta: { title: '添加学生', icon: 'tree' }
        },
        {
          path: 'edit/:sid',   
          name: 'EduStudentEdit',
          component: () => import('@/views/edu/student/save'),
          meta: { title: '编辑学生', noCache: true },
          hidden: true
        }
      ]
    },
    // 课程管理
    {
      path: '/course',
      component: Layout,
      redirect: '/course/table',
      name: '课程管理',
      meta: { title: '课程管理', icon: 'course' },
      children: [
        {
          path: 'table',
          name: '课程列表',
          component: () => import('@/views/edu/course/list'),
          meta: { title: '课程列表', icon: 'table' }
        },
        {
          path: 'save',
          name: '添加课程',  
          component: () => import('@/views/edu/course/save'),
          meta: { title: '添加课程', icon: 'tree' }
        },
        {
          path: 'edit/:cid',   
          name: 'EduCourseEdit',
          component: () => import('@/views/edu/course/save'),
          meta: { title: '编辑课程', noCache: true },
          hidden: true
        }
      ]
    },  
      // 开课管理
      {
        path: '/section',
        component: Layout,
        redirect: '/section/table',
        name: '开课管理',
        meta: { title: '开课管理', icon: 'section' },
        children: [
          {
            path: 'table',
            name: '开课列表',
            component: () => import('@/views/edu/section/list'),
            meta: { title: '开课列表', icon: 'table' }
          },
          {
            path: 'save',
            name: '添加开课',  
            component: () => import('@/views/edu/section/save'),
            meta: { title: '添加开课', icon: 'tree' }
          },
          {
            path: 'edit/:sec_id',   
            name: 'EduSectionEdit',
            component: () => import('@/views/edu/section/save'),
            meta: { title: '编辑开课', noCache: true },
            hidden: true
          }
        ]
      },
      // 开课时间段管理
      {
        path: '/time_slot',
        component: Layout,
        redirect: '/time_slot/table',
        name: '开课时间段管理',
        meta: { title: '开课时间段管理', icon: 'time_slot' },
        children: [
          {
            path: 'table',
            name: '开课时间段列表',
            component: () => import('@/views/edu/time_slot/list'),
            meta: { title: '开课时间段列表', icon: 'table' }
          },
          {
            path: 'save',
            name: '添加开课时间段',  
            component: () => import('@/views/edu/time_slot/save'),
            meta: { title: '编辑开课时间段', icon: 'tree' }
          },
          {
            path: 'edit/:time_slot_id',   
            name: 'EduTime_slotEdit',
            component: () => import('@/views/edu/time_slot/save'),
            meta: { title: '编辑开课时间段', noCache: true },
            hidden: true
          }
        ]
      },
      // 教室管理
      {
        path: '/classroom',
        component: Layout,
        redirect: '/classroom/table',
        name: '教室管理',
        meta: { title: '教室管理', icon: 'classroom' },
        children: [
          {
            path: 'table',
            name: '教室列表',
            component: () => import('@/views/edu/classroom/list'),
            meta: { title: '教室列表', icon: 'table' }
          },
          {
            path: 'save',
            name: '添加教室',  
            component: () => import('@/views/edu/classroom/save'),
            meta: { title: '添加教室', icon: 'tree' }
          },
          {
            path: 'edit/:classroom_id',   
            name: 'EduClassroomEdit',
            component: () => import('@/views/edu/classroom/save'),
            meta: { title: '编辑教室', noCache: true },
            hidden: true
          }
        ]
      },

          // 授课管理
    {
      path: '/teach',
      component: Layout,
      redirect: '/teach/table',
      name: '授课管理',
      meta: { title: '授课管理', icon: 'teach' },
      children: [
        {
          path: 'table',
          name: '授课列表',
          component: () => import('@/views/edu/teach/list'),
          meta: { title: '授课列表', icon: 'table' }
        },
        {
          path: 'save',
          name: '添加授课',  
          component: () => import('@/views/edu/teach/save'),
          meta: { title: '添加授课', icon: 'tree' }
        },
        {
          path: 'edit/:id',   
          name: 'EduTeachEdit',
          component: () => import('@/views/edu/teach/save'),
          meta: { title: '编辑授课', noCache: true },
          hidden: true
        }
      ]
    },
        // 选课管理
    {
      path: '/take',
      component: Layout,
      redirect: '/take/table',
      name: '选课管理',
      meta: { title: '选课管理', icon: 'take' },
      children: [
        {
          path: 'table',
          name: '选课列表',
          component: () => import('@/views/edu/take/list'),
          meta: { title: '选课列表', icon: 'table' }
        },
        {
          path: 'save',
          name: '添加选课',  
          component: () => import('@/views/edu/take/save'),
          meta: { title: '添加选课', icon: 'tree' }
        },
        {
          path: 'edit/:id',   
          name: 'EduTakeEdit',
          component: () => import('@/views/edu/take/edit'),
          meta: { title: '编辑选课', noCache: true },
          hidden: true
        }
      ]
    },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
