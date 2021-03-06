# -*- coding:utf-8 -*-

"""
    在pyctp2的父目录中, 执行
    python red.py pyctp2.sbin.trade
"""

import logging
import time

from ..common.base import INFO_PATH
from ..common.utils import fcustom
from ..trader.environ import Environ
from ..trader.account import Account
from ..md import ctp_md as cm
from ..common.contract_type import CM_ALL
from ..common.contract_type import CM_ZJ

#定制部分
from ..my.ports import ZSTraders as trader_infos
#from ..my.ports import ZSUsersC as my_ports
from ..trader.builder import CommonBuilder


class XTrader(object):
    def __init__(self,triples):
        self._env = Environ()
        self._account = Account(self._env,trader_infos)
        self._builder = CommonBuilder(self._env,triples)
        #print('build')

    def play(self,mduser):
        logging.info("begin xtrade play.........")
        controller = self._env._controller
        users = []
        for port in mduser.ports:   #多路注册
            md_spi = cm.MdSpiDelegate(name=mduser.name.encode(encoding='utf-8', errors = 'strict'),
                                 broker_id=mduser.broker.encode(encoding='utf-8', errors = 'strict'),
                                 investor_id= mduser.investor.encode(encoding='utf-8', errors = 'strict'),
                                 passwd= mduser.passwd.encode(encoding='utf-8', errors = 'strict'),
                                 controller = controller,
                        )
            user = md_spi
            path=INFO_PATH+'/'+mduser.name
            szpath=path.encode(encoding='utf-8', errors = 'strict')
            user.Create(szpath)
            #user.Create('%s/%s' % (INFO_PATH,mduser.name))
            print('path:'+path)
            controller.add_listener(md_spi)
            szport=port.encode(encoding='utf-8', errors = 'strict')
            user.RegisterFront(szport)
            print('port:'+port)
            #user.RegisterFront(port)
            #print('before init')
            user.Init()
            users.append(user)
        controller.reset()
        controller.start()
        return self._env,users

from ..common.contract_type import ContractManager
from ..trader.coordinator import Coordinator
from ..sbin.trade_strategy import SExampleA5,SExampleAB5
from ..common.contract_type import M,P,J
from ..my.ports import ZSUsersC as my_ports

def play1():
    logging.basicConfig(filename="%s/pyctp2_trade.log" % (INFO_PATH, ),
                        level=logging.DEBUG,
                        format="%(module)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s"
                    )

    #cm1=CM_ZJ
    cm1 = ContractManager([P])
    #cm1 = ContractManager([M,P,J])
    triples = [ (Coordinator,fcustom(SExampleA5,max_times_per_day=1),cm1),
            ]
    xtrader = XTrader(triples)
    env,users = xtrader.play(my_ports)
    time.sleep(0.5)
    env.initialize()
    return env,users


def play2():
    logging.basicConfig(filename="%s/pyctp2_trade.log" % (INFO_PATH, ),
                        level=logging.DEBUG,
                        format="%(module)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s"
                    )

    cm1 = ContractManager([P,J])
    triples = [ (Coordinator,fcustom(SExampleAB5),cm1),
            ]
    xtrader = XTrader(triples)
    env,users = xtrader.play(my_ports)
    time.sleep(0.5)
    env.initialize()
    return env,users

