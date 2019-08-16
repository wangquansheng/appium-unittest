from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class MultiPartyVideoPage(BasePage):
    """MultipartyVideoPage"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactSelectorActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '呼叫': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '灰色呼叫': (MobileBy.ID, 'com.chinasofti.rcs:id/imagebutton_choose_file_cancel'),
        '搜索或输入号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/local_contact_lv': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contact_lv'),
        'com.chinasofti.rcs:id/contact_list': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'),
        'com.chinasofti.rcs:id/local_contacts': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
        '选择和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
        '联系人item': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        'D': (MobileBy.ID, 'com.chinasofti.rcs:id/index_text'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
        '大佬1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138006': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138007': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '大佬4': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138008': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        'G': (MobileBy.ID, 'com.chinasofti.rcs:id/index_text'),
        '给个红包1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138000': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '给个红包2': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '13800138001': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '给个红包3': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '已选择成员': (MobileBy.ID, 'com.chinasofti.rcs:id/hor_contact_selection'),
        '挂断多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/end_video_call_btn'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '再次呼叫': (MobileBy.ID, 'com.chinasofti.rcs:id/call_again'),
        '一键建群': (MobileBy.ID, 'com.chinasofti.rcs:id/one_key_new_group'),
        '团队联系人图像': (MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_contactlist'),
        '团队联系人1': (MobileBy.ID, "com.chinasofti.rcs:id/tv_name_personal_contactlist"),

    }

    @TestLogger.log()
    def click_contact_head(self, index=0):
        """点击联系人头像"""
        el = self.get_elements(self.__locators["头像"])
        el[index].click()

    @TestLogger.log()
    def is_exist_contact_head(self):
        """是否存在搜索结果"""
        return self._is_element_present(self.__locators["头像"])

    @TestLogger.log()
    def is_on_multi_party_video_page(self):
        """判断当前是否在多方视频选择界面"""
        return self._is_element_present(self.__locators["多方视频"])

    @TestLogger.log()
    def is_exist_contact_selection(self):
        """判断当前是否存在已选择成员"""
        return self._is_element_present(self.__locators["已选择成员"])

    @TestLogger.log()
    def click_tv_sure(self):
        """点击呼叫"""
        self.click_element(self.__locators["呼叫"])

    @TestLogger.log()
    def input_contact_search(self, text):
        """输入电话号码并搜索"""
        self.input_text(self.__locators["搜索或输入号码"], text)

    @TestLogger.log()
    def click_end_video_call(self):
        """点击挂断多方通话"""
        self.click_element(self.__locators["挂断多方视频"])

    @TestLogger.log()
    def is_exist_end_video_call(self):
        """判断当前是否存在挂断多方通话"""
        return self._is_element_present(self.__locators["挂断多方视频"])

    @TestLogger.log()
    def click_btn_ok(self):
        """点击确定"""
        self.click_element(self.__locators["确定"])

    @TestLogger.log()
    def click_call_again(self):
        """点击再次呼叫"""
        self.click_element(self.__locators["再次呼叫"])

    @TestLogger.log()
    def click_one_key_new_group(self):
        """点击一键建群"""
        self.click_element(self.__locators["一键建群"])

    @TestLogger.log()
    def click_contact_icon(self, index=0):
        """点击联系人头像"""
        el = self.get_elements(self.__locators["联系人item"])
        print(len(el))
        if index <= len(el):
            for i in range(index):
                el[i].click()
        else:
            for i in range(len(el)):
                el[i].click()

    @TestLogger.log()
    def select_contacts_by_number(self, number):
        """根据号码选择一个联系人"""
        time.sleep(1)
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number" and @text ="%s"]' % number)
        max_try = 20
        current = 0
        while current < max_try:

            if self._is_element_present(locator):
                break
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            current += 1
        self.click_element(locator)

    @TestLogger.log()
    def select_contacts_by_name(self, name):
        """根据号码选择一个联系人"""
        time.sleep(1)
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name)
        max_try = 20
        current = 0
        while current < max_try:

            if self._is_element_present(locator):
                break
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
            current += 1
        self.click_element(locator)

    def click_select_contacts(self, index):
        """通过下标点击选择联系人"""
        elements = self.get_elements(self.__locators["联系人号码"])
        try:
            if len(elements) > 0:
                return elements[index].click()
        except:
            raise IndexError("元素超出索引")

    @TestLogger.log()
    def is_exist_back_button(self):
        """判断当前是否存在返回按钮"""
        return self._is_element_present(self.__locators["返回"])

    @TestLogger.log()
    def is_enabled_tv_sure(self):
        """判断呼叫按钮是否可用"""
        return self._is_enabled(self.__locators["灰色呼叫"])

    def get_img_icon_contactlist(self, index):
        """获取团队联系人图像Text"""
        elements = self.get_elements(self.__locators["团队联系人图像"])
        print(elements)
        try:
            if len(elements) > 0:
                return elements[index].text
        except:
            raise IndexError("元素超出索引")

    def get_contactlist_item(self):
        """获取团队联系人"""
        return len(self.get_elements(self.__locators["团队联系人图像"])) > 0


    @TestLogger.log()
    def click_img_icon_contactlist(self):
        """点击团队联系人图像"""
        self.click_element(self.__locators["团队联系人图像"])

    @TestLogger.log()
    def sure_button_is_enabled(self):
        """确定呼叫是否可点击"""
        return self._is_enabled(self.__class__.__locators["呼叫"])

    @TestLogger.log()
    def click_contact_list_item(self):
        """点击联系人"""
        self.click_element(self.__locators["联系人item"])

    @TestLogger.log()
    def click_contact_by_phone(self, phone):
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number" and @text ="%s"]' % phone)
        self.click_element(locator)

    @TestLogger.log()
    def click_end_ok(self):
        """点击联系人"""
        self.click_element(self.__locators["确定"])

    @TestLogger.log()
    def click_end_cancel(self):
        """点击联系人"""
        self.click_element(self.__locators["取消"])

    @TestLogger.log()
    def is_enabled_tv_sure(self):
        """判断呼叫按钮是否可用"""
        return self._is_enabled(self.__locators["呼叫"])
