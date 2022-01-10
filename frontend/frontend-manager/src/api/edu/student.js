import request from '@/utils/request'

// export function getList(params) {
//   return request({
//     url: '/table/list',
//     method: 'get',
//     params
//   })
// }


export default {  
    //学生分页查询
    // getStudentListPage(page,size,studentQuery){
    getStudentListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/student/pageStudentCondition/`,
            
            // method: 'post',
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            // data: studentQuery,
            params: {currentPage,pageSize,Queryset}
            // data:{page,size}
        })
    },

    // 删除学生
    deleteByStudentId(sid){
        return request({
            // url: '/edu/student/pageStudentCondition/'+page+'/'+size, 第一种写法
            url: `/edu/student/deleteStudent/${sid}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: studentQuery
        })
    },


    //添加学生
    addStudent(student){
        return request({
            url: `/edu/student/addStudent/`,
            method: 'post',
            data: student
        })
    },

    // 根据id查询学生
    getStudentInfo(sid){
        return request({
            url: `/edu/student/getStudent/${sid}`,
            method: 'get'
        })
    },
    getAllStudent(){
        return request({
            url: `/edu/student/getAllStudent/`,
            method: 'get'
        })
    },
    // 根据id修改学生
    updateStudent(sid,student){
        return request({
            url: `/edu/student/updateStudent/${sid}`,
            method: 'put',
            data: student,
        })
    
    }
    
}