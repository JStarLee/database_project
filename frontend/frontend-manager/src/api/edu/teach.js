import request from '@/utils/request'

export default {  
    //授课分页查询
    // getTeachListPage(page,size,teachQuery){
    getTeachListPage(currentPage,pageSize,Queryset){
        return request({
          url: `/edu/teach/pageTeachCondition/`,
            method: 'get',
            params: {currentPage,pageSize,Queryset}
        })
    },

    // 删除授课
    deleteByTeachId(id){
        return request({
            url: `/edu/teach/deleteTeach/${id}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: teachQuery
        })
    },


    //添加授课
    addTeach(teach){
        return request({
            url: `/edu/teach/addTeach/`,
            method: 'post',
            data: teach
        })
    },

    // 根据id查询授课
    getTeachInfo(id){
        return request({
            url: `/edu/teach/getTeach/${id}`,
            method: 'get'
        })
    },

    // 根据id修改授课
    updateTeach(id,teach){
        return request({
            url: `/edu/teach/updateTeach/${id}`,
            method: 'put',
            data: teach,
        })
    
    }
    
}