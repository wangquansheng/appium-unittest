import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
class FooterPage(BasePage):
    """主页页脚标签栏"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
    }

    @TestLogger.log()
    def open_me_page(self):
        """切换到标签页：我"""
        self.click_element(self.__locators['我'])
        time.sleep(1)

    @TestLogger.log()
    def open_message_page(self):
        """切换到标签页：消息"""
        self.click_element(self.__locators['消息'])

    @TestLogger.log()
    def open_call_page(self):
        """切换到标签页：通话"""
        self.click_element(self.__locators['通话'])

    @TestLogger.log()
    def open_workbench_page(self):
        """切换到标签页：工作台"""
        self.click_element(self.__locators['工作台'])

    @TestLogger.log()
    def open_contacts_page(self):
        """切换到标签页：通讯录"""
        from pages.contacts.Contacts import ContactsPage

        self.click_element(self.__locators['通讯录'])
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_sim_contact()



    @TestLogger.log()
    def message_icon_is_enabled(self):
        """消息图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["消息"])

    @TestLogger.log()
    def message_icon_is_selected(self):
        """消息图标是否被选中"""
        result = self.get_element_attribute(self.__class__.__locators["消息"], "selected")
        if result.lower() == "true":
            return True
        return False

    @TestLogger.log()
    def call_icon_is_enabled(self):
        """通话图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["通话"])

    @TestLogger.log()
    def workbench_icon_is_enabled(self):
        """工作台图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["工作台"])

    @TestLogger.log()
    def contacts_icon_is_enabled(self):
        """通讯录图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["通讯录"])

    @TestLogger.log()
    def me_icon_is_enabled(self):
        """我图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["我"])

    @TestLogger.log()
    def is_exist_message_icon(self):
        """是否存在消息图标"""
        return self._is_element_present(self.__class__.__locators["消息"])

    @TestLogger.log()
    def is_exist_call_icon(self):
        """是否存在通话图标"""
        return self._is_element_present(self.__class__.__locators["通话"])

    @TestLogger.log()
    def is_exist_workbench_icon(self):
        """是否存在工作台图标"""
        return self._is_element_present(self.__class__.__locators["工作台"])

    @TestLogger.log()
    def is_exist_contacts_icon(self):
        """是否存在通讯录图标"""
        return self._is_element_present(self.__class__.__locators["通讯录"])

    @TestLogger.log()
    def is_exist_me_icon(self):
        """是否存在我图标"""
        return self._is_element_present(self.__class__.__locators["我"])
