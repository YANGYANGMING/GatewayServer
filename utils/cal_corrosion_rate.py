from GWS import models
from apscheduler.schedulers.background import BackgroundScheduler
from GatewayServer import settings


cal_corrosion_rate_sche = BackgroundScheduler()


# def cal_corrosion_rate():
#     """
#     计算腐蚀率
#     :return:
#     """
#     # print('asdf')
#     pass
#
#
# # 每个一周计算一次腐蚀速率
# try:
#     cal_corrosion_rate_sche.add_job(cal_corrosion_rate, 'interval',
#                                     seconds=settings.cal_corrosion_rate_time['seconds'], id="cal_corrosion_rate")
#     cal_corrosion_rate_sche.start()
# except Exception as e:
#     print(e)
#     cal_corrosion_rate_sche.shutdown()

