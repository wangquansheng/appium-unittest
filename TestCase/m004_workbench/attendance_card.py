import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.attendance_card.AttendanceCard import AttendanceCardPage
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
    def enter_attendance_card_page():
        """进入考勤打卡首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_attendance_card()
        acp = AttendanceCardPage()
        # 解决工作台不稳定问题
        n = 1
        while not acp.page_should_contain_text2("考勤组"):
            acp.click_back_by_android()
            wbp.wait_for_workbench_page_load()
            wbp.click_attendance_card()
            n += 1
            if n > 20:
                break
        # 确保已经加入考勤组
        if not acp.is_on_attendance_card_page():
            acp.click_text("新建考勤组")
            time.sleep(2)
            if acp.is_text_present("始终允许"):
                acp.click_text("始终允许")
            time.sleep(2)
            acp.click_text("请选择")
            time.sleep(5)
            acp.click_text("全选")
            time.sleep(1)
            acp.click_text("确认")
            time.sleep(1)
            acp.click_create_attendance_group_button()
            time.sleep(5)
            acp.click_back()
            acp.wait_for_page_load()


class AttendanceCardAllTest(TestCase):
    """工作台->考勤打卡"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在考勤打卡首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_attendance_card_page()
            return
        acp = AttendanceCardPage()
        if acp.is_on_attendance_card_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_attendance_card_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0001(self):
        """帮助文档展示正常"""

        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        # # 解决工作台不稳定问题
        # acp.click_back()
        # wbp = WorkbenchPage()
        # wbp.wait_for_workbench_page_load()
        # wbp.click_attendance_card()
        # acp.wait_for_page_load()
        # 点击帮助图标
        acp.click_help_icon()
        time.sleep(2)
        # 1.进入各个帮助页
        acp.click_text("获取地址失败")
        acp.wait_for_help_page_load("获取地址失败")
        acp.click_back()
        time.sleep(1)
        acp.click_text("定位不准确")
        acp.wait_for_help_page_load("定位不准确")
        acp.click_back()
        time.sleep(1)
        acp.click_text("提示不在考勤组")
        acp.wait_for_help_page_load("提示不在考勤组")
        acp.click_back()
        time.sleep(1)
        acp.click_back()
        # 等待考勤打卡首页加载
        acp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_KQDK_0006(self):
        """点击顶部返回键，返回到上一级页面"""

        acp = AttendanceCardPage()
        acp.wait_for_page_load()
        acp.click_back()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_workbench_page_load()
        wbp.click_attendance_card()
        # 解决工作台不稳定问题
        n = 1
        while not acp.page_should_contain_text2("考勤组"):
            acp.click_back_by_android()
            wbp.wait_for_workbench_page_load()
            wbp.click_attendance_card()
            n += 1
            if n > 20:
                break
        acp.wait_for_page_load()
        acp.click_help_icon()
        time.sleep(2)
        acp.click_back()
        # 2.等待考勤打卡首页加载
        acp.wait_for_page_load()



