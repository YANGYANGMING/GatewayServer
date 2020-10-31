from GatewayServer.settings import accessKeyId, accessSecret, TemplateCode
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json


def send_sms(PhoneNumbers, sms_code):
    """
    发送短信验证码
    :param PhoneNumbers: 获取验证码的手机号
    :return:
    """
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', PhoneNumbers)
    request.add_query_param('SignName', "ABC商城")
    request.add_query_param('TemplateCode', TemplateCode)
    request.add_query_param('TemplateParam', "{\"code\": %s}" % sms_code)

    response = client.do_action_with_exception(request)
    print(response)

    return json.loads(str(response, encoding='utf-8'))
