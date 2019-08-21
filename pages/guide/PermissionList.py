import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PermissionListPage(BasePage):
    """权限列表页（引导页结束后会进入该页面）"""

    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.PermissionListActivity'

    __locators = {
        "确定": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_submit'),
        "不再提示已关闭权限": (MobileBy.ID, 'com.android.packageinstaller:id/do_not_ask_checkbox'),
        "和飞信权限管理-确定": (MobileBy.ID, 'android:id/button1'),
        "去授权": (MobileBy.XPATH, '//*[@text="去授权"]'),
    }

    @TestLogger.log()
    def click_submit_button(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def go_permission(self):
        """点击去授权"""
        self.click_element(self.__class__.__locators["去授权"])
        time.sleep(1)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待权限列表页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["确定"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_permission_button(self):
        """点击取消不再提示已关闭权限"""
        if self.is_text_present("和飞信权限管理"):
            el = self.get_element(self.__locators['不再提示已关闭权限'])
            if el.get_attribute("checked") == "true":
                time.sleep(3)
                self.click_text("不再提示已关闭权限")
                time.sleep(5)
                self.click_text("确定")

