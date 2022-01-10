import request from '@/utils/request'
export default {  
    //学生分页查询
    // getCourseListPage(page,size,courseQuery){
    getCourseListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/course/pageCourseCondition/`,
            
            // method: 'post',
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            // data: courseQuery,
            params: {currentPage,pageSize,Queryset}
            // data:{page,s  ize}
        })
    },

    // 删除学生
    deleteByCourseId(cid){
        return request({
            // url: '/edu/course/pageCourseCondition/'+page+'/'+size, 第一种写法
            url: `/edu/course/deleteCourse/${cid}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: courseQuery
        })
    },


    //添加学生
    addCourse(course){
        return request({
            url: `/edu/course/addCourse/`,
            method: 'post',
            data: course
        })
    },

    // 根据id查询学生
    getCourseInfo(cid){
        return request({
            url: `/edu/course/getCourse/${cid}`,
            method: 'get'
        })
    },
    getAllCourse(){
        return request({
            url: `/edu/course/getAllCourse/`,
            method: 'get'
        })
    },
    // 根据id修改学生
    updateCourse(cid,course){
        return request({
            url: `/edu/course/updateCourse/${cid}`,
            method: 'put',
            data: course,
        })
    }
    
}