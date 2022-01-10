from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class MyLimitOffsetPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 5
    # 默认每页显示3个，可以通过传入pager1/?currentPage=2&pageSize=4,改变默认每页显示的个数
    page_size_query_param = "pageSize"
    # 最大页数不超过10
    max_page_size = 100
    # 获取页码数的
    page_query_param = "currentPage"

    max_limit: 10 #表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
# default_limit：表示默认每页显示几条数据
# limit_query_param：表示url中本页需要显示数量参数
# offset_query_param：表示从数据库中的第几条数据开始显示参数
# max_limit：表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃