import request from '@/utils/request'
export default {  
    //开课分页查询
    // getSectionListPage(page,size,sectionQuery){
    getSectionListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/section/pageSectionCondition/`,
            
            // method: 'post',
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            // data: sectionQuery,
            params: {currentPage,pageSize,Queryset}
            // data:{page,size}
        })
    },
    getTakeSectionListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/section/pageTakeSectionCondition/`,
            
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            params: {currentPage,pageSize,Queryset}
        })
    },
    getTeachSectionListPage(currentPage,pageSize,Queryset){
        return request({

            url: `/edu/section/pageTeachSectionCondition/`,
            
            method: 'get',
            // params
            //data表示把对象转换json进行传递到接口里面
            params: {currentPage,pageSize,Queryset}
        })
    },
    // 删除开课
    deleteBySectionId(sec_id){
        return request({
            // url: '/edu/section/pageSectionCondition/'+page+'/'+size, 第一种写法
            url: `/edu/section/deleteSection/${sec_id}`,
            method: 'delete',
            // params
            //data表示把对象转换json进行传递到接口里面
            //data: sectionQuery
        })
    },


    //添加开课
    addSection(section){
        return request({
            url: `/edu/section/addSection/`,
            method: 'post',
            data: section
        })
    },

    // 根据id查询开课
    getSectionInfo(sec_id){
        return request({
            url: `/edu/section/getSection/${sec_id}`,
            method: 'get'
        })
    },
    getAllSectionSec_id(){
        return request({
            url: `/edu/section/getAllSectionSec_id/`,
            method: 'get'
        })
    },
    // 根据id修改开课
    updateSection(sec_id,section){
        return request({
            url: `/edu/section/updateSection/${sec_id}`,
            method: 'put',
            data: section,
        })
    }
    
}