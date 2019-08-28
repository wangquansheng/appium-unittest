import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0115():
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
    def test_msg_huangcaizui_D_0115(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        cmvp.click_text('未知号码')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(3)
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在飞信电话'))
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()


