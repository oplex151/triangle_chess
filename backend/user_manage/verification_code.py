from flask import jsonify
from backend.tools import setupLogger
from backend.message import *

import redis
import re
import uuid
import random
from datetime import datetime, timedelta
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

logger = setupLogger()

def expire(name, exp=None):
    """
    设置过期时间
    :return:
    """
    expire_in_seconds = exp if exp else 60
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    r.expire(name, expire_in_seconds)

def hset(name, key, value):
    """
    设置指定hash表
    :return:
    """
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    r.hset(name, key, value)

def hget(name, key):
    """
    读取指定hash表的键值
    """
    r = redis.StrictRedis('127.0.0.1', '6379', 1)
    value = r.hget(name, key)
    return value.decode('utf-8') if value else value


# 阿里云申请成功获取到的内容
smss = {
    "SMS_ACCESS_KEY_ID": "LTAI5tATCMM3GtfRmrayfn59",  # key ID
    "SMS_ACCESS_KEY_SECRET": "94yNxCm687uPgFC8owqjvWEUwlm5nZ",  # 密钥
    "SMS_SIGN_NAME": "三国象棋",  # 签名
    "AUTHENTICATION": "SMS_468415195",  # 身份验证模板编码
}


class SendSms(object):

    def __init__(self, phone: str = None, category: str = None, template_param=None):
        """
        :param phone: 发送的手机号
        :param category: 选择短信模板
        :param template_param: 短信验证码或者短信模板中需要替换的变量用字典传入类似：{"code":123456}
        """
        access_key_id = smss.get('SMS_ACCESS_KEY_ID', None)
        access_key_secret = smss.get('SMS_ACCESS_KEY_SECRET', None)
        sign_name = smss.get("SMS_SIGN_NAME", None)

        if access_key_id is None:
            raise ValueError("缺失短信key")

        if access_key_secret is None:
            raise ValueError("缺失短信secret")

        if phone is None:
            raise ValueError("手机号错误")

        if template_param is None:
            raise ValueError("短信模板参数无效")

        if category is None:
            raise ValueError("短信模板编码无效")

        if sign_name is None:
            raise ValueError("短信签名错误")

        self.acs_client = AcsClient(access_key_id, access_key_secret)
        self.phone = phone
        self.category = category
        self.template_param = template_param
        self.template_code = self.templateCode()
        self.sign_name = sign_name

    def templateCode(self):
        """
        选择模板编码
        :param self.category
        authentication: 身份验证
        :return:
        """
        if self.category == "authentication":
            code = smss.get('AUTHENTICATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码AUTHENTICATION")
            return code
        else:
            raise ValueError("短信模板编码无效")

    def sendSms(self):
        """
        发送短信
        :return:
        """

        sms_request = CommonRequest()

        # 固定设置
        sms_request.set_accept_format('json')
        sms_request.set_domain('dysmsapi.aliyuncs.com')
        sms_request.set_method('POST')
        sms_request.set_protocol_type('https')  # https | http
        sms_request.set_version('2017-05-25')
        sms_request.set_action_name('SendSms')

        # 短信发送的号码列表，必填。
        sms_request.add_query_param('PhoneNumbers', self.phone)
        # 短信签名，必填。
        sms_request.add_query_param('SignName', self.sign_name)

        # 申请的短信模板编码,必填
        sms_request.add_query_param('TemplateCode', self.template_code)

        # 短信模板变量参数 类似{"code":"12345"}，必填。
        sms_request.add_query_param('TemplateParam', self.template_param)

        # 设置业务请求流水号，必填。暂用UUID1代替
        build_id = uuid.uuid1()
        sms_request.add_query_param('OutId', build_id)

        # 调用短信发送接口，返回json
        sms_response = self.acs_client.do_action_with_exception(sms_request)

        return sms_response

def checkPhoneCode(phone: str, code: str) -> bool:
    """
    验证手机号码与验证码是否正确
    :param phone: 手机号码
    :param code: 验证码
    :return:
    """
    re_phone = checkPhone(phone)
    if re_phone is None:
        return False
    r_code = hget(re_phone, "code")
    if code == r_code:
        return True
    else:
        return False

def checkPhone(phone: str):
    """
    验证前端传入的字符串是否为手机号码
    :param phone:手机号码
    :return:
    """
    # 判断手机号长度
    if len(str(phone)) == 11:
        # 匹配手机号
        v_phone = re.match(r'^1[3-9][0-9]{9}$', phone)
        if v_phone is None:
            return None
        else:
            phone = v_phone.group()
            return phone
    else:
        return None

def getVerificationCode(category, phone):
    """
    用户通过短信方式获取手机验证码
    Args:
        category:短信模板编码
            authentication: 身份验证
        phone_num:手机号
    Returns:
        发送短信验证码成功200
    """
    now = datetime.now()
    res,status = {},None

    # 验证手机号码正确性
    re_phone = checkPhone(phone)
    if phone is None or re_phone is None:
        status = PHONE_NUMBER_ERROR #手机号码不正确
        return jsonify(res),status
    if category is None:
        status = CATEGORY_NOT_EXIST #参数缺失
        return jsonify(res),status
    try:
        # 获取手机验证码设置时间
        flag = hget(re_phone, 'expire_time')
        if flag is not None:
            flag = datetime.strptime(flag, '%Y-%m-%d %H:%M:%S')
            # 判断是否重复操作
            if (flag - now).total_seconds() < 60:
                status = FREQUENT_OPERATION #请勿频繁操作
                return jsonify(res),status
        # 获取随机验证码
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        template_param = {"code": code}
        # 发送验证码
        sms = SendSms(phone=re_phone, category=category, template_param=template_param)
        sms.sendSms()
        # 将验证码存入redis，方便接下来的验证
        hset(re_phone, "code", code)
        # 设置重复操作屏障  
        hset(re_phone, "expire_time", (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))
         # 设置验证码过去时间
        expire(re_phone, 60 * 3)
        status = SUCCESS
    except Exception as e:
        logger.error("User whose phone number is {0} failed to get verification code by category {1} due to\n{2}".format(phone, category, str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        return jsonify(res),status
    
def checkVerificationCode(phone, code):
    """
    用户验证码验证
    Args:
        phone:手机号
        code:用户输入的验证码
    Returns:
        验证码验证成功200
    """
    res,status = {},None
    if phone is None:
        status = PHONE_NUMBER_ERROR #手机号码不正确
        return jsonify(res),status
    try:
    # 验证手机号和验证码是否正确
        if code is None or not checkPhoneCode(phone, code):
            status = VERIFICATION_CODE_ERROR #验证码错误
            # return jsonify(res),status
    except Exception as e:
        logger.error("User whose phone number is {0} failed to check verification code by code {1} due to\n{2}".format(phone, code, str(e)),exc_info=True)
        status = OTHER_ERROR
    finally:
        return jsonify(res),status