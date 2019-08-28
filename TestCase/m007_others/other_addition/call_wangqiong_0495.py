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
    def setUp_test_call_wangqiong_0495():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0495(self):
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
        cmvp.input_contact_search("13800138222")
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
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        current_mobile().set_network_status(0)
        time.sleep(2)
        mess.page_should_contain_text('当前网络不可用，为管理通话成员状态，请连接wifi或启用VoLTE')
        current_mobile().set_network_status(6)
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()


    def tearDown_test_call_wangqiong_095(self):
        current_mobile().set_network_status(6)

