import time
import warnings
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, current_driver
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.create_group.CreateGroup import CreateGroupPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import WorkbenchPreconditions, ContactsPage, GroupListPage, GroupChatPage, \
    SelectContactsPage, SelectOneGroupPage, GroupChatSetPage

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

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
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_workbench_page():
        """进入工作台首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()

    @staticmethod
    def enter_create_group_page():
        """进入创建群首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_create_group()
        cgp = CreateGroupPage()
        cgp.wait_for_page_load()

    @staticmethod
    def add_phone_number_to_department(department_name):
        """添加本机号码到指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        time.sleep(3)
        if not osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name("添加子部门")
            time.sleep(2)
            osp.input_sub_department_name(department_name)
            osp.input_sub_department_sort("1")
            osp.click_confirm()
            if osp.is_toast_exist("部门已存在", 2):
                osp.click_back()
            osp.wait_for_page_load()
        osp.click_specify_element_by_name(department_name)
        time.sleep(2)
        osp.click_specify_element_by_name("添加联系人")
        time.sleep(2)
        osp.click_specify_element_by_name("手动输入添加")
        osp.input_contacts_name("admin")
        osp.input_contacts_number(phone_number)
        osp.click_confirm()
        osp.click_close()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def delete_department_by_name(department_name):
        """删除指定部门"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(5)
        if osp.is_exist_specify_element_by_name(department_name):
            osp.click_specify_element_by_name(department_name)
            time.sleep(2)
            osp.click_specify_element_by_name("更多")
            time.sleep(2)
            osp.click_specify_element_by_name("部门设置")
            time.sleep(2)
            osp.click_delete()
            osp.click_sure()
        osp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def add_phone_number_to_he_contacts():
        """添加本机号码到和通讯录"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        time.sleep(3)
        if not osp.is_exist_specify_element_by_name(phone_number):
            osp.click_specify_element_by_name("添加联系人")
            time.sleep(2)
            osp.click_specify_element_by_name("手动输入添加")
            osp.input_contacts_name("admin")
            osp.input_contacts_number(phone_number)
            osp.click_confirm()
            osp.wait_for_page_load()
        osp.click_back()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def get_into_enterprise_group_chat_page():
        """进入企业群聊天会话页面 返回群名"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个企业群
        name = sog.select_one_enterprise_group()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        return name


class EnterpriseLogAllTest(TestCase):
    """工作台->企业通讯录"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 2:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
                Preconditions.create_he_contacts2(contact_names2)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在工作台首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_workbench_page()
            return
        wbp = WorkbenchPage()
        if wbp.is_on_workbench_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_workbench_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'yx')
    def test_CJQ_0001(self):
        """创建群，并发起群聊"""
        # 1.进入创建群首页
        Preconditions.enter_create_group_page()
        cgp = CreateGroupPage()
        # 2.点击马上创建群
        cgp.click_create_group()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 3.添加企业联系人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_contacts_by_name("大佬2")
        # 4.点击确认
        sccp.click_sure_button()
        # 5.输入企业群名
        cgp.input_group_name("企业群创建测试1")
        # 6.点击马上创建群
        cgp.click_create_group()
        time.sleep(1)
        # 7.点击发起群聊
        cgp.click_initiate_group_chat()
        time.sleep(1)
        # 8.判断是否在群聊页面
        gcp = GroupChatPage()
        self.assertEqual(gcp.is_on_this_page(), True)
        time.sleep(1)

    @staticmethod
    def tearDown_test_CJQ_0001():
        """解散企业群"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击“—”移除成员
        for i in range(2):
            gcsp.click_delete_member()
            # 3.选择成员
            time.sleep(1)
            gcsp.click_first_group_member_avatar()
            time.sleep(1)
            # 4.点击确定移除
            gcsp.click_delete_member_sure()
            time.sleep(1)
            gcsp.click_sure()
            time.sleep(1)
        # 5.返回群聊页面
        gcsp.click_back()

    @tags('ALL', 'CMCC', 'workbench', 'yx')
    def test_CJQ_0002(self):
        """发送群消息"""
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 1.进入消息页面，进入指定群名企业群
        wbp.click_message_icon()
        Preconditions.get_into_group_chat_page("测试企业群")
        gcp = GroupChatPage()
        # 2.输入发送信息
        gcp.input_message('大家好，这里是测试消息')
        # 3.点击发送
        gcp.send_message()
        # 4.验证是否发送成功
        gcp.wait_for_msg_send_status_become_to('发送成功', 30)
