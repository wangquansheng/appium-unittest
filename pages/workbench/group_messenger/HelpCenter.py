from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class HelpCenterPage(BasePage):
    """群发信使->帮助中心页面"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '帮助中心': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_actionbar"),
        '应用简介': (MobileBy.XPATH, '//*[@text="应用简介"]'),
        '操作指引': (MobileBy.XPATH, '//*[@text="操作指引"]'),
        '资费说明': (MobileBy.XPATH, '//*[@text="资费说明"]'),
        '常见问题': (MobileBy.XPATH, '//*[@text="常见问题"]'),
        '应用简介页面标题': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="应用简介"]'),
        '操作指引页面标题': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="操作指引"]'),
        '资费说明页面标题': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="资费说明"]'),
        '常见问题页面标题': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_title_actionbar" and @text ="常见问题"]'),
        '返回': (MobileBy.ID, "com.chinasofti.rcs:id/btn_back_actionbar")
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待群发信使->帮助中心页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["帮助中心"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_introduction(self):
        """点击应用简介"""
        self.click_element(self.__class__.__locators["应用简介"])

    @TestLogger.log()
    def click_guide(self):
        """点击操作指引"""
        self.click_element(self.__class__.__locators["操作指引"])

    @TestLogger.log()
    def click_explain(self):
        """点击资费说明"""
        self.click_element(self.__class__.__locators["资费说明"])

    @TestLogger.log()
    def click_problem(self):
        """点击常见问题"""
        self.click_element(self.__class__.__locators["常见问题"])

    @TestLogger.log()
    def wait_for_introduction_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待帮助中心->应用简介页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["应用简介页面标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_guide_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待帮助中心->操作指引页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["操作指引页面标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_explain_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待帮助中心->资费说明页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["资费说明页面标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_problem_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待帮助中心->常见问题页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["常见问题页面标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
