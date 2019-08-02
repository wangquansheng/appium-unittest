from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeSetWefarePage(BasePage):
    """我-》福利"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.MultiLanguageSettingActivity'

    __locators = {'': (MobileBy.ID, ''),
                  '福利': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
                  '免费领取每月10G': (MobileBy.XPATH, "//*[contains(@text, '免费领取每月10G')]"),
                  '福利活动': (MobileBy.XPATH, "//*[@class='android.widget.Image']"),
                  '福利活动2': (MobileBy.XPATH, "//*[@class='android.view.View']"),
                  # 打开福利活动也
                  '每月10G订购首页': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
                  '关闭流量活动': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
                  '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_more'),
                  '转发给朋友': (MobileBy.XPATH, "//*[contains(@text, '转发给朋友')]"),
                  '在系统浏览器中打开': (MobileBy.XPATH, "//*[contains(@text, '在系统浏览器中打开')]"),
                  '复制链接': (MobileBy.XPATH, "//*[contains(@text, '复制链接')]"),
                  '刷新': (MobileBy.XPATH, "//*[contains(@text, '刷新')]"),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__locators["返回"])

    @TestLogger.log()
    def click_welfare_activities2(self):
        """点击福利活动"""
        self.click_element(self.__locators["福利活动2"])

    def click_welfare_activities(self):
        """点击福利活动"""
        self.click_element(self.__locators["福利活动"])

    @TestLogger.log()
    def click_close_welfare_activities(self):
        """点击关闭福利活动"""
        self.click_element(self.__locators["关闭流量活动"])

    @TestLogger.log()
    def click_more(self):
        """点击更多操作"""
        self.click_element(self.__locators["更多"])

    @TestLogger.log()
    def click_more_share(self):
        """点击转发给朋友"""
        self.click_element(self.__locators["转发给朋友"])

    @TestLogger.log()
    def click_open_browser(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["在系统浏览器中打开"])

    @TestLogger.log()
    def click_copy_link(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["复制链接"])

    @TestLogger.log()
    def click_refurbish(self):
        """点击在浏览器中打开"""
        self.click_element(self.__locators["刷新"])

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待设置语言页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['福利'])
            )
        except:
            message = "我的福利：{}s内没有加载完毕，或者没有包含文本：设置语言".format(timeout)
            raise AssertionError(
                message
            )
        return self

    def wait_for_page_load_welfare_activities(self, timeout=20, auto_accept_alerts=True):
        """等待设置语言页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['每月10G订购首页'])
            )
        except:
            message = "我的福利：{}s内没有加载完毕，或者没有包含文本：设置语言".format(timeout)
            raise AssertionError(
                message
            )
        return self

    def wait_for_page_load_welfare_activities_open(self, timeout=20, auto_accept_alerts=True):
        """等待设置语言页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("马上领取")
            )
        except:
            message = "我的福利连接没有打开：{}s内没有加载完毕，或者没有包含文本：".format(timeout)
            raise AssertionError(
                message
            )
        return self