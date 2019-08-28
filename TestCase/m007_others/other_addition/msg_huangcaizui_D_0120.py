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
    def setUp_test_msg_huangcaizui_D_0120():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
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
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0120(self):
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
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_voice_call_small()
        mess.click_me_icon()
        me = MePage()
        me.click_setting_menu_631()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)
        mess.open_message_page()
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在语音通话'))


    def tearDown_test_msg_huangcaizui_D_0120(self):
        Preconditions.disconnect_mobile('Android-移动')

