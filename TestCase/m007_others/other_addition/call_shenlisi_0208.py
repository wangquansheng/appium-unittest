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
    def setUp_test_call_shenlisi_0208():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0208(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(2)
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        ContactDetailsPage().click_video_call_icon()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        mess.page_should_contain_text('视频通话呼叫中')
        # Step 2、主叫方点击挂断按钮
        cp.hang_up_video_call()


