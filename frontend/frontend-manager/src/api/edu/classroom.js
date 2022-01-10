import request from '@/utils/request'
export default {  
    //教室分页查询
    // getClassroomListPage(page,size,classroomQuery){
    getClassroomListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/classroom/pageClassroomCondition/`,
            
            // method: 'post',
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            // data: classroomQuery,
            params: {currentPage,pageSize,Queryset}
            // data:{page,s  ize}
        })
    },

    // 删除教室
    deleteByClassroomId(classroom_id){
        return request({
            // url: '/edu/classroom/pageClassroomCondition/'+page+'/'+size, 第一种写法
            url: `/edu/classroom/deleteClassroom/${classroom_id}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: classroomQuery
        })
    },


    //添加教室
    addClassroom(classroom){
        return request({
            url: `/edu/classroom/addClassroom/`,
            method: 'post',
            data: classroom
        })
    },

    // 根据id查询教室
    getClassroomInfo(classroom_id){
        return request({
            url: `/edu/classroom/getClassroom/${classroom_id}`,
            method: 'get'
        })
    },
    getAllClassroom(){
        return request({
            url: `/edu/classroom/getAllClassroom/`,
            method: 'get'
        })
    },
    // 根据id修改教室
    updateClassroom(classroom_id,classroom){
        return request({
            url: `/edu/classroom/updateClassroom/${classroom_id}`,
            method: 'put',
            data: classroom,
        })
    }
    
}