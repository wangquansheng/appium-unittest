import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AppStorePage(BasePage):
    """应用商城首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '搜索应用': (MobileBy.XPATH,
                 "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.widget.EditText"),
        '搜索框': (MobileBy.XPATH, '//*[@class="android.widget.EditText"]'),
        '搜索': (MobileBy.XPATH, '//*[@text="搜索"]'),
        '添加': (MobileBy.XPATH, '//*[@text="添加"]'),
        '打开': (MobileBy.XPATH, '//*[@text="打开"]'),
        '确定': (MobileBy.XPATH, '//*[@text="确定"]'),
        '热门推荐': (MobileBy.XPATH, '//*[@text="热门推荐"]'),
        '个人专区': (MobileBy.XPATH, '//*[@text="个人专区"]'),
        '添加应用': (MobileBy.XPATH, '//*[@resource-id="tjyy_but"]'),
        '应用介绍': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text="应用介绍"]'),
        'brenner图1': (MobileBy.XPATH, '	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[3]/android.view.View[1]/android.view.View'),
        'brenner图2': (MobileBy.XPATH, '	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[3]/android.view.View[2]/android.view.View'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待应用商城首页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["热门推荐"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_app_store_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在应用商城首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["热门推荐"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def click_search_app(self):
        """点击搜索应用"""
        self.click_element(self.__class__.__locators["搜索应用"])

    @TestLogger.log()
    def input_store_name(self, name):
        """输入商店应用名称"""
        self.input_text(self.__class__.__locators["搜索框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_search(self):
        """点击搜索"""
        self.click_element(self.__class__.__locators["搜索"])

    @TestLogger.log()
    def is_exist_join(self):
        """是否存在添加"""
        return self._is_element_present(self.__class__.__locators["添加"])

    @TestLogger.log()
    def click_join(self):
        """点击添加"""
        self.click_element(self.__class__.__locators["添加"])

    @TestLogger.log()
    def click_open(self):
        """点击打开"""
        self.click_element(self.__class__.__locators["打开"])

    @TestLogger.log()
    def click_add_app(self):
        """点击添加应用"""
        self.click_element(self.__class__.__locators["添加应用"])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def get_search_box_text(self):
        """获取搜索栏文本"""
        el = self.get_element(self.__class__.__locators["搜索框"])
        return el.text

    @TestLogger.log()
    def is_search_result_match(self, name):
        """搜索结果是否匹配"""
        locator = (MobileBy.XPATH, '//*[@text="添加"]/../android.view.View[2]')
        text = self.get_element(locator).text
        if name in text:
            return True
        raise AssertionError('搜索结果"{}"没有找到包含关键字"{}"的文本'.format(text, name))

    @TestLogger.log()
    def click_search_result(self):
        """点击搜索结果"""
        locator = (MobileBy.XPATH, '//*[@text="添加"]/../android.view.View[2]')
        self.click_element(locator)

    @TestLogger.log()
    def wait_for_search_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待搜索页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["搜索"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_app_details_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用介绍详情页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["应用介绍"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_app_details_page_load2(self, timeout=20, auto_accept_alerts=True):
        """等待应用介绍详情页加载----没有应用介绍---添加 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("添加")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_app_group_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待应用分组页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("添加应用")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_personal_area_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待个人专区页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("同事圈")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_personal_area(self):
        """点击个人专区"""
        self.click_element(self.__class__.__locators["个人专区"])

    @TestLogger.log()
    def add_app_by_name(self, name):
        """添加指定应用"""
        locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]/../android.view.View[1]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def get_app_button_text_by_name(self, name):
        """获取指定应用后的按钮文本"""
        locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]/../android.view.View[1]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return self.get_element(locator).text

    @TestLogger.log()
    def swipe_by_brenner1(self):
        """滑动brenner图1"""
        self.swipe_by_direction(self.__class__.__locators["brenner图1"], "left", 800)

    @TestLogger.log()
    def swipe_by_brenner2(self):
        """滑动brenner图2"""
        self.swipe_by_direction(self.__class__.__locators["brenner图2"], "right", 800)

    @TestLogger.log()
    def click_brenner(self):
        """点击brenner图"""
        self.click_element(self.__class__.__locators["brenner图1"])

    @TestLogger.log()
    def click_text_by_name(self, name):
        """点击指定文本"""
        locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            time.sleep(5)
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        # 解决滑动找不到应用问题
        time.sleep(2)
        self.swipe_by_percent_on_screen(50, 50, 50, 30, 700)
        self.click_element(locator)