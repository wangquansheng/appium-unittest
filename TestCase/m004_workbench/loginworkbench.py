import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """
    分解前置条件
    """

    @staticmethod
    def select_single_cmcc_android_4g_client():
        """
        启动
        1、4G，安卓客户端
        2、移动卡
        :return:
        """
        client = switch_to_mobile(REQUIRED_MOBILES['测试机'])
        client.connect_mobile()

    @staticmethod
    def select_assisted_mobile2():
        """切换到单卡、异网卡Android手机 并启动应用"""
        switch_to_mobile(REQUIRED_MOBILES['辅助机2'])
        current_mobile().connect_mobile()

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        permission_list.click_permission_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def make_already_in_sms_login_page():
        """
        1、已经进入短信登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        permission_list.wait_for_page_load(30)
        permission_list.click_submit_button()
        page_name = one_key.wait_one_key_or_sms_login_page_load(30)
        if page_name == 'sms':
            return
        one_key.choose_another_way_to_login()
        SmsLoginPage().wait_for_page_load()

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        # one_key.click_read_agreement_detail()
        #
        # # 同意协议
        # agreement = AgreementDetailPage()
        # agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)
        return login_number

    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        # me.scroll_to_bottom()
        # me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def app_start_for_the_first_time():
        """首次启动APP（使用重置APP代替）"""
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().capabilities['appPackage']
        current_mobile().terminate_app(app_id)

    @staticmethod
    def background_app(seconds):
        """后台运行"""
        current_mobile().background_app(seconds)

    @staticmethod
    def diff_card_make_already_in_sms_login_page():
        """确保异网卡已在短信登录界面"""
        sms = SmsLoginPage()
        if sms.is_on_this_page():
            return
        current_mobile().reset_app()
        guide_page = GuidePage()
        guide_page.wait_until(
            lambda d: guide_page.is_text_present("解锁“免费通信”新攻略")
        )
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 确定
        PermissionListPage(). \
            wait_for_page_load(). \
            click_submit_button()
        SmsLoginPage().wait_for_page_load()

    @staticmethod
    def diff_card_enter_sms_login_page(required_mobiles_key):
        """异网卡进入短信登录界面"""
        client = switch_to_mobile(REQUIRED_MOBILES[required_mobiles_key])
        client.connect_mobile()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @staticmethod
    def diff_card_login_by_sms(card_type, login_time=60):
        """异网卡短信登录"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        phone_numbers = current_mobile().get_cards(card_type)
        # 输入电话号码
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        # 输入验证码
        sl.input_verification_code(code)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        MessagePage().wait_login_success(login_time)

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """
        前置条件：
        1.已登录客户端
        2.当前在消息页面
        """
        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        login_num = Preconditions.login_by_one_key_login()
        return login_num

@unittest.skip("一键登录先不执行")
class LoginWorkBench(TestCase):
    """登录"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    @staticmethod
    def setUp_test_DL_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_DL_0001(self):
        """ 一键登录"""
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()

    @staticmethod
    def setUp_test_DL_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_DL_0002(self):
        """ 双卡移动号码一键登录"""
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()

    @staticmethod
    def setUp_test_DL_0004():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_DL_0004(self):
        """ 移动号码一键登录"""
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()
