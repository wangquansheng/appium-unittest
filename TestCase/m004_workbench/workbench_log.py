import time
import warnings
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, current_driver
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.workbench_log.WorkbenchLog import WorkbenchLogPage
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
    def enter_log_page():
        """进入日志首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_journal()
        wlp = WorkbenchLogPage()
        wlp.wait_for_page_loads()

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


class EnterpriseLogAllTest(TestCase):
    """
    模块：工作台->企业通讯录
    文件位置：20190313工作台全量用例整理.xlsx
    表格：工作台->企业通讯录
    Author：刘晓东
    """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        # Preconditions.select_mobile('Android-移动')
        # # 导入测试联系人、群聊
        # fail_time1 = 0
        # flag1 = False
        # import dataproviders
        # while fail_time1 < 3:
        #     try:
        #         required_contacts = dataproviders.get_preset_contacts()
        #         conts = ContactsPage()
        #         current_mobile().hide_keyboard_if_display()
        #         Preconditions.make_already_in_message_page()
        #         conts.open_contacts_page()
        #         try:
        #             if conts.is_text_present("发现SIM卡联系人"):
        #                 conts.click_text("显示")
        #         except:
        #             pass
        #         for name, number in required_contacts:
        #             # 创建联系人
        #             conts.create_contacts_if_not_exits(name, number)
        #         required_group_chats = dataproviders.get_preset_group_chats()
        #         conts.open_group_chat_list()
        #         group_list = GroupListPage()
        #         for group_name, members in required_group_chats:
        #             group_list.wait_for_page_load()
        #             # 创建群
        #             group_list.create_group_chats_if_not_exits(group_name, members)
        #         group_list.click_back()
        #         conts.open_message_page()
        #         flag1 = True
        #     except:
        #         fail_time1 += 1
        #     if flag1:
        #         break
        #
        # # 导入团队联系人
        # fail_time2 = 0
        # flag2 = False
        # while fail_time2 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
        #         Preconditions.create_he_contacts(contact_names)
        #         contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
        #                           ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296")]
        #         Preconditions.create_he_contacts2(contact_names2)
        #         flag2 = True
        #     except:
        #         fail_time2 += 1
        #     if flag2:
        #         break

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
    def test_RZ_0001(self):
        """验证点击返回按钮是否正确"""
        # 1.进入日志首页
        Preconditions.enter_log_page()
        wlp = WorkbenchLogPage()
        # 2.点击返回
        wlp.click_back()
        # 3.验证是否在工作台页面
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        self.assertTrue(wbp.is_on_this_page())

    @tags('ALL', 'CMCC', 'workbench', 'yx')
    def test_RZ_0002(self):
        """新建日志"""
        # 1.进入日志首页
        Preconditions.enter_log_page()
        wlp = WorkbenchLogPage()
        # 2.点击写日志
        wlp.click_create_new_log()
        # 3.点击日报
        wlp.click_day_news()
        wlp.wait_for_input_page_loads()
        # 4.输入日报信息
        wlp.input_title("工作台日志-日报001")
        wlp.input_work_summary("今日工作总结")
        wlp.input_work_plan("明日工作计划")
        wlp.input_coordination_help("需要协调与帮助")
        wlp.input_remark("备注")
        # 5.点击“+”按钮
        wlp.click_add_contact()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 6.选择提交人
        sccp.click_contacts_by_name("大佬1")
        # 7.点击确认
        sccp.click_sure_button()
        wlp.wait_for_input_page_loads()
        wlp.page_up()
        # 8.点击提交
        wlp.click_submit()
        wlp.wait_for_input_page_loads()
        # 9.判断是否提交成功
        self.assertEquals(wlp.is_text_present("工作台日志-日报001"), True)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'workbench', 'yx')
    def test_RZ_0003(self):
        """新建日志 -- 提交人使用上次提交人"""
        # 1.进入日志首页
        Preconditions.enter_log_page()
        wlp = WorkbenchLogPage()
        # 2.点击写日志
        wlp.click_create_new_log()
        # 3.点击日报
        wlp.click_day_news()
        wlp.wait_for_input_page_loads()
        # 4.输入日报信息
        wlp.input_title("工作台日志-日报002")
        wlp.input_work_summary("今日工作总结")
        wlp.input_work_plan("明日工作计划")
        wlp.input_coordination_help("需要协调与帮助")
        wlp.input_remark("备注")
        # 5.点击添加上次联系人
        wlp.click_add_last_contact()
        wlp.page_up()
        # 6.点击提交
        wlp.click_submit()
        wlp.wait_for_input_page_loads()
        # 7.判断是否提交成功
        self.assertEquals(wlp.is_text_present("工作台日志-日报002"), True)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'workbench', 'yx')
    def test_RZ_0004(self):
        """新建日志 -- 删除已选择的提交人"""
        # 1.进入日志首页
        Preconditions.enter_log_page()
        wlp = WorkbenchLogPage()
        # 2.点击写日志
        wlp.click_create_new_log()
        # 3.点击日报
        wlp.click_day_news()
        wlp.wait_for_input_page_loads()
        # 4.输入日报信息
        wlp.input_title("工作台日志-日报003")
        wlp.input_work_summary("今日工作总结")
        wlp.input_work_plan("明日工作计划")
        wlp.input_coordination_help("需要协调与帮助")
        wlp.input_remark("备注")
        # 5.点击“+”按钮
        wlp.click_add_contact()
        sccp = SelectCompanyContactsPage()
        sccp.wait_for_page_load()
        # 6.选择接收人
        sccp.click_contacts_by_name("大佬1")
        # 7.点击确认
        sccp.click_sure_button()
        # 8.点击头像删除
        wlp.wait_for_input_page_loads()
        wlp.click_avatar_delete()
        # 9.点击“+”按钮
        wlp.click_add_contact()
        sccp.wait_for_page_load()
        # 10.选择接收人
        sccp.click_contacts_by_name("大佬2")
        # 11.点击确认
        sccp.click_sure_button()
        wlp.wait_for_input_page_loads()
        wlp.page_up()
        # 12.点击提交
        wlp.click_submit()
        wlp.wait_for_input_page_loads()
        # 13.判断是否提交成功
        self.assertEquals(wlp.is_text_present("工作台日志-日报003"), True)
        time.sleep(2)