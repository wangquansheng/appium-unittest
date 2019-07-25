import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CreateGroupPage(BasePage):
    """创建群首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '创建群标题': (MobileBy.ID, "com.chinasofti.rcs:id/tv_title_actionbar"),
        '马上创建群': (MobileBy.XPATH, '//*[@text="马上创建群" or @content-desc="马上创建群"]'),
        '群名输入框': (MobileBy.XPATH, '//*[@resource-id="gp_name"]'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '发起群聊': (MobileBy.XPATH, '//*[@text="发起群聊" or @content-desc="发起群聊"]'),
        '群名输入框2': (MobileBy.ID, 'com.chinasofti.rcs:id/et_group_name'),
    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待创建群首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["马上创建群"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_create_group(self):
        """点击马上创建群"""
        self.click_element(self.__class__.__locators["马上创建群"])

    @TestLogger.log()
    def input_group_name(self, name):
        """输入企业群名称"""
        self.input_text(self.__class__.__locators["群名输入框"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_group_name2(self, name):
        """输入企业群名称"""
        self.input_text(self.__class__.__locators["群名输入框2"], name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_initiate_group_chat(self):
        """点击发起群聊"""
        self.click_element(self.__class__.__locators["发起群聊"])


