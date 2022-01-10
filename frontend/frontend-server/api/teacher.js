import request from '@/utils/request'

export default{

  //分页讲师查询的方法
  getTeacherList(currentPage,pageSize,Queryset){
      return request({
          url: `/edu/teacherFront/getTeacherInfoList/`,
          method: 'get',
          params: {currentPage,pageSize,Queryset}      
      })
  },


  //讲师详情查询
  getTeacherInfo(teacherId){
      return request(
          {
            url: `/edu/teacherFront/getTeacherFrontInfo/${teacherId}`,
            method: 'get'
          }
      )
  }
}