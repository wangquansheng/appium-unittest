import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.message.Message import MessagePage
from pages.search.Search import SearchPage


class localContactPage(BasePage):
    """contacl_local"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/activity_main': (MobileBy.ID, 'com.chinasofti.rcs:id/activity_main'),
        'com.chinasofti.rcs:id/home_tag_view_pager': (MobileBy.ID, 'com.chinasofti.rcs:id/home_tag_view_pager'),
        'com.chinasofti.rcs:id/constraintLayout_home_tab': (
        MobileBy.ID, 'com.chinasofti.rcs:id/constraintLayout_home_tab'),
        'com.chinasofti.rcs:id/viewPager': (MobileBy.ID, 'com.chinasofti.rcs:id/viewPager'),
        'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        'com.chinasofti.rcs:id/action_add': (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        'com.chinasofti.rcs:id/rv_conv_list': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_conv_list'),
        '搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/et_search'),
        '搜索2': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query01'),
        'com.chinasofti.rcs:id/rl_conv_list_item': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_top': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_top'),
        '给个红包1': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '星期五': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        'com.chinasofti.rcs:id/ll_bottom': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_bottom'),
        '[名片]': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'com.chinasofti.rcs:id/rl_conv_list_item656df904-3eee-43f2-a460-1bd24aad3596': (
        MobileBy.ID, 'com.chinasofti.rcs:id/rl_conv_list_item'),
        'com.chinasofti.rcs:id/svd_head3191e8b6-7a2f-437b-bbb2-99e7c4d470c5': (
        MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
        'com.chinasofti.rcs:id/ll_topcc8ef4f4-f913-4d63-8a05-623378be2cc1': (
        MobileBy.ID, 'com.chinasofti.rcs:id/ll_top'),
        '和飞信团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
        '星期五0c025608-c338-4a33-b2ad-7ec913a9496a': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        'com.chinasofti.rcs:id/ll_bottomf2fc45ad-d791-42a3-b29d-6eb9e6c88a40': (
        MobileBy.ID, 'com.chinasofti.rcs:id/ll_bottom'),
        'Hi，你好！欢迎使用和飞信！如‥': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
        'com.chinasofti.rcs:id/ll_unread': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_unread'),
        'com.chinasofti.rcs:id/rnMessageBadge': (MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        'com.chinasofti.rcs:id/viewLine': (MobileBy.ID, 'com.chinasofti.rcs:id/viewLine'),
        'com.chinasofti.rcs:id/view_bg_home_tab': (MobileBy.ID, 'com.chinasofti.rcs:id/view_bg_home_tab'),
        '消息2d55f4e2-9bbc-4537-ae5f-e07252b94d2f': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMessage'),
        'com.chinasofti.rcs:id/rnMessageBadge4a9f8e62-ef21-4a37-b28b-b31a82d4c6a4': (
        MobileBy.ID, 'com.chinasofti.rcs:id/rnMessageBadge'),
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '工作台': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCircle'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tvMe'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        '联系人头像':(MobileBy.ID,'com.chinasofti.rcs:id/iv_head'),
        "联系人名字":(MobileBy.ID,'com.chinasofti.rcs:id/tv_name'),
        "联系人电话":(MobileBy.ID,'com.chinasofti.rcs:id/tv_phone'),
        "删除":(MobileBy.ID,'com.chinasofti.rcs:id/iv_delect01'),
        "无该本地联系人":(MobileBy.ID,"com.chinasofti.rcs:id/no_result_tip"),
        '显示SIM卡联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_show_sim_contact'),
        "开关按钮":(MobileBy.ID,"com.chinasofti.rcs:id/switch_show_sim_contact"),
        "联系人ID":(MobileBy.ID,"com.chinasofti.rcs:id/tv_name"),
        "短信按钮": (MobileBy.ID, "com.chinasofti.rcs:id/tv_normal_message"),
        "同意按钮": (MobileBy.ID, "com.chinasofti.rcs:id/btn_check"),
        "确定按钮": (MobileBy.ID, "com.chinasofti.rcs:id/dialog_btn_ok"),
        "信息编辑": (MobileBy.ID, "com.chinasofti.rcs:id/et_message"),
        "dalao4": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_name'),
        "信息发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_send"),
        "aaa":(MobileBy.XPATH,"//*[@text='aaa']"),
        "ccc":(MobileBy.XPATH,"//*[@text='ccc']"),
        "SIM_联系人": (MobileBy.ID, "com.chinasofti.rcs:id/iv_sim"),



    }
    @TestLogger.log("点击新信息")
    def click_new_message(self,text='aaa'):
        self.click_element(self.__locators[text],default_timeout=30)

    @TestLogger.log("点击某控件")
    def click_element_button(self,text='删除'):
        time.sleep(1)
        flag=self.get_elements(self.__locators[text])
        if flag:
            self.click_element(self.__locators[text])
            time.sleep(1)

    @TestLogger.log("输入内容")
    def click_input_button(self, text='信息编辑',text2='aaa'):
        time.sleep(1)
        self.input_text(self.__locators[text],text2)

    @TestLogger.log("点击新信息")
    def get_input_box_text(self):
        return self.get_text(self.__class__.__locators['搜索2'])

    @TestLogger.log("开启或关闭")
    def swich_sim_contact(self,flag=True):
        time.sleep(1)
        bool=self.is_selected(self.__locators["开关按钮"])
        if not bool and flag:
            # 打开
            self.click_element(self.__locators["开关按钮"])
        elif bool and  not flag:
            # 关闭
            self.click_element(self.__locators["开关按钮"])
        else:
            print(bool)
            print("找不到开关")

    @TestLogger.log("删除按钮")
    def click_delete_button(self):
        time.sleep(1)
        self.click_element(self.__locators["删除"])
        time.sleep(1)

    @TestLogger.log("获取元素个数")
    def get_element_number(self, text="联系人头像"):
        return  self.get_elements(self.__locators[text])

    @TestLogger.log("获取所有联系人名")
    def get_contacts_name(self):
        """获取所有联系人名"""
        max_try = 8
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["联系人名字"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["联系人名字"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        else:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        if "和通讯录" in contacts_name:
            contacts_name.remove("和通讯录")
        if "和飞信电话" in contacts_name:
            contacts_name.remove("和飞信电话")
        if "本机" in contacts_name:
            contacts_name.remove("本机")
        return contacts_name

    @TestLogger.log("点击搜索框")
    def click_search_box(self):
        time.sleep(1)
        self.click_element(self.__locators['搜索'])

    @TestLogger.log("输入搜索内容")
    def input_search_text(self, text='676560'):
        time.sleep(1)
        self.input_text(self.__locators['搜索2'], text)

    @TestLogger.log("查看控件是否存在")
    def page_contain_element(self,text='联系人头像'):
        time.sleep(1)
        self.page_should_contain_element(self.__locators[text])

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log("长按")
    def press_mess(self, mess):
        """长按消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)

    @TestLogger.log("发送短信")
    def send_message(self,contact='xk',text='aaa'):
        message_page = MessagePage()
        message_page.click_search()
        search_page = SearchPage()
        lcontact = localContactPage()
        search_key = contact
        search_page.input_search_keyword(search_key)
        search_page.hide_keyboard_if_display()
        time.sleep(0.5)
        lcontact.click_element_button("联系人ID")
        time.sleep(0.5)
        lcontact.click_element_button("短信按钮")
        time.sleep(0.5)
        lcontact.click_element_button("同意按钮")
        time.sleep(0.5)
        lcontact.click_element_button("确定按钮")
        time.sleep(0.5)
        lcontact.click_element_button("信息编辑")
        time.sleep(0.5)
        lcontact.click_input_button(text2=text)
        time.sleep(0.5)
        lcontact.click_element_button("信息发送按钮")
        time.sleep(1)

    @TestLogger.log("查看关键字是否存在")
    def check_keyword_if_exist(self,text="xiaowen"):
        mark=10
        while mark>0:
            if self.is_text_present(text=text):
                return True
            else:
                self.page_up()
                mark-=1
        return False

    @TestLogger.log()
    def get_all_contacts_name(self):
        """获取所有的联系人名字"""
        return self.get_elements(self.__class__.__locators["联系人名字"])

    @TestLogger.log()
    def get_all_contacts_head(self):
        """获取所有的联系人头像"""
        return self.get_elements(self.__class__.__locators['联系人头像'])

    @TestLogger.log()
    def get_all_contacts_number(self):
        """获取所有的联系人电话"""
        return self.get_elements(self.__class__.__locators['联系人电话'])
