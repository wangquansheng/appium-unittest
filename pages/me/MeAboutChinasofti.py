from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MeAboutChinasoftiPage(BasePage):
    """我-》关于和飞信"""
    ACTIVITY = 'com.chinasofti.rcs/com.cmicc.module_aboutme.ui.activity.AboutActivity'

    __locators = {
        '关于和飞信': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app'),
        '产品logo': (MobileBy.ID, 'com.chinasofti.rcs:id/logo'),
        '和飞信V6.2.8.0129 Beta': (MobileBy.ID, 'com.chinasofti.rcs:id/version'),
        '产品介绍': (MobileBy.ID, 'com.chinasofti.rcs:id/introduce_layout'),
        '新手引导': (MobileBy.ID, 'com.chinasofti.rcs:id/newer_guide_layout'),
        '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_text'),
        '检查更新': (MobileBy.ID, 'com.chinasofti.rcs:id/check_update_layout'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/about_app'),
        # 打开检查更新页面
        '抢先下载': (MobileBy.XPATH, '//*[@text = "抢先下载"]'),
        '分享': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_more'),
        # 打开新手引导页面
        '返回1': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '及时消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '即时消息': (MobileBy.XPATH, '//*[@class="android.view.View" and @text="即时消息"]'),
        '关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
        # 打开产品页面

    }

    @TestLogger.log("等待关于和飞信页面加载")
    def wait_for_page_load_about(self, timeout=8, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["产品logo"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("等待关于和飞信页面检查更新加载")
    def wait_for_page_load_update(self, timeout=8, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["分享"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("等待关于和飞信新手引导页面加载")
    def wait_for_page_new_guide(self, timeout=8, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("新手引导")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return

    @TestLogger.log()
    def click_current_msg(self):
        """点击查看进行中的事项"""
        self.click_element(self.__class__.__locators["即时消息"])

    @TestLogger.log("等待关于和飞信新手引导—及时消息页面加载")
    def wait_for_page_new_guide_details(self, timeout=8, auto_accept_alerts=True):
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators["及时消息"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('点击检查更新')
    def click_check_update(self):
        self.click_element(self.__locators["检查更新"])

    @TestLogger.log("检查该页面包含文本")
    def page_contain_text(self, menu):
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log("检查该页面包含元素")
    def page_contain_el(self, location):
        return self.page_should_contain_element(self.__locators[location])

    @TestLogger.log('点击抢先下载')
    def click_update(self):
        self.click_element(self.__locators["抢先下载"])

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators["返回"])

    @TestLogger.log('点击新手引导')
    def click_new_guide(self):
        self.click_element(self.__locators["新手引导"])

    @TestLogger.log('参与体验改善计划')
    def click_plan(self):
        self.page_up()
        self.click_element(self.__locators["参与体验改善计划"])

    @TestLogger.log('点击返回1')
    def click_back_new(self):
        self.click_element(self.__locators["返回1"])

    @TestLogger.log('点击关闭')
    def click_close(self):
        self.click_element(self.__locators["关闭"])

    @TestLogger.log('点击产品介绍')
    def click_product_introduction(self):
        self.click_element(self.__locators["产品介绍"])
