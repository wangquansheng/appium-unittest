from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetManagerPage(BasePage):
    """群管理页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupManageActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '群管理': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/group_transfer': (MobileBy.ID, 'com.chinasofti.rcs:id/group_transfer'),
                  '群主管理权转让': (MobileBy.ID, 'com.chinasofti.rcs:id/group_transfer_tv'),
                  'com.chinasofti.rcs:id/group_disband': (MobileBy.ID, 'com.chinasofti.rcs:id/group_disband'),
                  '解散群': (MobileBy.ID, 'com.chinasofti.rcs:id/group_disband_tv'),
                  "确认": (MobileBy.XPATH, '//*[@text ="确定"]'),
                  "取消": (MobileBy.XPATH, '//*[@text ="取消"]'),
                  '解散': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  }

    @TestLogger.log()
    def is_on_groupSetManager_contacts_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在群管理"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["群管理"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log()
    def click_confirm(self):
        """点击确认"""
        self.click_element(self.__locators['确认'])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def click_group_disband(self):
        """点击解散群"""
        self.click_element(self.__locators['解散群'])

    @TestLogger.log()
    def click_disband(self):
        self.click_element(self.__locators['解散'])

    @TestLogger.log()
    def click_group_transfer(self):
        """点击群主管理权转让"""
        self.click_element(self.__locators['群主管理权转让'])
