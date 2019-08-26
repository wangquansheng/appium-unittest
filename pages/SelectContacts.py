from appium.webdriver.common.mobileby import MobileBy
import re
import copy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time

from pages.groupset.GroupChatSetPicVideo import GroupChatSetPicVideoPage
from pages.message.Message import MessagePage
from pages.GroupChat import GroupChatPage

class SelectContactsPage(BasePage):
    """选择联系人页面"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactSelectorActivity'

    __locators = {
        '无搜索结果':(MobileBy.ID, 'com.chinasofti.rcs:id/no_contact_text'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
        'com.chinasofti.rcs:id/top_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/top_layout'),
        'com.chinasofti.rcs:id/layout_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_search'),
        '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        'com.chinasofti.rcs:id/bottom_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/bottom_layout'),
        'com.chinasofti.rcs:id/recyclerView_recently_person': (
            MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView_recently_person'),
        'com.chinasofti.rcs:id/local_contacts': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
        '选择一个群': (MobileBy.XPATH, '//*[@text ="选择一个群"]'),
        'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
        '本地联系人': (MobileBy.XPATH, '//*[@text ="选择手机联系人"]'),
        '选择和通讯录联系人': (MobileBy.XPATH, '//*[@text ="选择团队联系人"]'),
        '最近聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'),
        'X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '聊天电话': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        '最近聊天联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/item_rl'),
        # 分享二维码的选择联系人页面
        '选择手机联系人': (MobileBy.XPATH, '//*[@text ="选择手机联系人"]'),
        'tel:+86': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_number"]'),
        '群聊页面设置图标': (MobileBy.ID, 'com.chinasofti.rcs:id/coin_img'),
        # 未知号码
        '未知号码': (MobileBy.XPATH, '//*[contains(@text,"未知号码")]'),
        # 选择一个联系人转发消息时的弹框
        '发送给': (MobileBy.XPATH, "//*[contains(@text, '发送给')]"),
        '取消转发': (MobileBy.XPATH, "//*[contains(@text, '取消')]"),
        '确定转发': (MobileBy.XPATH, "//*[contains(@text, '确定')]"),
        'local联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '分享名片': (MobileBy.ID, 'com.chinasofti.rcs:id/send_tv'),
        '发送名片': (MobileBy.ID,'com.chinasofti.rcs:id/send_tv'),
        '联系人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        '右侧字母索引': (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/android.widget.TextView'),
        '左侧字母索引': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/index_text"]'),
        '查看更多': (MobileBy.XPATH, '//*[@text ="查看更多"]'),
        '和通讯录返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back'),
        "最近聊天消息名称": (MobileBy.ID, "com.chinasofti.rcs:id/tv_name"),
        "联系人横框": (MobileBy.ID, "com.chinasofti.rcs:id/contact_list_item"),
        "搜索框左边选中联系人": (MobileBy.ID, "com.chinasofti.rcs:id/image"),
       # 'aaa':(MobileBy.XPATH,"*[@text='aaa']"),
        'aaa':(MobileBy.ID,'com.chinasofti.rcs:id/contact_name'),

        "搜索群组":(MobileBy.ID,'com.chinasofti.rcs:id/et_search'),
        "搜索1":(MobileBy.ID,'com.chinasofti.rcs:id/edit_query'),
        "选择团队联系人":(MobileBy.XPATH,"//*[@text='选择团队联系人']"),
        # "选择手机联系人": (MobileBy.XPATH, "//*[@text='选择手机联系人']"),
        "中软国际科技服务有限公司": (MobileBy.XPATH, "//*[@text='中软国际科技服务有限公司']"),
        "选择联系人列表":(MobileBy.ID,'com.chinasofti.rcs:id/textview_action_bar_title'),
        "分组名":(MobileBy.ID,'com.chinasofti.rcs:id/img_icon_department'),
        "成员ID":(MobileBy.ID, 'com.chinasofti.rcs:id/img_icon_contactlist'),
        "我已阅读": (MobileBy.ID,'com.chinasofti.rcs:id/btn_check'),
        # "确定": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        "确定2": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        "确定3": (MobileBy.ID,'com.chinasofti.rcs:id/dialog_btn_ok'),
        "最近聊天联系人":(MobileBy.ID,'com.chinasofti.rcs:id/iv_photo'),
        "群二维码":(MobileBy.ID,'com.chinasofti.rcs:id/imageview_msg_image'),
        "保存图片":(MobileBy.XPATH,'//*[@text="保存图片"]'),
        "识别图中二维码": (MobileBy.XPATH, '//*[@text="识别图中二维码"]'),
        "转发": (MobileBy.XPATH, '//*[@text="转发"]'),
        "企业通讯录联系人": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),
        "搜索3":(MobileBy.ID,'com.chinasofti.rcs:id/search_edit'),
        "搜索4":(MobileBy.ID,'com.chinasofti.rcs:id/edit_query01'),
        "发送人头像":(MobileBy.ID,'com.chinasofti.rcs:id/svd_head'),
        "发送时间":(MobileBy.ID,'com.chinasofti.rcs:id/tv_time'),
        "选中联系人头像":(MobileBy.ID,'com.chinasofti.rcs:id/contact_icon'),

        '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        'A':(MobileBy.XPATH,'//*[@text ="A"]'),
        'K': (MobileBy.XPATH, '//*[@text ="K"]'),
        "字母栏":(MobileBy.ID,'	com.chinasofti.rcs:id/contact_index_bar_container'),
        'bm1': (MobileBy.XPATH, "//*[contains(@text, 'bm1')]"),
        'bm2': (MobileBy.XPATH, "//*[contains(@text, 'bm2')]"),
        "联系人姓名": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
        "部门名称": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_department'),
        "禁止": (MobileBy.ID, 'com.android.packageinstaller:id/permission_deny_button'),
        "联系人栏": (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        "企业名称": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        "查看更多2": (MobileBy.ID, 'com.chinasofti.rcs:id/show_more_text'),

    }

    @TestLogger.log("")
    def click_search_result_by_name(self, name):
        """根据名称点击搜索联系人结果"""
        els = self.get_elements(self.__class__.__locators["联系人横框"])
        if els:
            for ele in els:
                res = ele.get_elements(self.__class__.__locators["aaa"])
                if res[0].text == name:
                    self.click_element(ele)
                    return
            raise AssertionError("找不到对应的搜索结果")
        else:
            raise AssertionError("没有搜索结果")

    @TestLogger.log("")
    def click_contact_more2(self):
        """查看更多2--手机联系人-查看更多"""
        els = self.get_elements(self.__class__.__locators["查看更多2"])
        if els:
            if len(els) > 2:
                els[1].click()
        else:
            raise AssertionError("没有搜索结果")

    @TestLogger.log("")
    def get_search_result_name(self):
        """获取搜索联系人名称结果"""
        els = self.get_elements(self.__class__.__locators["aaa"])
        contacts = []
        if els:
            for el in els:
                contacts.append(el.text)
        else:
            return contacts
        flag = True
        while flag:
            self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)
            els = self.get_elements(self.__class__.__locators["aaa"])
            for el in els:
                if el.text not in contacts:
                    contacts.append(el.text)
                    flag = True
                else:
                    flag = False
        return contacts

    @TestLogger.log("")
    def get_search_result_number(self):
        """获取搜索联系人电话结果"""
        els = self.get_elements(self.__class__.__locators["聊天电话"])
        numbers = []
        if els:
            for el in els:
                numbers.append(el.text)
        else:
            return numbers
        flag = True
        while flag:
            self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)
            els = self.get_elements(self.__class__.__locators["聊天电话"])
            for el in els:
                if el.text not in numbers:
                    numbers.append(el.text)
                    flag = True
                else:
                    flag = False
        return numbers

    @TestLogger.log()
    def is_enabled_search_result(self):
        """判断搜索结果是否高亮展示"""
        els = self.get_elements(self.__class__.__locators["联系人横框"])
        if els:
            for el in els:
                if not self._is_enabled(el):
                    return False
        return True

    @TestLogger.log("点击右侧字母")
    def click_right_word(self,text='A'):
        self.click_element(self.__locators[text])

    @TestLogger.log("检查控件是否存在")
    def check_if_element_exist(self,text='发送人头像'):
        self.page_should_contain_element(self.__class__.__locators[text])

    @TestLogger.log("点击群二维码")
    def click_group_code(self, text='群二维码'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("识别图中二维码")
    def click_recognize_code(self, text='识别图中二维码'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("识别图中二维码")
    def click_recognize_code_631(self, text='识别图中二维码'):
        """点击组名"""
        time.sleep(2)
        GroupChatSetPicVideoPage().press_pre_file_to_do(text)


    @TestLogger.log("最近聊天联系人")
    def click_recent_contact(self, text='最近聊天联系人'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择团队联系人")
    def click_group_contact(self, text='选择团队联系人'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择手机联系人")
    def click_phone_contact(self, text='选择手机联系人'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择:中软国际科技服务有限公司")
    def click_group_chinasoft(self, text='中软国际科技服务有限公司'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择成员ID")
    def click_group_contact_member(self, text='成员ID'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("选择分组名")
    def click_group_contact_name(self, text='分组名'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("点击组名")
    def click_group_name(self,text='aaa'):
        """点击组名"""
        time.sleep(1)
        self.click_element(self.__locators[text])

    @TestLogger.log("点击搜索群组")
    def click_group_search(self):
        """搜索联系人"""
        self.click_element(self.__locators["搜索群组"])
        time.sleep(3)

    @TestLogger.log("搜索群组")
    def group_search(self, text='aaa'):
        """搜索联系人"""
        time.sleep(1)
        self.input_text(self.__class__.__locators["搜索1"], text)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    @TestLogger.log()
    def search(self, text):
        """搜索联系人"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], text)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

    @TestLogger.log()
    def is_present_unknown_member(self, timeout=3, auto_accept_alerts=True):
        """是否是未知号码（陌生号码）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["未知号码"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_unknown_member(self):
        """点击 未知号码（陌生号码）"""
        self.click_element(self.__class__.__locators["未知号码"])

    @TestLogger.log()
    def click_sure_forward(self):
        """点击确定转发"""
        self.click_element(self.__class__.__locators['确定转发'])

    @TestLogger.log()
    def click_cancel_forward(self):
        """点击取消转发"""
        self.click_element(self.__class__.__locators['取消转发'])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=3, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_groupchat_setting_icon(self):
        """群聊页面 点击 设置图标"""
        self.click_element(self.__class__.__locators["群聊页面设置图标"])


    @TestLogger.log()
    def click_he_back(self):
        """点击 和通讯录返回"""
        self.click_element(self.__class__.__locators["和通讯录返回"])

    @TestLogger.log('点击分享名片')
    def click_share_card(self):
        """点击分享名片"""
        self.click_element(self.__class__.__locators['发送名片'])
        time.sleep(2)

    @TestLogger.log('搜索联系人：*****')
    def click_search_local_contactst(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__locators['com.chinasofti.rcs:id/local_contacts'])

    @TestLogger.log('搜索或输入手机号')
    def click_search_contact(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__locators['搜索或输入手机号'])

    @TestLogger.log('判断键盘是否显示')
    def confrim_is_keyboard_shown(self):
        """判断键盘是否显示"""
        return self.is_keyboard_shown()

    @TestLogger.log('搜索或输入手机号')
    def input_search_keyword(self, keyword):
        """输入搜索内容"""
        self.input_text(self.__locators['搜索或输入手机号'], keyword)
        self.driver.hide_keyboard()

    @TestLogger.log()
    def click_search_keyword(self):
        """点击搜索或输入手机号"""
        self.click_element(self.__class__.__locators["搜索或输入手机号"])

    @TestLogger.log('点击联系人')
    def click_contact(self, name):
        """点击联系人"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log('是否存在名字为空的联系人')
    def is_exisit_null_contact(self, name):
        """是否存在名字为空的联系人"""
        els = self.get_elements((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name"]'))
        for i in range(len(els)):
            print("els"+ str(i) +"   = "+str(els[i].text))
            if els[i].text =="":
                return True
        print("els---------------------------")
        return False

    @TestLogger.log('获取群主名称')
    def get_contact_name(self):
        """获取群主名称"""
        els = self.get_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name"]'))
        return els.text

    def get_contact_obj(self):
        """获取群主名称"""
        els = self.get_elements((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name"]'))
        return els

    @TestLogger.log('点击联系人头像')
    def click_cantact_avatar(self):
        """点击联系人头像"""
        self.click_element(self.__locators['选中联系人头像'])

    @TestLogger.log()
    def click_select_one_group(self):
        """点击 选择一个群"""
        self.click_element(self.__class__.__locators["选择一个群"])
        time.sleep(1)

    @TestLogger.log()
    def click_he_contacts(self):
        """点击 选择和通讯录联系人/选择团队联系人"""
        self.click_element(self.__class__.__locators["选择团队联系人"])
        time.sleep(1)

    @TestLogger.log()
    def click_local_contacts(self):
        """点击 本地联系人"""
        self.click_element(self.__class__.__locators["本地联系人"])

    @TestLogger.log()
    def select_local_contacts(self):
        """选择本地联系人/选择手机联系人"""
        self.click_element(self.__class__.__locators["选择手机联系人"])
        time.sleep(1)

    @TestLogger.log()
    def click_one_local_contacts(self):
        """点击一个本地联系人"""
        # els = self.get_elements(self.__class__.__locators["local联系人"])
        # contactnames = []
        # if els:
        #     for el in els:
        #         contactnames.append(el.text)
        #     self.select_one_contact_by_name(contactnames[0])
        try:
            self.wait_until(
                condition=lambda x: self.get_elements(self.__class__.__locators["联系人列表"])[0],
                auto_accept_permission_alert=False
            ).click()
        # else:
        except:
            raise AssertionError("没有本地联系人可转发")

    @TestLogger.log()
    def select_one_contact_by_name(self, name):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def get_contact_name2(self):
        els = self.get_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name"]'))
        return els.text

    @TestLogger.log()
    def select_one_group_by_name(self, name):
        """通过群名选择一个群"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def select_one_group_by_name2(self, name):
        """通过名称选择一个联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def select_one_recently_contact_by_name(self, name):
        """通过名称选择一个最近聊天的联系人"""
        self.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text ="%s"]' % name))

    @TestLogger.log()
    def wait_for_page_local_contact_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择联系人页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def catch_message_in_page(self, text):
        return self.is_toast_exist(text)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[contains(@text, "%s")]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log()
    def input_search_contact_message(self, message):
        """输入查询联系人查询信息"""
        self.input_text(self.__class__.__locators["搜索或输入手机号"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log('检验搜索名称')
    def get_element_text_net_name(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = text + "(未知号码)"
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('检验搜索号码')
    def get_element_text_net_number(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        text = "tel: +86" + text
        return self.element_should_contain_text(self.__locators[locator], text)

    @TestLogger.log('获取元素文本内容')
    def get_element_texts(self, locator):
        text = self.get_text(self.__locators["搜索或输入手机号"])
        locator = self.get_text(self.__locators[locator])
        if text.startswith("+86"):
            text = text[3:]
        if text.startswith("+852"):
            text = text[4:]
        if text.startswith("+"):
            text = text[1:]
        if text in locator:
            return True
        return False

    @TestLogger.log('获取元素文本内容')
    def get_element_text(self, locator='选择联系人'):
        return self.get_text(self.__locators[locator])


    @TestLogger.log('判断该页面是否有元素')
    def page_contain_element(self, locator):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log('点击最近聊天')
    def click_search_he_contact(self):
        self.click_element(self.__locators["最近聊天"])

    @TestLogger.log()
    def click_x_icon(self):
        """点击 X"""
        self.click_element(self.__class__.__locators["X"])

    @TestLogger.log()
    def click_read_more(self):
        """点击查看更多"""
        self.click_element(self.__class__.__locators["查看更多"])

    @TestLogger.log()
    def wait_for_create_msg_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待 '消息页面 点击+ ->新建消息->选择联系人页面' 加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log()
    def is_left_letters_sorted(self):
        """左侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['左侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        # 过滤特殊字符
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def is_right_letters_sorted(self):
        """右侧字母是否顺序排序"""
        els = self.get_elements(self.__locators['右侧字母索引'])
        letters = []
        for el in els:
            letters.append(el.text)
        for item in letters:
            if not re.match(r'[A-Za-z]', item):
                letters.remove(item)
        arrs = copy.deepcopy(letters)
        letters = sorted(letters)
        return arrs == letters

    @TestLogger.log()
    def select_recent_chat_by_name(self, name):
        """根据名字选择某一条最近聊天记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="%s"]' % name)
        if self._is_element_present(locator):
            self.click_element(locator)

    @TestLogger.log()
    def is_exists_recent_chat_by_name(self, name):
        """是否存在指定最近聊天记录"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def select_recent_chat_by_number(self, number):
        """选择某一条最近聊天记录"""
        if self._is_element_present(self.__class__.__locators["最近聊天消息名称"]):
            els = self.get_elements(self.__class__.__locators["最近聊天消息名称"])
            els[number].click()

    @TestLogger.log()
    def is_page_more_text(self, menu):
        """选择某一条最近聊天记录"""
        for text in menu:
            self.is_text_present(text)
        return True

    @TestLogger.log()
    def click_sure_bottom(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_clear_record_sure(self):
        """是否清空聊天记录？ 点击 确定2"""
        self.click_element(self.__class__.__locators['确定2'])

    @TestLogger.log()
    def sure_icon_is_checkable(self):
        """确定按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['确定'])

    @TestLogger.log()
    def result_is_more_tree(self):
        """点击确定"""
        els = self.get_elements(self.__class__.__locators["local联系人"])
        if len(els) > 3:
            return True
        else:
            return False

    @TestLogger.log()
    def is_exsit_group_member(self):
        """群聊联系人成员数量 True:没有 False:存在群成员"""
        els = self.get_elements(self.__class__.__locators["local联系人"])
        if len(els) == 0:
            return True
        else:
            return False

    @TestLogger.log()
    def is_element_present_by_locator(self,text):
        """判断指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def swipe_and_find_element(self, text):
        """滑动并查找特定元素"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % text))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log("创建群")
    def create_message_group(self,text='aaa'):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
            time.sleep(3)
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        mess.click_text("大佬2")
        time.sleep(1)
        mess.click_text("大佬3")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=text)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("选择多个联系人")
    def create_multi_contacts_group(self,groupname='aaa',num=1,times=1):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
            time.sleep(3)
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        while times>0:
            self.page_up()
            els=self.get_elements(self.__locators['aaa'])
            if els is None:
                break
            for i in range(num):
               time.sleep(1)
               els[i].click()
            times-=1
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=groupname)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("选择团队联系人")
    def select_group_contacts(self, groupname='aaa', num=1, times=1):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)
        from pages.groupset.GroupChatSet import GroupChatSetPage
        if self.get_elements(self.__locators['aaa']):
            self.click_element(self.__locators['aaa'])
            time.sleep(1)
            gcp = GroupChatPage()
            group_set = GroupChatSetPage()
            time.sleep(1)
            gcp.click_setting()
            time.sleep(1)
            sc.page_up()
            time.sleep(1)
            group_set.click_delete_and_exit()
        else:
            self.click_back_by_android()
        # mess.click_create_group()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        mess.click_contact_group()
        while times > 0:
            self.page_up()
            els = self.get_elements(self.__locators['aaa'])
            if els is None:
                break
            for i in range(num):
                time.sleep(1)
                els[i].click()
            times -= 1
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=groupname)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log()
    def press_and_move_right(self):
        """元素内向右滑动"""
        self.swipe_by_direction(self.__class__.__locators["搜索或输入手机号"], "right")

    @TestLogger.log()
    def get_firm_contacts_name_list(self):
        """获取企业通讯录联系人名"""
        els = self.get_elements(self.__class__.__locators["企业通讯录联系人"])
        contacts_name = []
        if els:
            for el in els:
                contacts_name.append(el.text)
        return contacts_name

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])


    @TestLogger.log("删除自建群")
    def del_message_group(self):
        flag=True
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        # 删除原来的群
        while flag:
            mess.click_add_icon()
            # 点击 发起群聊
            mess.click_group_chat()
            # 选择联系人界面，选择一个群
            sc = SelectContactsPage()
            sc.click_select_one_group()
            time.sleep(1)
            from pages.groupset.GroupChatSet import GroupChatSetPage
            if self.get_elements(self.__locators['aaa']):
                self.click_element(self.__locators['aaa'])
                time.sleep(1)
                gcp = GroupChatPage()
                group_set = GroupChatSetPage()
                time.sleep(1)
                gcp.click_setting()
                time.sleep(1)
                sc.page_up()
                time.sleep(1)
                group_set.click_delete_and_exit()
                time.sleep(3)
            else:
                self.click_back_by_android()
                break

    @TestLogger.log("创建群,选择手机联系人")
    def create_message_group2(self,text='aaa'):
        time.sleep(2)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        #删除原来的群
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        time.sleep(1)
        mess.click_contact_group()
        mess.click_text("大佬2")
        time.sleep(1)
        mess.click_text("大佬3")
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)
        mess.click_group_name()
        time.sleep(1)
        mess.set_group_name(text=text)
        time.sleep(1)
        mess.click_sure_button()
        time.sleep(1)

    @TestLogger.log("当前页面是否在选择联系人页")
    def is_on_this_page(self):
        bol = self.wait_until(
            condition=lambda d: self._is_element_present(self.__class__.__locators["选择一个群"])
        )
        return bol

    @TestLogger.log("通过索引选择最近联系人最近聊天")
    def select_recent_chat_by_number(self, num):
        elements_list = self.get_elements(('id', 'com.chinasofti.rcs:id/item_rl'))
        elements_list[num].click()

    @TestLogger.log()
    def get_element_(self, text):
        """点击元素"""
        return self.get_element(self.__class__.__locators[text])

    @TestLogger.log("获取所有联系人名")
    def get_contacts_name(self):
        """获取所有联系人名"""
        max_try = 5
        current = 0
        while current < max_try:
            if self._is_element_present(self.__class__.__locators["local联系人"]):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        els = self.get_elements(self.__class__.__locators["local联系人"])
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

    @TestLogger.log("点击所有联系人名")
    def click_all_contacts(self):
        """"""

    @TestLogger.log('通过名字点击联系人')
    def click_contact_by_name(self, name):
        """点击联系人"""
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                            '@text="{}"]'.format(name)))

    @TestLogger.log('清空搜索框')
    def clear_serchbar_keyword(self):
        self.click_element(self.__locators['X'])

    @TestLogger.log()
    def selecting_contacts_by_name(self, name):
        """根据名字选择一个团队联系人"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and contains(@text,"%s")]' % name)
        time.sleep(2)
        max_try = 20
        current = 0
        while current < max_try:
            if self._is_element_present(locator):
                break
            current += 1
            self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        self.click_element(locator)

    @TestLogger.log()
    def is_on_select_contact_page(self):
        """当前页面是否在选择联系人页面"""
        el = self.get_elements(self.__locators['选择手机联系人'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log("全部导入成功")
    def catch_message_in_page(self):
        """全部导入成功"""
        return self.is_toast_exist("全部导入成功")

    @TestLogger.log("检查输入搜索内容后是否存在搜索团队联系人标签")
    def search_team_contact_message_is_exsit(self, username):
        """检查输入搜索内容后是否存在搜索团队联系人标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='搜索团队联系人 : %s']" % username
        print(tmp_path)
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        print(len(els))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("点击进入搜索团队联系人标签")
    def click_search_team_contact_message(self, username):
        """点击进入搜索团队联系人标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='搜索团队联系人 : %s']" % username
        self.click_element((MobileBy.XPATH, tmp_path))

    @TestLogger.log("点击进入团队联系人的搜索结果中")
    def click_search_the_contact_in_team(self):
        """点击进入团队联系人的搜索结果中"""
        tmp_path = "//android.widget.TextView[@resource-id='com.chinasofti.rcs:id/tv_name_personal_contactlist']"
        self.click_element((MobileBy.XPATH, tmp_path))

    @TestLogger.log("查看是否存在搜索结果")
    def search_contact_is_exsit_in_team(self):
        """查看是否存在搜索结果"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/tv_name_personal_contactlist']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("查看是否存在搜索结果")
    def search_contact_is_exsit(self):
        """查看是否存在搜索结果"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/contact_name']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("查看是否存在搜索结果,并点击进入")
    def click_search_the_contact(self, username):
        """查看是否存在搜索结果,并点击进入"""
        tmp_path = "//android.widget.TextView[@text='%s']" % username
        self.click_element((MobileBy.XPATH, tmp_path))

    @TestLogger.log("选择第一个搜索的结果点击进入")
    def click_the_first_search_the_contact(self):
        """查看是否存在搜索结果,并点击进入"""
        tmp_path = 'com.chinasofti.rcs:id/contact_list_item_layout'
        self.click_element((MobileBy.ID, tmp_path))


    @TestLogger.log("查看是否存在手机联系人标签")
    def phone_contact_is_exsit(self):
        """查看是否存在手机联系人标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='手机联系人']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("查看是否存在功能标签")
    def function_is_exsit(self):
        """查看是否存在功能标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='功能']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("查看是否存在网络搜索标签")
    def net_search_is_exsit(self):
        """查看是否存在网络搜索标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='网络搜索']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False

    @TestLogger.log("查看是否存在团队联系人标签")
    def team_contact_is_exsit(self):
        """查看是否存在团队联系人标签"""
        tmp_path = "//*[@resource-id='com.chinasofti.rcs:id/text_hint' and @text='团队联系人']"
        els = self.get_elements((MobileBy.XPATH, tmp_path))
        if len(els) > 0:
            return True
        return False
