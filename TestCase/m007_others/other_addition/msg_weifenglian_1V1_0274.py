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
    def setUp_test_msg_weifenglian_1V1_0274():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0274(self):
        """验证在单聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        # 1、当前在单聊会话窗口页面
        # 2、当前会话窗口有已下载的可预览文件
        # 3、网络正常
        mess = MessagePage()
        single_chat = SingleChatPage()
        single_chat.wait_for_page_load()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '2018-11-09 11-06-18-722582.log'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        single_chat.re_send_file_messages(file_name)


    def tearDown_test_msg_weifenglian_1V1_0274(self):
        Preconditions.disconnect_mobile('Android-移动')

