import unittest

from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.super_meeting.SuperMeeting import SuperMeetingPage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import *
import time

from pages.workbench.create_team.CreateTeam import CreateTeamPage
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from TestCase.m001_login.login import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


class SuperMeetingTest(TestCase):
    """工作台->超级会议"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """进入超级会议页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_super_meeting_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_super_meeting_page()
            return
        smp = SuperMeetingPage()
        if smp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_super_meeting_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC','workbench', 'CJHY')
    def test_CJHY_0001(self):
        """查看超级会议使用说明"""
        # 1、点击超级会议顶部下拉箭头
        # 2、点击“使用指南”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        # 1.点击点击右上角【？】
        smp.click_element_('？')
        smp.wait_for_page_loads("发起超级会议")
        # 2.上下滑动浏览页面
        a=0
        while a<10:
            smp.page_up()
            a+=1
        if not smp.is_text_present("时长权益扣减说明"):
            raise AssertionError("不可正常浏览页面")
        smp.click_close_more()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC','workbench', 'CJHY')
    def test_CJHY_0002(self):
        """添加搜索出的企业通讯录联系人"""
        # 1、点击“预约会议”
        # 2、搜索关键词，如“测试”
        # 3、选择“搜索企业通讯录联系人：测试
        # 4、点击搜索出的成员
        # 5、点击“确定”
        # 6、选择开始时间，点击“下一步”
        # 7、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.input_search_contact_message("yyx")
        time.sleep(2)
        sc.click_text("18920736596")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(6)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        #取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        time.sleep(3)
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        # smp.press_element_("(2人)",3000)
        # time.sleep(2)
        # smp.click_text("消除所有")
        # time.sleep(2)
        # smp.click_element_("确定删除所有记录")
        # time.sleep(2)
        current_mobile().back()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC','workbench', 'CJHY')
    def test_CJHY_0003(self):
        """添加搜索出的本地联系人"""
        # 1、点击“预约会议”
        # 2、搜索关键词，如“测试”
        # 3、选择本地联系人搜索结果
        # 4、点击搜索出的成员
        # 5、点击“确定”
        # 6、选择开始时间，点击“下一步”
        # 7、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("飞信")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        time.sleep(3)
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC','workbench', 'CJHY')
    def test_CJHY_0004(self):
        """添加搜索的陌生号码"""
        # 1、点击“预约会议”
        # 2、搜索陌生号码
        # 3、点击搜索出的成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_contact_message("15202265088")
        time.sleep(2)
        sc.click_text("未知号码")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        sc.click_text("确定")
        time.sleep(6)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.wait_for_page_loads()
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC','workbench', 'CJHY')
    def test_CJHY_0005(self):
        """添加搜索的陌生固话"""
        # 1、点击“预约会议”
        # 2、搜索陌生固话号码
        # 3、点击搜索出的成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_contact_message("06638820702")
        time.sleep(2)
        sc.click_text("未知号码")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        time.sleep(3)
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0006(self):
        """11位号码精准搜索"""
        # 1.在搜索框输入11位号码，查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp= ContactsPage()
            cp.create_contacts_if_not_exits("主子","18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("18920796596")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("18920796596")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0007(self):
        """6-10位数字可支持模糊搜索匹配结果"""
        # 1.在搜索框输入6 - 10位数字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("189207965")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("189207965")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0008(self):
        """联系人姓名（全名）精准搜索"""
        # 1.在搜索框输入联系人姓名（全名）, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("主子")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("主子")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0009(self):
        """联系人姓名（非全名）模糊搜索"""
        # 1.在搜索框输入联系人联系人姓名（非全名）, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("主")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("主")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0010(self):
        """字母搜索，按照联系人的姓（包含字母）"""
        # 1.在搜索框输入1字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0011(self):
        """字母搜索，按照联系人的姓（包含字母）"""
        # 1.在搜索框输入1字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0012(self):
        """字母搜索可支持多个字母大小写同时匹配"""
        # 1.在搜索框输入多方大小写字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("Zhu")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("Zhu")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0013(self):
        """特殊字符可支持搜索匹配"""
        # 1.在搜索框输入特殊字符, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("&")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("&")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0014(self):
        """纯空格键不支持搜索匹配"""
        # 1.在搜索框输入空格，查看显示
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword(" ")
            time.sleep(2)
            if sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(" ")
            time.sleep(2)
            if sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0015(self):
        """空格键+文本 可支持匹配"""
        # 1.在搜索框输入空格键 + 文本, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword(" 属下")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(" 属下")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0016(self):
        """搜索框输入，不限制字符，可一键删除，可按输入盘删除键删除"""
        # 1.在搜索框输入长文本
        # 2.在输入框滑动已输入的文字
        # 3.点击键盘删除
        # 4.点击X一键删除
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        mess = "哈" * 30
        sc.input_search_keyword(mess)
        time.sleep(2)
        sc.press_and_move_right()
        time.sleep(2)
        smp.click_element_("查询文本删除X")
        if not sc.is_text_present("搜索或输入号码"):
            raise AssertionError("输入框没有自动清空")
        current_mobile().back()
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0017(self):
        """搜索本机号码"""
        # 1.在搜索框输入本机号码，查看匹配结果
        # 2.点击本机联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        if not sc.swipe_and_find_element(phone_number):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("本机", phone_number)
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword(phone_number)
            time.sleep(2)
            if not sc.is_text_present("本机"):
                if not sc.is_text_present("aa"):
                    raise AssertionError("搜索结果有误")
                else:
                    sc.click_text("aa")
            else:
                sc.click_text("本机")
            if not sc.is_toast_exist("该联系人不可选择"):
                raise AssertionError("没有toast提示该联系人不可选择")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(phone_number)
            time.sleep(2)
            if not sc.is_text_present("本机"):
                if not sc.is_text_present("aa"):
                    raise AssertionError("搜索结果有误")
                else:
                    sc.click_text("aa")
            else:
                sc.click_text("本机")
            if not sc.is_toast_exist("该联系人不可选择"):
                raise AssertionError("没有toast提示该联系人不可选择")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0019(self):
        """字母+汉字组合可精准搜索"""
        # 1.在搜索框输入：字母 + 汉字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("a加1"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("a加1", "18920798888")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("a加")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("a加")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0020(self):
        """字母+汉字+数字组合可精准搜索"""
        # 1.在搜索框输入：字母 + 汉字 + 数字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("a加1"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("a加1", "18920798888")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            time.sleep(2)
            sc.input_search_keyword("a加1")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("a加1")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/63"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0021(self):
        """搜索固话"""
        # 1.在搜索框输入：固话号码, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.input_search_keyword("06638820709")
        time.sleep(2)
        if not sc.is_text_present("未知号码"):
            raise AssertionError("搜索结果有误")
        sc.click_text("未知号码")
        time.sleep(2)
        if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
            raise AssertionError("不可成功选中")
        current_mobile().back()
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0022(self):
        """用户不在任何部门下"""
        # 1.点击“+”添加联系人
        # 2.点击返回或者面包屑中的企业通讯录
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("飞信")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        smp.wait_for_page_loads("会议开始时间")
        time.sleep(2)
        smp.click_text("取消")
        smp.click_element_("加号")
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if not sc.is_text_present("企业通讯录"):
            raise AssertionError("没有直接进入企业子一层级")
        current_mobile().back()
        time.sleep(2)
        if not smp.is_element_exit("右三角"):
            raise AssertionError("页面没有跳转到企业层级")
        current_mobile().back()
        current_mobile().back()
        smp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', 'CMCC1', 'workbench1', 'CJHY')
    def test_CJHY_0023(self):
        """用户在企业部门下"""
        # 1.点击“+”添加联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if sc.is_text_present("企业通讯录") or (not sc.is_text_present("用户在企业部门下1")):
            current_mobile().launch_app()
            mess=MessagePage()
            mess.wait_for_page_load()
            mess.open_workbench_page()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp=OrganizationStructurePage()
            osp.wait_for_page_load()
            osp.click_text("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name("用户在企业部门下1")
            osp.click_text("完成")
            osp.wait_for_page_load()
            time.sleep(5)
            sc.click_one_contact("用户在企业部门下1")
            time.sleep(2)
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("本机")
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
            osp.input_contacts_number(phone_number)
            time.sleep(3)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择手机联系人")
            time.sleep(2)
            sc.input_search_contact_message("飞信")
            time.sleep(2)
            sc.click_text("飞信电话")
            time.sleep(2)
            sc.click_text("确定")
            smp.wait_for_page_loads("会议开始时间")
            time.sleep(2)
            smp.click_text("取消")
            smp.click_element_("加号")
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(3)
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            time.sleep(2)
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            if sc.is_text_present("企业通讯录"):
                raise AssertionError("跳转后没有直接进入企业层级：企业+部门名称")
            current_mobile().back()
            current_mobile().back()
            smp.click_close_more()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp.wait_for_page_load()
            sc.click_one_contact("用户在企业部门下1")
            osp.click_text("更多")
            time.sleep(1)
            osp.click_text("部门设置")
            time.sleep(1)
            osp.click_text("删除")
            time.sleep(2)
            osp.click_element_("确定删除部门")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("删除部门失败")
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
        else:
            print("用户一开始已经在企业部门下，请删除部门让用户一开始不在企业部门下")

    @tags('ALL', 'CMCC1', 'workbench1', 'CJHY')
    def test_CJHY_0024(self):
        """用户在企业部门下又在企业子一层级中，直接进入企业层级"""
        # 1.点击“+”添加联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if sc.is_text_present("企业通讯录"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp = OrganizationStructurePage()
            osp.wait_for_page_load()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
            if not osp.swipe_and_find_element(phone_number):
                osp.click_text("添加联系人")
                time.sleep(1)
                osp.click_text("手动输入添加")
                time.sleep(1)
                osp.input_contacts_name("本机")
                osp.input_contacts_number(phone_number)
                time.sleep(2)
                osp.click_text("完成")
                if not osp.is_toast_exist("成功"):
                    raise AssertionError("手动添加失败")
                osp.wait_for_page_load()
            osp.click_text("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name("用户在企业部门下1")
            osp.click_text("完成")
            osp.wait_for_page_load()
            time.sleep(2)
            sc.click_one_contact("用户在企业部门下1")
            time.sleep(2)
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("本机")
            osp.input_contacts_number(phone_number)
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择手机联系人")
            time.sleep(2)
            sc.input_search_contact_message("飞信")
            time.sleep(2)
            sc.click_text("飞信电话")
            time.sleep(2)
            sc.click_text("确定")
            smp.wait_for_page_loads("会议开始时间")
            time.sleep(2)
            smp.click_text("取消")
            smp.click_element_("加号")
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(3)
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            if sc.is_text_present("企业通讯录"):
                raise AssertionError("跳转后没有直接进入企业层级：企业+部门名称")
            current_mobile().back()
            current_mobile().back()
            smp.click_close_more()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp.wait_for_page_load()
            sc.click_one_contact("用户在企业部门下1")
            osp.click_text("更多")
            time.sleep(1)
            osp.click_text("部门设置")
            time.sleep(1)
            osp.click_text("删除")
            time.sleep(2)
            osp.click_element_("确定删除部门")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("删除部门失败")
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
        else:
            print("用户一开始已经在企业部门下，请删除部门让用户一开始不在企业部门下")

    @tags('ALL', 'CMCC1', 'workbench1', 'CJHY')
    def test_CJHY_0025(self):
        """用户同时在两个部门下"""
        # 1.点击“+”添加联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if sc.is_text_present("企业通讯录"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp = OrganizationStructurePage()
            osp.wait_for_page_load()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
            osp.click_text("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name("用户在企业部门下1")
            osp.click_text("完成")
            osp.wait_for_page_load()
            time.sleep(2)
            sc.click_one_contact("用户在企业部门下1")
            time.sleep(2)
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("本机")
            osp.input_contacts_number(phone_number)
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            osp.wait_for_page_load()
            osp.click_text("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name("用户在企业部门下2")
            osp.click_text("完成")
            osp.wait_for_page_load()
            time.sleep(2)
            sc.click_one_contact("用户在企业部门下2")
            time.sleep(2)
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("本机")
            osp.input_contacts_number(phone_number)
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(3)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择手机联系人")
            time.sleep(2)
            sc.input_search_contact_message("飞信")
            time.sleep(2)
            sc.click_text("飞信电话")
            time.sleep(2)
            sc.click_text("确定")
            smp.wait_for_page_loads("会议开始时间")
            time.sleep(2)
            smp.click_text("取消")
            smp.click_element_("加号")
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(3)
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            if sc.is_text_present("企业通讯录"):
                raise AssertionError("跳转后没有直接进入企业层级：企业+部门名称")
            current_mobile().back()
            current_mobile().back()
            smp.click_close_more()
            workbench.wait_for_page_load()
            workbench.click_organization()
            osp.wait_for_page_load()
            sc.click_one_contact("用户在企业部门下1")
            osp.click_text("更多")
            time.sleep(1)
            osp.click_text("部门设置")
            time.sleep(1)
            osp.click_text("删除")
            time.sleep(2)
            osp.click_element_("确定删除部门")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("删除部门失败")
            time.sleep(2)
            osp.wait_for_page_load()
            sc.click_one_contact("用户在企业部门下2")
            osp.click_text("更多")
            time.sleep(1)
            osp.click_text("部门设置")
            time.sleep(1)
            osp.click_text("删除")
            time.sleep(2)
            osp.click_element_("确定删除部门")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("删除部门失败")
            current_mobile().back()
            workbench.wait_for_page_load()
            workbench.click_super_meeting()
            smp.wait_for_page_loads()
            smp.click_element_("预约会议")
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench.wait_for_page_load()
        else:
            print("用户一开始已经在企业部门下，请删除部门让用户一开始不在企业部门下")

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0026(self):
        """添加企业通讯录联系人"""
        # 1、点击“预约会议”
        # 2、点击“企业通讯录”
        # 3、勾选成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.click_one_contact("yyx")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(6)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        time.sleep(3)
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        # smp.press_element_("(2人)",3000)
        # time.sleep(2)
        # smp.click_text("消除所有")
        # time.sleep(2)
        # smp.click_element_("确定删除所有记录")
        # time.sleep(2)
        current_mobile().back()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0027(self):
        """添加企业通讯录联系人"""
        # 1、点击“预约会议”
        # 2、点击“企业通讯录”
        # 3、勾选成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.click_one_contact("yyx")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(6)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        # smp.press_element_("(2人)",3000)
        # time.sleep(2)
        # smp.click_text("消除所有")
        # time.sleep(2)
        # smp.click_element_("确定删除所有记录")
        # time.sleep(2)
        current_mobile().back()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0028(self):
        """添加本地联系人"""
        # 1、点击“预约会议”
        # 2、点击“本地联系人”
        # 3、勾选成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        smp.swipe_by_up()
        time.sleep(5)
        sc.click_text("确定")
        time.sleep(6)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0029(self):
        """添加本地联系人，搜索结果"""
        # 1、点击“预约会议”
        # 2、点击“本地联系人”
        # 3、搜索框中输入关键词，点击搜索出的成员
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("飞信")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(2)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0034(self):
        """添加最近聊天"""
        # 1、点击“预约会议”
        # 2、点击“最近聊天”中的联系人
        # 3、点击选中联系人
        # 4、点击“确定”
        # 5、选择开始时间，点击“下一步”
        # 6、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.open_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个手机联系人发信息
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        sc.input_search_contact_message("飞信")
        sc.click_text("飞信电话")
        sc.click_sure_bottom()
        time.sleep(2)
        chat = SingleChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        info = "哈"
        chat.input_message(info)
        chat.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        mess.wait_for_page_load()
        mess.open_workbench_page()
        wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        smp.swipe_by_up()
        time.sleep(5)
        sc.click_text("确定")
        time.sleep(5)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0038(self):
        """预约会议详情"""
        # 1、点击已经预约成功的会议，进入详情
        # 2、点击“+”
        # 3、选择其他未选择的成员，点击“确定”
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("飞信")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(10)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        time.sleep(3)
        smp.click_element_("加号")
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.click_one_local_contacts()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        smp.click_text("确定")
        if not smp.is_toast_exist("修改预约会议成功"):
            raise AssertionError("修改预约会议失败")
        # 取消会议
        time.sleep(10)
        smp.click_text("(3人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0039(self):
        """预约会议详情"""
        # 1、点击已经预约成功的会议，进入详情
        # 2、点击“-”
        # 3、点击成员旁边红色“x”
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("预约会议")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_one_local_contacts()
        sc.click_text("确定")
        time.sleep(5)
        smp.swipe_by_up()
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(5)
        sc.click_text("确定")
        if not smp.is_toast_exist("会议预约成功"):
            raise AssertionError("会议预约失败")
        time.sleep(5)
        smp.click_text("(3人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_element_("减号5")
        time.sleep(2)
        smp.click_element_("去掉会议人员X")
        time.sleep(2)
        smp.click_text("确定")
        if not smp.is_toast_exist("修改预约会议成功"):
            raise AssertionError("修改预约会议失败")
        # 取消会议
        time.sleep(5)
        smp.click_text("(2人)")
        smp.wait_for_page_loads("取消会议")
        smp.click_text("取消会议")
        time.sleep(5)
        smp.click_element_("确定取消此次会议")
        time.sleep(8)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0040(self):
        """添加搜索出的企业通讯录联系人"""
        # 1、点击“马上开会”
        # 2、搜索关键词，如“测试”
        # 3、选择“搜索企业通讯录联系人：测试”
        # 4、点击搜索出的成员
        # 5、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.input_search_contact_message("yyx")
        time.sleep(2)
        sc.click_text("18920736596")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(5)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0041(self):
        """添加搜索出的本地联系人"""
        # 1、点击“马上开会”
        # 2、搜索关键词，如“测试”
        # 3、选择本地联系人搜索结果
        # 4、点击搜索出的成员
        # 5、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("飞信")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0042(self):
        """添加搜索的陌生号码"""
        # 1、点击“马上开会”
        # 2、搜索陌生号码
        # 3、点击搜索出的成员
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_contact_message("15202265088")
        time.sleep(2)
        sc.click_text("未知号码")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0043(self):
        """添加搜索的陌生固话"""
        # 1、点击“马上开会”
        # 2、搜索陌生固话号码
        # 3、点击搜索出的成员
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_contact_message("06638820708")
        time.sleep(2)
        sc.click_text("未知号码")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0044(self):
        """添加企业通讯录联系人"""
        # 1、点击“马上开会”
        # 2、点击“企业通讯录”
        # 3、勾选成员
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            time.sleep(2)
            current_mobile().back()
            wbp.wait_for_page_load()
        else:
            current_mobile().back()
            wbp.wait_for_page_load()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if not sc.is_text_present("企业通讯录"):
            sc.click_element_("部门名称")
            time.sleep(2)
        sc.click_one_contact("yyx")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0045(self):
        """添加本地联系人"""
        # 1、点击“马上开会”
        # 2、点击“本地联系人”
        # 3、勾选成员
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text("选择手机联系人")
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0046(self):
        """添加本地联系人"""
        # 1、点击“马上开会”
        # 2、点击“本地联系人”
        # 3、搜索框中输入关键词，点击搜索出的成员
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.input_search_contact_message("12560")
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_CJHY_0047():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_super_meeting_page()

    @tags('ALL', 'CMCC_skip', 'workbench', 'CJHY')
    def test_CJHY_0047(self):
        """读取本地联系人权限"""
        # 1、点击“马上开会”
        # 2、点击“本地联系人”
        # 3、出现弹窗，点击“拒绝”
        # 4、查看本地联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        time.sleep(2)
        if sc.is_text_present("始终允许"):
            sc.get_element_("禁止").click()
        time.sleep(2)
        sc.click_text("选择手机联系人")
        time.sleep(2)
        if sc.is_element_present_by_locator("联系人栏"):
            raise AssertionError("拒绝后可以展示本地通讯录")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_CJHY_0050():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.enter_super_meeting_page()

    @tags('ALL', 'CMCC_skip', 'workbench', 'CJHY')
    def test_CJHY_0050(self):
        """读取本地联系人权限"""
        # 1、点击“马上开会”
        # 2、点击“本地联系人”
        # 3、出现弹窗，点击“允许”
        # 4、查看本地联系人
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        time.sleep(2)
        if sc.is_text_present("始终允许"):
            sc.click_text("始终允许")
        time.sleep(2)
        sc.click_text("选择手机联系人")
        time.sleep(2)
        if not sc.is_element_present_by_locator("联系人栏"):
            raise AssertionError("允许后不可以展示本地通讯录")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0051(self):
        """添加最近聊天"""
        # 1、点击“马上开会”
        # 2、点击“最近聊天”中的联系人
        # 3、点击选中联系人
        # 4、点击“确定”
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
        wbp.open_message_page()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择手机联系人")
        time.sleep(2)
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        chat = SingleChatPage()
        time.sleep(2)
        if  chat.is_text_present("1元/条"):
            chat.click_i_have_read()
        time.sleep(2)
        chat.input_message("哈哈")
        # 点击发送
        chat.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        mess.open_workbench_page()
        wbp.click_super_meeting()
        smp.wait_for_page_loads()
        smp.click_element_("马上开会")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.click_text("飞信电话")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(8)
        current_mobile().hang_up_the_call()
        time.sleep(2)
        smp.click_text("结束会议")
        time.sleep(2)
        smp.click_text("确定")
        time.sleep(2)
        current_mobile().back()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0057(self):
        """断网提示"""
        # 1、断开网络
        # 2、点击页面其他元素
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.set_network_status(0)
        time.sleep(8)
        smp.click_enter_more()
        time.sleep(2)
        if not smp.is_text_present("网络出错，轻触屏幕重新加载"):
            raise AssertionError("没有出现‘网络出错，轻触屏幕重新加载’字段")
        smp.click_text("网络出错，轻触屏幕重新加载")
        if not smp.is_toast_exist("网络不可用，请检查网络设置"):
            raise AssertionError("没有出现tosat提示‘网络不可用，请检查网络设置’")
        time.sleep(2)
        smp.set_network_status(6)
        time.sleep(8)
        current_mobile().back()
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    def tearDown_test_CJHY_0057(self):
        #重新连接网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0058(self):
        """点击顶部返回键"""
        # 1、在任意页面点击顶部【 < 】
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        smp.click_element_("返回")
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'CJHY')
    def test_CJHY_0059(self):
        """点击顶部关闭按钮"""
        # 在其他有关闭按钮页面，点击顶部【x】
        smp = SuperMeetingPage()
        smp.wait_for_page_loads()
        time.sleep(3)
        smp.click_text("2人")
        time.sleep(3)
        smp.click_close_more()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()
