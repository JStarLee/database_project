import request from '@/utils/request'

export default{

  //分页课程查询的方法
  getFrontCourseList(currentPage,pageSize,Queryset){
      return request({
          url: `/edu/courseFront/getFrontCourse/`,
          method: 'get',
          params: {currentPage,pageSize,Queryset} 
      })
  },


  //课程详情查询
  getFrontCourseInfo(courseId){
      return request(
          {
            url: `/edu/courseFront/getFrontCourseInfo/${courseId}`,
            method: 'get'
          }
      )
  },


  //查询所有分类
  getAllSubject(){
      return request({
          url: '/edu/subject/findAllSubject',
          method: 'get'
      })
  }
}