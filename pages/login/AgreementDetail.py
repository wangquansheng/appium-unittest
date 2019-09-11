from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class AgreementDetailPage(BasePage):
    """软件许可及服务协议-用户确认页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.AgreementActivity'

    __locators = {
        # 'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        # 'android:id/content': (MobileBy.ID, 'android:id/content'),
        # 'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        # 'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '软件许可及服务协议': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '和飞信软件许可及服务协议': (MobileBy.ID, ''),
        '协议内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content2'),
        '不同意': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '同意': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_positive_button'),
        # 'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground')
        # 6.3.1版本元素
        '同意_631': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_positive_button'),
        '不同意_631': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_negative_button'),
        '热门问题': (MobileBy.ID, '//android.view.View[@content-desc="1、什么是实名认证？"]'),
        '和包余额': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_cash_area'),
    }

    @TestLogger.log()
    def click_agree_button(self):
        """点击同意"""
        self.click_element(self.__locators['同意'])

    @TestLogger.log()
    def is_exist_element_by_id(self,text):
        """点击同意"""
        els = self.get_elements(self.__locators[text])
        if els:
            return True
        else:
            return False

    @TestLogger.log()
    def click_agree_button_631(self):
        """点击同意（6.3.1版本）"""
        self.click_element(self.__locators['同意_631'])

    @TestLogger.log()
    def click_not_agree_button_631(self):
        """点击不同意（6.3.1版本）"""
        self.click_element(self.__locators['不同意_631'])

    @TestLogger.log()
    def click_not_agree_button(self):
        """点击不同意"""
        self.click_element(self.__locators['不同意'])

    @TestLogger.log()
    def click_hot_question(self):
        """帮助中心：热点问题"""
        self.click_element(self.__locators['热门问题'])
