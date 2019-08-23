from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
from pages.call.Call import CallPage


class CalllogBannerPage(BasePage):
    """多方通话引导页面"""
    ACTIVITY = 'com.cmicc.module_call.ui.activity.CalllogBannerActivity'

    __locators = {
        '多方通话': (MobileBy.ID, "com.chinasofti.rcs:id/mutil_btnFreeCall"),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_arror'),
        '知道了': (MobileBy.XPATH, "//*[contains(@text, '知道了')]"),
        '搜索或输入号码': (MobileBy.ID, "com.chinasofti.rcs:id/contact_search_bar"),
        '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
        '多方电话图标': (MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"),
        '飞信电话提示': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_arror'),
        '飞信电话提示2': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_btnFreeCall'),

    }

    @TestLogger.log()
    def click_multiparty_call_by_calllogbanner(self):
        """点击多方通话"""
        self.click_element(self.__locators["多方通话"])

    @TestLogger.log()
    def click_feixin_call_tip(self):
        """飞信电话提示2"""
        self.click_element(self.__locators["飞信电话提示2"])

    @TestLogger.log()
    def is_exist_feixin_call_tip(self):
        """飞信电话提示"""
        try:
            el = self.get_element(self.__locators["飞信电话提示"])
            if el:
                return True
        except:
            return False
        return False

    @TestLogger.log()
    def click_free_call(self):
        """点击多方通话图标"""
        self.click_element(self.__locators["多方电话图标"])

    @TestLogger.log()
    def is_on_the_calllog_banner_page(self):
        """判断当前页是否在多方通话引导页"""
        time.sleep(2)
        flag = self.is_text_present("点击按钮发起电话")
        return flag

    @TestLogger.log()
    def click_i_know(self):
        """点击知道了"""
        self.click_element(self.__locators["知道了"])

    @TestLogger.log()
    def input_telephone(self, text):
        """输入电话号码"""
        self.input_text(self.__locators["搜索或输入号码"], text)

    @TestLogger.log()
    def press_contact_search_bar(self):
        """长按搜索输入框"""
        el = self.get_element(self.__locators["搜索或输入号码"])
        self.press(el)

    @TestLogger.log()
    def get_contact_search_bar_text(self):
        """获取搜索输入框text"""
        return self.get_element_attribute(self, locator=self.__locators["搜索或输入号码"], attr="text", wait_time=3)

    @TestLogger.log()
    def click_copy(self):
        """点击复制"""
        self.click_element(self.__locators["复制"])

    @TestLogger.log()
    def multiparty_call(self):
        """跳过多方通话引导页面，返回到通话菜单"""
        self.click_multiparty_call_by_calllogbanner()
        self.click_i_know()
        self.click_back()
        time.sleep(1)

    @TestLogger.log()
    def skip_multiparty_call(self):
        """跳过多方通话引导页面"""
        if self.is_on_the_calllog_banner_page():
            self.multiparty_call()
            CallPage().click_call()
            CallPage().click_call()
            # if CallPage().is_exist_allow_button():
            #     CallPage().click_allow_button(auto_accept_permission_alert=False)
        time.sleep(1)

    @TestLogger.log()
    def is_exist_contact_search_bar(self):
        """是否存在搜索或输入号码"""
        return self._is_element_present(self.__locators["搜索或输入号码"])

    @TestLogger.log("多方通话点击“我知道了”弹框")
    def click_elsfif_ikonw(self):
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        if self._is_element_present(self.__locators["知道了"]):
            self.click_element(self.__locators["知道了"])