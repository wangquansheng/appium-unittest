from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SingleChatSetPage(BasePage):
    """单聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.OneToOneSettingActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '聊天设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_setting_avatar'),
                  '+号': (MobileBy.ID, 'com.chinasofti.rcs:id/ivCreateGroup'),
                  'axz': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_setting_name'),
                  '消息免打扰按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_switch_undisturb'),
                  '消息免打扰': (MobileBy.XPATH, '//*[@text="消息免打扰"]'),
                  '置订聊天按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '置顶聊天': (MobileBy.XPATH, '//*[@text="置顶聊天"]'),
                  '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
                  "消息免打扰开关": (MobileBy.ID, "com.chinasofti.rcs:id/switch_undisturb"),
                  '聊天设置标题': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title" and @text ="聊天设置"]')
                  }

    @TestLogger.log()
    def click_avatar(self):
        """点击 头像"""
        self.click_element(self.__class__.__locators['头像'])

    @TestLogger.log()
    def click_add_icon(self):
        """点击 +号"""
        self.click_element(self.__class__.__locators['+号'])
        time.sleep(1)

    @TestLogger.log()
    def is_open_msg_undisturb_switch(self):
        """消息免打扰开关是否开启"""
        el = self.get_element(self.__class__.__locators['消息免打扰按钮'])
        return el.text == '开启'

    @TestLogger.log()
    def is_open_chat_set_to_top_switch(self):
        """置订聊天按钮开关是否开启"""
        el = self.get_element(self.__class__.__locators['置订聊天按钮'])
        return el.text == '开启'

    @TestLogger.log()
    def click_msg_undisturb_switch(self):
        """点击 消息免打扰按钮"""
        self.click_element(self.__class__.__locators['消息免打扰按钮'])

    @TestLogger.log()
    def click_chat_set_to_top_switch(self):
        """点击 置订聊天按钮"""
        self.click_element(self.__class__.__locators['置订聊天按钮'])

    @TestLogger.log()
    def search_chat_record(self):
        """点击 查找聊天内容"""
        self.click_element(self.__class__.__locators['查找聊天内容'])
        time.sleep(2)

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])
        time.sleep(1)

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊设置页面"""
        try:
            self.wait_until(
                timeout=5,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["聊天设置"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def get_name(self):
        """获取聊天人的人名"""
        return self.get_element(self.__class__.__locators['axz']).text

    @TestLogger.log()
    def is_selected_no_disturb(self):
        """消息免打扰是否开启"""
        return self.is_selected(self.__class__.__locators["消息免打扰开关"])

    @TestLogger.log()
    def click_no_disturb(self):
        """点击 消息免打扰开关"""
        self.click_element(self.__class__.__locators['消息免打扰开关'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待单聊设置页面加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["聊天设置标题"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self
