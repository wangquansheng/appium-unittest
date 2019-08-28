import unittest

import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import ContactsPage
from pages import GroupListPage
from pages import MessagePage
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.group_messenger.GroupMessenger import GroupMessengerPage
from pages.workbench.group_messenger.HelpCenter import HelpCenterPage
from pages.workbench.group_messenger.MessageGroup import MessageGroupPage
from pages.workbench.group_messenger.NewMessage import NewMessagePage
from pages.workbench.group_messenger.Organization import Organization
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import WorkbenchPreconditions

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
    def enter_message_page():
        """进入到消息列表页面"""
        Preconditions.select_mobile('Android-移动', False)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

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
    def enter_group_messenger_page():
        """进入群发信使首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_group_messenger()
        n = 1
        # 解决工作台不稳定问题
        while not wbp.page_should_contain_text2("新建短信"):
            wbp.click_group_messenger()
            n += 1
            if n > 20:
                break

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


class MassMessengerTest(TestCase):
    """群发信使 模块"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保进入消息列表页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        wp = WorkbenchPage()
        if wp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            wp.open_message_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_message_page()

    def default_tearDown(self):
        pass

    @unittest.skip("不稳定")
    def test_QFXS_0008(self):
        """1、点击用户本人头像"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        #点击群发信使
        wp.click_group_messenger()
        #等待页面加载
        mgp=MessageGroupPage()
        mgp.wait_for_page_load()
        #点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        #点击收件人
        mgp.click_addressee()
        #点击本机号码
        sccp=SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sccp.click_text(phone_number)
        if not sccp.is_toast_exist("该联系人不可选"):
            raise AssertionError("没有toast提示该联系人不可选")
        sccp.click_back()
        time.sleep(2)
        sccp.click_back()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL', 'CMCC', 'workbench')
    def test_QFXS_0010(self):
        """1、搜索不存在的用户名称"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击本机号码
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        import random
        a=str(random.random())
        #搜索框输入不存在用户名
        sccp.input_search_message(a)
        if not sccp.is_toast_exist("无搜索结果"):
            raise AssertionError("没有提示 无搜索结果")
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL', 'CMCC', 'workbench')
    def test_QFXS_0011(self):
        """1、再次点击头像，取消选择人员"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击组织架构，添加联系人
        wp.click_organization()
        org=Organization()
        org.wait_for_page_load()
        if not org.is_exit_element_by_text_swipe("飞信电话"):
            org.click_text("添加联系人")
            time.sleep(2)
            org.click_text("从手机通讯录添加")
            sccp = SelectCompanyContactsPage()
            sccp.wait_for_page_load()
            # 飞信电话 or 和飞信电话
            sccp.click_one_contact("飞信电话")
            sccp.click_sure()
            time.sleep(1)
            org.click_back_by_android()
            time.sleep(2)
            org.wait_for_page_load()
        org.click_back()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击指定联系人
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_one_contact("飞信电话")
        time.sleep(3)
        sccp.click_text("飞信电话")
        if sccp.is_left_head_exit():
            raise AssertionError("搜索栏左侧被取消人员人名和头像没有被移除")
        #返回
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()

    @tags('ALL', 'CMCC', 'workbench')
    def test_QFXS_0013(self):
        """1、点击“+”，添加接收人
            2、添加人数小于当前企业剩余条数"""
        mess = MessagePage()
        mess.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 点击群发信使
        wp.click_group_messenger()
        # 等待页面加载
        mgp = MessageGroupPage()
        mgp.wait_for_page_load()
        # 点击新建短信
        mgp.click_build_message()
        mgp.wait_for_edit_message_page_load()
        # 点击收件人
        mgp.click_addressee()
        # 点击指定联系人
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        sccp.click_one_contact("飞信电话")
        if not sccp.is_left_head_exit():
            raise AssertionError("找不到搜索栏左侧被点击人员人名和头像")
        #返回
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        mgp.wait_for_edit_message_page_load()
        mgp.click_close()


class MassMessengerAllTest(TestCase):
    """工作台->群发信使"""

    @classmethod
    def setUpClass(cls):
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

        # 导入团队联系人、企业部门
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
                department_names = ["测试部门1", "测试部门2"]
                Preconditions.create_department_and_add_member(department_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在群发信使首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_group_messenger_page()
            return
        gmp = GroupMessengerPage()
        if gmp.is_on_group_messenger_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_group_messenger_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0001(self):
        """可以正常查看帮助中心内容"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_help_icon()
        hcp = HelpCenterPage()
        # 等待等待群发信使->帮助中心页面加载
        hcp.wait_for_page_load()
        # 1.查看应用简介
        hcp.click_introduction()
        hcp.wait_for_introduction_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        time.sleep(1)
        # 查看操作指引
        hcp.click_guide()
        hcp.wait_for_guide_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        time.sleep(1)
        # 查看资费说明
        hcp.click_explain()
        hcp.wait_for_explain_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        time.sleep(1)
        # 查看常见问题
        hcp.click_problem()
        hcp.wait_for_problem_page_load()
        hcp.click_back()
        hcp.wait_for_page_load()
        hcp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0005(self):
        """添加搜索出的联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.搜索出的联系人是否被选择
        self.assertEquals(nmp.is_exist_text(search_name), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0006(self):
        """添加成员之后再移除成员"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        sccp.click_department_by_name("测试部门1")
        # 添加多个联系人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_contacts_by_name("大佬2")
        sccp.click_contacts_by_name("大佬3")
        # 是否成功选中
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 点击部门已选成员图像取消勾选
        sccp.click_contacts_image_by_name("大佬1")
        time.sleep(2)
        # 点击顶部已选成员信息移除成员
        sccp.click_select_contacts_name("佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 1.是否正常移除成员
        self.assertEquals(nmp.is_exist_text("大佬1"), False)
        self.assertEquals(nmp.is_exist_text("大佬2"), False)
        self.assertEquals(nmp.is_exist_text("大佬3"), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0007(self):
        """多个部门累计添加成员"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.进入多个部门，添加成员
        sccp.click_department_by_name("测试部门1")
        sccp.click_contacts_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        sccp.click_department_by_name("测试部门2")
        sccp.click_contacts_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        # 2.各个部门添加成员是否累计
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        self.assertEquals(nmp.is_exist_text("大佬1"), True)
        self.assertEquals(nmp.is_exist_text("大佬2"), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0009(self):
        """用户不在任何部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业子一层级
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back()
        time.sleep(2)
        # 2.页面是否跳转到企业层级
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_corporate_name(), True)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0010(self):
        """用户在企业部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户在企业部门下
        gmp.click_back()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        time.sleep(2)
        ecp.click_back()
        time.sleep(2)
        if ecp.is_exist_department_name():
            ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exist_department_by_name(department_name), True)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0010():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department")
                workbench_name = wbp.get_workbench_name()
                # 查找并点击所有展开元素
                wbp.find_and_click_open_element()
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                if ecp.is_exist_department_by_name(workbench_name):
                    ecp.click_corporate_by_name(workbench_name)
                time.sleep(2)
                ecp.click_back()
                sccp = SelectCompanyContactsPage()
                time.sleep(2)
                if sccp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                wbp.click_group_messenger()
                n = 1
                # 解决工作台不稳定问题
                while not wbp.page_should_contain_text2("新建短信"):
                    wbp.click_group_messenger()
                    n += 1
                    if n > 20:
                        break
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0011(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户既在企业部门下又在企业子一层级
        gmp.click_back()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门
        department_name = "admin_department"
        Preconditions.add_phone_number_to_department(department_name)
        # 添加本机号码到和通讯录
        Preconditions.add_phone_number_to_he_contacts()
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        time.sleep(2)
        ecp.click_back()
        time.sleep(2)
        if ecp.is_exist_department_name():
            ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.是否直接进入企业层级：企业+部门名称
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals(sccp.is_exist_department_by_name(department_name), True)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0011():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department")
                workbench_name = wbp.get_workbench_name()
                # 查找并点击所有展开元素
                wbp.find_and_click_open_element()
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                if ecp.is_exist_department_by_name(workbench_name):
                    ecp.click_corporate_by_name(workbench_name)
                time.sleep(2)
                ecp.click_back()
                sccp = SelectCompanyContactsPage()
                time.sleep(2)
                if sccp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                wbp.click_group_messenger()
                n = 1
                # 解决工作台不稳定问题
                while not wbp.page_should_contain_text2("新建短信"):
                    wbp.click_group_messenger()
                    n += 1
                    if n > 20:
                        break
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0012(self):
        """用户同时在两个部门下"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保用户在企业部门下
        gmp.click_back()
        wbp = WorkbenchPage()
        # 添加本机号码到指定部门1
        department_name1 = "admin_department1"
        Preconditions.add_phone_number_to_department(department_name1)
        # 添加本机号码到指定部门2
        department_name2 = "admin_department2"
        Preconditions.add_phone_number_to_department(department_name2)
        workbench_name = wbp.get_workbench_name()
        # 解决用户部门变更后不能及时刷新的问题
        wbp.click_company_contacts()
        ecp = EnterpriseContactsPage()
        ecp.wait_for_page_load()
        time.sleep(2)
        ecp.click_back()
        time.sleep(2)
        if ecp.is_exist_department_name():
            ecp.click_back()
        wbp.wait_for_workbench_page_load()
        wbp.click_group_messenger()
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.跳转后是否显示企业层级：企业+部门名称（部门随机显示一个）
        self.assertEquals(sccp.is_exist_corporate_grade(), False)
        self.assertEquals(sccp.is_exist_department_by_name(workbench_name), True)
        self.assertEquals((sccp.is_exist_department_by_name(department_name1) or sccp.is_exist_department_by_name(department_name2)), True)
        sccp.click_back()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @staticmethod
    def tearDown_test_QFXS_0012():
        """恢复环境"""

        fail_time = 0
        while fail_time < 5:
            try:
                Preconditions.make_already_in_message_page()
                mp = MessagePage()
                mp.open_workbench_page()
                wbp = WorkbenchPage()
                Preconditions.delete_department_by_name("admin_department1")
                Preconditions.delete_department_by_name("admin_department2")
                workbench_name = wbp.get_workbench_name()
                # 查找并点击所有展开元素
                wbp.find_and_click_open_element()
                # 解决用户部门变更后不能及时刷新的问题
                wbp.click_company_contacts()
                ecp = EnterpriseContactsPage()
                ecp.wait_for_page_load()
                if ecp.is_exist_department_by_name(workbench_name):
                    ecp.click_corporate_by_name(workbench_name)
                time.sleep(2)
                ecp.click_back()
                sccp = SelectCompanyContactsPage()
                time.sleep(2)
                if sccp.is_exist_department_name():
                    ecp.click_back()
                wbp.wait_for_workbench_page_load()
                wbp.click_group_messenger()
                n = 1
                # 解决工作台不稳定问题
                while not wbp.page_should_contain_text2("新建短信"):
                    wbp.click_group_messenger()
                    n += 1
                    if n > 20:
                        break
                return
            except:
                fail_time += 1

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0016(self):
        """搜索“我的电脑”"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        time.sleep(2)
        # 输入查找信息
        sccp.input_search_message("我的电脑")
        time.sleep(2)
        # 1.是否显示“无搜索结果”
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0017(self):
        """11位号码精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 1.检查搜索结果是否完全匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_full_match(search_number), True)
        # 选择搜索结果
        sccp.click_contacts_by_number(search_number)
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0018(self):
        """6-10位数字可支持模糊搜索匹配结果"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(sccp.is_search_contacts_number_match(search_number), True)
        # 选择搜索结果
        sccp.click_contacts_by_number("13800138005")
        # 2.是否成功选中，输入框是否自动清空
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_clear_search_box(search_number), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0019(self):
        """联系人姓名（全名）精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬1"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否精准匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(search_name)
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0020(self):
        """联系人姓名（非全名）模糊搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "大佬"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name("大佬1")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0025(self):
        """纯空格键不支持搜索匹配"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_content = " "
        # 输入查找信息
        sccp.input_search_message(search_content)
        time.sleep(2)
        # 1.纯空格键不支持搜索匹配
        self.assertEquals(sccp.is_exist_corporate_grade(), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0026(self):
        """空格键+文本 可支持匹配"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = " 马上"
        # 输入查找信息
        sccp.input_search_message(search_name)
        time.sleep(2)
        # 1.检查搜索结果是否模糊匹配关键字
        self.assertEquals(sccp.is_search_contacts_name_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name("哈 马上")
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("马上"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("马上"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0030(self):
        """字母+汉字组合可精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "b测算"
        # 1.输入查找信息，检查搜索结果是否精准匹配关键字
        sccp.input_search_message(search_name)
        time.sleep(2)
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(search_name)
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("测算"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("测算"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0031(self):
        """字母+汉字+数字 组合可精准搜索"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_name = "c平5"
        # 1.输入查找信息，检查搜索结果是否精准匹配关键字
        sccp.input_search_message(search_name)
        time.sleep(2)
        self.assertEquals(sccp.is_search_contacts_name_full_match(search_name), True)
        # 选择搜索结果
        sccp.click_contacts_by_name(search_name)
        # 2.搜索栏是否清空，是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_clear_search_box(search_name), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("平5"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("平5"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0032(self):
        """搜索非企业联系人提示无结果"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        time.sleep(2)
        # 输入不存在在企业通讯录中的用户电话号码
        sccp.input_search_message("13900009999")
        time.sleep(2)
        # 1.是否显示“无搜索结果”
        self.assertEquals(sccp.is_exist_text(), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0033(self):
        """任意点击搜索结果联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        search_number = "13800138005"
        # 输入查找信息
        sccp.input_search_message(search_number)
        time.sleep(2)
        # 点击勾选搜索出的联系人头像
        sccp.click_contacts_image()
        # 1.是否出现已选人名和头像，是否展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0035(self):
        """多选-任意选择多位联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 选择三位联系人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_contacts_by_name("大佬2")
        sccp.click_contacts_by_name("大佬3")
        time.sleep(2)
        # 联系人是否为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬3"), True)
        # 是否展示已选人数/上限人数
        self.assertEquals(sccp.is_exist_select_and_all("3"), True)
        # 取消已选联系人
        sccp.click_contacts_by_name("大佬1")
        time.sleep(2)
        # 1.被取消联系人名和头像是否被移除，已选人数/上限人数是否改变
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), False)
        self.assertEquals(sccp.is_exist_select_contacts_image("佬1"), False)
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        sccp.click_back()
        time.sleep(2)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0036(self):
        """添加多部门联系人"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 1.部门人数可以叠加，同一号码（不同姓名、不同部门）选择一个则其余都选上
        sccp.click_department_by_name("测试部门1")
        sccp.click_contacts_by_name("大佬1")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_and_all("1"), True)
        sccp.click_back()
        sccp.click_department_by_name("测试部门2")
        sccp.click_contacts_by_name("大佬2")
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        self.assertEquals(sccp.is_exist_select_and_all("2"), True)
        sccp.click_back()
        time.sleep(1)
        sccp.click_back()
        time.sleep(1)
        if sccp.is_exist_corporate_name():
            sccp.click_back_by_android()
            time.sleep(1)
        nmp.wait_for_page_load()
        nmp.click_back()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0039(self):
        """直接添加接收人后再次点击'+'"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp = SelectCompanyContactsPage()
        # 等待群发信使->新建短信->选择联系人页面加载
        sccp.wait_for_page_load()
        # 选择两位联系人
        sccp.click_contacts_by_name("大佬1")
        sccp.click_contacts_by_name("大佬2")
        # 点击确定
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        nmp.click_add_icon()
        sccp.wait_for_page_load()
        # 1.跳转联系人选择器后，上次添加的联系人是否为已选中状态
        self.assertEquals(sccp.is_exist_select_contacts_name("佬1"), True)
        self.assertEquals(sccp.is_exist_select_contacts_name("佬2"), True)
        sccp.click_contacts_by_name("大佬3")
        sccp.click_sure_button()
        nmp.wait_for_page_load()
        # 2.是否添加成功，已添加与新添加用户均展示正常
        self.assertEquals(nmp.is_exist_text("大佬1"), True)
        self.assertEquals(nmp.is_exist_text("大佬2"), True)
        self.assertEquals(nmp.is_exist_text("大佬3"), True)
        nmp.click_back()
        time.sleep(2)
        nmp.click_no()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0042(self):
        """点击返回键返回上一级页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        # 返回上一级
        nmp.click_back()
        # 1.等待群发信使首页加载
        gmp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QFXS_0043(self):
        """点击顶部关闭按钮退出到工作台页面"""

        gmp = GroupMessengerPage()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
        # 确保有【x】控件可点击
        gmp.click_new_message()
        nmp = NewMessagePage()
        # 等待群发信使->新建短信页面加载
        nmp.wait_for_page_load()
        nmp.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台页面加载
        wbp.wait_for_workbench_page_load()
        wbp.click_group_messenger()
        # 等待群发信使首页加载
        gmp.wait_for_page_load()
