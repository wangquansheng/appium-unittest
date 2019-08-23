import random

from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time
from pages import MessagePage, MePage, SettingPage, MeSetDialPage, MeSetDialWayPage, GroupListPage, SelectContacts
from pages.call.CallTypeSelect import CallTypeSelectPage
from pages.components import FooterPage
from pages.contacts.local_contact import localContactPage
from pages.call.MultiPartyVideo import MultiPartyVideoPage


class CallPage(FooterPage, BasePage):
    """主界面-通话tab页"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.HomeActivity'

    __locators = {
        '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCall'),
        '多方通话': (MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"),
        '返回箭头': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_arror'),
        "消息": (MobileBy.ID, "com.chinasofti.rcs:id/tvMessage"),
        "拨号盘": (MobileBy.ID, "com.chinasofti.rcs:id/tvCall"),
        '拨号键1': (MobileBy.ID, 'com.chinasofti.rcs:id/iv1'),
        '拨号键2': (MobileBy.ID, 'com.chinasofti.rcs:id/iv2'),
        '拨号键3': (MobileBy.ID, 'com.chinasofti.rcs:id/iv3'),
        '拨号键4': (MobileBy.ID, 'com.chinasofti.rcs:id/iv4'),
        '拨号键5': (MobileBy.ID, 'com.chinasofti.rcs:id/iv5'),
        '拨号键6': (MobileBy.ID, 'com.chinasofti.rcs:id/iv6'),
        '拨号键7': (MobileBy.ID, 'com.chinasofti.rcs:id/iv7'),
        '拨号键8': (MobileBy.ID, 'com.chinasofti.rcs:id/iv8'),
        '拨号键9': (MobileBy.ID, 'com.chinasofti.rcs:id/iv9'),
        '拨号键0': (MobileBy.ID, 'com.chinasofti.rcs:id/iv0'),
        '拨号键*': (MobileBy.ID, 'com.chinasofti.rcs:id/ivStar'),
        '拨号键#': (MobileBy.ID, 'com.chinasofti.rcs:id/ivSharp'),
        '删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDelete'),
        '拨号盘收缩删除X': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDeleteHide'),
        '拨打电话按键': (MobileBy.ID, 'com.chinasofti.rcs:id/ivVoiceCall'),
        '通话界面高清显示图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ivNoRecords'),
        '直接拨号或开始搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edt_t9_keyboard'),
        '新建联系人': (MobileBy.XPATH, "//*[contains(@text, '新建联系人')]"),
        '发送消息': (MobileBy.XPATH, "//*[contains(@text, '发送消息')]"),
        '结束通话': (MobileBy.ID, 'com.android.incallui:id/endButton'),
        '呼叫中': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAvatar'),
        '挂断语音通话': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_out_term'),
        '挂断视频通话': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_out_Cancel'),
        '挂断和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDecline'),
        '通话显示': (MobileBy.ID, 'com.chinasofti.rcs:id/tvTitle'),
        '通话记录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvName'),
        '0731210086': (MobileBy.XPATH, "//*[contains(@text, '0731210086')]"),
        '删除通话记录': (MobileBy.ID, "com.chinasofti.rcs:id/tvContent"),
        '通话profile': (MobileBy.ID, "com.chinasofti.rcs:id/sdDetail"),
        "多方电话提示框": (MobileBy.ID, "com.chinasofti.rcs:id/mutil_btnFreeCall"),
        "返回": (MobileBy.ID, "com.chinasofti.rcs:id/back"),
        "指定提示": (MobileBy.XPATH, "//*[contains(@text, '点击按钮发起电话')]"),
        '知道了': (MobileBy.XPATH, '//*[@text="知道了"]'),
        '始终允许': (MobileBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
        "多方视频图标": (MobileBy.ID, "com.chinasofti.rcs:id/ivMultipartyVideo"),
        "通话记录时间": (MobileBy.ID, "com.chinasofti.rcs:id/tvCallTime"),
        "profileName": (MobileBy.ID, "com.chinasofti.rcs:id/tv_profile_name"),
        "+号": (MobileBy.ID, 'com.chinasofti.rcs:id/action_add'),
        '视频通话': (MobileBy.XPATH, '//*[@text="视频通话"]'),
        '语音通话': (MobileBy.XPATH, '//*[@text="语音通话"]'),
        '继续拨打': (MobileBy.XPATH, '//*[@text="继续拨打"]'),
        '暂不开启': (MobileBy.XPATH, '//*[@text="暂不开启"]'),
        '多方电话': (MobileBy.XPATH, '//*[@text="多方电话"]'),
        '多方视频': (MobileBy.XPATH, '//*[@text="多方视频"]'),
        '我知道了': (MobileBy.XPATH, '//*[@text="我知道了"]'),
        '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '通话类型': (MobileBy.ID, 'com.chinasofti.rcs:id/tvCallManner'),
        '刚刚': (MobileBy.XPATH, '//*[@text="刚刚"]'),
        '你正在多方通话': (MobileBy.ID, 'com.chinasofti.rcs:id/status_tv'),
        '再次呼叫': (MobileBy.ID, 'com.chinasofti.rcs:id/call_again'),
        '一键建群': (MobileBy.ID, 'com.chinasofti.rcs:id/one_key_new_group'),
        '<': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        # 结束飞信电话并关闭会场管理
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        # 结束通话弹框
        '结束通话弹框': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_title'),
        '你正在飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/status_tv'),
        '呼叫选择飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_calltype_fetion'),
        '结束通话提示框': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_title'),
        '结束通话提示框-确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '开关摄像头按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_open_self_camera'),
        '1': (MobileBy.ID, 'com.chinasofti.rcs:id/iv1'),
        '2': (MobileBy.ID, 'com.chinasofti.rcs:id/iv2'),
        '3': (MobileBy.ID, 'com.chinasofti.rcs:id/iv3'),
        '4': (MobileBy.ID, 'com.chinasofti.rcs:id/iv4'),
        '5': (MobileBy.ID, 'com.chinasofti.rcs:id/iv5'),
        '6': (MobileBy.ID, 'com.chinasofti.rcs:id/iv6'),
        '7': (MobileBy.ID, 'com.chinasofti.rcs:id/iv7'),
        '8': (MobileBy.ID, 'com.chinasofti.rcs:id/iv8'),
        '9': (MobileBy.ID, 'com.chinasofti.rcs:id/iv9'),
        '0': (MobileBy.ID, 'com.chinasofti.rcs:id/iv0'),
        '语音通话接受按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_voice_call_answer'),
        '语音通话拒绝按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_voice_call_refuse'),
        '语音通话结束按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_out_term_new'),
        '切换到视频按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_switch_video'),
        '结束双人视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_term'),
        '话筒开关按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/video_iv_mute'),
        '多方视频接听': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAnswer'),
        '多方视频挂断': (MobileBy.ID, 'com.chinasofti.rcs:id/ivCancel'),
        '结束多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/end_video_call_btn'),
        '语音通话免提': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_speaker'),
        '语音通话静音': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_call_mute'),
        '切换到语音': (MobileBy.ID, 'com.chinasofti.rcs:id/video_iv_change_to_voice'),
        '切换摄像头': (MobileBy.ID, 'com.chinasofti.rcs:id/video_iv_switch_camera'),
        '语音通话缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_voice_hide'),
        '视频通话缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_video_hide'),
        '飞信电话按钮': (MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"),
        '多方视频缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_hide'),
        '取消拨打': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_normal_call_end'),

    }

    @TestLogger.log()
    def is_exist_free_call(self):
        """是否存在“多方通话”文本"""
        return self._is_element_present(self.__class__.__locators["多方通话"])

    @TestLogger.log()
    def click_free_call(self):
        """点击多方通话"""
        self.click_element(self.__locators["多方通话"])

    @TestLogger.log()
    def wait_for_call_page(self, timeout=10, auto_accept_alerts=True):
        """
        等待通话界面
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("拨号盘")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def wait_for_call_page2(self, timeout=10, auto_accept_alerts=True):
        """
        等待通话界面
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__locators['多方视频图标'])
                                    or self.is_text_present('再次呼叫')
                                    or self._is_element_present(self.__class__.__locators["+号"])

            )
            return True
        except:
            return False

    @TestLogger.log()
    def is_on_the_call_page(self):
        """判断当前页是否通话界面"""
        flag = False
        element = self.get_elements(self.__locators["多方视频图标"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def is_on_the_dial_pad(self):
        """判断当前页是否调起拨号盘"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_dial_pad(self):
        """点击拨号盘"""
        self.click_element(self.__locators["拨号盘"])

    @TestLogger.log()
    def click_one(self):
        """点击拨号键1"""
        self.click_element(self.__locators["拨号键1"])

    @TestLogger.log()
    def click_two(self):
        """点击拨号键2"""
        self.click_element(self.__locators["拨号键2"])

    @TestLogger.log()
    def click_three(self):
        """点击拨号键3"""
        self.click_element(self.__locators["拨号键3"])

    @TestLogger.log()
    def click_four(self):
        """点击拨号键4"""
        self.click_element(self.__locators["拨号键4"])

    @TestLogger.log()
    def click_five(self):
        """点击拨号键5"""
        self.click_element(self.__locators["拨号键5"])

    @TestLogger.log()
    def click_six(self):
        """点击拨号键6"""
        self.click_element(self.__locators["拨号键6"])

    @TestLogger.log()
    def click_seven(self):
        """点击拨号键7"""
        self.click_element(self.__locators["拨号键7"])

    @TestLogger.log()
    def click_eight(self):
        """点击拨号键8"""
        self.click_element(self.__locators["拨号键8"])

    @TestLogger.log()
    def click_nine(self):
        """点击拨号键9"""
        self.click_element(self.__locators["拨号键9"])

    @TestLogger.log()
    def click_zero(self):
        """点击拨号键0"""
        self.click_element(self.__locators["拨号键0"])

    @TestLogger.log()
    def click_star(self):
        """点击拨号键*"""
        self.click_element(self.__locators["拨号键*"])

    @TestLogger.log()
    def click_sharp(self):
        """点击拨号键#"""
        self.click_element(self.__locators["拨号键#"])

    @TestLogger.log()
    def click_delete(self):
        """点击删除X"""
        self.click_element(self.__locators["删除X"])

    @TestLogger.log()
    def click_delete_hide(self):
        """点击拨号盘收缩删除X"""
        self.click_element(self.__locators["拨号盘收缩删除X"])

    @TestLogger.log()
    def press_zero(self):
        """长按按键0"""
        el = self.get_element(self.__locators["拨号键0"])
        self.press(el)

    @TestLogger.log()
    def press_delete(self):
        """长按删除X"""
        el = self.get_element(self.__locators["删除X"])
        self.press(el)

    @TestLogger.log()
    def press_delete_hide(self):
        """拨号盘收缩删除X"""
        el = self.get_element(self.__locators["拨号盘收缩删除X"])
        self.press(el)

    @TestLogger.log()
    def click_phone_number(self, phone):
        """点击拨号"""
        for i in phone:
            self.click_element(self.__locators["拨号键%s" % i])

    @TestLogger.log()
    def click_call(self):
        """点击通话"""
        self.click_element(self.__locators["通话"])

    @TestLogger.log()
    def click_message(self):
        """点击消息"""
        self.click_element(self.__locators["消息"])

    @TestLogger.log()
    def click_call_phone(self):
        """点击拨打电话按键"""
        self.click_element(self.__locators["拨打电话按键"])

    @TestLogger.log()
    def check_call_phone(self):
        """检查拨打电话按键"""
        flag = False
        element = self.get_elements(self.__locators["拨打电话按键"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_image(self):
        """检查通话界面高清图片"""
        flag = False
        element = self.get_elements(self.__locators["通话界面高清显示图片"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def check_call_text(self, val=""):
        """检查拨号输入框文本内容与输入相同
        value：输入的文本内容：电话号码，str
        """
        callText = self.get_text(self.__locators["直接拨号或开始搜索"])
        flag = False
        if callText == val:
            flag = True
        return flag

    @TestLogger.log()
    def check_delete_hide(self):
        """检查拨号盘收缩删除X"""
        flag = False
        element = self.get_elements(self.__locators["拨号盘收缩删除X"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_new_contact(self):
        """点击新建联系人"""
        self.click_element(self.__locators["新建联系人"])

    @TestLogger.log()
    def click_send_message(self):
        """点击发送消息"""
        self.click_element(self.__locators["发送消息"])

    @TestLogger.log()
    def click_call_end(self):
        """点击结束通话"""
        self.click_element(self.__locators["结束通话"])

    @TestLogger.log()
    def check_call_success(self):
        """检查拨打电话成功"""
        flag = False
        element = self.get_elements(self.__locators["结束通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def wait_for_dial_pad(self, timeout=60, auto_accept_alerts=True):
        """
        等待拨号键盘
        """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("直接拨号")
            )
        except:
            raise AssertionError("通话界面未显示")
        return self

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """通过android键返回"""
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log()
    def get_call_color_of_element(self):
        """获取打电话控件坐标颜色"""
        self.get_coordinate_color_of_element(element=self.__locators["通话"], x=50, y=50, by_percent=True, mode='RGBA')

    @TestLogger.log()
    def check_end_voice_call(self):
        """检查语音通话结束按键是否存在"""
        flag = False
        element = self.get_elements(self.__locators["挂断语音通话"])
        if len(element) > 0:
            flag = True
        return flag

    @TestLogger.log()
    def click_end_voice_call(self):
        """点击结束语音通话"""
        self.click_element(self.__locators["挂断语音通话"])

    @TestLogger.log()
    def hang_up_voice_call(self):
        """挂断语音通话"""
        if self._is_element_present(self.__class__.__locators["挂断语音通话"]):
            self.click_element(self.__class__.__locators["挂断语音通话"])

    @TestLogger.log()
    def hang_up_video_call(self):
        """挂断视频通话"""
        if self._is_element_present(self.__class__.__locators["挂断视频通话"]):
            self.click_element(self.__class__.__locators["挂断视频通话"])

    @TestLogger.log()
    def hang_up_hefeixin_call(self):
        """挂断和飞信电话"""
        if self._is_element_present(self.__class__.__locators["挂断和飞信电话"]):
            self.click_element(self.__class__.__locators["挂断和飞信电话"])

    @TestLogger.log()
    def is_phone_in_calling_state(self):
        """判断是否在通话界面"""
        return self.driver.current_activity == '.InCallActivity'

    @TestLogger.log()
    def is_on_calling_page(self, timeout=20, auto_accept_alerts=True):
        """当前是否在通话页面"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.driver.current_activity == '.InCallActivity'
            )
            return True
        except:
            return False

    @TestLogger.log()
    def hang_up_the_call(self):
        """挂断电话"""
        command = 'input keyevent KEYCODE_ENDCALL'
        if self.is_phone_in_calling_state():
            return self.execute_shell_command(command)

    @TestLogger.log()
    def check_multiparty_video(self):
        """判断是否存在视频图片来检查是否在通话界面"""
        return self._is_element_present(self.__locators["多方视频图标"])

    @TestLogger.log()
    def check_call_display(self):
        """判断是否存在通话显示"""
        return self._is_element_present(self.__locators["通话显示"])

    @TestLogger.log()
    def check_free_call(self):
        """判断是否存在多方通话"""
        return self._is_element_present(self.__locators["多方通话"])

    def get_call_history(self, index):
        """通过下标获取通话记录号码"""
        elements = self.get_elements(self.__locators["通话记录"])
        try:
            if len(elements) > 0:
                return elements[index].text
        except:
            raise IndexError("元素超出索引")

    def dial_number(self, text):
        """输入拨打号码"""
        self.input_text(self.__locators["直接拨号或开始搜索"], text)

    @TestLogger.log()
    def press_delete_entry(self):
        """长按删除通话记录"""
        el = self.get_element(self.__locators["通话记录"])
        self.press(el)

    @TestLogger.log()
    def click_delete_entry(self):
        """删除通话记录"""
        self.click_element(self.__locators["删除通话记录"])

    @TestLogger.log()
    def check_delete_entry(self):
        """判断是否删除通话记录弹框"""
        return self._is_element_present(self.__locators["删除通话记录"])

    @TestLogger.log("清空通话记录")
    def delete_all_call_entry(self):
        """前置条件：当前已进入call界面"""
        ret = True
        if self.check_multiparty_video():
            for i in range(20):
                el = self.get_elements(self.__locators["通话记录"])
                if len(el) > 0:
                    self.press(el[0])
                    self.click_delete_entry()
                    if ret:
                        if self.is_exist_allow_button():
                            self.click_allow_button(auto_accept_permission_alert=False)
                        ret = False
                else:
                    print("已删除通话记录")
                    break

    @TestLogger.log()
    def get_call_entry_color_of_element(self):
        """获取通话记录控件坐标颜色"""
        return self.get_coordinate_color_of_element(element=self.__locators["通话记录"], x=50, y=50, by_percent=True,
                                                    mode='RGBA')

    @TestLogger.log()
    def click_call_profile(self):
        """点击通话profile"""
        self.click_element(self.__locators["通话profile"])

    @TestLogger.log()
    def press_keyboard(self):
        """长按拨号盘输入框"""
        el = self.get_element(self.__locators["直接拨号或开始搜索"])
        self.press(el)

    @TestLogger.log()
    def is_exist_specified_prompt(self):
        """是否存在指定提示"""
        return self._is_element_present(self.__class__.__locators["指定提示"])

    @TestLogger.log()
    def is_exist_multi_party_telephone(self):
        """是否存在“多方电话”文本"""
        return self._is_element_present(self.__class__.__locators["多方电话提示框"])

    @TestLogger.log()
    def click_multi_party_telephone(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话提示框"])

    @TestLogger.log()
    def is_exist_know(self):
        """是否存在“知道了”文本"""
        return self._is_element_present(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_know(self):
        """点击知道了"""
        self.click_element(self.__class__.__locators["知道了"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_allow_button(self):
        """是否存在始终允许"""
        return self._is_element_present(self.__class__.__locators["始终允许"])

    @TestLogger.log()
    def click_allow_button(self, auto_accept_permission_alert=True):
        """点击允许"""
        self.click_element(self.__class__.__locators["始终允许"], auto_accept_permission_alert=auto_accept_permission_alert)

    def wait_for_freemsg_load(self, timeout=8, auto_accept_alerts=True):
        """等待免费短信页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择联系人"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待通话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方视频图标"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_call_time(self):
        """点击通话记录时间"""
        self.click_element(self.__class__.__locators["通话记录时间"])

    @TestLogger.log()
    def is_exist_call_time(self):
        """判断是否存在通话记录时间"""
        return self._is_element_present(self.__locators["通话记录时间"])

    @TestLogger.log()
    def is_exist_profile_name(self):
        """判断是否存在profile_name"""
        return self._is_element_present(self.__locators["profileName"])

    @TestLogger.log()
    def get_profile_name(self):
        """获取profile_name"""
        return self.get_text(self.__locators["profileName"])

    @TestLogger.log()
    def select_dial_mode(self):
        """进入拨号方式选择"""
        MessagePage().open_me_page()
        MePage().click_setting_menu()
        SettingPage().click_dial_setting()
        MeSetDialPage().click_dial_mode()

    @TestLogger.log()
    def setting_dial_mode_and_go_back_call(self):
        """设置拨号方式为总是询问，并返回call界面"""
        self.select_dial_mode()
        MeSetDialWayPage().click_call_type_alaways_ask()
        self.click_back_by_android(times=3)
        self.click_call()

    @TestLogger.log()
    def create_call_entry(self, text):
        """当前界面已在call界面，创建通话记录，并返回call界面"""
        self.click_call()
        time.sleep(1)
        self.dial_number(text)
        time.sleep(1)
        self.click_call_phone()
        time.sleep(2)
        if CallTypeSelectPage().is_select_call():
            CallTypeSelectPage().click_call_by_general()
        self.click_call_end()
        time.sleep(1)
        if not self.is_on_the_call_page():
            self.click_call()

    @TestLogger.log()
    def click_multi_party_video(self):
        """点击多方视频"""
        self.click_element(self.__class__.__locators["多方视频图标"])

    @TestLogger.log()
    def select_type_start_call(self, text, calltype):
        """在call界面，输入号码选择拨打电话类型并拨打电话"""
        if not self.is_on_the_dial_pad():
            self.click_call()
        self.dial_number(text)
        self.click_call_phone()
        time.sleep(2)
        if CallTypeSelectPage().is_select_call():
            if calltype == 2:
                CallTypeSelectPage().click_call_by_general()
            if calltype == 1:
                CallTypeSelectPage().click_call_by_voice()
            if calltype == 0:
                CallTypeSelectPage().click_call_by_app()
        time.sleep(1)

    @TestLogger.log()
    def is_on_this_messagepage(self):
        """当前页面是否在消息页"""
        try:
            self.wait_until(
                timeout=30,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["+号"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def enter_contact_details(self, name):
        """进入联系人详情界面"""
        GroupListPage().open_contacts_page()
        for i in range(10):
            time.sleep(2)
            if self.is_text_present(name):
                self.click_text(name)
                break
            else:
                self.page_up()

    @TestLogger.log()
    def click_video_call(self):
        """点击视频通话"""
        self.click_element(self.__class__.__locators["视频通话"])

    @TestLogger.log()
    def click_voice_call(self):
        """点击语音通话"""
        self.click_element(self.__class__.__locators["语音通话"])

    @TestLogger.log()
    def click_mutil_call(self):
        """点击多方电话"""
        self.click_element(self.__class__.__locators["多方电话"])

    @TestLogger.log()
    def click_mutil_video_call(self):
        """点击多方视频"""
        self.click_element(self.__class__.__locators["多方视频"])

    @TestLogger.log('点击继续拨打')
    def click_go_on(self):
        self.click_element(self.__locators['继续拨打'])

    @TestLogger.log()
    def is_exist_go_on(self):
        """是否存在继续拨打按钮"""
        return self._is_element_present(self.__class__.__locators["继续拨打"])

    @TestLogger.log()
    def click_cancel_open(self):
        """点击暂不开启"""
        if self._is_element_present(self.__class__.__locators["暂不开启"]):
            self.click_element(self.__locators['暂不开启'])
        else:
            return

    @TestLogger.log()
    def click_i_know(self):
        """点击我知道了"""
        if self._is_element_present(self.__class__.__locators["我知道了"]):
            self.click_element(self.__class__.__locators["我知道了"])

    @TestLogger.log()
    def wait_for_chat_page(self):
        """等待单聊界面展示"""
        self.wait_until(
            timeout=30,
            auto_accept_permission_alert=True,
            condition=lambda d: self.is_text_present("说点什么..."))

    @TestLogger.log()
    def get_calltype_history(self, index):
        """通过下标获取通话记录类型"""
        elements = self.get_elements(self.__locators["通话类型"])
        try:
            if len(elements) > 0:
                return elements[index].text
        except:
            raise IndexError("元素超出索引")

    @TestLogger.log()
    def is_type_hefeixin(self, index, type):
        """判断下标获取通话记录类型是否为指定类型"""
        text = self.get_calltype_history(index)
        try:
            if text == type:
                return True
        except:
            raise AssertionError("通话类型不是{}".format(type))

    @TestLogger.log()
    def click_ganggang_call_time(self):
        """点击'刚刚'的通话记录，进入详情页"""
        self.click_element(self.__locators["刚刚"], auto_accept_permission_alert=False)
        time.sleep(3)

    @TestLogger.log()
    def is_hefeixin_page(self, text):
        """通话记录详情页面标题是否是text？"""

        self.element_should_contain_text((MobileBy.ID, "com.chinasofti.rcs:id/tx_name_multi_call"), text)

    @TestLogger.log()
    def click_back_to_call(self):
        """点击你正在多方通话,进入通话会控页"""
        self.click_element(self.__locators["你正在多方通话"])

    @TestLogger.log()
    def click_back_to_fetion_call(self):
        """点击你正在多方通话,进入通话会控页"""
        locator = (MobileBy.ID, "android:id/statusBarBackground")
        self.click_element(locator)

    @TestLogger.log()
    def click_back_to_call_631(self):
        """点击你正在飞信电话,进入通话会控页"""
        self.click_element(self.__locators["你正在飞信电话"])

    @TestLogger.log()
    def is_you_are_calling_exists(self):
        """页面是否存在“你正在飞信电话”"""
        self._is_element_present(self.__locators["你正在飞信电话"])

    @TestLogger.log()
    def click_mutil_call_again(self):
        """点击再次呼叫"""
        self.find_element_by_swipe(self.__locators["再次呼叫"])
        self.click_element(self.__locators["再次呼叫"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_onekey_build_group(self):
        """点击一键建群"""
        self.click_element(self.__locators["一键建群"], auto_accept_permission_alert=False)

    @TestLogger.log()
    def click_lefticon_back(self):
        """点击<图标返回"""
        self.click_element(self.__class__.__locators["<"])

    @TestLogger.log()
    def wait_for_click_freecal(self):
        """等待呼叫方式选择界面弹出并点击飞信电话"""
        self.wait_until(
            timeout=5,
            auto_accept_permission_alert=True,
            condition=lambda d: self._is_element_present(self.__class__.__locators["呼叫选择飞信电话"]))
        self.click_element(self.__class__.__locators["呼叫选择飞信电话"])

    @TestLogger.log()
    def hang_up_hefeixin_call_631(self):
        """挂断和飞信电话"""
        self.wait_until(
            timeout=5,
            auto_accept_permission_alert=True,
            condition=lambda d: self._is_element_present(self.__class__.__locators["挂断和飞信电话"]))
        self.click_element(self.__class__.__locators["挂断和飞信电话"])
        self.wait_until(
            timeout=5,
            auto_accept_permission_alert=True,
            condition=lambda d: self._is_element_present(self.__class__.__locators["结束通话提示框"]))
        self.click_element(self.__class__.__locators["结束通话提示框-确定"])

    def click_call_history(self):
        """点击通话记录号码"""
        self.click_element(self.__locators['通话记录'])

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_voice_call_small(self):
        self.click_element(self.__locators['语音通话缩放按钮'])

    @TestLogger.log()
    def click_video_call_small(self):
        time.sleep(1)
        self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/iv_switch"))

    @TestLogger.log()
    def click_more_video_call_small(self):
        time.sleep(1)
        print(self.get_source())
        self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/iv_hide"))

    @TestLogger.log()
    def click_call_cancel(self):
        """点击取消拨打"""
        self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/iv_normal_call_end"))

    @TestLogger.log()
    def end_multi_video_phone(self):
        self.click_element(self.__locators['结束多方视频'])
        self.click_element(self.__class__.__locators["结束通话提示框-确定"])

    @TestLogger.log()
    def randomly_generated_number(self):
        """随机生成8位号码"""
        number = ""
        for i in range(8):
            tmp = random.randint(0, 9)
            number += str(tmp)
        return number
