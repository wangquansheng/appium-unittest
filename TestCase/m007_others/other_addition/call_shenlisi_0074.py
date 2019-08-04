import time
import unittest
from pages.components.dialogs import SuspendedTips
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
    def setUp_test_call_shenlisi_0074():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])



    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0074(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_voice_call_icon()
        cp = CallPage()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        cp.page_should_contain_text('测试短信1')


    def tearDown_test_call_shenlisi_0074(self):
        Preconditions.disconnect_mobile('Android-移动')

