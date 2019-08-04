import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from pages.components import ChatNoticeDialog, SearchBar, ContactsSelector
from pages.components.PickGroup import PickGroupPage
from pages.components.SearchGroup import SearchGroupPage
from pages.message.FreeMsg import FreeMsgPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *

class Preconditions(LoginPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0320():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_my_computer_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0320(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的不可预览文件
        # 3、网络异常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_transmit_record_file()

    def tearDown_test_msg_weifenglian_PC_0320(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

