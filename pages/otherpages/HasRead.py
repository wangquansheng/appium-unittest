from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class HasRead(BasePage):
    """已读动态界面"""
    # ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'

    __locators = {
        '已读动态': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '已读未读': (MobileBy.XPATH, '//android.view.View[@resource-id="root"]/android.view.View[1]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '已读': (MobileBy.XPATH, '//*[contains(@text,"已读")]'),
        '未读': (MobileBy.XPATH, '//*[contains(@text,"未读")]'),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待已读动态界面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["已读未读"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('已读')
    def click_has_read(self):
        """点击已读"""
        self.click_element(self.__locators['已读'])

    @TestLogger.log('未读')
    def click_has_not_read(self):
        """点击未读"""
        self.click_element(self.__locators['未读'])

    @TestLogger.log()
    def has_one_contact(self, name):
        """判断是否有此人"""
        locator = (MobileBy.XPATH, '//android.view.View[@text="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                return True
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        return False

    @TestLogger.log()
    def click_contact(self, name):
        """点击此联系人"""
        locator = (MobileBy.XPATH, '//android.view.View[@text="%s"]' % name)
        self.click_element(locator)

    @TestLogger.log()
    def click_first_contact(self):
        """点击第一个联系人"""
        locator = (MobileBy.XPATH, '//android.view.View[@resource-id="root"]/android.view.View[2]')
        if self._is_element_present(locator):
            self.click_element(locator)
        else:
            raise RuntimeError("当前没有已读联系人")

    @TestLogger.log()
    def click_first_contact2(self):
        """点击第一个联系人"""
        locator = (MobileBy.XPATH, "//android.webkit.WebView[@content-desc='已读动态']/android.view.View[2]")
        if self._is_element_present(locator):
            self.click_element(locator)
        else:
            raise RuntimeError("当前没有已读联系人")
