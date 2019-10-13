import random
import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):

    """前置条件"""
    def make_contact(name):
        contacts = ContactsPage()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        # 创建联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        number = "147752" + str(time.time())[-5:]
        ccp.create_contact(name, number)
        time.sleep(1)
        ccp.click_back_by_android(1)

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            sog.click_back()
            return
        sog.click_back()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_me_zhangshuli_064():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_064(self):
        """分享我的二维码"""
        # 打开‘我’页面
        me = MePage()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.click_phone_contact()
        local_contacts_page = SelectLocalContactsPage()
        local_contacts_page.input_search_keyword("大佬")
        local_contacts_page.hide_keyboard()
        elements = local_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name"]'))
        self.assertTrue(len(elements) > 2)

    @staticmethod
    def setUp_test_me_zhangshuli_065():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_qr_code_icon()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_065(self):
        """分享我的二维码"""
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.input_search_keyword("a")

        text = sc.get_text((MobileBy.ID, "com.chinasofti.rcs:id/tv_member_count"))
        self.assertTrue(lambda :(text.endswith(')') and text.startswith('(')))

    @staticmethod
    def setUp_test_me_zhangshuli_069():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_069(self):
        """分享我的二维码"""
        # 打开‘我’页面
        me = MePage()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.click_group_contact()
        # 选择团队联系人
        select_he_contacts_page = SelectHeContactsPage()

        select_he_contacts_page.input_search_contact_message('admin')
        select_he_contacts_page.driver.hide_keyboard()
        page = SelectContactsPage()
        page.wait_for_page_load()
        page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        exist = page.is_toast_exist("该联系人不可选择")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_070():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_070(self):
        """分享我的二维码"""
        team_name = 'admin'
        # 打开‘我’页面
        me = MePage()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()
        sc.input_search_contact_message(team_name)
        sc.driver.hide_keyboard()
        SelectContactsPage().click_search_he_contact()
        sc.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        exist = sc.is_toast_exist("该联系人不可选择")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_071():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_071(self):
        """分享我的二维码"""
        # 打开‘我’页面
        me = MePage()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()

        sc.input_search_contact_message('asdasdasfewefwe')
        sc.driver.hide_keyboard()
        SelectContactsPage().click_search_he_contact()
        time.sleep(3)
        elements = sc.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/no_contact_text'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_me_zhangshuli_078():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_078(self):
        """分享我的二维码"""
        # 打开‘我’页面
        me = MePage()
        me.click_qr_code_icon()
        my_qr_code_page = MyQRCodePage()
        my_qr_code_page.click_forward_qr_code()
        sc = SelectContactsPage()

        sc.input_search_contact_message("我的电脑")
        sc.driver.hide_keyboard()
        sc.select_one_contact_by_name("我的电脑")
        sc.click_sure_forward()
        exist = sc.is_toast_exist("已转发")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_083():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_083(self):
        """和包支付--授权"""

        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))

        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        if agreement_detail_page.page_should_contain_text("确认授权"):
            agreement_detail_page.click_text_or_description("确认授权")
        result = agreement_detail_page.is_exist_element_by_id('和包余额')
        self.assertTrue(result)

    @staticmethod
    def setUp_test_me_zhangshuli_084():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()
        me_page.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        if agreement_detail_page.page_should_contain_text("确认授权"):
            agreement_detail_page.click_text_or_description("确认授权")
        agreement_detail_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_084(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        result = agreement_detail_page.is_exist_element_by_id('和包余额')
        self.assertTrue(result)

    @staticmethod
    def setUp_test_me_zhangshuli_088():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_088(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        if agreement_detail_page.page_should_contain_text("确认授权"):
            agreement_detail_page.click_text_or_description("确认授权")
        agreement_detail_page.click_back()

    @staticmethod
    def setUp_test_me_zhangshuli_109():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_109(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "0.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_me_zhangshuli_110():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_110(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID,"com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        # 1.00
        # self.assertTrue(text == "1.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        # status = agreement_detail_page.get_network_status()
        # if status != 1:
        agreement_detail_page.set_network_status(0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_recharge'))
        exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)

    def tearDown_test_me_zhangshuli_110(self):
        mess = MessagePage()
        mess.set_network_status(6)

    def setUp_test_me_zhangshuli_112(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_112(self):
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        time.sleep(1)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)
        # 和包余额 区域id
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(1)
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        # 断开网络
        agreement_detail_page.set_network_status(0)
        # 点击充值
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_recharge'))
        exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)

    def tearDown_test_me_zhangshuli_112(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_116():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过,RCS用户")
    def test_me_zhangshuli_116(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        # 1.00
        # self.assertTrue(text == "1.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash_recharge'))

    @staticmethod
    def setUp_test_me_zhangshuli_123():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_123(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_cash'))
        self.assertTrue(text == "0.00")
        title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(title == "和包余额")
        get_elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        flag = False
        for el in get_elements:
            if el.text == "原和飞信零钱已合并至和包余额":
                flag = True
        self.assertTrue(flag)
        agreement_detail_page.click_text_or_description("提现")
        # exist = agreement_detail_page.is_toast_exist("和飞信：提现金额需大于0元")
        # self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_135():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过,RCS用户")
    def test_me_zhangshuli_135(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_goto_charge_redpaper'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/charge_content'))
        self.assertTrue(text == '可用流量不足100M，暂不能充到手机')

    @staticmethod
    def setUp_test_me_zhangshuli_136():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过,RCS用户")
    def test_me_zhangshuli_136(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_goto_charge_redpaper'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/charge_content'))
        self.assertTrue(text == '可用流量不足100M，暂不能充到手机')

    @staticmethod
    def setUp_test_me_zhangshuli_141():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过,RCS用户")
    def test_me_zhangshuli_141(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_goto_charge_redpaper'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/charge_content'))
        self.assertTrue(text == '可用流量不足100M，暂不能充到手机')
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_action_bar_help'))
        help_title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(help_title == '帮助手册')

    @staticmethod
    def setUp_test_me_zhangshuli_142(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_142(self):
        # 用例描述为:点击流量
        # 现版本无流量，修改为;点击和包余额
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        time.sleep(1)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)
        # 断开网络
        agreement_detail_page.set_network_status(0)
        # 和包余额 区域id
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)

    def tearDown_test_me_zhangshuli_142(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_143():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_143(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/lv_flow_area'))

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_right'))

        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/id_tv_no_data'))
        flag = False
        if text == "暂无流量相关账单":
            flag = True
        # 有数据怎么处理 TODO
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_me_zhangshuli_144():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_144(self):
        """和包支付--授权"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(5)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))

    @staticmethod
    def setUp_test_me_zhangshuli_146():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_146(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "111111111")
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "false")

    @staticmethod
    def setUp_test_me_zhangshuli_147():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_147(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "1111111111111111111111111")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        exist = agreement_detail_page.is_toast_exist("您的银行卡号有误，请核对后重试")
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_me_zhangshuli_148():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_148(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(5)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_mobile'), "")
        # TODO 身份证号无法修改
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_nextBtn'), "enabled")
        self.assertTrue(attribute == "false")

    @staticmethod
    def setUp_test_me_zhangshuli_149():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_149(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_mobile'), "")
        # TODO 身份证号无法修改
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_nextBtn'), "enabled")
        self.assertTrue(attribute == "false")

    @staticmethod
    def setUp_test_me_zhangshuli_153():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_153(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_mobile'), "")
        # TODO 身份证号无法修改
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_nextBtn'), "enabled")
        self.assertTrue(attribute == "false")

    @staticmethod
    def setUp_test_me_zhangshuli_155():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_155(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        time.sleep(5)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_agreement'))
        time.sleep(3)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_agreement_buttonConfirm'))
        addbankcard_title = agreement_detail_page.get_text(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_title'))

        self.assertTrue(addbankcard_title == "填写银行预留信息")

    @staticmethod
    def setUp_test_me_zhangshuli_156():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_156(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        time.sleep(5)
        # text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addcard_text'))
        # self.assertTrue(text == "绑定新的银行卡")# 绑定新的银行卡  添加银行卡
        # agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addcard_text'))

        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")
        time.sleep(3)
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_phone_btn'))
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_dialog_order_ok_button'))

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_name_img'))
        title_text = agreement_detail_page.get_text(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_dialog_explain_titleText'))
        self.assertTrue(title_text == "持卡人说明")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_dialog_explain_dismissBtn'))

        addbankcard_title = agreement_detail_page.get_text(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_title'))

        self.assertTrue(addbankcard_title == "填写银行预留信息")

    @staticmethod
    def setUp_test_me_zhangshuli_162():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_162(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "6214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_mobile'),
                                         "01234567891")
        # TODO  持卡人身份证号无法修改
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_inputKjCardInfo_nextBtn'), "enabled")
        self.assertTrue(attribute == "false")

    @staticmethod
    def setUp_test_me_zhangshuli_172():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_172(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "1214180300001315198")

        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        # FIXME 此处提示不是 请您输入有效的15-19位银行号  而是

        message_content = agreement_detail_page.get_text(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_dialog_message_content'))
        self.assertTrue(message_content == "您的银行卡号有误，请核对后重试")

    @staticmethod
    def setUp_test_me_zhangshuli_173():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_173(self):
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(5)
        # 点击银行卡
        elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        for e in elements:
            if e.text == "银行卡":
                e.click()
                # exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
                # self.assertTrue(exist)
                break
            else:
                continue
        time.sleep(3)
        # 点击 绑定新的银行卡
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         "1214180300001315198")
        # 断开网络
        agreement_detail_page.set_network_status(0)
        time.sleep(1)
        # 判断下一步是否可用
        attribute = agreement_detail_page.get_element_attribute((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        # 点击 下一步
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'))
        # 判定
        exist = agreement_detail_page.is_text_present("您的网络连接可能存在问题，请检查网络设置")
        self.assertTrue(exist)

    def tearDown_test_me_zhangshuli_173(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_174():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_174(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(5)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        card_number = "6214 1803 0000 1315 1981"
        error_card_number = card_number + "96"

        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         error_card_number)
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        message_content = agreement_detail_page.get_text(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'))
        self.assertTrue(message_content == card_number)

    @staticmethod
    def setUp_test_me_zhangshuli_175():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_175(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/id_iv_avatar'))
        self.assertTrue(agreement_detail_page.page_should_contain_text("绑定新的银行卡"))
        agreement_detail_page.click_text_or_description("绑定新的银行卡")

        time.sleep(5)
        card_number = "6214 1803 0000 1315 198"
        agreement_detail_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addbankcard_cardnoEdit'),
                                         card_number)
        attribute = agreement_detail_page.get_element_attribute(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addkjbankcard_next'), "enabled")
        self.assertTrue(attribute == "true")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ipos_addKjbankcard_return'))
        agreement_detail_page.page_should_contain_text("绑定新的银行卡")

    @staticmethod
    def setUp_test_me_zhangshuli_283():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_283(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        time.sleep(2)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_action_bar_help'))

        elements = agreement_detail_page.get_elements(
            (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_list_item_name'))
        for e in elements:
            if e.text == "帮助中心":
                e.click()
        actionbar_title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(actionbar_title == "帮助中心")
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_actionbar_left_back'))
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'))
        time.sleep(3)
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_me_zhangshuli_284():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_284(self):
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        time.sleep(2)
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_action_bar_help'))
        # 断开网络
        agreement_detail_page.set_network_status(0)
        elements = agreement_detail_page.get_elements(
            (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_list_item_name'))
        for e in elements:
            if e.text == "帮助中心":
                e.click()
        actionbar_title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(actionbar_title == "帮助中心")
        time.sleep(3)
        exist = agreement_detail_page.is_text_present("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_actionbar_left_back'))
        time.sleep(1)

    def tearDown_test_me_zhangshuli_284(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_285():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_285(self):
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        time.sleep(2)
        agreement_detail_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_action_bar_help'))

        elements = agreement_detail_page.get_elements(
            (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_list_item_name'))
        for e in elements:
            if e.text == "帮助中心":
                e.click()
        actionbar_title = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(actionbar_title == "帮助中心")
        time.sleep(3)
        # 断开网络
        agreement_detail_page.set_network_status(0)
        agreement_detail_page.click_text_or_description("1、什么是实名认证？")
        exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
        self.assertTrue(exist)


    def tearDown_test_me_zhangshuli_285(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_290():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_290(self):
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        # 断开网络
        agreement_detail_page.set_network_status(0)
        elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        for e in elements:
            if e.text == "活动中心":
                e.click()
                exist = agreement_detail_page.is_toast_exist("当前网络不可用，请检查网络设置")
                self.assertTrue(exist)
                break
            else:
                continue
        # 返回
        me.click_element(["id", 'com.chinasofti.rcs:id/iv_actionbar_left_back'], 15)
        time.sleep(1)
        self.assertTrue(agreement_detail_page.page_should_contain_text("和包支付"))

    def tearDown_test_me_zhangshuli_290(self):
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.set_network_status(6)

    @staticmethod
    def setUp_test_me_zhangshuli_291():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_291(self):
        """和包支付--银行卡页面填写0-14位银行卡号"""
        # 打开‘我’页面
        me = MePage()
        me.click_element((MobileBy.ID, "com.chinasofti.rcs:id/redpager"))
        agreement_detail_page = AgreementDetailPage()
        agreement_detail_page.is_current_activity_match_this_page()
        time.sleep(3)
        elements = agreement_detail_page.get_elements((MobileBy.CLASS_NAME, 'android.widget.TextView'))
        for e in elements:
            if e.text == "和包支付":
                e.click()
        text = agreement_detail_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/tv_actionbar_title'))
        self.assertTrue(text == "和包支付")

