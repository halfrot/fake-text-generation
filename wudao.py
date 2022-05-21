api_key = ""
public_key = ""
ability_qa = "question_answer"
engine_qa = "txl-general-engine-v1"
ability_cc = "content_creation"
engine_cc = "text-general-engine-v1"
'''
response information
{
  "code": 200,  # 请求响应状态 200 为业务处理成功
  "msg": "成功",  # 错误信息
  "data": {
           "prompt": "世界的终极意义是什么？",  # 用户输入项 
           "promptDesc": None, 
           "outputText": "司机与乘客之间是信息不对称的。乘客不知道司机的行驶路线和目的地;司机也不知道乘客是否愿意支付费用。在这种情况下,通过平台进行预约后由平台提供车辆和服务(包括驾驶员),并收取服务费的方式可以有效解决这一问题。",  # 平台输出
           "inputTokenNum": 39,  # 输入词块数
           "outputTokenNum": 54, # 输出词块数
           "totalTokenNum": 93,  # 总词块数
           "taskOrderNo": "1000651507247240199147520", # 任务订单号
           "taskStatus":"SUCCESS"
           }, 
  "success": True
}
'''
