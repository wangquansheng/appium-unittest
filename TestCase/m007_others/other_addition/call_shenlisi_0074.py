import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components.dialogs import SuspendedTips
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_shenlisi_0074():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
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


