from TestCase.m001_login.login import *
from pages.workbench.announcement_message.AnnouncementMessage import AnnouncementMessagePage
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


class AnnouncementMessageTest(TestCase):
    """工作台->公告信息"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """进入公告信息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page()

    @tags('ALL', 'CMCC','workbench', 'GGXX')
    def test_GGXX_0001(self):
        """检查公告信息入口是否正确"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击公告信息应用图标
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        if not amp.is_text_present("公告信息"):
            raise AssertionError("不能正常进入公告信息首页")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0002(self):
        """检查点击返回按钮控件是否正确"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击【 < 】
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(3)
        amp.click_back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0003(self):
        """检查点击关闭按钮控件【X】"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击【x】
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(3)
        amp.click_text("发布公告")
        time.sleep(2)
        amp.click_element_("X")
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0004(self):
        """管理员进入发布公告，检查初始化页面"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】初始化页面
        # 3、检查【公告信息】初始化页面
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        time.sleep(2)
        if not amp.is_text_present("向团队所有成员发出第一条公告"):
            raise AssertionError("没有出现初始化页面显示文字")
        if not amp.is_text_present("发布公告"):
            raise AssertionError("没有发布公告按钮")
        if not amp.is_text_present("公告信息"):
            raise AssertionError("没有未发公告按钮")
        time.sleep(2)
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0006(self):
        """管理员进入发布公告，公告搜索-按中文搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按中文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("哈哈")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("哈")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("哈哈"):
            raise AssertionError("搜索不成功")
        amp.click_text("哈哈")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0007(self):
        """管理员进入发布公告，公告搜索-按英文搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按英文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("hello")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("hel")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("hello"):
            raise AssertionError("搜索不成功")
        amp.click_text("hello")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0008(self):
        """管理员进入发布公告，公告搜索-按特殊字符搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按特殊字符搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha*")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("*")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha*"):
            raise AssertionError("搜索不成功")
        amp.click_text("ha*")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0009(self):
        """管理员进入发布公告，公告搜索-空格搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、带空格搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha *")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text(" *")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha *"):
            raise AssertionError("搜索不成功")
        amp.click_text("ha *")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0010(self):
        """管理员进入发布公告，公告搜索-XSS安全"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、在搜索框输入 < imgsrc = 1onmouseover = alert(1) / >
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("<img src=1 onmouseover=alert(1) />")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("未查询到公告数据"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0011(self):
        """管理员进入发布公告，公告搜索-按数字搜索"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按数字搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("6")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha6"):
            raise AssertionError("搜索不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0012(self):
        """管理员检查搜索页面元素"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、搜索到多条公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("6")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha6"):
            raise AssertionError("搜索不成功")
        if not amp.is_element_exit("公告标题"):
            raise AssertionError("没有公告标题")
        if not amp.is_element_exit("创建公告人"):
            raise AssertionError("没有创建公告人")
        if not amp.is_element_exit("创建时间"):
            raise AssertionError("没有创建时间")
        if not amp.is_element_exit("浏览人数"):
            raise AssertionError("没有浏览人数")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0013(self):
        """发布公告页面元素检查"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、检查发布公告页面是否默认选择图文方式--文字发布
        # 5、检查消息推送是否默认不推送
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        if not amp.is_element_exit("文字发布"):
            raise AssertionError("没有文字发布")
        if not amp.is_element_exit("链接发布"):
            raise AssertionError("没有链接发布")
        if not amp.is_element_exit("消息推送"):
            raise AssertionError("没有消息推送")
        if not amp.is_element_exit("保存"):
            raise AssertionError("没有保存按钮")
        if not amp.is_element_exit("发布"):
            raise AssertionError("没有发布按钮")
        if not amp.is_text_present("公告内容"):
            raise AssertionError("没有默认选择图文发布")
        current_mobile().back()
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0014(self):
        """管理员通过图文发布方式新建公告，打开消息推送"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择【图文发布】方式
        # 5、正确填写公告标题和公告内容
        # 6、开启消息推送
        # 7、点击【发布】
        # 8、点击【确定】
        # 9、验证公告信息首页历史记录是否正确
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        # 开启消息推送
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("首页显示不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0015(self):
        """管理员通过图文发布方式新建公告，关闭消息推送"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择【图文发布】方式
        # 5、正确填写公告标题和公告内容
        # 6、关闭消息推送
        # 7、点击【发布】
        # 8、点击【确定】
        # 9、验证公告信息首页历史记录是否正确
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("首页显示不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0016(self):
        """管理员通过链接发布方式新建公告，打开消息推送"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择【链接发布】方式
        # 5、正确填写公告标题和链接公告
        # 6、开启消息推送
        # 7、点击【发布】
        # 8、点击【确定】
        # 9、验证公告信息首页历史记录是否正确
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.click_element_("链接发布")
        amp.input_link_title_text("哈哈")
        amp.input_link_content_text("http://www.google.com")
        current_mobile().hide_keyboard()
        time.sleep(2)
        # 开启消息推送
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("哈哈"):
            raise AssertionError("首页显示不成功")
        amp.click_text("哈哈")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0017(self):
        """管理员通过链接发布方式新建公告，关闭消息推送"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择【链接发布】方式
        # 5、正确填写公告标题和链接公告
        # 6、关闭消息推送
        # 7、点击【发布】
        # 8、点击【确定】
        # 9、验证公告信息首页历史记录是否正确
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.click_element_("链接发布")
        amp.input_link_title_text("哈哈")
        amp.input_link_content_text("http://www.google.com")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("哈哈"):
            raise AssertionError("首页显示不成功")
        amp.click_text("哈哈")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0018(self):
        """管理员发布公告成功"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择发布方式
        # 5、正确填写页面消息
        # 6、点击【发布】按钮
        # 7、点击【确定】按钮
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("公告发布不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0019(self):
        """管理员发布公告，取消发布，不发布公告"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【发布公告】
        # 4、选择发布方式
        # 5、正确填写页面消息
        # 6、点击【发布】按钮
        # 7、点击【取消】按钮
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("取消")
        current_mobile().back()
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0020(self):
        """管理员删除未发布公告，删除成功"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【未发公告】
        # 4、选中一条未发布公告
        # 5、点击【删除】按钮
        # 6、点击【确定】按钮
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("保存")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("未发公告")
        time.sleep(2)
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_element_("删除")
        time.sleep(2)
        amp.click_element_("确定")
        time.sleep(2)
        amp.click_element_("X")
        wbp=WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0021(self):
        """管理员发布未发布公告，发布成功"""
        # 1、管理员登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、点击【未发布公告】
        # 4、选中一条未发布公告
        # 5、点击【发布】按钮
        # 6、点击【确定】按钮
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("保存")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("未发公告")
        time.sleep(2)
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_element_("发布text")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("公告发布不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0022(self):
        """验证未发公告页搜索是否正确"""
        # 1、点击右上角放大镜图标
        # 2、点击搜索栏，输入输入存在的关键字
        # 3、点击搜索
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("保存")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_element_("未发公告")
        time.sleep(2)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("ha")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha6"):
            raise AssertionError("搜索不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_element_("删除")
        time.sleep(2)
        amp.click_element_("确定")
        time.sleep(2)
        amp.click_element_("X")
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0023(self):
        """已发布公告下线"""
        # 1、点击公告列表的一条公告
        # 2、在详情界面，点击底部“下线”
        # 3、点击下线提示框弹窗“确定”
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_notice_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("首页显示不成功")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if amp.is_text_present("ha6"):
            raise AssertionError("下线公告没有消失")

    @staticmethod
    def setUp_test_GGXX_0024():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0024(self):
        """非管理员进入公告信息，检查初始空白页"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、检查公告信息初始页
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        if not amp.is_text_present("管理员还未发布任何公告"):
            raise AssertionError("初始页提示有错误")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0026():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0026(self):
        """非管理员进入发布公告，公告搜索-按中文搜索"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按中文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("哈")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("哈哈"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0027():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0027(self):
        """非管理员进入发布公告，公告搜索-按英文搜索"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按英文搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("h")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha 6"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0028():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0028(self):
        """非管理员进入发布公告，公告搜索-按特殊字符搜索"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按特殊字符搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("*")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("**"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0029():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0029(self):
        """非管理员进入发布公告，公告搜索-空格搜索"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、带空格搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text(" 6")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha 6"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0030():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0030(self):
        """非管理员-公告搜索-XSS安全"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、在搜索框输入 < imgsrc = 1onmouseover = alert(1) / >
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("<img src=1 onmouseover=alert(1) />")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("未查询到公告数据"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0031():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0031(self):
        """非管理员进入发布公告，公告搜索-按数字搜索"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、按数字搜索公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("6")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha 6"):
            raise AssertionError("搜索不成功")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @staticmethod
    def setUp_test_GGXX_0032():

        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_announcement_message_page_not_admin()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_announcement_message_page_not_admin()
            return
        amp = AnnouncementMessagePage()
        if amp.is_on_this_page_not_admin():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_announcement_message_page_not_admin()

    @tags('ALL', 'CMCC_skip', 'workbench', 'GGXX')
    def test_GGXX_0032(self):
        """非管理员进入发布公告，检查搜索页面元素"""
        # 1、普通用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、搜索到多条公告信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads_not_admin()
        time.sleep(3)
        amp.click_element_("搜索")
        time.sleep(2)
        amp.click_element_("搜索输入框")
        time.sleep(2)
        amp.input_search_text("6")
        time.sleep(3)
        amp.click_text("搜索")
        time.sleep(2)
        if not amp.is_text_present("ha 6"):
            raise AssertionError("搜索不成功")
        if not amp.is_element_exit("公告标题"):
            raise AssertionError("没有公告标题")
        if not amp.is_element_exit("创建公告人"):
            raise AssertionError("没有创建公告人")
        if not amp.is_element_exit("创建时间"):
            raise AssertionError("没有创建时间")
        if not amp.is_element_exit("浏览人数"):
            raise AssertionError("没有浏览人数")
        current_mobile().back()
        wbp = WorkbenchPage()
        wbp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0033(self):
        """检验统计浏览人数功能是否正确"""
        # 1、用户登录移动端和飞信工作台
        # 2、点击进入【公告信息】页面
        # 3、查看之后返回到列表
        # 4、查看浏览人数
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_text_present("ha6"):
            raise AssertionError("首页显示不成功")
        amp.click_text("ha6")
        amp.click_element_("返回")
        time.sleep(3)
        if not amp.get_element_("浏览人数").get_attribute("text")=="1":
            raise AssertionError("浏览人数显示不正确")
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if amp.is_text_present("ha6"):
            raise AssertionError("下线公告没有消失")

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0034(self):
        """消息首页公告信息推送入口检查"""
        # 1、用户登录移动端和飞信消息首页
        # 2、点击公告信息推送
        # 3、点击任意一条信息
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        if not amp.is_element_exit("公告标题"):
            raise AssertionError("没有公告标题")
        if not amp.is_element_exit("创建公告人"):
            raise AssertionError("没有创建公告人")
        if not amp.is_element_exit("创建时间"):
            raise AssertionError("没有创建时间")
        if not amp.is_element_exit("浏览人数"):
            raise AssertionError("没有浏览人数")
        amp.click_text("ha6")
        time.sleep(2)
        if not amp.is_text_present("你好啊"):
            raise AssertionError("页面展示不准确")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()

    @tags('ALL', 'CMCC', 'workbench', 'GGXX')
    def test_GGXX_0035(self):
        """公告消息返回控件检查"""
        # 1、用户登录移动端和飞信消息首页
        # 2、点击公告信息推送 - 点击【 < 】返回
        # 3、点击公告信息推送 - 点击任意一条信息 - 点击【 < 】返回
        amp = AnnouncementMessagePage()
        amp.wait_for_page_loads()
        amp.click_text("发布公告")
        time.sleep(2)
        amp.input_title_text("ha6")
        amp.input_content_text("你好啊")
        current_mobile().hide_keyboard()
        time.sleep(2)
        amp.click_element_("发布")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_element_("返回")
        amp.wait_for_page_loads()
        amp.click_text("ha6")
        time.sleep(2)
        amp.click_text("下线")
        time.sleep(2)
        amp.click_element_("确定")
        amp.wait_for_page_loads()



