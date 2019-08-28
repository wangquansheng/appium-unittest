import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, current_driver
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.mobile_attendance.MobileAttendance import MobileAttendancePage
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
    def enter_mobile_attendance_page():
        """进入移动出勤首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_mobile_attendance()
        # 解决工作台不稳定问题
        map = MobileAttendancePage()
        n = 1
        while not map.page_should_contain_text2("考勤签到"):
            map.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_mobile_attendance()
            n += 1
            if n > 20:
                break


class MobileAttendanceAllTest(TestCase):
    """工作台->移动出勤"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在移动出勤首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_mobile_attendance_page()
            return
        map = MobileAttendancePage()
        if map.is_on_mobile_attendance_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_mobile_attendance_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0001(self):
        """可正常进入应用"""

        map = MobileAttendancePage()
        # 1.等待移动出勤首页加载
        map.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0009(self):
        """点击顶部返回键"""

        map = MobileAttendancePage()
        # 等待移动出勤首页加载
        map.wait_for_page_load()
        # 移动出勤首页点击顶部【<】
        map.click_back()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_workbench_page_load()
        wbp.click_mobile_attendance()
        map.wait_for_page_load()
        map.click_field_attendance()
        time.sleep(2)
        # 其他页面点击顶部【<】
        map.click_back()
        # 2.等待移动出勤首页加载
        map.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_YDCQ_0010(self):
        """点击顶部关闭按钮"""

        map = MobileAttendancePage()
        # 等待移动出勤首页加载
        map.wait_for_page_load()
        map.click_field_attendance()
        time.sleep(2)
        # 点击顶部【x】
        map.click_close()
        wbp = WorkbenchPage()
        # 1.等待工作台首页加载
        wbp.wait_for_workbench_page_load()
        wbp.click_mobile_attendance()
        map.wait_for_page_load()