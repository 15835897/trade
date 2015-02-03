# -*- coding:utf-8 -*-

"""
    在pyctp2的父目录中, 执行
    python red.py pyctp2.sbin.md2 md_exec
"""


import logging

from ..common.base import INFO_PATH,DATA_PATH
from ..md import ctp_md as cm
from ..common import controller as ctl
from ..common.contract_type import CM_ALL
from ..md import save_agent as save_agent

from ..my.ports import ZSUsersC as my_ports

def make_users(mduser,contract_managers):
    controller = ctl.TController()
    mdagents = [save_agent.SaveAgent(cmng,DATA_PATH) for cmng in contract_managers]
    #logging.info('md2,mdagents:%s',mdagents)
    for mdagent in mdagents:
        controller.register_agent(mdagent)
    tt = ctl.Scheduler(160000,controller.day_finalize,24*60*60)
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
        controller.add_listener(md_spi)
        szport=port.encode(encoding='utf-8', errors = 'strict')
        user.RegisterFront(szport)
        #print('before init')
        user.Init()
        users.append(user)
    controller.reset()
    controller.start()
    return controller,users#,tt

def md_exec():
    '''
        当前使用版本
    '''
    logging.basicConfig(filename="%s/pyctp2_md.log" % (INFO_PATH,),level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    return make_users(my_ports,[CM_ALL])

