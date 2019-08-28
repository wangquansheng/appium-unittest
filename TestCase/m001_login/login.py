import re
import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.login import Agreement
import preconditions
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
    """分解前置条件"""

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
class LoginTest(TestCase):
    """Login 模块"""

    @staticmethod
    def setUp_test_login_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        Preconditions.take_logout_operation_if_already_login()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_login_0001(self, login_time=60):
        """ 本网非首次登录已设置头像-一键登录页面元素检查"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 检查电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_MOBILE)
        oklp.assert_phone_number_equals_to(phone_numbers[0])
        # 检查 服务协议等待页面进入引导页第一页（自动允许权限）
        oklp.page_should_contain_text("服务条款")
        # 登录
        # oklp.check_the_agreement()
        oklp.click_one_key_login()
        MessagePage().wait_login_success(login_time)

    @staticmethod
    def setUp_test_login_0002():
        # 1、已登录
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        # 2、进入我页面（切换到后台之前不应该停留在消息页面，防止误判）
        MessagePage().open_me_page()
        MePage().wait_for_page_load()
        # 3、退出后台
        current_mobile().press_home_key()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_login_0002(self):
        """已登录状态后，退出后台"""
        current_mobile().activate_app('com.chinasofti.rcs')
        mp = MePage()
        # 验证打开的页面是否是退出之前的界面（我 页面）
        mp.wait_for_page_load()

    @unittest.skip("IOS先不做")
    def test_login_0003(self, phone_number='14775970982', login_time=60):
        """登录页面检查"""
        # TODO IOS手机还没做
        OneKeyLoginPage(). \
            wait_for_page_load(). \
            assert_phone_number_equals_to(phone_number). \
            check_the_agreement(). \
            click_one_key_login()

        MessagePage().wait_for_page_load(login_time)

    @staticmethod
    def setUp_test_login_0004():
        """选择安卓移动卡手机进入一键登录页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()

    @unittest.skip("存在自动化无法实现的高频点击操作")
    def test_login_0004(self):
        """登录页面检查"""
        # TODO XIN  存在自动化无法实现的高频点击操作
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        one_key.choose_another_way_to_login()

        sms = SmsLoginPage()
        sms.wait_for_page_load()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sms.input_phone_number(phone_number)
        result = sms.get_verification_code(60)
        self.assertIn('【登录验证】尊敬的用户', result)
        code = re.findall(r'\d+', result)
        sms.input_verification_code(code)
        sms.click_login()
        sms.click_i_know()
        MessagePage().wait_for_page_load(60)

    @unittest.skip("IOS用例先不做")
    def test_login_0005(self):
        """登录页面检查"""
        # TODO IOS用例先不做
        pass

    @staticmethod
    def setUp_test_login_0006():
        """选择安卓移动卡手机进入一键登录页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_login_0006(self):
        """服务条款检查"""
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        # 检查服务条款内容
        AgreementPage().wait_for_license_agreement_load()

    @staticmethod
    def setUp_test_login_0007():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_login_0007(self):
        """服务条款检查"""
        oklp = OneKeyLoginPage()
        # 点击许可服务协议
        oklp.click_license_agreement()
        Agreement.AgreementPage().wait_for_license_agreement_load()

    def setUp_test_login_0008(self):
        """测试机登录客户端、辅助机打开到验证码登录页"""
        # A手机已经登录
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        Preconditions.make_already_in_one_key_login_page()
        one_key = OneKeyLoginPage().wait_for_tell_number_load(60)
        self.login_number = one_key.get_login_number()
        Preconditions.login_by_one_key_login()

        # B手机进入短信登录界面
        Preconditions.select_mobile('Android-电信')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        Preconditions.make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', '移动-电信')
    def test_login_0008(self):
        """下线提醒"""
        # 切换到辅助机2，并用测试机的号码登录
        Preconditions.select_mobile('Android-电信')
        sms_page = SmsLoginPage()
        sms_page.wait_for_page_load(30)
        sms_page.input_phone_number(self.login_number)
        # sms_page.click_get_code()

        # 切换回测试机取验证码
        mobile1 = Preconditions.select_mobile('Android-移动')
        with mobile1.listen_verification_code(120) as code:
            # 切换到手机2获取验证码
            switch_to_mobile(REQUIRED_MOBILES['Android-电信'])
            sms_page.click_get_code()
        # code = sms_page.listen_verification_code(60)

        # 切换到辅助机2
        Preconditions.select_mobile('Android-电信')
        sms_page.input_verification_code(code)
        sms_page.click_login()
        OneKeyLoginPage().click_read_agreement_detail()
        AgreementDetailPage().click_agree_button()
        sms_page.click_i_know()

        message_page = MessagePage()
        message_page.wait_for_page_load(60)

        # 切换回测试机等待下线提示
        Preconditions.select_mobile('Android-移动')
        message_page.wait_until(
            condition=lambda d: message_page.is_text_present('下线通知'),
            timeout=30
        )

    @staticmethod
    def setUp_test_login_0009():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC_RESET')
    def test_login_0009(self):
        """登录页面检查"""
        oklp = OneKeyLoginPage()
        oklp.page_should_contain_text("语言")
        oklp.page_should_contain_text("一键登录")
        oklp.page_should_contain_text("服务条款")
        oklp.page_should_contain_client_logo_pic()


    @staticmethod
    def setUp_test_login_0010():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', '移动-联通')
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

    @staticmethod
    def setUp_test_login_0020():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', "移动-移动")
    def test_login_0020(self):
        """双移动卡登录"""
        oklp = OneKeyLoginPage()
        # 获取网络链接状态
        network_status = oklp.get_network_status()
        # 断开网络连接
        oklp.set_network_status(1)
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 恢复网络连接
        oklp.set_network_status(network_status)

    @staticmethod
    def setUp_test_login_0022():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', "移动-联通")
    def test_login_0022(self):
        """一移动一异网卡登录"""
        oklp = OneKeyLoginPage()
        # 断开网络连接
        oklp.set_network_status(1)
        # 页面检查
        oklp.page_should_contain_text("语言")
        oklp.page_should_contain_text("一键登录")
        oklp.page_should_contain_text("服务条款")
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        sms = SmsLoginPage()
        sms.wait_for_page_load()
        sms.page_should_contain_text("切换另一号码登录")
        self.assertEqual(sms.login_btn_is_checked(), 'false')
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sms.input_phone_number(phone_numbers[0])
        sms.input_verification_code(654805)
        # 点击登录
        sms.click_login()
        time.sleep(0.5)
        if sms.is_text_present("查看详情"):
            # 查看详情
            sms.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sms.is_text_present("我知道了"):
            # 点击‘我知道了’
            sms.click_i_know()
        # 网络异常提示
        flag = sms.is_toast_exist("当前网络不可用(102101)")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0022():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        oklp.set_network_status(6)

    @staticmethod
    def setUp_test_login_0023():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', "移动-移动")
    def test_login_0023(self):
        """双移动卡登录"""
        oklp = OneKeyLoginPage()
        # 检查一键登录
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)
        # 切换另一号码登录
        oklp.choose_another_way_to_login()
        oklp.wait_for_page_load()
        oklp.wait_for_tell_number_load(timeout=60)

    @staticmethod
    def setUp_test_login_0025():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0025(self):
        """非首次已设置头像昵称登录短信登录页元素显示(异网单卡)"""
        sl = SmsLoginPage()
        sl.page_should_contain_text("输入本机号码")
        sl.page_should_contain_text("输入验证码")
        sl.page_should_contain_text("获取验证码")
        self.assertEqual(sl.login_btn_is_checked(), 'false')

    @staticmethod
    def setUp_test_login_0026():
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0026(self):
        """输入验证码验证-异网用户，正确有效的6位（断网)"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入验证码
        sl.input_verification_code(code)
        # 断开网络连接
        sl.set_network_status(1)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 网络异常提示
        flag = sl.is_toast_exist("当前网络不可用(102101)")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0026():
        # 恢复网络连接
        sl = SmsLoginPage()
        sl.set_network_status(6)

    @staticmethod
    def setUp_test_login_0027():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0027(self):
        """输入验证码验证-错误的6位（异网用户）"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入错误验证码
        code = str(int(code) + 1)
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
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0029():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0029(self):
        """输入验证码验证-（异网）正确失效的6位验证码"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code)
        # 输入失效的验证码
        for i in range(60):
            xxx = sl.driver.current_activity
            time.sleep(5)
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
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0036():
        """异网账号进入登录页面"""
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', '联通')
    def test_login_0036(self):
        """验证码重新获取后-（异网用户）输入之前的验证码提示"""
        sl = SmsLoginPage()
        sl.wait_for_page_load()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        # 获取验证码
        code1 = sl.get_verify_code_by_notice_board()
        self.assertIsNotNone(code1)
        time.sleep(30)
        # 第二次获取验证码
        code2 = sl.get_verify_code_by_notice_board()
        # 输入之前的验证码
        sl.input_verification_code(code1)
        # 点击登录
        sl.click_login()
        time.sleep(0.5)
        if sl.is_text_present("查看详情"):
            # 查看详情
            sl.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sl.is_text_present("我知道了"):
            # 点击‘我知道了’
            sl.click_i_know()
        # 获取异常提示
        flag = sl.is_toast_exist("验证码有误，请重新输入(103108)")
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_login_0047():
        Preconditions.select_mobile('Android-电信')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_sms_login_page()

    @unittest.skip('移动单卡短信登录做不了')
    def test_login_0047(self):
        """验证码获取-重新获取，输入框已输内容清空"""
        # TODO 移动单卡短信登录做不了
        pass

    @staticmethod
    def setUp_test_login_0048():
        """
        预置条件：
        1、异网账号首次进入登录页面
        """
        Preconditions.select_mobile('Android-电信')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "电信")
    def test_login_0048(self):
        """短信验证码登录-（电信）异网用户首次登录"""
        Preconditions.diff_card_login_by_sms(CardType.CHINA_TELECOM)


    @staticmethod
    def setUp_test_login_0049():
        """
        预置条件：
        1、异网账号首次进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0049(self):
        """短信验证码登录-（联通）异网用户首次登录"""
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)

    @staticmethod
    def setUp_test_login_0050():
        """
        预置条件：
        1、异网账号(非首次登录)进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0050(self):
        """短信验证码登录-异网用户登录（非首次)"""
        # 登录
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)
        # 退出
        Preconditions.take_logout_operation_if_already_login()
        # 登录
        Preconditions.diff_card_login_by_sms(CardType.CHINA_UNION)

    @staticmethod
    def setUp_test_login_0051():
        """
        预置条件：
        1、异网账号进入登录页面
        """
        Preconditions.select_mobile('Android-联通')
        current_mobile().hide_keyboard_if_display()
        Preconditions.diff_card_make_already_in_sms_login_page()

    @tags('ALL', 'SMOKE', "联通")
    def test_login_0051(self):
        """短信验证码登录-异网不显示一键登录入口"""
        sl = SmsLoginPage()
        # 输入电话号码
        phone_numbers = current_mobile().get_cards(CardType.CHINA_UNION)
        sl.input_phone_number(phone_numbers[0])
        sl.page_should_not_contain_text("一键登录")

    @staticmethod
    def setUp_test_login_0052():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0052(self):
        """ 界面点击“语言”按钮"""
        oklp = OneKeyLoginPage()
        oklp.wait_for_page_load()
        # 点击“语言”按钮
        oklp.click_language()
        sml = MeSetMultiLanguagePage()
        # 点击繁体中文
        sml.select_traditional_chinese()
        # 点击完成
        sml.click_finish()
        # 检查繁体中文
        try:
            oklp.wait_until(
                condition=lambda d: oklp.is_text_present('一鍵登入')
            )
        except TimeoutException:
            raise AssertionError('没有找到繁体字文案：一键登录')
        # 为不影响其他用例，切换回简体中文
        oklp.click_language()
        sml.select_simplified_chinese()
        sml.click_finish()
        oklp.wait_for_page_load()

    @staticmethod
    def setUp_test_login_0056():
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        if not current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                         replace=True)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0056(self):
        """ 先卸载后安装"""
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        Preconditions.make_already_in_message_page()

    def tearDown_test_login_0056(self):
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        if current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            return

        # 预防安装应用的时候发生异常，尝试恢复安装，（还不知道好不好使）
        reinstall_try_time = 3
        while reinstall_try_time > 0:
            try:
                current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
                current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                             replace=True)
                break
            except:
                reinstall_try_time -= 1
                if reinstall_try_time == 0:
                    import traceback
                    traceback.print_exc()

    @staticmethod
    def setUp_test_login_0057():
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        if not current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                         replace=True)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_login_0057(self):
        """ 覆盖安装"""
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        Preconditions.make_already_in_message_page()

    def tearDown_test_login_0057(self):
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        if current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            return

        # 预防安装应用的时候发生异常，尝试恢复安装，（还不知道好不好使）
        reinstall_try_time = 3
        while reinstall_try_time > 0:
            try:
                current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
                current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                             replace=True)
                break
            except:
                reinstall_try_time -= 1
                if reinstall_try_time == 0:
                    import traceback
                    traceback.print_exc()


    @staticmethod
    def setUp_test_login_0072():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC_RESET')
    def test_login_0072(self, login_time=60):
        '''
        有网络,安卓和飞信APP未登录开机屏检查
        :param login_time:
        :return:
        '''
        oklp = OneKeyLoginPage()
        Preconditions.terminate_app()
        sl = SmsLoginPage()
        sl.page_should_not_contain_text('一键登陆')

    @staticmethod
    def setUp_test_login_0073():

        Preconditions.select_mobile('Android-移动')
        oklp = OneKeyLoginPage()
        oklp.set_network_status(1)
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC')
    def test_login_0073(self, logintime=60):
        '''
        无网络,安桌飞信APP未登录开机屏检查
        :param logintime:
        :return:
        '''
        oklp = OneKeyLoginPage()
        # preconditions.force_close_and_launch_app()
        current_mobile().launch_app()
        sl = SmsLoginPage()
        sl.page_should_not_contain_text('一键登陆')

    @staticmethod
    def tearDown_test_login_0073():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        oklp.set_network_status(6)

    @staticmethod
    def setUp_test_login_0074():
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        if not current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                         replace=True)

    @tags('ALL', 'Login', 'CMCC_RESET')
    def test_login_0074(self):
        """ 先卸载后安装"""
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        #  Preconditions.make_already_in_message_page()
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        sl = SmsLoginPage()
        sl.page_should_not_contain_text('一键登陆')

    @staticmethod
    def setUp_test_login_0075():
        from settings.available_devices import TARGET_APP
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        if not current_mobile().is_app_installed(TARGET_APP.get('APP_PACKAGE')):
            current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                         replace=True)

    @tags('ALL', 'Login', 'CMCC_RESET')
    def test_login_0075(self):
        """ 先卸载后安装"""
        # 卸载和飞信
        from settings.available_devices import TARGET_APP
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        #  Preconditions.make_already_in_message_page()
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.app_start_for_the_first_time()
        sl = SmsLoginPage()
        sl.page_should_not_contain_text('一键登陆')

    @staticmethod
    def setUp_test_login_0096():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        oklp = OneKeyLoginPage()
        oklp.set_network_status(1)
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', "移动")
    def test_login_0096(self):
        """一移动一异网卡登录"""
        oklp = OneKeyLoginPage()
        oklp.click_one_key_login()
        sms = SmsLoginPage()
        time.sleep(0.5)
        if sms.is_text_present("查看详情"):
            # 查看详情
            sms.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sms.is_text_present("我知道了"):
            # 点击‘我知道了’
            sms.click_i_know()
        # 网络异常提示
        flag = sms.is_toast_exist("当前网络不可用(102101)")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0096():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        oklp.set_network_status(6)

    @staticmethod
    def setUp_test_login_0113():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC')
    def test_login_0113(self):
        """ 界面点击“语言”按钮"""
        oklp = OneKeyLoginPage()
        oklp.wait_for_page_load()
        # 点击“语言”按钮
        oklp.click_language()
        sml = MeSetMultiLanguagePage()
        # 点击繁体中文
        sml.select_traditional_chinese()
        # 点击完成
        sml.click_finish()
        # 检查繁体中文
        time.sleep(2)
        try:
            oklp.wait_until(
                condition=lambda d: oklp.is_text_present('一鍵登入')
            )
        except TimeoutException:
            raise AssertionError('没有找到繁体字文案：一键登录')
        # 为不影响其他用例，切换回简体中文
        oklp.click_language()
        sml.select_simplified_chinese()
        sml.click_finish()
        oklp.wait_for_page_load()

    @staticmethod
    def setUp_test_login_0114():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC')
    def test_login_0114(self):
        """ 界面点击“语言”按钮"""
        oklp = OneKeyLoginPage()
        oklp.wait_for_page_load()
        # 点击“语言”按钮
        oklp.click_one_key_login()
        time.sleep(5)
        oklp.page_should_contain_text('查看详情')
        oklp.press_home_key(2)

    @staticmethod
    def setUp_test_login_0116():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC')
    def test_login_0116(self):
        """ 界面点击“语言”按钮"""

        oklp = OneKeyLoginPage()
        sl = SmsLoginPage()
        oklp.wait_for_page_load()
        oklp.click_one_key_login()
        time.sleep(1)
        oklp.page_should_contain_text('查看详情')
        # 查看详情
        sl.click_read_agreement_detail()
        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()
        time.sleep(1)
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')
        me_page.click_menu('退出')

    @staticmethod
    def setUp_test_login_0117():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', 'CMCC_RESET')
    def test_login_0117(self):
        """ 老版用户更新后登录"""
        oklp = OneKeyLoginPage()
        sl = SmsLoginPage()
        oklp.wait_for_page_load()
        oklp.click_one_key_login()
        time.sleep(1)
        oklp.page_should_contain_text('查看详情')
        # 查看详情
        sl.click_read_agreement_detail()
        # 同意协议
        agreement = AgreementDetailPage()
        agreement.click_agree_button()
        time.sleep(1)
        from settings.available_devices import TARGET_APP
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        time.sleep(5)
        current_mobile().activate_app()
        time.sleep(10)
        oklp.page_should_contain_text('消息')

    @staticmethod
    def tearDown_test_login_0117():
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()

    @staticmethod
    def setUp_test_login_0131():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        oklp = OneKeyLoginPage()
        oklp.set_network_status(1)
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', "移动")
    def test_login_0131(self):
        """无网络时，android统一认证提示"""
        oklp = OneKeyLoginPage()
        oklp.click_one_key_login()
        sms = SmsLoginPage()
        time.sleep(0.5)
        if sms.is_text_present("查看详情"):
            # 查看详情
            sms.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sms.is_text_present("我知道了"):
            # 点击‘我知道了’
            sms.click_i_know()
            # 网络异常提示
            #  flag = sms.is_toast_exist("当前网络不可用(102101)")
        flag = sms.is_toast_exist("当前网络不可用(102101)，请检查网络设置")
        self.assertTrue(flag)

    @staticmethod
    def tearDown_test_login_0131():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        oklp.set_network_status(6)
        oklp.press_home_key(2)

    @staticmethod
    def setUp_test_login_0135():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', "移动")
    def test_login_0135(self):
        """网络超时（ 假wifi或弱网环境），android统一认证提示"""
        oklp = OneKeyLoginPage()
        oklp.click_one_key_login()

        sms = SmsLoginPage()
        time.sleep(0.5)
        if sms.is_text_present("查看详情"):
            # 查看详情
            sms.click_read_agreement_detail()
            # 同意协议
            agreement = AgreementDetailPage()
            agreement.click_agree_button()
            time.sleep(0.5)
        if sms.is_text_present("我知道了"):
            # 点击‘我知道了’
            sms.click_i_know()
        # 网络异常提示
     #   flag=oklp.is_toast_exist('登录失败(57347)，请稍后重试')

        flag = sms.is_toast_exist("网络连接超时(102102)，请使用短信验证码登录")
        self.assertTrue(flag)
        oklp.press_home_key(2)

    @staticmethod
    def setUp_test_login_0122():
        """进入一键登录页"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.app_start_for_the_first_time()
        Preconditions.make_already_in_one_key_login_page()

    @tags('ALL', 'Login', "移动")
    def test_login_0122(self):
        """安卓/IOS登录界面，显示本机号码"""
        oklp = OneKeyLoginPage()
        time.sleep(3)
        phone_numbers = current_mobile().get_cards(CardType.CHINA_MOBILE)
        print(phone_numbers)
        oklp.assert_phone_number_equals_to(phone_numbers[0])
        oklp.press_home_key(times=2)