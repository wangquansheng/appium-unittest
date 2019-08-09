import traceback

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupChatSetSeeMembersPage(BasePage):
    """查看群成员页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '群成员列表页返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '群成员': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/top_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/top_layout'),
                  'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
                  '搜索群成员': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  '还有人未进群,再次邀请': (MobileBy.XPATH, '//*[@text ="还有人未进群,再次邀请"]'),
                  'com.chinasofti.rcs:id/bottom_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottom_layout'),
                  'com.chinasofti.rcs:id/contact_selection_list_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
                  'com.chinasofti.rcs:id/contact_list': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
                  'com.chinasofti.rcs:id/contact_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
                  'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
                  'M': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/contact_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
                  '成员名字': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'X': (MobileBy.ID, ''),
                  'xzq': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
                  'com.chinasofti.rcs:id/contact_index_bar_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_view'),
                  'com.chinasofti.rcs:id/contact_index_bar_container': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),
                  '再次邀请': (MobileBy.XPATH,  '//*[@text ="再次邀请"]'),
                  '邀请返回>': (MobileBy.ID,  'com.chinasofti.rcs:id/left_back'),
                  '邀请人员': (MobileBy.ID,  'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '邀请人员名字': (MobileBy.ID,  'com.chinasofti.rcs:id/phone'),
                  # 成员简介页 'com.cmicc.module_aboutme.ui.activity.UserProfileShowActivity'
                  'profile返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'profile返回2': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '个人名字': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),
                  '电话': (MobileBy.XPATH,  '//*[@text ="电话"]'),
                  '公司': (MobileBy.XPATH, '//*[@text ="公司"]'),
                  '职位': (MobileBy.XPATH,  '//*[@text ="职位"]'),
                  }

    @TestLogger.log()
    def search(self, text):
        """搜索群成员"""
        self.input_text(self.__class__.__locators["搜索群成员"], text)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_back(self):
        """群成员列表页返回"""
        self.click_element(self.__class__.__locators["群成员列表页返回"])

    @TestLogger.log()
    def get_all_group_member_names(self):
        """获取所有群成员名字"""
        names = []
        els = self.get_elements(self.__class__.__locators['成员名字'])
        if els:
            for el in els:
                names.append(el.text)
        return names

    @TestLogger.log()
    def click_group_member(self):
        """点击群成员列表中的成员"""
        self.click_element(self.__class__.__locators['成员名字'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待查看群成员页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("群成员")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_invite_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待邀请人员页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("邀请人员")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_profile_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待个人profile页页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("编辑")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def profile_back(self):
        """profile页点击返回"""
        try:
            self.click_element(self.__class__.__locators["profile返回"])
        except:
            self.click_element(self.__class__.__locators["profile返回2"])


    @TestLogger.log()
    def click_invite_prompt(self):
        """点击邀请提示"""
        self.click_element(self.__class__.__locators["还有人未进群,再次邀请"])

    @TestLogger.log()
    def click_again_invite(self):
        """点击再次邀请"""
        self.click_element(self.__class__.__locators["再次邀请"])

    @TestLogger.log()
    def invite_back(self):
        """点击邀请返回>"""
        self.click_element(self.__class__.__locators["邀请返回>"])

    @TestLogger.log()
    def is_others_not_in_group(self, timeout=5, auto_accept_alerts=True):
        """是否还有人未进群"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["还有人未进群,再次邀请"])
            )
            return True
        except Exception:
            traceback.print_exc()
            return False

