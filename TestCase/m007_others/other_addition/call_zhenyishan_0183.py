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
    def setUp_test_call_zhenyishan_0183():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0183(self):
        """主叫多方视频管理界面，检查挂断按钮"""
        # 1、已成功发起多方视频
        # 2、当前为主叫多方视频管理界面
        mess = MessagePage()
        # Step 1、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        cmvp.click_text('未知号码')
        cmvp.input_contact_search("13800138222")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        # Step 2、主叫方点击挂断按钮
        cmvp.click_end_video_call()
        cmvp.click_end_cancel()
        cmvp.page_should_contain_text('关闭摄像头')
        cmvp.click_end_video_call()
        cmvp.click_end_ok()
        time.sleep(3)
        cmvp.page_should_not_contain_text('关闭摄像头')


