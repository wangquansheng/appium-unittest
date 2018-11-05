import re
import unittest

from library.core import Keywords
from library.core.TestCase import TestCase
from library.core.utils.WebDriverCache import DriverCache
from pages import *
from pages import Agreement
import time
from appium.webdriver.common.mobileby import MobileBy


class LoginTest(TestCase):
    """Login 模块"""

    @classmethod
    def setUpClass(cls):
        if DriverCache.current_driver is None:
            Keywords.Android.open_app()

    @classmethod
    def tearDownClass(cls):
        Keywords.Android.closed_current_driver()

    def default_setUp(self):
        """
        预置条件：
        1、双卡手机
        2、测试机能正常联网
        """
        # self.assertIn(Keywords.Android.get_network_state_code(), [2, 4, 6])  # 存在有网但是状态为0 的情况，不可以作为是否有网的条件
        guide_page = GuidePage()
        if guide_page.driver.current_activity == guide_page.ACTIVITY:
            # if guide_page._is_text_present("解锁“免费通信”新攻略"):
            guide_page.wait_until(
                lambda d: guide_page._is_text_present("解锁“免费通信”新攻略")
            )
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            guide_page.click_start_the_experience()

            # 确定
            PermissionListPage(). \
                wait_for_page_load(). \
                click_submit_button()

            # 等待页面进入一键登录页
            OneKeyLoginPage().wait_for_page_load()
        elif OneKeyLoginPage().is_current_activity_match_this_page():
            pass
        else:
            Keywords.Android.launch_app()
            guide_page.wait_for_page_load()
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            guide_page.click_start_the_experience()

            # 确定
            PermissionListPage(). \
                wait_for_page_load(). \
                click_submit_button()

            # 等待页面进入一键登录页
            OneKeyLoginPage().wait_for_page_load()

    def default_tearDown(self):
        pass

    @staticmethod
    def diff_card_enter_login_page():
        """异网卡进入登录界面"""
        guide_page = GuidePage()
        if guide_page.driver.current_activity == guide_page.ACTIVITY:
            guide_page.wait_until(
                lambda d: guide_page._is_text_present("解锁“免费通信”新攻略")
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
    def enter_login_page():
        """移动单卡进入登录界面"""
        guide_page = GuidePage()
        if guide_page.driver.current_activity == guide_page.ACTIVITY:
            # if guide_page._is_text_present("解锁“免费通信”新攻略"):
            guide_page.wait_until(
                lambda d: guide_page._is_text_present("解锁“免费通信”新攻略")
            )
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            guide_page.click_start_the_experience()

            # 确定
            PermissionListPage(). \
                wait_for_page_load(). \
                click_submit_button()

            # 等待页面进入一键登录页
            OneKeyLoginPage().wait_for_page_load()
        elif OneKeyLoginPage().is_current_activity_match_this_page():
            pass
        else:
            Keywords.Android.launch_app()
            guide_page.wait_for_page_load()
            guide_page.swipe_to_the_second_banner()
            guide_page.swipe_to_the_third_banner()
            guide_page.click_start_the_experience()

            # 确定
            PermissionListPage(). \
                wait_for_page_load(). \
                click_submit_button()

            # 等待页面进入一键登录页
            OneKeyLoginPage().wait_for_page_load()

    @staticmethod
    def one_key_login(phone_number='14775970982', login_time=60):
        """一键登录"""
        LoginTest.enter_login_page()
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            wait_for_tell_number_load(timeout=60). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0001(self):
        LoginTest.enter_login_page()

    @unittest.skip("skip 本网单卡测试test_login_0001")
    def test_login_0001(self, phone_number='14775970982', login_time=60):
        """ 本网非首次登录已设置头像-一键登录页面元素检查"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 检查电话号码
        oklp.assert_phone_number_equals_to(phone_number)
        # 检查 服务协议
        oklp.page_should_contain_text("服务协议")
        # 登录
        oklp.check_the_agreement()
        oklp.click_one_key_login()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0002(self):
        LoginTest.one_key_login()

    @unittest.skip("skip 本网单卡测试test_login_0002")
    def test_login_0002(self):
        """已登录状态后，退出后台"""
        mp = MessagePage()
        # app进入后台
        mp.run_app_in_background()
        mp.wait_for_page_load()
        # 检查是否是进入后台之前的页面
        mp.page_should_contain_text("我")
        mp.page_should_contain_text("通讯录")
        mp.page_should_contain_text("工作台")

    @unittest.skip("skip 移动账号登录")
    def test_login_C0003(self, phone_number='14775970982', login_time=60):
        """移动账号登录"""
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            wait_for_tell_number_load(timeout=60).\
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()
        MessagePage().wait_for_page_load(login_time)

    @unittest.skip("skip 测试条件是双卡")
    def test_login_C0004(self, phone_number='14775970982', login_time=60):
        """切换验证码登录"""
        onekey = OneKeyLoginPage()
        onekey.wait_for_page_load()
        onekey.choose_another_way_to_login()

        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.input_phone_number(phone_number)
        result = sms.get_verification_code(60)
        self.assertIn('【登录验证】尊敬的用户', result)
        code = re.findall(r'\d+', result)
        sms.input_verification_code(code)
        sms.click_login()
        sms.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0007(self):
        LoginTest.enter_login_page()

    @unittest.skip("skip 本网单卡测试test_login_0007")
    def test_login_0007(self):
        """服务条款检查"""
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        time.sleep(2)
        text = """和飞信业务是中国移动提供的通信服务，用户首次登录和飞信客户端即表示同意开通本业务，本业务不收取订购费用。如使用和飞信进行发送短信、拨打电话等功能可能会收取一定的费用。"""
        Agreement.AgreementPage().page_should_contain_text(text)

    def setUp_test_login_0010(self):
        LoginTest.enter_login_page()

    @unittest.skip("skip 一移动一异网卡登录测试test_login_0010")
    def test_login_0010(self):
        """一移动一异网卡登录"""
        oklp = OneKeyLoginPage()
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.page_should_contain_text("输入本机号码")
        sms.page_should_contain_text("输入验证码")
        sms.page_should_contain_text("获取验证码")
        sms.page_should_contain_text("切换另一号码登录")

    def setUp_test_login_0025(self):
        """异网账号进入登录页面"""
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试login_0025")
    def test_login_0025(self):
        """非首次已设置头像昵称登录短信登录页元素显示(异网单卡)"""
        sl = SmsLoginPage()
        sl.page_should_contain_text("输入本机号码")
        sl.page_should_contain_text("输入验证码")
        sl.page_should_contain_text("获取验证码")
        self.assertEqual(sl.login_btn_is_checked(), 'false')

    def setUp_test_login_0050(self):
        """
        预置条件：
        1、异网账号进入登录页面
        """
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试")
    def test_login_0050(self, phone_number='18681151872', login_time=60):
        """短信验证码登录-（联通）异网用户首次登录"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码，点击获取验证码
        sl.input_phone_number(phone_number)
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码，点击登录
        sl.input_verification_code(code)
        sl.click_login()
        sl.wait_for_i_know_load()
        # 点击‘我知道了’
        sl.click_i_know()
        MessagePage().wait_for_page_load(login_time)

    def setUp_test_login_0052(self):
        """
        预置条件：
        1、异网账号进入登录页面
        """
        LoginTest.diff_card_enter_login_page()

    @unittest.skip("skip 单卡异网账户测试login_0052")
    def test_login_0052(self, phone_number='18681151872'):
        """短信验证码登录-异网不显示一键登录入口"""
        sl = SmsLoginPage()
        # 输入电话号码
        sl.input_phone_number(phone_number)
        sl.page_should_not_contain_text("一键登录")


if __name__ == '__main__':
    unittest.main()
