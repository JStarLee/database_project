import request from '@/utils/request'
export default {  
    //开课时间段分页查询
    // getTime_slotListPage(page,size,time_slotQuery){
    getTime_slotList(){
        return request({
            url: `/edu/time_slot/Time_slotCondition/`,
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
        })
    },
    getAllTime_slotSelect(){
        return request({
            url: `/edu/time_slot/getAllTime_slotSelect/`,
            method: 'get'
        })
    },
    getAllTime_slot(){
        return request({
            url: `/edu/time_slot/getAllTime_slot/`,
            method: 'get'
        })
    },
    // 根据id修改开课时间段
    updateTime_slot(time_slot){
        return request({
            url: `/edu/time_slot/updateTime_slot/`,
            method: 'put',
            data: time_slot,
        })
    }
    
}