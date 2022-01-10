import request from '@/utils/request'


export default {  
    //选课分页查询
    getTakeListPage(currentPage,pageSize,Queryset){
        return request({
          url: `/edu/take/pageTakeCondition/`,
            method: 'get',
            params: {currentPage,pageSize,Queryset}
        })
    },

    // 删除选课
    deleteByTakeId(id){
        return request({
            url: `/edu/take/deleteTake/${id}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: takeQuery
        })
    },


    //添加选课
    addTake(take){
        return request({
            url: `/edu/take/addTake/`,
            method: 'post',
            data: take
        })
    },

    // 根据id查询选课
    getTakeInfo(id){
        return request({
            url: `/edu/take/getTake/${id}`,
            method: 'get'
        })
    },

    // 根据id修改选课
    updateTake(id,take){
        return request({
            url: `/edu/take/updateTake/${id}`,
            method: 'put',
            data: take,
        })
    
    }
    
}