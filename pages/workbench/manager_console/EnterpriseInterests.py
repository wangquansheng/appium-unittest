import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class EnterpriseInterestsPage(BasePage):
    """企业权益页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '企业权益': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        '图标': (MobileBy.XPATH, '//*[@resource-id="cp_logo"]'),
        '企业名称': (MobileBy.XPATH, '//*[@resource-id="cp_name"]'),
        '认证': (MobileBy.XPATH, '//*[@resource-id="qyrz_logo_span"]'),
        '人数': (MobileBy.XPATH, '//*[@resource-id="userCount"]'),
        '超级会议剩余时长': (MobileBy.XPATH, '//*[@resource-id="smCPRemaining"]'),
        '群发信使剩余条数': (MobileBy.XPATH, '//*[@resource-id="gsCPRemaining"]'),
        '语音通知剩余次数': (MobileBy.XPATH, '//*[@resource-id="mnCPRemaining"]'),
        '增值服务': (MobileBy.XPATH, '//*[@resource-id="hfxServiceAddSpanId"]'),
        '增值服务协议': (MobileBy.XPATH, '//*[@text="《增值服务协议》"]'),
        '确认': (MobileBy.XPATH, '//*[@text="确 认"]'),
        '确认弹窗': (MobileBy.XPATH, '//*[@text="确认"]'),
        '支付收银台': (MobileBy.XPATH, '//*[@text="支付收银台"]'),
        '购买记录': (MobileBy.XPATH, '//*[@text="购买记录"]'),
        '同意协议按钮': (MobileBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[13]/android.view.View[1]/android.view.View[1]'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待企业权益页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["企业名称"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_close(self):
        """点击关闭"""
        self.click_element(self.__class__.__locators["关闭"])

    @TestLogger.log()
    def is_exist_element_by_name(self, name):
        """是否存在元素"""
        return self._is_element_present(self.__class__.__locators[name])

    @TestLogger.log()
    def click_service(self):
        """点击增值服务"""
        self.click_element(self.__class__.__locators["增值服务"])

    @TestLogger.log()
    def click_service_agreement(self):
        """点击增值服务协议"""
        self.click_element(self.__class__.__locators["增值服务协议"])

    @TestLogger.log()
    def click_agree_button(self):
        """点击同意协议按钮"""
        self.click_element(self.__class__.__locators["同意协议按钮"])

    @TestLogger.log()
    def click_sure(self):
        """点击确认"""
        self.click_element(self.__class__.__locators["确认"])

    @TestLogger.log()
    def click_sure_popup(self):
        """点击确认弹窗"""
        self.click_element(self.__class__.__locators["确认弹窗"])

    @TestLogger.log()
    def click_purchase_record(self):
        """点击购买记录"""
        self.click_element(self.__class__.__locators["购买记录"])

    @TestLogger.log()
    def wait_for_service_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待增值服务页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("同意为该企业购买，已阅读并确认")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_purchase_record_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待购买记录页加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("返回工作台")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_pay_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待支付收银台界面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["支付收银台"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_text_by_name(self, name):
        """点击指定文本"""
        locator = (MobileBy.XPATH, '//*[@text="%s"]' % name)
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

