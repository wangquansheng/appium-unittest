from TestCase.m001_login.login import *
from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


class WorkBenchManagerTest(TestCase):
    """工作台->工作台管理"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """进入工作台管理页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_workbench_manager_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_workbench_manager_page()
            return
        wmp = WorkBenchManagerPage()
        if wmp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_workbench_manager_page()

    def default_tearDown(self):
        pass

    @tags('ALL', "CMCC", 'workbench', 'GZTGL')
    def test_GZTGL_0003(self):
        """搜索不存在的应用名称"""
        # 1、点击“工作台管理”
        # 2、点击页面“常用应用”下的“+”号
        # 3、搜索应用商城不存在的应用名称
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()
        time.sleep(1)
        wmp.click_add()
        wmp.wait_for_store_page_load()
        time.sleep(2)
        wmp.click_search_store()
        time.sleep(2)
        wmp.input_store_name("哈哈")
        time.sleep(2)
        wmp.click_search()
        time.sleep(6)
        if not wmp.is_text_present("暂无相关的应用"):
            raise AssertionError("搜索不成功")
        wmp.click_close()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'GZTGL')
    def test_GZTGL_0007(self):
        """点击顶部返回键，返回到上一级页面"""
        # 1、点击“工作台管理”应用
        # 2、点击顶部返回键【<】
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()
        time.sleep(1)
        wmp.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'GZTGL')
    def test_GZTGL_0008(self):
        """点击顶部关闭按钮返回工作台页面"""
        # 1、点击“工作台管理”应用
        # 2、点击分组后边的“+”
        # 3、进入应用商城
        # 4、点击顶部【X】
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()
        time.sleep(1)
        wmp.click_add()
        wmp.wait_for_store_page_load()
        time.sleep(2)
        wmp.click_close()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'GZTGL')
    def test_GZTGL_0009(self):
        """断网提示"""
        # 1、打开客户端
        # 2、进入工作台页面
        # 3、点击“工作台管理”图标
        # 4、断开网络
        # 5、点击其他元素
        wmp = WorkBenchManagerPage()
        wmp.wait_for_page_load()
        wmp.set_network_status(0)
        time.sleep(8)
        wmp.click_add()
        time.sleep(2)
        if not wmp.is_text_present("网络出错，轻触屏幕重新加载"):
            raise AssertionError("没有出现‘网络出错，轻触屏幕重新加载’")
        wmp.click_text("网络出错，轻触屏幕重新加载")
        if not wmp.is_toast_exist("网络不可用，请检查网络设置"):
            raise AssertionError("没有出现‘网络不可用，请检查网络设置’toast提示")

    def tearDown_test_GZTGL_0009(self):
        # 重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(8)
