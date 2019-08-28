import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile, current_driver
from pages import MessagePage
from pages import WorkbenchPage
from pages.workbench.manager_console.EnterpriseInterests import EnterpriseInterestsPage
from pages.workbench.manager_console.ManagerGuide import ManagerGuidePage
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
    def enter_manager_guide_page():
        """进入管理员指引首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp = ManagerGuidePage()
        mgp.wait_for_page_load()

    @staticmethod
    def enter_enterprise_interests_page():
        """进入企业权益首页"""

        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_rights()
        eip = EnterpriseInterestsPage()
        eip.wait_for_page_load()


class ManagerGuideAllTest(TestCase):
    """工作台->管理员指引、权益"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

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

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0001(self):
        """能够正常打开管理员指引页面，可以正常返回"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        # 解决工作台不稳定问题
        mgp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        # 1、2.进入各个指引页
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("添加/邀请成员")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_back()
        time.sleep(1)
        mgp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        mgp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        time.sleep(2)
        # 3.进入帮助中心
        mgp.click_guide_by_name("帮助中心")
        mgp.wait_for_guide_page_load("创建团队")
        time.sleep(5)
        mgp.click_guide_by_name("员工手册")
        mgp.wait_for_guide_page_load("常见问题")
        mgp.click_guide_by_name("应用大全")
        mgp.wait_for_guide_page_load("和飞信特色通讯套件")
        mgp.click_guide_by_name("开发者文档")
        mgp.wait_for_guide_page_load("开发者接入")
        mgp.click_back()
        # 等待管理员指引首页加载
        mgp.wait_for_page_load()
        mgp.click_back()
        # 等待工作台首页加载
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0002(self):
        """点击返回键返回上一级页面"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        # 1.进入各个指引页，点击顶部【<】
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("添加/邀请成员")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_back()
        time.sleep(1)
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_back()
        # 等待管理员指引首页加载
        mgp.wait_for_page_load()
        mgp.click_back()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0003(self):
        """点击关闭按钮返回到工作台页面"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        wbp = WorkbenchPage()
        # 1.进入各个指引页，点击顶部【X】
        mgp.click_guide_by_name("添加/邀请成员 壮大团队，提高协同办公效率")
        mgp.wait_for_guide_page_load("添加/邀请成员")
        mgp.click_close()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("快速建群 根据组织架构快速建群，方便快捷")
        mgp.wait_for_guide_page_load("快速建群")
        mgp.click_close()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("应用配置 灵活配置应用，打造专属工作台")
        mgp.wait_for_guide_page_load("应用配置")
        mgp.click_close()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("企业认证 官方认证更权威，免费获取更多权益")
        mgp.wait_for_guide_page_load("企业认证")
        mgp.click_close()
        wbp.wait_for_workbench_page_load()
        wbp.click_manager_guide()
        mgp.wait_for_page_load()
        mgp.click_guide_by_name("后台登录指引 更多管理功能，登录和飞信企业管理后台")
        mgp.wait_for_guide_page_load("后台登录指引")
        mgp.click_close()
        # 等待工作台首页加载
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0004(self):
        """断网提示"""

        # 进入管理员指引首页
        Preconditions.enter_manager_guide_page()
        mgp = ManagerGuidePage()
        # 设置手机网络断开
        mgp.set_network_status(0)
        time.sleep(2)
        mgp.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        time.sleep(2)
        mgp.click_guide_by_name("帮助中心")
        time.sleep(2)
        # 1.页面是否提示“网络出错，轻触屏幕重新加载”
        self.assertEquals(mgp.is_text_present("网络出错，轻触屏幕重新加载"), True)
        mgp.click_guide_by_name("网络出错，轻触屏幕重新加载")
        # 2.是否提示“网络不可用，请检查网络设置”
        self.assertEquals(mgp.is_toast_exist("网络不可用，请检查网络设置"), True)
        mgp.click_back()
        mgp.click_back()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @staticmethod
    def tearDown_test_QY_0004():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0005(self):
        """点击权益页面可正常打开"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 1.页面是否存在元素
        self.assertEquals(eip.is_exist_element_by_name("图标"), True)
        self.assertEquals(eip.is_exist_element_by_name("企业名称"), True)
        self.assertEquals(eip.is_exist_element_by_name("认证"), True)
        self.assertEquals(eip.is_exist_element_by_name("人数"), True)
        self.assertEquals(eip.is_exist_element_by_name("超级会议剩余时长"), True)
        self.assertEquals(eip.is_exist_element_by_name("群发信使剩余条数"), True)
        self.assertEquals(eip.is_exist_element_by_name("语音通知剩余次数"), True)
        self.assertEquals(eip.is_exist_element_by_name("增值服务"), True)
        eip.click_back()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0007(self):
        """和飞信套餐购买"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击增值服务
        eip.click_service()
        eip.wait_for_service_page_load()
        eip.click_text_by_name("和飞信套餐")
        eip.click_text_by_name("5元套餐包")
        eip.click_agree_button()
        eip.click_sure()
        time.sleep(2)
        eip.click_sure_popup()
        # 1.等待支付收银台界面加载
        eip.wait_for_pay_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0008(self):
        """和飞信套餐购买- 不勾选同意"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击增值服务
        eip.click_service()
        eip.wait_for_service_page_load()
        eip.click_text_by_name("和飞信套餐")
        eip.click_text_by_name("5元套餐包")
        eip.click_sure()
        time.sleep(2)
        # 1.是否弹出提示“请先阅读协议内容”
        self.assertEquals(eip.is_text_present("请先阅读协议内容"), True)
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0009(self):
        """和飞信套餐购买"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击增值服务
        eip.click_service()
        eip.wait_for_service_page_load()
        eip.click_text_by_name("超级会议套餐")
        time.sleep(2)
        eip.click_text_by_name("1200分钟超级会议")
        eip.click_agree_button()
        eip.click_sure()
        time.sleep(2)
        eip.click_sure_popup()
        # 1.等待支付收银台界面加载
        eip.wait_for_pay_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0010(self):
        """查看增值服务协议"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 解决工作台不稳定问题
        eip.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_rights()
        eip.wait_for_page_load()
        # 点击增值服务
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击增值服务协议
        eip.click_service_agreement()
        time.sleep(2)
        # 1.是否打开协议内容
        self.assertEquals(eip.is_text_present("欢迎您使用中国移动和飞信增值服务"), True)
        eip.click_close()
        # 等待工作台首页加载
        wbp.wait_for_workbench_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QY_0011(self):
        """历史记录查看"""

        # 进入企业权益首页
        Preconditions.enter_enterprise_interests_page()
        eip = EnterpriseInterestsPage()
        # 点击增值服务
        eip.click_service()
        eip.wait_for_service_page_load()
        # 点击购买记录
        eip.click_purchase_record()
        # 1.等待购买记录页加载
        eip.wait_for_purchase_record_page_load()
        eip.click_close()
        # 等待工作台首页加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()

