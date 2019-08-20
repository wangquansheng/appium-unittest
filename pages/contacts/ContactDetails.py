from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
import os


class ContactDetailsPage(BasePage):
    """个人详情"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.ContactDetailActivity'

    __locators = {
        '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        "联系人头像": (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
        '编辑2': (MobileBy.XPATH, "//*[@text='编辑']"),
        '星标图标': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_star'),
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
        '名片标题': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_name'),

        '标题': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_name'),
        '手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_phone'),

        '星标': (MobileBy.ID, 'com.chinasofti.rcs:id/star'),
        '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/txt_call_detail_edit'),
        '好久不见~打个招呼吧': (MobileBy.ID, 'com.chinasofti.rcs:id/recent_contact_hint'),
        '名片号码': (MobileBy.ID, 'com.chinasofti.rcs:id/phone'),
        '名片首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/profile_photo_tv'),
        '名片首字母2': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_photo_tv'),
        '联系人头像图片': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclesafeimageview_profile_photo'),
        '头像': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_profile_photo_tv'),
        '消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_message'),
        '电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_normal_call'),
        '语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_voice_call'),
        '视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_call'),
        '和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_dial_hefeixin'),
        '详细信息列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/sv_info'),
        '公司': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '公司名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '职位': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '职位名': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/property'),
        '邮箱地址': (MobileBy.ID, 'com.chinasofti.rcs:id/value'),
        '分享名片': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_share_card" and @text="分享名片"]'),
        '分享名片左上角X按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/cancle_img'),
        '分享名片头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_card_img'),
        '分享名片名字': (MobileBy.ID, 'com.chinasofti.rcs:id/name_tv'),
        '分享名片号码': (MobileBy.ID, 'com.chinasofti.rcs:id/phone_tv'),
        '分享名片公司': (MobileBy.ID, 'com.chinasofti.rcs:id/company_tv'),
        '分享名片职位': (MobileBy.ID, 'com.chinasofti.rcs:id/position_tv'),
        '分享名片邮箱': (MobileBy.ID, 'com.chinasofti.rcs:id/email_tv'),
        '保存到通讯录': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_share_card" and @text="保存到通讯录"]'),
        'com.chinasofti.rcs:id/btn_share_card_line': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card_line'),
        '邀请使用': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_invitation_to_use'),
        '大图': (MobileBy.ID, 'com.chinasofti.rcs:id/img_smooth'),
        '电话号码': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/et" and @text="13800138005"]'),
        "确定": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),
        "确定删除": (MobileBy.ID, 'com.chinasofti.rcs:id/bt_button2'),
        "删除联系人": (MobileBy.ID, "com.chinasofti.rcs:id/tv_delete_contact"),
        "呼叫(1/8)": (MobileBy.ID, "com.chinasofti.rcs:id/tv_sure"),
        "暂不开启": (MobileBy.ID, "android:id/button2"),
        "挂断电话": (MobileBy.ID, "com.chinasofti.rcs:id/ivDecline"),
        # 备注：包名与和飞信不同
        "挂断电话2": (MobileBy.ID, "com.android.incallui:id/endButton"),
        "结束通话": (MobileBy.ID, "com.chinasofti.rcs:id/smart_call_out_term"),
        "视频通话呼叫中": (MobileBy.XPATH, "//*[@text='	视频通话呼叫中']"),
        "挂断视频通话": (MobileBy.ID, "com.chinasofti.rcs:id/iv_out_Cancel"),
        "取消拨打": (MobileBy.XPATH, "//*[@text='取消拨打']"),
        "联系人名称": (MobileBy.ID, "com.chinasofti.rcs:id/contact_name"),
        "用户名称": (MobileBy.ID, "com.chinasofti.rcs:id/tv_profile_name"),
        "用户头像": (MobileBy.ID, "com.chinasofti.rcs:id/recyclesafeimageview_profile_photo"),
        "用户号码": (MobileBy.ID, "com.chinasofti.rcs:id/tv_phone"),
        '添加桌面快捷方式': (MobileBy.XPATH, '//*[@text="添加桌面快捷方式"]'),
        '我知道了': (MobileBy.XPATH, '//*[@text="我知道了"]'),
        '快捷方式-确定添加': (MobileBy.ID, "android:id/button1"),
        '快捷方式-取消添加': (MobileBy.ID, "android:id/button2"),
        "和飞信电话-挂断电话": (MobileBy.ID, "com.android.incallui:id/declinebutton"),
        "团队选择一个联系人": (MobileBy.XPATH, "//*[contains(@text,'给个红包1')]"),
        "团队选择一个联系人2": (MobileBy.XPATH, "//*[contains(@text,'1测试团队保存联系人')]"),
        "团队选择一个联系人3": (MobileBy.XPATH, "//*[contains(@text,'2测试团队保存联系人子级')]"),
        "我知道了": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_confirm'),
        "快捷方式": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_shortcut'),
        "不再提醒": (MobileBy.ID, 'com.chinasofti.rcs:id/cb_show_again'),
        '允许': (MobileBy.XPATH, '//*[@text="允许"]'),
        "继续拨打": (MobileBy.ID, 'com.chinasofti.rcs:id/continue_call'),
        "以后不再提醒": (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_not_pop_btn_image'),
    }

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """默认使用activity作为判断页面是否加载的条件，继承类应该重写该方法"""
        try:
            self.wait_until(
                lambda d: self.is_text_present('立即创建团队'),
                timeout,
                auto_accept_alerts
            )
            return self
        except:
            return self.is_text_present('立即创建团队')

    @TestLogger.log("点击继续拨打")
    def click_continue_call(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['继续拨打']):
            self.click_element(self.__class__.__locators['继续拨打'])
        return True

    @TestLogger.log("点击允许权限")
    def click_allow_button(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['允许']):
            self.click_element(self.__class__.__locators['允许'])
        return True

    @TestLogger.log("点击快捷方式")
    def click_shortcut(self):
        """点击快捷方式"""
        self.click_element(self.__locators['快捷方式'])

    @TestLogger.log("")
    def page_contain_shortcut(self):
        """当前页面是否存在快捷方式"""
        return self.page_should_contain_element(self.__locators['快捷方式'])

    @TestLogger.log("")
    def page_not_contain_i_know(self):
        """当前页面是否存在快捷方式"""
        return self.page_should_not_contain_element(self.__locators['我知道了'])

    @TestLogger.log("")
    def is_on_this_page(self):
        """当前页面是否在个人详情"""
        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["编辑2"])
            )
            return True
        except:
            return False

    @TestLogger.log("")
    def click_i_know(self):
        """当前页面是否在个人详情"""
        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.page_should_contain_element(self.__locators['我知道了'])
            )
            self.click_element(self.__locators['我知道了'])
        except:
            pass

    @TestLogger.log("")
    def click_i_know_and_no_remind(self):
        """当前页面是否在个人详情"""
        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self.page_should_contain_element(self.__locators['我知道了'])
            )
            self.click_element(self.__locators['不再提醒'])
            time.sleep(1)
            self.click_element(self.__locators['我知道了'])
        except:
            pass

    @TestLogger.log("是否在当前页面")
    def is_on_this_page(self):
        time.sleep(2)
        return self.is_text_present('分享名片')

    @TestLogger.log("添加桌面快捷方式")
    def click_add_desktop_shortcut(self):
        time.sleep(1)
        self.click_element(self.__locators["添加桌面快捷方式"])

    @TestLogger.log("始终允许弹框处理")
    def click_permission_box(self):
        time.sleep(1)
        while self.is_text_present('始终允许'):
            self.click_text('始终允许')

    @TestLogger.log("点击我知道了")
    def click_I_know(self):
        time.sleep(1)
        self.click_element(self.__class__.__locators["我知道了"])

    @TestLogger.log("点击确定添加快捷方式")
    def click_sure_add_desktop_shortcut(self):
        time.sleep(1)
        self.click_element(self.__locators["快捷方式-确定添加"])

    @TestLogger.log("更改手机号码")
    def change_mobile_number(self):
        self.input_text(self.__locators["电话号码"], "13800138006")

    @TestLogger.log("点击呼叫")
    def send_call_number(self):
        time.sleep(1)
        self.click_element(self.__locators["呼叫(1/8)"])
        time.sleep(1)

    @TestLogger.log("设置授权窗口")
    def cancel_permission(self):
        time.sleep(3)
        self.click_element(self.__locators["暂不开启"])

    @TestLogger.log("")
    def cancel_call(self):
        time.sleep(3)
        self.click_element(self.__locators["挂断电话"])

    @TestLogger.log("")
    def cancel_call2(self):
        try:
            time.sleep(3)
            self.click_element(self.__locators["挂断电话2"])
        except:
            pass

    @TestLogger.log("")
    def is_element_present(self, locator='挂断电话'):
        time.sleep(4)
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log("")
    def cancel_hefeixin_call(self):
        time.sleep(4)
        if self._is_element_present(self.__locators["和飞信电话-挂断电话"]):
            self.click_element(self.__locators["和飞信电话-挂断电话"])
        else:
            time.sleep(2)

    # 香港大佬
    @TestLogger.log("")
    def click_end_call(self):
        time.sleep(2)
        self.click_element(self.__locators["结束通话"])

    @TestLogger.log("")
    def change_delete_number(self):
        time.sleep(1)
        self.click_element(self.__locators['删除联系人'])

    @TestLogger.log()
    def open_contacts_page(self):
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])

    @TestLogger.log("删除所有的联系人")
    def delete_all_contact(self):
        """使用此方法前，app进入消息界面"""
        self.open_contacts_page()
        flag = True
        while flag:
            time.sleep(2)
            elements = self.get_elements(self.__locators['联系人列表'])
            if elements:
                elements[0].click()
                self.click_edit_contact()
                time.sleep(1)
                self.hide_keyboard()
                time.sleep(1)
                self.page_up()
                self.change_delete_number()
                time.sleep(1)
                self.click_sure_delete()
            else:
                self.take_screen_out()
                print("无可删除联系人")
                flag = False

    @TestLogger.log("通过Name删除指定联系人")
    def delete_contact(self, text):
        """使用此方法前，app进入消息界面"""
        self.open_contacts_page()
        from pages import ContactsPage
        ContactsPage().click_mobile_contacts()
        if ContactsPage().is_text_present('发现SIM卡联系人'):
            ContactsPage().click_sim_contact_ok()
        time.sleep(2)
        ContactsPage().select_contacts_by_name(text)
        time.sleep(1)
        self.click_edit_contact()
        time.sleep(1)
        self.hide_keyboard()
        self.page_up()
        self.change_delete_number()
        self.click_sure_delete()

    @TestLogger.log("点击返回按钮")
    def click_back_icon(self):
        """点击返回"""
        self.click_element(self.__locators['返回上一页'])
        time.sleep(1)

    @TestLogger.log("点击确定")
    def click_sure_icon(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log("确定删除")
    def click_sure_delete(self):
        """确定删除"""
        time.sleep(3)
        self.click_element(self.__locators['确定删除'])

    @TestLogger.log("点击编辑")
    def click_edit_contact(self):
        """点击编辑按钮"""
        self.click_element(self.__locators['编辑2'])

    @TestLogger.log("获取名片名称")
    def get_contact_name(self, wait_time=0):
        title = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片标题']),
            timeout=wait_time
        )
        return title.text

    @TestLogger.log('获取名片号码')
    def get_contact_number(self, wait_time=0):
        number = self.wait_until(
            condition=lambda d: self.get_element(self.__locators['名片号码']),
            timeout=wait_time
        )
        return number.text

    @TestLogger.log("点击消息图标")
    def click_message_icon(self):
        self.click_element(self.__locators['消息'])

    @TestLogger.log('点击电话图标')
    def click_call_icon(self):
        self.click_element(self.__locators['电话'])

    @TestLogger.log("点击语音通话图标")
    def click_voice_call_icon(self):
        self.click_element(self.__locators['语音通话'])

    @TestLogger.log("点击视频通话图标")
    def click_video_call_icon(self):
        self.click_element(self.__locators['视频通话'])

    @TestLogger.log("点击和飞信电话菜单")
    def click_hefeixin_call_menu(self):
        self.click_element(self.__locators['和飞信电话'])

    @TestLogger.log("点击头像查看大图")
    def click_avatar(self):
        """点击头像查看大图"""
        self.click_element(self.__locators['头像'])

    @TestLogger.log("点击大图")
    def click_big_avatar(self):
        """点击大图"""
        self.click_element(self.__locators['大图'])

    @TestLogger.log()
    def is_exists_big_avatar(self):
        """是否存在大图"""
        return self._is_element_present(self.__class__.__locators["大图"])

    @TestLogger.log("点击分享名片")
    def click_share_business_card(self):
        """点击分享名片"""
        self.click_element(self.__locators['分享名片'])

    @TestLogger.log("邀请使用")
    def click_invitation_use(self):
        """邀请使用"""
        self.click_element(self.__locators['邀请使用'])

    @TestLogger.log()
    def message_btn_is_clickable(self):
        """消息按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators["消息"])

    @TestLogger.log()
    def call_btn_is_clickable(self):
        """电话按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators["电话"])

    @TestLogger.log()
    def voice_btn_is_clickable(self):
        """语音通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def video_call_btn_is_clickable(self):
        """视频通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["视频通话"])

    @TestLogger.log("挂断视频通话")
    def end_video_call(self):
        time.sleep(2)

        if self.get_elements(self.__locators["挂断视频通话"]):
            self.click_element(self.__locators["挂断视频通话"])
        else:
            self.click_element(self.__locators["取消拨打"])

    @TestLogger.log("")
    def end_voice_call(self):
        try:
            self.click_element(self.__locators["取消拨打"])
        except:
            pass

    @TestLogger.log()
    def hefeixin_call_btn_is_clickable(self):
        """和飞信通话按钮状态是否可点击"""
        return self._is_clickable(self.__class__.__locators["和飞信电话"])

    @TestLogger.log()
    def page_should_contain_element_first_letter(self):
        """页面应该包含首字母"""
        return self.page_should_contain_element(self.__class__.__locators['名片首字母'])

    @TestLogger.log()
    def page_should_contain_element_first_letter2(self):
        """页面应该包含首字母2"""
        return self.page_should_contain_element(self.__class__.__locators['名片首字母2'])

    @TestLogger.log()
    def page_contain_contacts_avatar(self):
        """页面应该包含联系人头像"""
        return self.page_should_contain_element(self.__class__.__locators['联系人头像图片'])

    @TestLogger.log()
    def is_exists_contacts_image(self):
        """是否存在联系人头像"""
        return self._is_element_present(self.__class__.__locators["用户头像"])

    @TestLogger.log()
    def click_contacts_image(self):
        """点击联系人头像"""
        self.click_element(self.__class__.__locators["用户头像"])

    @TestLogger.log()
    def is_exists_contacts_name(self):
        """是否存在联系人名"""
        return self._is_element_present(self.__class__.__locators["用户名称"])

    @TestLogger.log()
    def is_exists_contacts_number(self):
        """是否存在联系人号码"""
        return self._is_element_present(self.__class__.__locators["用户号码"])

    @TestLogger.log()
    def is_exists_contacts_image(self):
        """是否存在联系人头像"""
        return self._is_element_present(self.__class__.__locators["用户头像"])

    @TestLogger.log()
    def is_exists_message_icon(self):
        """是否存在消息图标"""
        return self._is_element_present(self.__class__.__locators["消息"])

    @TestLogger.log()
    def message_icon_is_enabled(self):
        """消息图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["消息"])

    @TestLogger.log()
    def is_exists_call_icon(self):
        """是否存在电话图标"""
        return self._is_element_present(self.__class__.__locators["电话"])

    @TestLogger.log()
    def call_icon_is_enabled(self):
        """电话图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["电话"])

    @TestLogger.log()
    def is_exists_voice_call_icon(self):
        """是否存在语音通话图标"""
        return self._is_element_present(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def voice_call_icon_is_enabled(self):
        """语音通话图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def is_exists_video_call_icon(self):
        """是否存在视频通话图标"""
        return self._is_element_present(self.__class__.__locators["视频通话"])

    @TestLogger.log()
    def video_call_icon_is_enabled(self):
        """视频通话图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["视频通话"])

    @TestLogger.log()
    def is_exists_dial_hefeixin_icon(self):
        """是否存在和飞信电话图标"""
        return self._is_element_present(self.__class__.__locators["和飞信电话"])

    @TestLogger.log()
    def dial_hefeixin_icon_is_enabled(self):
        """和飞信电话图标是否可点击"""
        return self._is_enabled(self.__class__.__locators["和飞信电话"])

    @TestLogger.log()
    def is_exists_share_card_icon(self):
        """是否存在分享名片图标"""
        return self._is_element_present(self.__class__.__locators["分享名片"])

    @TestLogger.log()
    def click_share_card_icon(self):
        """点击分享名片图标"""
        self.click_element(self.__class__.__locators["分享名片"])

    @TestLogger.log()
    def is_exists_save_contacts_icon(self):
        """是否存在保存到通讯录图标"""
        return self._is_element_present(self.__class__.__locators["保存到通讯录"])

    @TestLogger.log()
    def click_save_contacts_icon(self):
        """点击保存到通讯录图标"""
        self.click_element(self.__class__.__locators["保存到通讯录"])

    @TestLogger.log()
    def is_exists_share_card_close_icon(self):
        """是否存在分享名片左上角X按钮"""
        return self._is_element_present(self.__class__.__locators["分享名片左上角X按钮"])

    @TestLogger.log()
    def is_exists_share_card_head_img(self):
        """是否存在分享名片头像"""
        return self._is_element_present(self.__class__.__locators["分享名片头像"])

    @TestLogger.log()
    def is_exists_share_card_name(self):
        """是否存在分享名片名字"""
        return self._is_element_present(self.__class__.__locators["分享名片名字"])

    @TestLogger.log()
    def is_exists_share_card_number(self):
        """是否存在分享名片号码"""
        return self._is_element_present(self.__class__.__locators["分享名片号码"])

    @TestLogger.log()
    def is_exists_share_card_company(self):
        """是否存在分享名片公司"""
        return self._is_element_present(self.__class__.__locators["分享名片公司"])

    @TestLogger.log()
    def is_exists_share_card_position(self):
        """是否存在分享名片职位"""
        return self._is_element_present(self.__class__.__locators["分享名片职位"])

    @TestLogger.log()
    def is_exists_share_card_email(self):
        """是否存在分享名片邮箱"""
        return self._is_element_present(self.__class__.__locators["分享名片邮箱"])

    @TestLogger.log()
    def is_exists_value_by_name(self, name):
        """用户信息有值时是否显示"""
        locator = (MobileBy.XPATH,
                   '//*[@resource-id="com.chinasofti.rcs:id/property" and @text="%s"]/../android.widget.TextView[@resource-id="com.chinasofti.rcs:id/value"]' % name)
        if self._is_element_present(locator):
            text = self.get_element(locator).text
            if text:
                # 有此信息有值时返回True
                # print(text)
                return True
            else:
                # 有此信息无值时返回False
                # print("出错")
                return False
        else:
            # 没有此信息时返回True
            # print("无" + name)
            return True

    @TestLogger.log("截图")
    def take_screen_out(self):

        path = os.getcwd() + "/screenshot"
        print(path)
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        os.popen("adb wait-for-device")
        time.sleep(1)
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        if not os.path.isdir(os.getcwd() + "/screenshot"):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp/tmp.png " + path + "/" + timestamp + ".png")
        os.popen("adb shell rm /data/local/tmp/tmp.png")

    @TestLogger.log()
    def click_star(self):
        """点击星级图标"""
        self.click_element(self.__class__.__locators["星标图标"])

    @TestLogger.log()
    def click_selectone(self):
        """团队选择一个联系人"""
        self.click_element(self.__class__.__locators["团队选择一个联系人"])

    @TestLogger.log()
    def click_selectone2(self):
        """团队选择一个联系人2"""
        self.click_element(self.__class__.__locators["团队选择一个联系人2"])

    @TestLogger.log()
    def click_selectone3(self):
        """团队选择一个联系人3"""
        self.click_element(self.__class__.__locators["团队选择一个联系人3"])

    @TestLogger.log('断言：检查页面是否包含文本')
    def assert_screen_contain_text(self, text):
        if not self.is_text_present(text):
            raise AssertionError("Page should have contained text '{}' "
                                 "but did not".format(text))

    @TestLogger.log()
    def get_people_name(self):
        time.sleep(2)
        el = self.get_element(self.__class__.__locators['标题'])
        return el.text

    @TestLogger.log()
    def get_people_number(self):
        time.sleep(2)
        return self.get_element(self.__class__.__locators['手机号']).text


def add(func):
    def wrapper(*args):
        try:
            func(*args)
        except:  # 等待AssertionError
            path = os.getcwd() + "/screenshot"
            print(path)
            timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            os.popen("adb wait-for-device")
            time.sleep(2)
            os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
            time.sleep(2)
            if not os.path.isdir(os.getcwd() + "/screenshot"):
                os.makedirs(path)
            os.popen("adb pull /data/local/tmp/tmp.png " + path + "/" + timestamp + ".png")
            os.popen("adb shell rm /data/local/tmp/tmp.png")
            # raise ArithmeticError

    return wrapper
