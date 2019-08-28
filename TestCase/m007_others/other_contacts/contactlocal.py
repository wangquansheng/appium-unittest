import random
import time
import unittest
import preconditions
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages.components import ChatNoticeDialog, SearchBar, ContactsSelector
from pages import *
from pages.contacts.EditContactPage import EditContactPage
from pages.message.Send_CardName import Send_CardNamePage

class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_contacts_chenjixiang_0083():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0083(self):
        """联系-选择一个联系人"""
        contacts = ContactsPage()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0083_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
            cdp.wait_for_page_load()
            cdp.click_back_icon()
            contacts = ContactsPage()
            time.sleep(1)
        else:
            name = names[0]
        contacts.is_exist_contracts_list()
        contacts.select_contacts_by_name(name)
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        self.assertTrue(cdp.is_on_this_page())


    @staticmethod
    def setUp_test_contacts_chenjixiang_0130():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0130(self):
        """联系-创建一个联系人-编辑-让姓名为空"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.click_input_number()
        self.assertTrue(ccp.is_toast_exist("姓名不能为空，请输入"))
        ccp.assert_save_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0137():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0137(self):
        """联系-创建一个联系人-编辑-让手机为空"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.input_name("test")
        time.sleep(1)
        ccp.click_input_number()
        time.sleep(1)
        ccp.click_input_name()
        self.assertTrue(ccp.is_toast_exist("手机号码不能为空，请输入"))
        ccp.assert_save_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0138():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0138(self):
        """联系-创建一个联系人-编辑-让手机位数小于3"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        ccp.click_input_name()
        ccp.input_name("test")
        time.sleep(1)
        ccp.click_input_number()
        ccp.input_number("13")
        time.sleep(1)
        ccp.click_input_name()
        self.assertTrue(ccp.is_toast_exist("号码输入有误，请重新输入"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0140():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0140(self):
        """联系-创建一个联系人-编辑-让手机位数为3"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0138_" + str(random.randint(100, 999))
        ccp.click_input_name()
        ccp.input_name(name)
        time.sleep(1)
        ccp.click_input_number()
        ccp.input_number("138")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0147():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0147(self):
        """联系-创建一个联系人-编辑-公司输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0147_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_company("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0154():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0154(self):
        """联系-创建一个联系人-编辑-职位输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0154_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_position("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0161():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0161(self):
        """联系-创建一个联系人-编辑-邮箱输入1个字符"""
        contacts = ContactsPage()
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0161_" + str(random.randint(100, 999))
        ccp.input_name(name)
        number = "147752" + str(time.time())[-5:]
        ccp.input_number(number)
        ccp.hide_keyboard_if_display()
        ccp.input_email_address("a")
        ccp.save_contact()
        self.assertTrue(ccp.is_toast_exist("创建成功"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0194():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0194_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0194(self):
        """联系-选择一个联系人-编辑-让姓名为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_name("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_number()
        self.assertTrue(ecp.is_toast_exist('姓名不能为空，请输入'))
        ecp.assert_ensure_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0201():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0201_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0201(self):
        """联系-选择一个联系人-编辑-让手机号为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.click_input_number()
        ecp.input_number("")
        ecp.click_input_name()
        self.assertTrue(ecp.is_toast_exist('电话不能为空，请输入'))
        ecp.assert_ensure_button_should_not_be_clickable()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0209():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0209_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0209(self):
        """联系-选择一个联系人-编辑-让公司名为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_company("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0214():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0214_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0214(self):
        """联系-选择一个联系人-编辑-让公司名特殊字符，字母加数字组合"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        name = "Ⅰcom" + str(random.randint(100, 999))
        ecp.input_company(name)
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0216():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0216_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0216(self):
        """联系-选择一个联系人-编辑-让职位为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_position("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0223():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0223_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0223(self):
        """联系-选择一个联系人-编辑-让邮箱为空"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.input_email_address("")
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0228():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0228_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0228(self):
        """联系-选择一个联系人-编辑-让邮箱名为特殊字符，字母加数字组合"""
        cdp = ContactDetailsPage()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        name = "Ⅰtest" + str(random.randint(100, 999)) + "@Ⅱ" + str(random.randint(100, 999)) + ".com"
        ecp.input_company(name)
        ecp.hide_keyboard_if_display()
        ecp.click_input_name()
        ecp.assert_ensure_button_should_be_clickable()
        ecp.click_ensure()
        ecp.click_allow_button()
        cdp.wait_for_page_load()
        self.assertTrue(ecp.is_toast_exist('保存成功'))
        self.assertTrue(cdp.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0230():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0230(self):
        """联系-选择一个联系人-编辑-删除联系人"""
        contacts = ContactsPage()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0230_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            name = names[0]
            contacts.select_people_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        ecp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        ecp.click_delete_contact()
        ecp.click_sure_delete()
        ecp.click_allow_button()
        contacts = ContactsPage()
        time.sleep(2)
        names = contacts.get_all_contacts_name()
        self.assertTrue(name not in names)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0237():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0237_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0237(self):
        """联系-选择一个联系人-分享名片"""
        cdp = ContactDetailsPage()
        cdp.click_share_business_card()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        self.assertTrue(scp.is_element_present_by_locator("搜索或输入手机号"))
        self.assertTrue(scp.is_element_present_by_locator("选择一个群"))
        self.assertTrue(scp.is_element_present_by_locator("选择团队联系人"))
        self.assertTrue(scp.is_element_present_by_locator("选择手机联系人"))
        self.assertTrue(scp.is_element_present_by_locator("最近聊天"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0246():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0246(self):
        """联系-选择一个联系人-点击聊天"""
        single_chat_page = SingleChatPage()
        single_chat_page.wait_for_page_load()
        self.assertTrue(single_chat_page.is_on_this_page)

    @staticmethod
    def setUp_test_contacts_chenjixiang_0247():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0247_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0247(self):
        """联系-选择一个联系人-点击电话"""
        cdp = ContactDetailsPage()
        cdp.click_call_icon()
        cdp.click_allow_button()
        time.sleep(3)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0248():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0248_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0248(self):
        """联系-选择一个联系人-点击语音"""
        cdp = ContactDetailsPage()
        cdp.click_voice_call_icon()
        cdp.click_continue_call()
        time.sleep(1)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0250():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0250_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0250(self):
        """联系-选择一个联系人-点击视频电话"""
        cdp = ContactDetailsPage()
        cdp.click_video_call_icon()
        cdp.click_continue_call()
        time.sleep(1)
        self.assertTrue(current_mobile().is_phone_in_calling_state)
        current_mobile().hang_up_the_call()

    @staticmethod
    def setUp_test_contacts_chenjixiang_0259():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0259_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0259(self):
        """联系-选择一个联系人判断是否存在新增桌面快捷方式"""
        cdp = ContactDetailsPage()
        self.assertTrue(cdp.page_contain_shortcut())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0262():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0262_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0262(self):
        """联系-选择联系人-添加桌面快捷方式"""
        cdp = ContactDetailsPage()
        cdp.click_shortcut()
        cdp.click_i_know_and_no_remind()
        cdp.click_allow_button()
        cdp.click_shortcut()
        self.assertTrue(cdp.page_not_contain_i_know())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0291():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(4)
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        cdp = ContactDetailsPage()
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0291_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
        else:
            contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0291(self):
        """联系-选择没有号码的联系人-判断是否存在添加桌面快捷方式"""
        cdp = ContactDetailsPage()
        cdp.click_shortcut()
        cdp.click_i_know_and_no_remind()
        cdp.click_allow_button()
        cdp.click_shortcut()
        self.assertTrue(cdp.is_toast_exist('已添加'))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0352():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0352(self):
        """联系-选择一个联系人-编辑-判断条件"""
        contacts = ContactsPage()
        cdp = ContactDetailsPage()
        # 创建联系人号码部分为+的联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0352_" + str(random.randint(100, 999))
        tail = str(time.time())[-5:]
        number = "++++++" + tail
        ccp.create_contact(name, number)
        ccp.click_allow_button()
        cdp.wait_for_page_load()
        cdp.click_back()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.select_contacts_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        self.assertTrue(ecp.check_element_word("输入号码", "+" + tail))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0353():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0353(self):
        """联系-选择一个联系人-编辑-判断条件"""
        contacts = ContactsPage()
        cdp = ContactDetailsPage()
        # 创建联系人号码全为+的联系人
        contacts.click_add()
        ccp = CreateContactPage()
        ccp.wait_for_page_load()
        name = "atest_0353_" + str(random.randint(100, 999))
        number = "+++++++++++"
        ccp.create_contact(name, number)
        cdp.wait_for_page_load()
        cdp.click_back()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.select_contacts_by_name(name)
        cdp.wait_for_page_load()
        cdp.click_edit_contact()
        ecp = EditContactPage()
        ecp.wait_for_page_load()
        ecp.hide_keyboard_if_display()
        self.assertTrue(ecp.check_element_word("输入号码", "+"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0433():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        # 不存在联系则创建联系人
        if not names:
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0433_" + str(random.randint(100, 999))
            number = "147752" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back()
            contacts = ContactsPage()
            contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0433(self):
        """联系-标签分组-选择分组-跳转联系人选择器-搜索号码-点击联系人"""
        contacts = ContactsPage()
        names = contacts.get_all_contacts_name()
        self.assertTrue(len(names) > 1)
        contacts.click_label_grouping()
        lgp = LabelGroupingPage()
        lgp.wait_for_page_load()
        # 无分组则创建分组
        group_names = lgp.get_label_grouping_names()
        if len(group_names) == 0:
            group_name = "gtest_0433_" + str(random.randint(100, 999))
            lgp.click_new_create_group()
            time.sleep(1)
            lgp.input_label_grouping_name(group_name)
            lgp.click_sure()
            scp = SelectContactsPage()
            scp.wait_for_page_load()
            scp.click_back()
            lgp = LabelGroupingPage()
            lgp.wait_for_page_load()
            lgp.new_group_click_back()
        else:
            group_name = group_names[0]
        # 点击分组
        lgp.click_label_group(group_name)
        lgdp = LableGroupDetailPage()
        lgdp.wait_for_page_load()
        time.sleep(1)
        lgdp.click_i_know()
        # 点击添加成员
        lgdp.click_add_members()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 全量查询
        scp.click_group_search()
        scp.group_search(names[0])
        if scp.is_keyboard_shown():
            scp.hide_keyboard()
        time.sleep(1)
        # 点击查询结果
        scp.click_search_result_by_name(names[0])
        self.assertTrue(scp.check_if_element_exist("选中联系人头像"))

    @staticmethod
    def setUp_test_contacts_chenjixiang_0733():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0733(self):
        """联系-搜索-查看提示词"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.page_should_not_contain_text("本地通讯录")
        clsp.page_should_not_contain_text("和通讯录")
        self.assertFalse(clsp.is_exist_contacts())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0734():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0734(self):
        """联系-搜索-查看提示词"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.page_should_contain_text("输入关键词快速搜索")

    @staticmethod
    def setUp_test_contacts_chenjixiang_0735():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0735(self):
        """联系-搜索-点击返回"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.wait_for_page_load()
        clsp.click_back()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        self.assertTrue(contacts.is_on_this_page())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0737():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        for i in range(3):
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0737_" + str(random.randint(100, 999))
            number = "147652" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back()
            contacts = ContactsPage()
            contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0737(self):
        """联系-搜索-查看是否有显示更多标识"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.input_search_keyword("atest_0737")
        self.assertFalse(clsp.is_show_more_display())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0738():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        for i in range(4):
            contacts.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            name = "atest_0738_" + str(random.randint(100, 999))
            number = "147652" + str(time.time())[-5:]
            ccp.create_contact(name, number)
            ccp.click_allow_button()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back()
            contacts = ContactsPage()
            contacts.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0738(self):
        """联系-搜索-查看是否有显示更多标识"""
        contacts = ContactsPage()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.input_search_keyword("atest_0738")
        self.assertTrue(clsp.is_show_more_display())

    @staticmethod
    def setUp_test_contacts_chenjixiang_0759():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_all_contacts_name()
        if '本机' in names:
            names.remove('本机')
        # 删除所有联系人
        contacts.swipe_to_top()
        for name in names:
            contacts.select_contacts_by_name(name)
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_edit_contact()
            ecp = EditContactPage()
            ecp.wait_for_page_load()
            ecp.page_up()
            time.sleep(1)
            ecp.click_delete_contact()
            ecp.click_sure_delete()
            ecp.click_allow_button()
            contacts = ContactsPage()
            time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_chenjixiang_0759(self):
        """联系-搜索-点击返回"""
        contacts = ContactsPage()
        contacts.swipe_to_top()
        contacts.click_search_box()
        clsp = ContactListSearchPage()
        clsp.input_search_keyword("123")
        self.assertFalse(clsp.is_exist_contacts())

    @staticmethod
    def setUp_test_contacts_quxinli_0002():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0002(self):
        contacts = ContactsPage()
        createteampage = CreateTeamPage()

        # """1.测试“搜索栏”存在并点击有效，并返回"""
        contacts.click_search_box()
        contacts.click_search_return()

        # """测试“备份提示”是否存在，并返回"""
        contacts.is_exist_backup_tips()
        contacts.is_exist_backup_tips_text()

        # """测试“群聊”存在并点击有效，并返回"""
        contacts.open_group_chat_list()
        contacts.click_return()

        # """测试“标签分组”存在并点击有效，并返回"""
        contacts.click_label_grouping()
        contacts.click_label_grouping_return()

        # """测试“公众号”存在并点击有效，并返回"""
        contacts.click_official_account_icon()
        contacts.click_return()

        # """测试“创建团队”存在并点击有效，并返回"""
        contacts.click_creatteam()
        contacts.click_creatteam_return()

        # """手机联系人标签显示所有手机联系人
        contacts.is_exists_star()

        # """有星标联系人时最上面显示星标联系人
        # 待补充

        # """2.右上角显示新建联系人按钮 +"""
        contacts.click_add()
        contacts.click_add_return()


        # """3.测试“字母导航栏”存在并点击有效，并返回"""
        # contacts.click_element()
        # 待补充

    @staticmethod
    def setUp_test_contacts_quxinli_0003():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0003(self):
        contacts = ContactsPage()
        createteampage = CreateTeamPage()

        # """1.测试“搜索栏”存在并点击有效，并返回"""
        contacts.click_search_box()
        contacts.click_search_return()

        # """测试“备份提示”是否存在，并返回"""
        contacts.is_exist_backup_tips()
        contacts.is_exist_backup_tips_text()

        # """测试“群聊”存在并点击有效，并返回"""
        contacts.open_group_chat_list()
        contacts.click_return()

        # """测试“标签分组”存在并点击有效，并返回"""
        contacts.click_label_grouping()
        contacts.click_label_grouping_return()

        # """测试“公众号”存在并点击有效，并返回"""
        contacts.click_official_account_icon()
        contacts.click_return()

        # """测试“创建团队”存在并点击有效，并返回"""
        contacts.click_creatteam()
        contacts.click_creatteam_return()

        # """手机联系人标签显示所有手机联系人
        contacts.is_exists_star()

        # """有星标联系人时最上面显示星标联系人
        # 待补充

        # """2.右上角显示新建联系人按钮 +"""
        contacts.click_add()
        contacts.click_add_return()


        # """3.测试“字母导航栏”存在并点击有效，并返回"""
        # contacts.click_element()
        # 待补充

    @staticmethod
    def setUp_test_contacts_quxinli_0019():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return
        #待补充 我的团队搜索结果中有已保存到本地的RCS用户

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0019(self):
        contacts = ContactsPage()

        # """1.点击联系tab的搜索框输入关键字"""
        contacts.click_search_box()
        contactlistsearchpage = ContactListSearchPage()
        contactlistsearchpage.click_myteam()
        contactlistsearchpage.input_search_keyword('给个红包1')
        time.sleep(0.5)
        contactlistsearchpage.click_result_icon()
        time.sleep(0.5)
        # """页面跳转到该用户的Profile页，显示用户的详情：姓名、号码、头像，公司"""
        contactdetailspage = ContactDetailsPage()
        contactdetailspage.is_exists_contacts_name()
        contactdetailspage.is_exists_contacts_number()
        contactdetailspage.is_exists_contacts_image()
        contacts.assert_screen_contain_text('测试zrtest')
        # """消息、电话、语音通话、视频通话，飞信电话，分享名片"""
        contactdetailspage.is_exists_message_icon()
        contactdetailspage.is_exists_call_icon()
        contactdetailspage.is_exists_voice_call_icon()
        contactdetailspage.is_exists_video_call_icon()
        contactdetailspage.is_exists_dial_hefeixin_icon()
        contactdetailspage.is_exists_share_card_icon()


        # """点击头像显示大图
        contactdetailspage.click_avatar()
        contactdetailspage.is_exists_big_avatar()
        contactdetailspage.click_big_avatar()
        time.sleep(2)

        # """点击消息按钮进入会话界面
        contactdetailspage.message_btn_is_clickable()

        # """点击电话弹出拨打弹出
        contactdetailspage.call_btn_is_clickable()

        # """点击语音通话弹出语音会话弹窗
        contactdetailspage.voice_btn_is_clickable()

        # """点击视频通话弹窗视频会话弹窗
        contactdetailspage.video_call_btn_is_clickable()

        # """点击和飞信电话直接拨打和飞信电话
        contactdetailspage.hefeixin_call_btn_is_clickable()

        # """3.点击分享名片,掉起分享名片的联系人选择"""
        contactdetailspage.click_share_business_card()
        time.sleep(0.5)
        contactdetailspage.assert_screen_contain_text('选择一个群')
        contactdetailspage.assert_screen_contain_text('选择手机联系人')
        contacts.share_to_contact()

        # """可以成功分享给群、联系人"""
        contacts.select_people_by_name('给个红包2')
        contacts.share_sure()
        time.sleep(0.5)
        contacts.assert_screen_contain_text('已发送')

    @staticmethod
    def setUp_test_contacts_quxinli_0426():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0426(self):
        contacts = ContactsPage()
        contactdetailspage = ContactDetailsPage()
        # """删除联系人"""
        contactdetailspage.delete_contact('2测试团队保存联系人子级')

        # """进入我的团队"""
        contacts.choose_zetest_group()
        contacts.choose_zetest_group_son()
        contactdetailspage.click_selectone3()
        # """保存"""
        contactdetailspage.click_save_contacts_icon()
        contactdetailspage.click_sure_icon()


        # """页面跳转到该用户的Profile页，显示用户的详情：姓名、号码、头像，公司"""
        contactdetailspage = ContactDetailsPage()
        contactdetailspage.is_exists_contacts_name()
        contactdetailspage.is_exists_contacts_number()
        contactdetailspage.is_exists_contacts_image()
        contacts.assert_screen_contain_text('测试zrtest')
        # """消息、电话、语音通话、视频通话，飞信电话，分享名片"""
        contactdetailspage.is_exists_message_icon()
        contactdetailspage.is_exists_call_icon()
        contactdetailspage.is_exists_voice_call_icon()
        contactdetailspage.is_exists_video_call_icon()
        contactdetailspage.is_exists_dial_hefeixin_icon()
        contactdetailspage.is_exists_share_card_icon()


        # """点击头像显示大图
        contactdetailspage.click_avatar()
        contactdetailspage.is_exists_big_avatar()
        contactdetailspage.click_big_avatar()
        time.sleep(2)

        # """点击消息按钮进入会话界面
        contactdetailspage.message_btn_is_clickable()

        # """点击电话弹出拨打弹出
        contactdetailspage.call_btn_is_clickable()

        # """点击语音通话弹出语音会话弹窗
        contactdetailspage.voice_btn_is_clickable()

        # """点击视频通话弹窗视频会话弹窗
        contactdetailspage.video_call_btn_is_clickable()

        # """点击和飞信电话直接拨打和飞信电话
        contactdetailspage.hefeixin_call_btn_is_clickable()

        # """3.点击分享名片,掉起分享名片的联系人选择"""
        contactdetailspage.click_share_business_card()
        time.sleep(0.5)
        contactdetailspage.assert_screen_contain_text('选择一个群')
        contactdetailspage.assert_screen_contain_text('选择手机联系人')
        contacts.share_to_contact()

        # """可以成功分享给群、联系人"""
        contacts.select_people_by_name('给个红包2')
        contacts.share_sure()
        time.sleep(0.5)
        contacts.assert_screen_contain_text('已发送')

    @staticmethod
    def setUp_test_contacts_quxinli_0019():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return
        #待补充 我的团队搜索结果中有已保存到本地的RCS用户

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0019(self):
        contacts = ContactsPage()

        # """1.进入我的团队联系人的Profile页"""
        contacts.choose_zetest_group()

        contactdetailspage = ContactDetailsPage()
        contactdetailspage.click_selectone()

        # """点击消息按钮"""
        contactdetailspage.click_message_icon()
        singlechatpage = SingleChatPage()
        singlechatpage.is_exist_inputtext()

    @staticmethod
    def setUp_test_contacts_quxinli_0426():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # """点击到“联系”页"""
        if mess.is_on_this_page():
            mess.open_contacts_page()
            return

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_contacts_quxinli_0426(self):
        contacts = ContactsPage()
        contactdetailspage = ContactDetailsPage()
        # """删除联系人"""
        contactdetailspage.delete_contact('测试团队保存联系人')

        # """进入我的团队"""
        contacts.choose_zetest_group()
        contactdetailspage.click_selectone2()
        # """保存"""
        contactdetailspage.click_save_contacts_icon()
        contactdetailspage.click_sure_icon()


        # """1.点击星标，提示已成功添加为星标联系人"""
        contactdetailspage.click_star()
        time.sleep(1)
        contactdetailspage.assert_screen_contain_text('已成功添加为星标联系人')


        # """2.点击编辑,进入编辑联系人页面，有值字段自动填充"""
        contactdetailspage.click_edit_contact()
        ecp = EditContactPage()
        ecp.is_exist_name('1测试团队保存联系人')

        # """3.修改姓名及其他字段的值并点击确定,保存成功，手机联系人显示修改后的信息"""
        number = "147752" + str(time.time())[-5:]
        ccp = CreateContactPage()
        ccp.create_contact('1测试团队保存联系人', number)
        contactdetailspage.assert_screen_contain_text('1测试团队保存联系人')
        contactdetailspage.assert_screen_contain_text(number)

        # """4.点击分享名片,掉起分享名片的联系人选择"""
        contactdetailspage.click_share_business_card()
        time.sleep(0.5)
        contactdetailspage.assert_screen_contain_text('选择一个群')
        contactdetailspage.assert_screen_contain_text('选择手机联系人')
        contacts.share_to_contact()

        # """可以成功分享给群、联系人"""
        contacts.select_people_by_name('1测试团队保存联系人')
        contacts.share_sure()
        time.sleep(0.5)
        contacts.assert_screen_contain_text('已发送')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0102():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0102(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        # 4、已获取相机权限
        # Step 创建群聊并进入
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        # Step 等待群聊天页加载
        groupchat.wait_for_page_load()
        # Step 1、点击输入框上方的相机
        groupchat.click_take_picture()
        chat_photo = ChatPhotoPage()
        # Checkpoint 可以正常调起相机操作页
        chat_photo.wait_for_page_load()
        # Step 轻触拍摄按钮
        chat_photo.take_photo()
        # Checkpoint 会拍摄成功一张照片
        # Step 点击右下角的“√”按钮
        chat_photo.send_photo()
        time.sleep(5)
        # Checkpoint 可以发送成功
        groupchat.is_exist_pic_msg()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0103():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0103(self):
        """在群聊会话窗口，点击输入框上方的相机ICON，进入到相机拍摄页"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        # 4、已获取相机权限
        # 创建群聊
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 1、点击输入框上方的相机ICON，调起相机操作页
        groupchat.click_take_picture()
        chat_photo = ChatPhotoPage()
        # Checkpoint 调起相机操作页
        chat_photo.wait_for_page_load()
        # Step 2、长按拍摄按钮3、录制时间超过1秒钟后，松手
        chat_photo.record_video(3000)
        # Step 4、点击右下角的“√”按钮
        chat_photo.send_video()
        time.sleep(5)
        # Checkpoint 3、录制时间超过1秒钟后，松手，会录制成功的视频4、点击右下角的“√”按钮，可以发送成功
        groupchat.is_exist_video_record()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0104():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0104(self):
        """点击输入框上方的名片ICON——进入到联系人选择器页"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        # Step 创建群聊
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 点击输入框上方的名片ICON
        groupchat.click_profile()
        selectcontact = SelectLocalContactsPage()
        # Checkpoint 进入到联系人选择器页面
        selectcontact.wait_for_page_load()
        # Step 任意选中一个联系人的名片，发送出去
        ContactsSelector().click_local_contacts('测试短信1')
        time.sleep(2)
        Send_CardNamePage().click_share_btn()
        # Checkpoint 在会话页面展示正常
        groupchat.page_should_contain_text('测试短信1')
        groupchat.page_should_contain_text('个人名片')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0105():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0105(self):
        """点击输入框上方的GIFICON——展示GIF图片推荐列表"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 点击输入框上方的GIFICON
        groupchat.click_gif()
        chatgif = ChatGIFPage()
        # Checkpoint 展示推荐图
        chatgif.wait_for_page_load()
        # Step 任意点击一个推荐图片，发送
        chatgif.send_gif(1)
        chatgif.close_gif()
        time.sleep(2)
        # Checkpoint 发送成功后的展示会另起一个头像和一个昵称
        groupchat.is_send_gif()
        chatgif.is_gif_head_exist()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0106():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0106(self):
        """点击输入框上方的+号——展示隐藏的：文件、群短信（群主）、位置、红包"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        # 4、本网用户
        mess = MessagePage()
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 点击输入框上方的+号
        groupchat.click_more()
        time.sleep(2)
        # Checkpoint 展示：文件、群短信（群主）、位置、红包ICON
        mess.page_should_contain_text("文件")
        mess.page_should_contain_text("位置")
        mess.page_should_contain_text("红包")
        mess.page_should_contain_text("群短信")


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_xiaoqiu_0109():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0109(self):
        """在群聊会话页，点击输入框——调起小键盘"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊天会话页面
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        # Step 在群聊会话页面
        groupchat.wait_for_page_load()
        # Step 点击输入框
        groupchat.click_input_box()
        time.sleep(1)
        # Checkpoint 默认调起小键盘
        self.assertTrue(current_mobile().is_keyboard_shown())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0111():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0111(self):
        """在群聊设置页面，群成员头像上方文案展示"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊设置页面
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 群聊设置页面
        groupchat.click_setting()
        time.sleep(1)
        # Checkpoint 展示了：群成员+括号+群聊天人数
        groupchat.page_should_contain_text('群成员(1人)')
        # Checkpoint 展示了群聊设置，返回按钮
        groupchat.return_btn_is_exist()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0112():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0112(self):
        """在群聊设置页面，群成员展示"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊设置页面
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 群聊设置页面
        groupchat.click_setting()
        time.sleep(1)
        # Checkpoint 群头像默认展示为：头像+昵称
        GroupChatSetPage().group_avatar_is_exist()
        GroupChatSetPage().group_name_is_exist()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0122():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0122(self):
        """在群聊设置页面中——群成员头像展示"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊设置页面
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 群聊天设置页面
        groupchat.click_setting()
        time.sleep(1)
        # Checkpoint 展示的群成员头像，最少会展示一个头像
        GroupChatSetPage().group_avatar_is_exist()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0123():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0123(self):
        """在群聊设置页面中——群主头像展示"""
        # 1、网络正常
        # 2、已加入普通群
        # 3、在群聊设置页面
        # 4、群主权限
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        # Step 群聊天设置页面
        groupchat.click_setting()
        time.sleep(1)
        # Checkpoint 校验群主头像皇冠
        GroupChatSetPage().group_chairman_tag_is_exist()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0124():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0124(self):
        """普通群——群主——添加一个成员"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个群聊
        # 3、群聊人数为1
        # 4、在群聊设置页面
        # 5、群主权限
        mess = MessagePage()
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        # Step 点击添加成员的“+”号按钮
        GroupChatSetPage().click_add_number()
        # Checkpoint 跳转到联系人选择器页面
        # Step 任意选中一个联系人，点击右上角的确定按钮
        ContactsSelector().select_local_contacts('测试短信1')
        time.sleep(2)
        # Checkpoint 会向邀请人发送一条消息
        mess.page_should_contain_text("你向 测试短信1... 发出群邀请")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0125():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0125(self):
        """普通群——群主——添加2个成员"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个群聊
        # 3、群聊人数为1
        # 4、在群聊设置页面
        # 5、群主权限
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        contactsel = ContactsSelector()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        # Step 点击添加成员的“+”号按钮
        GroupChatSetPage().click_add_number()
        # Step 任意选中2个联系人，点击右上角的确定按钮
        contactsel.click_local_contacts('测试短信1')
        contactsel.click_local_contacts('测试短信2')
        contactsel.click_ok_button()
        time.sleep(2)
        # Checkpoint 会向邀请人发送一条消息
        groupchat.page_should_contain_text('你向 测试短信1,测试短信2... 发出群邀请')


    @staticmethod
    def setUp_test_msg_xiaoqiu_0135():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0135(self):
        """无群成员时——点击移除成员按钮"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、群聊人数为1
        # 4、在群聊设置页面
        # 5、群主权限
        mess = MessagePage()
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        GroupChatSetPage().wait_for_page_load()
        # Step 点击移除群成员按钮
        GroupChatSetPage().click_del_member()
        # Checkpoint 跳转到群成员选择列表页面
        mess.page_should_not_contain_text("删除群成员")


    @staticmethod
    def setUp_test_msg_xiaoqiu_0161():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0161(self):
        """群主——清除旧名片——录入1个字母（不区分大、小写）"""
        # 1、网络正常（4G/WIFI）
        # 2、已创建一个普通群
        # 3、在群聊设置页面
        # 4、群主权限
        mess = MessagePage()
        Preconditions.create_group_if_not_exist('测试群组1', "测试短信1", "测试短信2")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        # Step 群名片编辑页面，清除旧名片后，录入1个字母
        groupset.clear_group_name()
        # Checkpoint 可以正常录入1个字母
        groupset.input_new_group_name("A")
        # Step 录入成功，点击右上角的完成按钮
        groupset.save_group_card_name()
        # Checkpoint 可以完成保存操作
        groupset.wait_for_page_load()
        groupset.check_group_nickname('A')


