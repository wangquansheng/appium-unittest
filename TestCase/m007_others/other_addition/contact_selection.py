import random
import string
import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.team import *
from preconditions.BasePreconditions import LoginPreconditions
from preconditions.BasePreconditions import WorkbenchPreconditions

TEAM_NAME = "测试团体2"
TEAM_ADMIN = "admin"
TEAM_EMAIL = "18792938179@139.com"
USER_NAME = "测试人员1"
USER_NUMBER = "13800138000"


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def team_add_contact(group_name, user_name):
        """给指定团队添加指定用户"""
        mess = MessagePage()
        mess.click_contacts()
        mess.click_all_team()
        time.sleep(3)
        teamlist = EnterPriseHomeListPage()
        if not teamlist.click_the_group(group_name):
            return False
        team = EnterPrisePage()
        time.sleep(3)
        if team.search_user_is_exsit(user_name):
            team.click_back_button()
            teamlist.click_back_button()
            return True
        team.click_more()
        team.click_group_mgmt()
        time.sleep(10)
        teamh5 = AddTeamContacrH5Page()
        teamh5.click_add_contacter()
        time.sleep(5)
        teamh5.click_add_contact_by_phone()
        contact_selector = SelectContactsPage()
        contact_selector.search(user_name)
        contact_selector.select_one_group_by_name2(user_name)
        contact_selector.click_sure_bottom()
        time.sleep(2)
        teamh5.click_back_button()
        time.sleep(3)
        teamh5.click_back_button()
        time.sleep(2)
        team.click_back_button()
        time.sleep(2)
        teamlist.click_back_button()
        return True

    @staticmethod
    def create_new_team(team_name, real_name):
        """创建团队"""
        # 查看团队是否存在,若存在直接返回message界面
        mess = MessagePage()
        mess.click_contacts()
        mess.click_all_team()
        time.sleep(3)
        teamlist = EnterPriseHomeListPage()
        if teamlist.search_group_is_exsit(team_name):
            teamlist.click_back_button()
            mess.click_tag_messages()
            return True
        # 创建团队
        teamlist.click_back_button()
        mess.click_create_team()
        time.sleep(3)
        team = CreateTeamPage()
        team.input_team_name(team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name(real_name)
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.wait_for_setting_workbench_page_load()
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 进入工作台并进入消息界面
        team.click_enter_workbench()
        time.sleep(5)
        mess.click_tag_messages()

    @staticmethod
    def get_current_number():
        """获取当前和飞信号"""
        # 进入我界面获取和飞信号
        mess = MessagePage()
        mess.click_me()
        number = mess.get_number()
        mess.click_tag_messages()
        print(number)
        return number


class MsgContactsSelect(TestCase):
    """单聊-联系人选择器-新建消息"""

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0002():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0002(self):
        """新建消息—输入姓名/号码搜索"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 点击搜索框
        select_contacts = SelectContactsPage()
        select_contacts.click_search_contact()
        self.assertTrue(select_contacts.confrim_is_keyboard_shown())
        # 姓名搜索
        select_contacts.input_search_keyword(USER_NAME)
        self.assertTrue(select_contacts.search_team_contact_message_is_exsit(USER_NAME))
        self.assertTrue(select_contacts.search_contact_is_exsit())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0003():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0003(self):
        """新建消息—输入姓名/号码搜索—查看搜索结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 点击搜索框
        select_contacts = SelectContactsPage()
        select_contacts.click_search_contact()
        self.assertTrue(select_contacts.confrim_is_keyboard_shown())
        # 姓名或手机号码搜索，当本地有搜索结果时
        select_contacts.search(USER_NAME)
        time.sleep(3)
        self.assertTrue(select_contacts.search_team_contact_message_is_exsit(USER_NAME))
        self.assertTrue(select_contacts.search_contact_is_exsit())
        self.assertTrue(select_contacts.phone_contact_is_exsit())
        # 姓名或手机号码搜索，当本地无搜索结果时
        select_contacts.search("测试23456789")
        time.sleep(3)
        self.assertTrue(select_contacts.search_contact_is_exsit())
        self.assertFalse(select_contacts.phone_contact_is_exsit())
        # 搜索关键字与我的电脑有关时
        select_contacts.search("我的电脑")
        time.sleep(3)
        self.assertTrue(select_contacts.search_contact_is_exsit())
        self.assertTrue(select_contacts.function_is_exsit())
        # 当无手机联系人且为手机号时，查看搜索结果展示
        select_contacts.search("18300001000")
        time.sleep(3)
        self.assertTrue(select_contacts.search_contact_is_exsit())
        self.assertTrue(select_contacts.net_search_is_exsit())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0004():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits("测试A_0004", "22222222222")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0004(self):
        """新建消息—输入姓名/号码搜索—查看本地搜索结果的展示"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 点击搜索框，查看键盘是否显示
        select_contacts = SelectContactsPage()
        select_contacts.click_search_contact()
        self.assertTrue(select_contacts.confrim_is_keyboard_shown())
        # 姓名或手机号码搜索
        select_contacts.search("测试A_0004")
        time.sleep(3)
        self.assertTrue(select_contacts.search_team_contact_message_is_exsit("测试A_0004"))
        self.assertTrue(select_contacts.search_contact_is_exsit())
        self.assertTrue(select_contacts.phone_contact_is_exsit())
        # 点击手机联系人
        select_contacts.click_search_the_contact("测试A_0004")
        time.sleep(5)
        # 查看是否进入单聊界面
        chat = SingleChatPage()
        self.assertTrue(chat.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0005():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, USER_NAME)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0005(self):
        """新建消息—搜索-搜索团队联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 点击搜索框，查看键盘是否显示
        select_contacts = SelectContactsPage()
        select_contacts.click_search_contact()
        self.assertTrue(select_contacts.confrim_is_keyboard_shown())
        # 姓名或手机号码搜索
        select_contacts.search(USER_NAME)
        time.sleep(3)
        self.assertTrue(select_contacts.search_team_contact_message_is_exsit(USER_NAME))
        # 点击搜索团队联系人
        select_contacts.click_search_team_contact_message(USER_NAME)
        time.sleep(3)
        self.assertTrue(select_contacts.team_contact_is_exsit())
        # 点击任意联系人
        select_contacts.click_search_the_contact_in_team()
        time.sleep(3)
        chat = SingleChatPage()
        self.assertTrue(chat.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0011():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0011(self):
        """新建消息—选择手机联系人"""
        # 获取当前和飞信号
        current_number = Preconditions.get_current_number()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 搜索本机号码
        select_contacts = SelectContactsPage()
        select_contacts.search(current_number)
        time.sleep(3)
        select_contacts.click_the_first_search_the_contact()
        chat = SingleChatPage()
        # 查看是否进入单聊界面
        self.assertFalse(chat.is_on_this_page())
        # 点击新增联系人
        select_contacts.search(USER_NAME)
        time.sleep(3)
        select_contacts.click_search_the_contact(USER_NAME)
        time.sleep(3)
        # 查看是否进入单聊界面
        self.assertTrue(chat.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0295():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0295(self):
        """查看页面标签是否为选择联系人,搜索框中是否为：搜索或输入手机号"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 查看页面标签是否为选择联系人
        self.assertTrue(prise_contact.confirm_text_in_select_contacts())
        # 判断搜索框中是否为：搜索或输入手机号
        self.assertTrue(prise_contact.confirm_text_in_select_box())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0296():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0296(self):
        """在顶部向右滑动，查看小键盘是否收起"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 在顶部向右滑动，查看小键盘是否收起
        prise_contact.swipe_up_on_the_keyboard()
        self.assertFalse(prise_contact.confrim_is_keyboard_shown())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0297():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0297(self):
        """键入内容查看是否存在一键消除X键"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 判断是否存在一键消除X键
        self.assertFalse(prise_contact.is_element_present())
        # 键入内容查看是否存在一键消除X键
        prise_contact.input_search_contact_message("183")
        self.assertTrue(prise_contact.is_element_present())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0298():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, USER_NAME)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0298(self):
        """点击搜索框查看是否调起小键盘,键入内容查看搜索结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 键入内容查看搜索结果
        prise_contact.input_search_contact_message(USER_NAME)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0299():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0299(self):
        """键入内容查看未搜索到结果时是否提示无搜索结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown)
        # 键入内容查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("88888888888")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0300():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0300(self):
        """键入183内容查看搜索到结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入183内容查看搜索到结果
        prise_contact.input_search_contact_message("138")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0310():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0310(self):
        """键入一个字母查看搜索到结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入一个字母查看搜索到结果
        str = "".join(random.sample(string.ascii_letters, 1))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0311():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, USER_NAME)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0311(self):
        """键入一个团队联系人的名称拼音查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入一个团队联系人的名称拼音查看搜索到结果
        str = "ceshirenyuan"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0312():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, USER_NAME)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0312(self):
        """键入一个团队联系人的名称的汉字查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入一个团队联系人的名称的汉字查看搜索到结果
        str = "测"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0313():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits(USER_NAME, USER_NUMBER)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, USER_NAME)
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0313(self):
        """键入一个团队联系人号码的前三位查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入一个团队联系人号码的前三位查看搜索到结果
        str = "138"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0314():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员2', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员2")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0314(self):
        """输入号码规则的11位数字——搜索"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入一个团队联系人号码规则的11位数字——查看搜索到结果
        str = "15875537272"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0315():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0315(self):
        """键入内容查看未搜索到结果时是否提示无搜索结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入内容查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("135331108701")
        time.sleep(2)
        self.assertTrue(prise_contact.no_result_is_element_present())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0316():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0316(self):
        """键入9查看未搜索到结果时是否提示无搜索结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入9查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("9")
        time.sleep(2)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0317():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0317(self):
        """键入1查看未搜索到结果时是否提示无搜索结果"""
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入1查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("1")
        time.sleep(2)
        self.assertTrue(prise_contact.confirm_exist_result())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0318():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员+', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员+")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0318(self):
        """输入特殊字符‘+’，搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入特殊字符‘+’，搜索联系人
        str = "+"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0319():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0319(self):
        """输入特殊字符‘.’，搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入特殊字符‘.’，搜索联系人
        str = "."
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0320():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测123', '11111111111')
        time.sleep(2)
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测123")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0320(self):
        """输入汉字和数字，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入汉字和数字，组合搜索联系人
        str = "测123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0321():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('123@￥%', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "123@￥%")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0321(self):
        """输入数字和特殊字符组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入数字和特殊字符组合，组合搜索联系人
        str = "123@￥%"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0322():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce123', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce123")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0322(self):
        """输入数字和字母组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入数字和字母组合，组合搜索联系人
        str = "ce123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0323():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce试")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0323(self):
        """输入汉字和字母组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入汉字和字母组合，组合搜索联系人
        str = "ce试"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0324():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce@￥#', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce@￥#")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0324(self):
        """输入字母和特殊字符组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入字母和特殊字符组合，组合搜索联系人
        str = "ce@￥#"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0326():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0326(self):
        """查看页面标签是否为选择联系人,搜索框中是否为：搜索或输入手机号"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 查看页面标签是否为选择联系人
        self.assertTrue(prise_contact.confirm_text_in_select_contacts())
        # 判断搜索框中是否为：搜索或输入手机号
        self.assertTrue(prise_contact.confirm_text_in_select_box())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0327():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0327(self):
        """点击搜索框查看是否调起小键盘"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 在顶部向右滑动，查看小键盘是否收起
        prise_contact.swipe_right_on_the_keyboard()
        self.assertFalse(prise_contact.confrim_is_keyboard_shown())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0328():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0328(self):
        """团队搜索框测试"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 判断是否存在一键消除X键
        self.assertFalse(prise_contact.is_element_present())
        # 键入内容查看是否存在一键消除X键
        prise_contact.input_search_contact_message("138")
        self.assertTrue(prise_contact.is_element_present())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0329():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试A_0329', '13888888888')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试A_0329")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0329(self):
        """输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 输入框输入姓名或者号码进行搜索（如：13888888888），查看搜索结果展示
        str = "13888888888"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0330():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0330(self):
        """键入内容查看未搜索到结果时是否提示无搜索结果"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入内容查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("111111111111")
        time.sleep(2)
        self.assertTrue(prise_contact.no_result_is_element_present())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0331():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0331(self):
        """键入138内容查看搜索到结果"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入138内容查看搜索到结果
        prise_contact.input_search_contact_message("138")
        time.sleep(2)
        prise_contact.scroll_to_bottom_on_times()
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0332():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0332(self):
        """搜索框输入一个大写/小写字母进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入一个大写/小写字母进行搜索
        str = ''.join(random.sample(string.ascii_letters, 1))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0333():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('我是测试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "我是测试")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0333(self):
        """搜索框输入联系人的姓名拼音进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入联系人的姓名拼音进行搜索
        str = "woshiceshi"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0334():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('我是测试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "我是测试")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0334(self):
        """搜索框输入汉字进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入汉字进行搜索
        str = "我"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0335():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试A_0335', '11111111135')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "我是测试")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0335(self):
        """搜索框输入“135”进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入“135”进行搜索
        str = "135"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0336():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员2', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员2")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0336(self):
        """搜索框输入“13533110870”进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入“15875537272”进行搜索
        str = "15875537272"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0337():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0337(self):
        """键入内容查看未搜索到结果时是否提示无搜索结果"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入内容查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("135331108701")
        time.sleep(2)
        self.assertTrue(prise_contact.no_result_is_element_present())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0338():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0338(self):
        """键入9查看未搜索到结果时是否提示无搜索结果"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入9查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("9")
        time.sleep(2)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0339():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0339(self):
        """键入1查看未搜索到结果时是否提示无搜索结果"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入1查看未搜索到结果时是否提示无搜索结果
        prise_contact.input_search_contact_message("1")
        time.sleep(2)
        self.assertTrue(prise_contact.confirm_exist_result())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0340():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员+', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员+")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0340(self):
        """搜索框输入特殊字符‘+’进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入特殊字符‘+’进行搜索
        str = "+"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0341():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0341(self):
        """搜索框输入特殊字符‘.’进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入特殊字符‘.’进行搜索
        str = "."
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0342():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测123', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测123")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0342(self):
        """搜索框输入汉字和数字（如测123）进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入汉字和数字（如测123）进行搜索
        str = "测123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0343():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('123@￥%', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "123@￥%")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0343(self):
        """搜索框输入数字和特殊字符组合（如123@￥%）进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入数字和特殊字符组合（如123@￥%）进行搜索
        str = "123@￥%"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0344():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce123', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce123")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0344(self):
        """搜索框输入数字和字母组合（如ce123）进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入数字和字母组合（如ce123）进行搜索
        str = "ce123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0345():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce试")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0345(self):
        """搜索框输入汉字和字母组合（如ce试）进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入汉字和字母组合（如ce试）进行搜索
        str = "ce试"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0346():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce@￥#', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce@￥#")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0346(self):
        """搜索框输入字母和特殊字符组合（如ce@￥#）进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入汉字和字母组合（如ce试）进行搜索
        str = "ce@￥#"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0348():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce试")
        contactspage.open_message_page()
        """给我的电脑发送一条随机消息，并转发该条消息"""
        mess = MessagePage()
        mess.click_search()
        mess.input_search_message_631("我的电脑")
        time.sleep(3)
        mess.click_search_my_computer()
        chatwindow = ChatWindowPage()
        message = ''.join(random.sample(string.ascii_letters, 20))
        chatwindow.input_message_text(message)
        chatwindow.click_send_button()
        chatwindow.is_exist_message(message)
        chatwindow.long_press_message(message)
        chatwindow.click_transpond()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0348(self):
        """搜索框输入ce试进行搜索"""
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 关闭网络
        prise_contact.set_network_status(0)
        # 搜索框输入汉字和字母组合（如ce试）进行搜索
        str = "ce试"
        prise_contact.input_search_contact_message(str)
        # 查看是否出现“网络连接异常”提示
        self.assertEquals(prise_contact.is_toast_exist("网络连接异常"), True)

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0348():
        try:
            prise_contact = SelectHeContactsPage()
            prise_contact.set_network_status(6)
        except:
            prise_contact = SelectHeContactsPage()
            prise_contact.set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0637():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0637(self):
        """查看页面标签是否为选择联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 查看页面标签是否为选择联系人
        self.assertTrue(prise_contact.confirm_text_in_select_contacts())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0638():
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0638(self):
        """判断搜索框中是否为：搜索或输入手机号"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 判断搜索框中是否为：搜索或输入手机号
        self.assertTrue(prise_contact.confirm_text_in_select_box())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0639():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0639(self):
        """点击搜索框查看是否调起小键盘"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 点击搜索框查看是否调起小键盘
        prise_contact.click_input_box()
        self.assertTrue(prise_contact.confrim_is_keyboard_shown())
        # 在顶部向右滑动，查看小键盘是否收起
        prise_contact.swipe_right_on_the_keyboard()
        self.assertFalse(prise_contact.confrim_is_keyboard_shown())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0640():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0640(self):
        """不键入内容查看是否存在一键消除X键"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 判断是否存在一键消除X键
        self.assertFalse(prise_contact.is_element_present())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0641():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0641(self):
        """键入内容查看是否存在一键消除X键"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入内容查看是否存在一键消除X键
        prise_contact.input_search_contact_message("138")
        self.assertTrue(prise_contact.is_element_present())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0642():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员2', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员2")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0642(self):
        """搜索框输入联系人进行搜索"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 搜索框输入联系人进行搜索
        str = "测试人员2"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0643():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0643(self):
        """点击+号——》点击发起群聊"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入138内容查看搜索到结果
        prise_contact.input_search_contact_message("138")
        time.sleep(2)
        prise_contact.scroll_to_bottom_on_times()
        self.assertTrue(prise_contact.is_element_present())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0649():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0649(self):
        """键入随机的一个小写字母，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机的一个小写字母，查看搜索到结果
        str = "".join(random.sample(string.ascii_lowercase, 1))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0651():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0651(self):
        """键入随机的两个小写字母组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机的两个小写字母组合，查看搜索到结果
        str = "".join(random.sample(string.ascii_lowercase, 2))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0653():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0653(self):
        """键入联系人中不存在的名字的拼音，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入联系人中不存在的名字的拼音，查看搜索到结果
        prise_contact.input_search_contact_message("ceshilianxirenshiwo")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0655():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0655(self):
        """键入联系人名称中不存在的汉字，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入联系人名称中不存在的汉字，查看搜索到结果
        prise_contact.input_search_contact_message("嚄")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0657():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0657(self):
        """键入随机的三个数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机的三个数字组合，查看搜索到结果
        str = "".join(random.sample(string.digits, 3))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0659():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0659(self):
        """键入随机的6个数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机的6个数字组合，查看搜索到结果
        str = "".join(random.sample(string.digits, 6))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0661():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0661(self):
        """键入以32开头随机的11个数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入以32开头随机的11个数字组合，查看搜索到结果
        str = "32"+"".join(random.sample(string.digits, 9))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0662():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0662(self):
        """键入以32开头随机的10个数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入以32开头随机的10个数字组合，查看搜索到结果
        str = "32" + "".join(random.sample(string.digits, 8))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0663():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0663(self):
        """键入随机的12个数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机的12个数字组合，查看搜索到结果
        str = "".join(random.sample(string.digits+string.digits, 12))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0664():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试0664', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试0664")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0664(self):
        """键入数字6，存在搜索结果时，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入数字6，查看搜索到结果
        prise_contact.input_search_contact_message("6")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0665():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0665(self):
        """键入数字1组合，不存在搜索结果时，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入数字1组合，不存在搜索结果时，查看搜索到结果
        prise_contact.input_search_contact_message("1")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0666():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测试人员+', '15875537272')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测试人员+")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0666(self):
        """输入特殊字符‘+’，搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入特殊字符‘+’，搜索联系人
        str = "+"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0667():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0667(self):
        """键入"+"，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入"+"，查看搜索到结果
        prise_contact.input_search_contact_message("+")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0668():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('.测试', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, ".测试")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0668(self):
        """输入特殊字符‘.’，搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入特殊字符‘.’，搜索联系人
        str = "."
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0669():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0669(self):
        """键入"."，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入"."，查看搜索到结果
        prise_contact.input_search_contact_message(".")
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0671():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0671(self):
        """键入汉字和数字组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入汉字和数字组合，查看搜索到结果
        str = "嚄"+"".join(random.sample(string.digits, 1))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0673():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0673(self):
        """键入随机数字和标点符合组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入随机数字和标点符合组合，查看搜索到结果
        str = "".join(random.sample(string.digits, 1)) + "".join(random.sample(string.punctuation, 1))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0674():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce123', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce123")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0674(self):
        """输入数字和字母组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入数字和字母组合，组合搜索联系人
        str = "ce123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0675():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0675(self):
        """键入数字和标点符合组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入数字和标点符合组合，查看搜索到结果
        str = "".join(random.sample(string.ascii_letters + string.digits, 4))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0676():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('测123', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "测123")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0676(self):
        """输入汉字和字母组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入汉字和字母组合，组合搜索联系人
        str = "测123"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0677():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0677(self):
        """键入汉字和字母符合组合，不存在搜索结果，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入汉字和字母符合组合，不存在搜索结果，查看搜索到结果
        str = "嚄" + "".join(random.sample(string.ascii_letters, 2))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0678():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('ce@￥#', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "ce@￥#")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0678(self):
        """输入字母和特殊字符组合，组合搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入字母和特殊字符组合，组合搜索联系人
        str = "ce@￥#"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0679():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0679(self):
        """键入三位字母和两位标点符合随机组合，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入三位字母和两位标点符合随机组合，查看搜索到结果
        str = "".join(random.sample(string.ascii_letters, 3)) + "".join(random.sample(string.punctuation, 2))
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0680():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('666666', '11111111111')
        contactspage.open_message_page()
        """预制一个团队"""
        Preconditions.create_new_team(TEAM_NAME, TEAM_ADMIN)
        """在团队中添加一个联系人"""
        Preconditions.team_add_contact(TEAM_NAME, "666666")
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0680(self):
        """输入短号666666，搜索联系人"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 输入短号666666，搜索联系人
        str = "666666"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0681():
        """连接手机"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0681(self):
        """键入短号777777，查看搜索到结果"""
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_group_chat()
        # 选择团队联系人
        select_contacts = SelectContactsPage()
        select_contacts.click_group_contact()
        # 查看是否进入企业通讯录列表页面
        prise_contact = SelectHeContactsPage()
        prise_contact.wait_for_page_load()
        # 键入短号777777，查看搜索到结果
        str = "777777"
        prise_contact.input_search_contact_message(str)
        time.sleep(5)
        if prise_contact.confirm_exist_result() == 0:
            # 若不存在搜索结果，则判断是否存在无搜索结果标签
            self.assertTrue(prise_contact.no_result_is_element_present())
        else:
            # 若存在搜索结果，则确认是否存在"团队联系人标签"
            self.assertTrue(prise_contact.is_seach_exist_contacts())
            # 若存在搜索结果则判断搜索到的联系人标签大于0
            self.assertTrue(prise_contact.confirm_exist_result() > 0)
