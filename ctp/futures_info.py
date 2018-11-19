# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/21 9:15
"""
期货品种信息
品种名称
最小变动单位
保证金
手续费_固定
手续费_浮动
交易所代码
上市年份
上市月份
本地数据的最早年份
本地数据的最早月份
交易时段
交易时段模式
主力合约
"""
"""
商品期货数据当前所有品种
有色1 - 6: 铜 铝 锌 铅 镍 锡
贵金属7 - 8: 金 银
黑色9 - 13: 螺纹 热卷 铁矿 焦煤 焦炭
铁合金14 - 15：硅铁 锰硅
建材16 - 17: 沥青 玻璃
电力原料18: 动力煤
油脂油料19 - 25: 豆粕 豆油 豆一 豆二 棕榈油 菜粕 菜油
谷物26 - 27: 玉米 玉米淀粉
饲料下游28: 鸡蛋
软商29 - 30: 白糖 棉花
鲜果31: 苹果
其它农产品32: 橡胶
化工33 - 37: 塑料 PVC PP PTA 甲醇
能源38：原油 燃油
不活跃品种
胶板 纤板 棉纱 郑麦 早稻 晚稻 粳稻 菜籽
"""

"""
股指
IF沪深300
IH上证50
IC中证500
国债
TF5年国债
T十年国债
"""
import datetime

class Futures_Info:
    def __init__(self):
        self.today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    # 所有期货品种的list，只提供这一个接口，接口写死，有需要就改这个接口
    def futures_list(self):
        finance_list = ['IF', 'IH', 'IC', 'TF', 'T']
        commodity_list = [
            'CU', 'AL', 'ZN', 'PB', 'NI', 'SN',
            'AU', 'AG',
            'RB', 'HC', 'I', 'JM', 'J',
            'SF', 'SM',
            'BU', 'FG',
            'ZC',
            'M', 'Y', 'A', 'B', 'P', 'RM', 'OI',
            'C', 'CS',
            'JD',
            'SR', 'CF',
            'AP',
            'RU',
            'L', 'V', 'PP', 'TA', 'MA',
            'FU', 'SC']
        return commodity_list, finance_list
    # 所有期货品种的info，只提供这一个接口，接口写死，有需要改这个接口
    def futures_info(self):
        endtime = '2018-08-21 15:00:00'
        phase=[['21:00:00', '23:00:00'],
               ['23:00:01', '23:30:00'],
               ['23:30:01', '23:59:59'],
               ['00:00:00', '01:00:00'],
               ['01:00:01', '02:30:00'],
               ['09:00:00', '10:15:00'],
               ['10:30:00', '11:30:00'],
               ['13:30:00', '15:00:00'],
               ]

        commodity = [
            'CU','AL','ZN','PB','NI','SN',
            'AU','AG',
            'RB','HC','I','JM','J',
            'SF','SM',
            'BU','FG',
            'ZC',
            'M','Y','A','B','P','RM','OI',
            'C','CS',
            'JD',
            'SR','CF',
            'AP',
            'RU',
            'L','V','PP','TA','MA',
            'FU','SC'
            'BB','FB','CY','WH','RI','LR','JR','RS']
        finance = ['IF','IH','IC','TF','T']
        commodity_info = {}
        """
        品种名称
        最小变动单位
        保证金
        手续费_固定
        手续费_浮动
        交易所代码
        上市年份
        上市月份
        本地数据的最早年份
        本地数据的最早月份
        交易时段
        交易时段模式
        主力合约
        """
        cu_dict = {'code':'cu',
                   'trading_unit':5,
                   'min_change':10,
                   'margin':0.07,
                   'commision_fix':0,
                   'commision_float':0.00005,
                   'commision_fix_today':0,
                   'commision_float_today':0,
                   'exchange_id':'shfe',
                   'ipo':'1993-03-01',
                   'begintime_local':'2013-12-20 21:00:00',
                   'endtime_local': endtime,
                   'trading_period':[
                                     ['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['23:30:01', '23:59:59'],
                                     ['00:00:00', '01:00:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00']],
                   'trading_period_mode':'4',
                   'domi_month':['01','02','03','04','05','06',
                                 '07','08','09','10','11','12'],
                   }
        al_dict = {'code': 'al',
                   'trading_unit': 5,
                   'min_change': 5,
                   'margin': 0.07,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '1992-05-28',
                   'begintime_local':'2013-12-20 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '4',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '10', '11', '12'],
                   }
        zn_dict = {'code': 'zn',
                   'trading_unit': 5,
                   'min_change': 5,
                   'margin': 0.08,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2007-03-26',
                   'begintime_local':'2013-12-20 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '4',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '10', '11', '12'],
                   }
        pb_dict = {'code': 'pb',
                   'trading_unit': 5,
                   'min_change': 5,
                   'margin': 0.08,
                   'commision_fix': 0,
                   'commision_float': 0.00004,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2011-03-24',
                   'begintime_local':'2013-12-20 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '4',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '10', '11', '12'],
                   }
        ni_dict = {'code': 'ni',
                   'trading_unit': 1,
                   'min_change': 10,
                   'margin': 0.08,
                   'commision_fix': 6,
                   'commision_float': 0,
                   'commision_fix_today': 6,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2015-03-27',
                   'begintime_local':'2015-03-27 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '4',
                   'domi_month': ['01', '03', '05', '07', '09', '11'],
                   }
        sn_dict = {'code': 'sn',
                   'trading_unit': 1,
                   'min_change': 10,
                   'margin': 0.07,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2015-03-27',
                   'begintime_local':'2015-03-27 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '4',
                   'domi_month': ['01', '05', '09'],
                   }
        au_dict = {'code': 'au',
                   'trading_unit': 1000,
                   'min_change': 0.05,
                   'margin': 0.05,
                   'commision_fix': 10,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2008-01-09',
                   'begintime_local':'2013-07-05 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['01:00:01', '02:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '5',
                   'domi_month': ['06', '12'],
                   }
        ag_dict = {'code': 'ag',
                   'trading_unit': 15,
                   'min_change': 1,
                   'margin': 0.06,
                   'commision_fix': 0,
                   'commision_float': 0.0005,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.0005,
                   'exchange_id': 'shfe',
                   'ipo': '2012-05-10',
                   'begintime_local':'2013-07-05 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['01:00:01', '02:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': 'au',
                   'domi_month': ['06', '12'],
                   }
        rb_dict = {'code': 'rb',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.09,
                   'commision_fix': 0,
                   'commision_float': 0.0001,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.0001,
                   'exchange_id': 'shfe',
                   'ipo': '2009-03-27',
                   'begintime_local':'2014-12-26 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '2',
                   'domi_month': ['01', '05', '10'],
                   }
        hc_dict = {'code': 'hc',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.09,
                   'commision_fix': 0,
                   'commision_float': 0.0001,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.0001,
                   'exchange_id': 'shfe',
                   'ipo': '2014-03-21',
                   'begintime_local':'2014-12-26 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '2',
                   'domi_month': ['01', '05', '10'],
                   }
        i_dict = {'code': 'i',
                  'trading_unit': 100,
                  'min_change': 0.5,
                  'margin': 0.05,
                  'commision_fix': 0,
                  'commision_float': 0.00006,
                  'commision_fix_today': 0,
                  'commision_float_today': 0.00012,
                  'exchange_id': 'dce',
                  'ipo': '2013-10-18',
                  'begintime_local': '2014-12-26 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                   }
        jm_dict = {'code': 'jm',
                   'trading_unit': 60,
                   'min_change': 0.5,
                   'margin': 0.12,
                   'commision_fix': 0,
                   'commision_float': 0.00006,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00018,
                   'exchange_id': 'dce',
                   'ipo': '2013-03-22',
                   'begintime_local': '2014-12-26 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                  }
        j_dict = {'code': 'j',
                   'trading_unit': 100,
                   'min_change': 0.5,
                   'margin': 0.12,
                   'commision_fix': 0,
                   'commision_float': 0.00006,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00018,
                   'exchange_id': 'dce',
                   'ipo': '2011-04-15',
                   'begintime_local': '2014-07-04 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        sf_dict = {'code': 'sf',
                  'trading_unit': 5,
                  'min_change': 2,
                  'margin': 0.07,
                  'commision_fix': 3,
                  'commision_float': 0,
                  'commision_fix_today': 9,
                  'commision_float_today': 0,
                  'exchange_id': 'czce',
                  'ipo': '2014-08-08',
                  'begintime_local': '2014-08-08 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00']],
                  'trading_period_mode': '1',
                  'domi_month': ['01', '05', '09'],
                  }
        sm_dict = {'code': 'sm',
                   'trading_unit': 5,
                   'min_change': 2,
                   'margin': 0.07,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 6,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2014-08-08',
                   'begintime_local': '2014-08-08 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00']],
                   'trading_period_mode': '1',
                   'domi_month': ['01', '05', '09'],
                   }

        bu_dict = {'code': 'bu',
                   'trading_unit': 10,
                   'min_change': 2,
                   'margin': 0.08,
                   'commision_fix': 0,
                   'commision_float': 0.0001,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'shfe',
                   'ipo': '2013-10-09',
                   'begintime_local': '2015-09-28 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '2',
                   'domi_month': ['06', '12'],
                   }
        fg_dict = {'code': 'fg',
                   'trading_unit': 20,
                   'min_change': 1,
                   'margin': 0.07,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 6,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2012-12-03',
                   'begintime_local': '2015-06-11 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        zc_dict = {'code': 'zc',
                   'trading_unit': 100,
                   'min_change': 0.2,
                   'margin': 0.08,
                   'commision_fix': 4,
                   'commision_float': 0,
                   'commision_fix_today': 4,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2013-09-26',
                   'begintime_local': '2015-12-17 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        m_dict = {'code': 'm',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.05,
                   'commision_fix': 1.5,
                   'commision_float': 0,
                   'commision_fix_today': 1.5,
                   'commision_float_today': 0,
                   'exchange_id': 'dce',
                   'ipo': '2000-07-17',
                   'begintime_local': '2014-12-26 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        y_dict = {'code': 'y',
                  'trading_unit': 10,
                  'min_change': 2,
                  'margin': 0.07,
                  'commision_fix': 2.5,
                  'commision_float': 0,
                  'commision_fix_today': 2.5,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2006-01-09',
                  'begintime_local': '2014-12-26 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                  }
        a_dict = {'code': 'a',
                  'trading_unit': 10,
                  'min_change': 1,
                  'margin': 0.07,
                  'commision_fix': 2,
                  'commision_float': 0,
                  'commision_fix_today': 2,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2002-03-15',
                  'begintime_local': '2014-12-26 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                  }
        b_dict = {'code': 'b',
                  'trading_unit': 10,
                  'min_change': 1,
                  'margin': 0.07,
                  'commision_fix': 1,
                  'commision_float': 0,
                  'commision_fix_today': 1,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2004-12-22',
                  'begintime_local': '2018-04-09 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                  }
        p_dict = {'code': 'p',
                  'trading_unit': 10,
                  'min_change': 2,
                  'margin': 0.07,
                  'commision_fix': 2.5,
                  'commision_float': 0,
                  'commision_fix_today': 2.5,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2014-07-04',
                  'begintime_local': '2018-04-09 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                  }
        rm_dict = {'code': 'rm',
                  'trading_unit': 10,
                  'min_change': 1,
                  'margin': 0.06,
                  'commision_fix': 1.5,
                  'commision_float': 0,
                  'commision_fix_today': 0,
                  'commision_float_today': 0,
                  'exchange_id': 'czce',
                  'ipo': '2014-12-12',
                  'begintime_local': '2014-12-12 21:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                  'trading_period_mode': '3',
                  'domi_month': ['01', '05', '09'],
                  }
        oi_dict = {'code': 'oi',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.07,
                   'commision_fix': 2,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2007-06-08',
                   'begintime_local': '2016-06-11 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        c_dict = {'code': 'c',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.07,
                   'commision_fix': 1.2,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'dce',
                   'ipo': '2004-09-22',
                   'begintime_local': '2008-07-10 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00']],
                   'trading_period_mode': '1',
                   'domi_month': ['01', '05', '09'],
                   }
        cs_dict = {'code': 'cs',
                  'trading_unit': 10,
                  'min_change': 1,
                  'margin': 0.07,
                  'commision_fix': 1.5,
                  'commision_float': 0,
                  'commision_fix_today': 1.5,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2014-12-19',
                  'begintime_local': '2014-12-19 09:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00']],
                  'trading_period_mode': '1',
                  'domi_month': ['01', '05', '09'],
                  }
        jd_dict = {'code': 'jd',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.08,
                   'commision_fix': 0,
                   'commision_float': 0.00015,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00015,
                   'exchange_id': 'dce',
                   'ipo': '2013-11-08',
                   'begintime_local': '2013-11-08 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00']],
                   'trading_period_mode': '1',
                   'domi_month': ['01', '05', '09'],
                   }
        sr_dict = {'code': 'sr',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.05,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2006-01-06',
                   'begintime_local': '2014-12-12 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        cf_dict = {'code': 'cf',
                   'trading_unit': 5,
                   'min_change': 5,
                   'margin': 0.07,
                   'commision_fix': 4.3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2004-06-01',
                   'begintime_local': '2014-12-12 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        ap_dict = {'code': 'ap',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.11,
                   'commision_fix': 20,
                   'commision_float': 0,
                   'commision_fix_today': 20,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2017-12-22',
                   'begintime_local': '2017-12-25 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00']],
                   'trading_period_mode': '1',
                   'domi_month': ['01', '05', '09'],
                   }
        ru_dict = {'code': 'ru',
                   'trading_unit': 10,
                   'min_change': 5,
                   'margin': 0.09,
                   'commision_fix': 0,
                   'commision_float': 0.000045,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.000045,
                   'exchange_id': 'shfe',
                   'ipo': '1993-11-30',
                   'begintime_local': '2014-12-26 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '2',
                   'domi_month': ['01', '05', '09'],
                   }
        l_dict = {'code': 'l',
                   'trading_unit': 5,
                   'min_change': 5,
                   'margin': 0.07,
                   'commision_fix': 2,
                   'commision_float': 0,
                   'commision_fix_today': 2,
                   'commision_float_today': 0,
                   'exchange_id': 'dce',
                   'ipo': '2007-07-31',
                   'begintime_local': '2008-06-25 09:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00']],
                   'trading_period_mode': '1',
                   'domi_month': ['01', '05', '09'],
                   }
        v_dict = {'code': 'v',
                  'trading_unit': 5,
                  'min_change': 5,
                  'margin': 0.07,
                  'commision_fix': 2,
                  'commision_float': 0,
                  'commision_fix_today': 0,
                  'commision_float_today': 0,
                  'exchange_id': 'dce',
                  'ipo': '2009-05-25',
                  'begintime_local': '2009-05-25 09:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00']],
                  'trading_period_mode': '1',
                  'domi_month': ['01', '05', '09'],
                  }
        pp_dict = {'code': 'pp',
                  'trading_unit': 5,
                  'min_change': 1,
                  'margin': 0.07,
                  'commision_fix': 0,
                  'commision_float': 0.00006,
                  'commision_fix_today': 0,
                  'commision_float_today': 0.00006,
                  'exchange_id': 'dce',
                  'ipo': '2014-02-28',
                  'begintime_local': '2014-02-28 09:00:00',
                  'endtime_local': endtime,
                  'trading_period': [['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00']],
                  'trading_period_mode': '1',
                  'domi_month': ['01', '05', '09'],
                  }
        ta_dict = {'code': 'ta',
                   'trading_unit': 5,
                   'min_change': 1,
                   'margin': 0.06,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 0,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2006-12-18',
                   'begintime_local': '2014-12-12 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        ma_dict = {'code': 'ma',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.07,
                   'commision_fix': 2,
                   'commision_float': 0,
                   'commision_fix_today': 6,
                   'commision_float_today': 0,
                   'exchange_id': 'czce',
                   'ipo': '2011-10-28',
                   'begintime_local': '2014-12-12 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '3',
                   'domi_month': ['01', '05', '09'],
                   }
        sc_dict = {'code': 'sc',
                   'trading_unit': 1000,
                   'min_change': 0.1,
                   'margin': 0.07,
                   'commision_fix': 20,
                   'commision_float': 0,
                   'commision_fix_today': 20,
                   'commision_float_today': 0,
                   'exchange_id': 'ine',
                   'ipo': '2018-03-26',
                   'begintime_local': '2018-03-26 09:00:00',
                   'endtime_local': endtime,
                   'trading_period':[['21:00:00', '23:00:00'],
                                     ['23:00:01', '23:30:00'],
                                     ['23:30:01', '23:59:59'],
                                     ['00:00:00', '01:00:00'],
                                     ['01:00:01', '02:30:00'],
                                     ['09:00:00', '10:15:00'],
                                     ['10:30:00', '11:30:00'],
                                     ['13:30:00', '15:00:00'],
                                     ],
                   'trading_period_mode': '5',
                   'domi_month': ['01','02','03','04','05','06',
                                 '07','08','09','10','11','12'],
                   }
        fu_dict = {'code': 'fu',
                   'trading_unit': 10,
                   'min_change': 1,
                   'margin': 0.10,
                   'commision_fix': 0,
                   'commision_float': 0.00005,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00005,
                   'exchange_id': 'shfe',
                   'ipo': '2018-07-16',
                   'begintime_local': '2018-07-16 21:00:00',
                   'endtime_local': endtime,
                   'trading_period': [['21:00:00', '23:00:00'],
                                      ['23:00:01', '23:30:00'],
                                      ['23:30:01', '23:59:59'],
                                      ['00:00:00', '01:00:00'],
                                      ['01:00:01', '02:30:00'],
                                      ['09:00:00', '10:15:00'],
                                      ['10:30:00', '11:30:00'],
                                      ['13:30:00', '15:00:00'],
                                      ],
                   'trading_period_mode': '5',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '10', '11', '12'],
                   }





        commodity_info['cu'] = cu_dict
        commodity_info['al'] = al_dict
        commodity_info['zn'] = zn_dict
        commodity_info['pb'] = pb_dict
        commodity_info['ni'] = ni_dict
        commodity_info['sn'] = sn_dict
        commodity_info['au'] = au_dict
        commodity_info['ag'] = ag_dict
        commodity_info['rb'] = rb_dict
        commodity_info['hc'] = hc_dict
        commodity_info['i'] = i_dict
        commodity_info['jm'] = jm_dict
        commodity_info['j'] = j_dict
        commodity_info['sf'] = sf_dict
        commodity_info['sm'] = sm_dict
        commodity_info['bu'] = bu_dict
        commodity_info['fg'] = fg_dict
        commodity_info['zc'] = zc_dict
        commodity_info['m'] = m_dict
        commodity_info['y'] = y_dict
        commodity_info['a'] = a_dict
        commodity_info['b'] = b_dict
        commodity_info['p'] = p_dict
        commodity_info['rm'] = rm_dict
        commodity_info['oi'] = oi_dict
        commodity_info['c'] = c_dict
        commodity_info['cs'] = cs_dict
        commodity_info['jd'] = jd_dict
        commodity_info['sr'] = sr_dict
        commodity_info['cf'] = cf_dict
        commodity_info['ap'] = ap_dict
        commodity_info['ru'] = ru_dict
        commodity_info['l'] = l_dict
        commodity_info['v'] = v_dict
        commodity_info['pp'] = pp_dict
        commodity_info['ta'] = ta_dict
        commodity_info['ma'] = ma_dict
        commodity_info['sc'] = sc_dict
        commodity_info['fu'] = fu_dict

        finance_info = {}
        finance = ['IF', 'IH', 'IC', 'TF', 'T']

        if_dict = {'code': 'if',
                   'trading_unit': 300,
                   'min_change': 0.2,
                   'margin': 0.15,
                   'commision_fix': 0,
                   'commision_float': 0.00025,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00025,
                   'exchange_id': 'cffex',
                   'ipo': '2010-04-16',
                   'local_year': 2010,
                   'local_month': 5,
                   'trading_period': [['09:30:00', '11:30:00'],
                                      ['13:00:00', '15:00:00']],
                   'trading_period_mode': 'if',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '12'],
                   }
        ih_dict = {'code': 'ih',
                   'trading_unit': 300,
                   'min_change': 0.2,
                   'margin': 0.15,
                   'commision_fix': 0,
                   'commision_float': 0.00025,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00025,
                   'exchange_id': 'cffex',
                   'ipo': '2015-04-16',
                   'local_year': 2015,
                   'local_month': 8,
                   'trading_period': [['09:30:00', '11:30:00'],
                                      ['13:00:00', '15:00:00']],
                   'trading_period_mode': 'if',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '12'],
                   }
        ic_dict = {'code': 'ic',
                   'trading_unit': 200,
                   'min_change': 0.2,
                   'margin': 0.08,
                   'commision_fix': 0,
                   'commision_float': 0.00025,
                   'commision_fix_today': 0,
                   'commision_float_today': 0.00025,
                   'exchange_id': 'cffex',
                   'ipo': '2015-04-16',
                   'local_year': 2015,
                   'local_month': 4,
                   'trading_period': [['09:30:00', '11:30:00'],
                                      ['13:00:00', '15:00:00']],
                   'trading_period_mode': 'if',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '12'],
                   }
        tf_dict = {'code': 'tf',
                   'trading_unit': 10000,
                   'min_change': 0.005,
                   'margin': 0.01,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 3,
                   'commision_float_today': 0,
                   'exchange_id': 'cffex',
                   'ipo': '2015-04-16',
                   'local_year': 2013,
                   'local_month': 12,
                   'trading_period': [['09:15:00', '11:30:00'],
                                      ['13:00:00', '15:15:00']],
                   'trading_period_mode': 'tf',
                   'domi_month': ['03', '06', '09', '12'],

                   }
        t_dict = {'code': 't',
                   'trading_unit': 10000,
                   'min_change': 0.005,
                   'margin': 0.02,
                   'commision_fix': 3,
                   'commision_float': 0,
                   'commision_fix_today': 3,
                   'commision_float_today': 0,
                   'exchange_id': 'cffex',
                   'ipo': '2015-03-20',
                   'local_year': 2015,
                   'local_month': 9,
                   'trading_period': [['09:30:00', '11:30:00'],
                                      ['13:00:00', '15:15:00']],
                   'trading_period_mode': 'if',
                   'domi_month': ['01', '02', '03', '04', '05', '06',
                                  '07', '08', '09', '12'],
                   }
        finance_info['if'] = if_dict
        finance_info['ih'] = ih_dict
        finance_info['ic'] = ic_dict
        finance_info['tf'] = tf_dict
        finance_info['t'] = t_dict


        return commodity_info, finance_info
    # 输入id，date，获取当前“可能”运行的主力合约，只要运行时间在一年内的，1809，只认为它在17年10月份之后再“运行”
    def instrumentid_contract(self, id, date):
        commodity_info, futures_info = self.futures_info()
        # 获取id的info
        try:
            domi_mon = commodity_info[id.lower()]['domi_month']
        except KeyError:
            domi_mon = futures_info[id.lower()]['domi_month']
        # 年份当年和下一年，月份
        year_1 = date[0:4]
        year_2 = str(int(date[0:4]) + 1)
        mon = date[5:7]
        # 当年的list 和下一年的list
        li1 = []
        li2 = []
        for m in domi_mon:
            li1.append([year_1, m])
            li2.append([year_2, m])
        i = 0
        while i < len(domi_mon):
            if domi_mon[i] > mon:
                li = li1[i:]
                for j in li2:
                    li.append(j)
                break
            # 如果主力合约循环至最后也没有大于当前月份
            elif i == len(domi_mon) - 1:
                li = li2
                break
            else:
                i += 1
        # 只要合约长度那么多的list
        li = li[0:len(domi_mon)]
        # 查看最后的合约，如果月份大于当前月份，不要这个月份的
        if li[-1][1] >= mon:
            li.remove(li[-1])
        return li
    # id，某年y，某月m下一个合约
    def next_domi(self, id, y, m): # 输入id，年份，月份，获取下一个主力合约
        commodity_info, futures_info = self.futures_info()
        domi_mon = commodity_info[id.lower()]['domi_month']
        year_1 = y
        year_2 = str(int(y) + 1)
        li = []
        for y_ in [year_1, year_2]:
            for m_ in domi_mon:
                li.append([y_, m_])
        i = 0
        while i < len(li):
            if li[i][0] == y and li[i][1] == m:
                out_y = li[i + 1][0]
                out_m = li[i + 1][1]
                break
            else:
                i += 1

        return out_y, out_m
    # id，某年y，某月m上一个主力合约
    def pre_domi(self, id, y, m): # 输入id，年份，月份，获取上一个主力合约
        commodity_info, futures_info = self.futures_info()
        domi_mon = commodity_info[id.lower()]['domi_month']
        year_1 = str(int(y) - 1)
        year_2 = y
        li = []
        for y_ in [year_1, year_2]:
            for m_ in domi_mon:
                li.append([y_, m_])
        i = 0
        while i < len(li):
            if li[i][0] == y and li[i][1] == m:
                out_y = li[i - 1][0]
                out_m = li[i - 1][1]
                break
            else:
                i += 1
        return out_y, out_m
    # 获取某个date=‘2018-02-02’下的需要更新的windlist
    def wind_list(self, date, datepre): # 获取所有某一日期所有需要更新的InstrumentID
        commodity_list, finance_list = self.futures_list()
        commodity_info, futures_info = self.futures_info()
        f_list = []
        c_list = []
        for id in finance_list:
            id = id.lower()
            codes = self.instrumentid_contract(id, date) # 解决codes
            for tempt in codes:
                field = 'last,volume,oi' # field
                if id == 't' or id == 'tf':
                    begintime = date + ' 09:15:00' # begintime
                    endtime = date + ' 15:15:00'
                else:
                    begintime = date + ' 09:30:00'
                    endtime = date + ' 15:00:00'
                code = id.upper() + tempt[0][2:4] + tempt[1] + '.CFE'
                f_list.append([code, field, begintime, endtime])
        for id in commodity_list:
            id = id.lower()
            codes = self.instrumentid_contract(id, date)
            for cod in codes:
                # 处理cod
                code = id.upper() + cod[0][2:4] + cod[1]
                if commodity_info[id]['exchange_id'] == 'shfe':
                    exchange_id = '.SHF'
                elif commodity_info[id]['exchange_id'] == 'dce':
                    exchange_id = '.DCE'
                elif commodity_info[id]['exchange_id'] == 'czce':
                    exchange_id = '.CZC'
                elif commodity_info[id]['exchange_id'] == 'ine':
                    exchange_id = '.INE'
                else:
                    pass
                code = code + exchange_id
                field = 'last,volume,oi' # field
                # 处理begintime
                if commodity_info[id]['trading_period_mode'] > '1':
                    begintime = datepre + ' 21:00:00'
                    endtime = date + ' 15:00:00'
                elif commodity_info[id]['trading_period_mode'] == '1':
                    begintime = date + ' 09:00:00'
                    endtime = date + ' 15:00:00'
                c_list.append([code, field, begintime, endtime])

        return f_list, c_list
    # 用于ctp方法更新数据的方法date='2018-02-02'，所有品种不适合，对网络造成较大压力
    def ctp_list(self, date):
        commodity_list, finance_list = self.futures_list()
        commo_list = []
        for id in commodity_list:
            id = id.lower()
            codes = self.instrumentid_contract(id, date)  # 解决codes
            for tempt in codes:
                code = id + tempt[0][2:4] + tempt[1]
                # 尽量减少合约的订阅，省掉计算机的内存等
                if tempt[0] != self.today[0:4] and tempt[1] >= self.today[5:7]:
                    pass
                else:
                    commo_list.append(code)
        return commo_list

    def update_list(self, date):
        commodity_info, futures_info = self.futures_info()
        commodity_list, finance_list = self.futures_list()
        self.ctp_list()
        year_1 = date[0:4]
        year_2 = str(int(date[0:4]) + 1)
        mon = date[5:7]
        for co in commodity_list:
            domi_mon = commodity_info[co.lower()]['domi_month']
            i = 0
            # 从第0个开始循环，直至发现大于当前月份的主力合约月份
            while i < len(domi_mon):
                # 如果主力合约月份 > 当前月份
                if domi_mon[i] > mon:
                    final_m = domi_mon[i]
                    year_1 = year_1
                    break
                # 如果主力合约循环至最后也没有大于当前月份
                elif i == len(domi_mon) - 1 :
                    final_m = 0
                    break
                else:
                    i += 1
            if final_m == 0:
                pass


if __name__ == '__main__':
    # 测试
    self = Futures_Info()
    commodity_list, finance_list = self.futures_list()
    commodity_info, finance_info = self.futures_info()
    li = self.instrumentid_contract('cu', '2018-08-21')
    y, m = self.next_domi('cu', '2018', '01')
    y, m = self.pre_domi('cu', '2018', '01')
    f_list, c_list = self.wind_list('2018-08-21', '2018-08-20')
    self.ctp_list('2018-08-21')


