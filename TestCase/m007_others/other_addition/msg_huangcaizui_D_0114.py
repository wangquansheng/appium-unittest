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
    def setUp_test_msg_huangcaizui_D_0114():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0114(self):
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
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_more_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在多方视频'))


