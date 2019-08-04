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
    def setUp_test_call_zengxi_0005():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0005(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在视频通话'))
        mess.click_element_by_text('你正在视频通话')
        time.sleep(4)
        mess.is_toast_exist('通话结束')

    def tearDown_test_call_zengxi_0005(self):
        Preconditions.disconnect_mobile('Android-移动')

