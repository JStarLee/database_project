def jwt_response_payload_handler(token,user=None,request=None):
    """
    自定义jwt认证成功返回的数据
    """
    
    return{"success":"true","code":20000,"data":{'token':token,'username':user.username}}

    # return {
    #     'token':token,
    #     'username':user.username,
    # }