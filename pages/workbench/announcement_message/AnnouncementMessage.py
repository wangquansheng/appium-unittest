from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AnnouncementMessagePage(BasePage):
    """公告信息页面"""
    ACTIVITY = ''

    __locators = {
        '？': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '未发公告': (MobileBy.XPATH, '//*[@text="未发公告" or @content-desc="未发公告"]'),
        '(3人)': (MobileBy.XPATH, '//*[@text="（3人）"]'),
        '公告标题输入框': (MobileBy.XPATH, '//*[@resource-id ="title"]'),
        '公告内容输入框': (MobileBy.XPATH, '//*[@resource-id ="content"]'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_right1'),
        '搜索输入框': (MobileBy.XPATH, '//*[@resource-id ="cBdTitle"]'),
        '发布': (MobileBy.XPATH, '//*[@resource-id ="publish"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定" or @content-desc="确定"]'),
        '公告标题': (MobileBy.XPATH, '//*[@resource-id ="gg_title"]'),
        '创建公告人': (MobileBy.XPATH, '//*[@resource-id ="gg_name"]'),
        '创建时间': (MobileBy.XPATH, '//*[@resource-id ="gg_time"]'),
        '浏览人数': (MobileBy.XPATH, '//*[@resource-id ="gg_traffic"]'),
        '图文发布': (MobileBy.XPATH, '//*[@text="图文发布" or @content-desc="图文发布"]'),
        '文字发布': (MobileBy.XPATH, '//*[@text="文字发布" or @content-desc="文字发布"]'),
        '链接发布': (MobileBy.XPATH, '//*[@text="链接发布" or @content-desc="链接发布"]'),
        '消息推送': (MobileBy.XPATH, '//*[@text="消息推送" or @content-desc="消息推送"]'),
        '保存': (MobileBy.XPATH, '//*[@text="保存"or @content-desc="保存"]'),
        '链接公告输入框': (MobileBy.XPATH, '//*[@resource-id ="linkUrl"]'),
        '链接公告标题输入框': (MobileBy.XPATH, '//*[@resource-id ="title_link"]'),
        '取消': (MobileBy.XPATH, '//*[@text="取消" or @content-desc="取消"]'),
        '删除': (MobileBy.XPATH, '//*[@text="删除" or @content-desc="删除"]'),
        '发布text': (MobileBy.XPATH, '//*[@text="发布" or @content-desc="发布"]'),
        '发布公告': (MobileBy.XPATH, '//*[@text="发布公告" or @content-desc="发布公告"]'),
    }

    @TestLogger.log()
    def wait_for_page_loads(self, text="公告信息", timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self.is_text_present(text),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_enter_more(self):
        """点击进入工作台"""
        self.click_element(self.__class__.__locators['？'])

    @TestLogger.log()
    def click_notice_text(self, text):
        self.click_element(self.__class__.__locators[text])

    def swipe_half_page_up(self):
        """向上滑动半页"""
        self.swipe_by_percent_on_screen(50, 80, 50, 30, 800)

    def swipe_half_page_down(self):
        """向下滑动半页"""
        self.swipe_by_percent_on_screen(50, 30, 50, 80, 800)

    @TestLogger.log()
    def click_element_(self,text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_element_(self, text,times):
        """长按元素"""
        el=self.get_element(self.__class__.__locators[text])
        self.press(el,times)

    @TestLogger.log()
    def is_element_exit(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在公告信息页"""
        el = self.get_elements(self.__class__.__locators['未发公告'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def input_title_text(self, name):
        """输入公告标题"""
        self.input_text(self.__class__.__locators["公告标题输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_content_text(self, name):
        """输入公告内容"""
        self.input_text(self.__class__.__locators["公告内容输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_search_text(self, name):
        """输入搜索内容"""
        self.input_text(self.__class__.__locators["搜索输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_link_title_text(self, name):
        """输入链接公告标题"""
        self.input_text(self.__class__.__locators["链接公告标题输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_link_content_text(self, name):
        """输入链接公告内容"""
        self.input_text(self.__class__.__locators["链接公告输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def wait_for_page_loads_not_admin(self, text="搜索", timeout=60):
        """等待 页面加载--非管理员"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators[text]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page_not_admin(self):
        """当前页面是否在公告信息页--非管理员"""
        el = self.get_elements(self.__class__.__locators['搜索'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def get_element_(self, text):
        """点击元素"""
        return self.get_element(self.__class__.__locators[text])
