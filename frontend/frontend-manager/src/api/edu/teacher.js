import request from '@/utils/request'

// export function getList(params) {
//   return request({
//     url: '/table/list',
//     method: 'get',
//     params
//   })
// }


export default {  
    //讲师分页查询
    // getTeacherListPage(page,size,teacherQuery){
    getTeacherListPage(currentPage,pageSize,Queryset){
        return request({
            // url: '/edu/teacher/pageTeacherCondition/'+page+'/'+size, 第一种写法
            // url: `/edu/teacher/pageTeacherCondition/${page}/${size}`,
            // url: `/edu/teacher/pageTeacherCondition/?currentPage=${page}&pageSize=${size}`,
            url: `/edu/teacher/pageTeacherCondition/`,
            
            // method: 'post',
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            // data: teacherQuery,
            params: {currentPage,pageSize,Queryset}
            // data:{page,size}
        })
    },

    // 删除讲师
    deleteByTeacherId(tid){
        return request({
            // url: '/edu/teacher/pageTeacherCondition/'+page+'/'+size, 第一种写法
            url: `/edu/teacher/deleteTeacher/${tid}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: teacherQuery
        })
    },


    //添加讲师
    addTeacher(teacher){
        return request({
            url: `/edu/teacher/addTeacher/`,
            method: 'post',
            data: teacher
        })
    },

    // 根据id查询讲师
    getTeacherInfo(tid){
        return request({
            url: `/edu/teacher/getTeacher/${tid}`,
            method: 'get'
        })
    },
    getAllTeacher(){
        return request({
            url: `/edu/teacher/getAllTeacher/`,
            method: 'get'
        })
    },
    // 根据id修改讲师
    updateTeacher(tid,teacher){
        return request({
            url: `/edu/teacher/updateTeacher/${tid}`,
            method: 'put',
            data: teacher,
        })
    
    }
    
}