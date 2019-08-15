from appium.webdriver.common.mobileby import MobileBy
import re
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class GroupChatSetPage(BasePage):
    """群聊设置页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupSettingActivity'

    __locators = {'菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/layout_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群聊设置': (MobileBy.ID, 'com.chinasofti.rcs:id/text_title'),
                  'com.chinasofti.rcs:id/show_more_member': (MobileBy.ID, 'com.chinasofti.rcs:id/show_more_member'),
                  '群成员(2人)': (MobileBy.ID, 'com.chinasofti.rcs:id/member_count'),
                  '群成员展开>': (
                      MobileBy.XPATH,
                      '//*[@resource-id="com.chinasofti.rcs:id/member_count"]/../android.widget.ImageView'),
                  'com.chinasofti.rcs:id/member_list': (MobileBy.ID, 'com.chinasofti.rcs:id/member_list'),
                  'com.chinasofti.rcs:id/iv_avatar': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_avatar'),
                  'com.chinasofti.rcs:id/iv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
                  'com.chinasofti.rcs:id/iv_group_chairman_tag': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_chairman_tag'),
                  'mobile0...': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'com.chinasofti.rcs:id/tv_name': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  'com.chinasofti.rcs:id/group_name_line': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_line'),
                  '群聊名称': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_chat_name_tv'),
                  '群聊001': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  '修改群聊名称': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_right_arrow'),
                  'com.chinasofti.rcs:id/rl_group_avatars': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_avatars'),
                  '群二维码': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_code_tv'),
                  'com.chinasofti.rcs:id/iv_group_avatars': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_avatars'),
                  'com.chinasofti.rcs:id/arrow1': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow1'),
                  'com.chinasofti.rcs:id/my_group_name_line': (MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_line'),
                  '我在本群的昵称': (MobileBy.ID, 'com.chinasofti.rcs:id/left_me_group_name_tv'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name'),
                  'com.chinasofti.rcs:id/my_group_name_right_arrow': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name_right_arrow'),
                  'com.chinasofti.rcs:id/group_manage': (MobileBy.ID, 'com.chinasofti.rcs:id/group_manage'),
                  '群管理': (MobileBy.ID, 'com.chinasofti.rcs:id/left_group_manage_tv'),
                  '消息免打扰': (MobileBy.ID, 'com.chinasofti.rcs:id/left_message_interruption_tv'),
                  '消息免打扰开关': (MobileBy.ID, 'com.chinasofti.rcs:id/switch_undisturb'),
                  '置顶聊天开关': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '置顶聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_tv'),
                  'com.chinasofti.rcs:id/tv_serarch_chat_record': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/tv_serarch_chat_record'),
                  '查找聊天内容': (MobileBy.ID, 'com.chinasofti.rcs:id/left_find_chat_record_tv'),
                  '清空聊天记录2': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_chat_empty'),
                  '清空聊天记录': (MobileBy.ID, 'com.chinasofti.rcs:id/left_empty_chat_tv'),
                  '删除并退出': (MobileBy.ID, 'com.chinasofti.rcs:id/delete_and_exit'),
                  "确认": (MobileBy.XPATH, '//*[@text ="确认"]'),
                  # "确定": (MobileBy.XPATH, '//*[@text ="确定"]'),
                  "取消": (MobileBy.XPATH, '//*[@text ="取消"]'),
                  "退出": (MobileBy.XPATH, '//*[@text ="退出"]'),
                  "日志转聊天(开启后会将单聊消息发送给接收人)": (MobileBy.XPATH, '//*[@text ="日志转聊天(开启后会将单聊消息发送给接收人)"]'),
                  "分享至当前群(开启后将发送至当前群)": (MobileBy.XPATH, '//*[@text ="分享至当前群(开启后将发送至当前群)"]'),
                  '群成员': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_head'),
                  '完成': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name_save'),
                  '修改群名或群名片返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  'X按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
                  '群名片完成': (MobileBy.ID, 'com.chinasofti.rcs:id/group_card_save'),
                  '二维码转发': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_share_btn'),
                  '二维码下载': (MobileBy.ID, 'com.chinasofti.rcs:id/qecode_save_btn'),
                  '二维码返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '群管理返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '群主管理权转让': (MobileBy.ID, 'com.chinasofti.rcs:id/group_transfer'),
                  '解散群': (MobileBy.ID, 'com.chinasofti.rcs:id/group_disband'),
                  '添加桌面快捷方式': (MobileBy.XPATH, '//*[@text ="添加桌面快捷方式"]'),
                  '我知道': (MobileBy.XPATH, '//*[@text ="我知道了"]'),

                  "二维码重置": (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_icon'),

                  # 邀请分享群口令
                  '分享群口令框': (MobileBy.XPATH, '//*[@text ="分享群口令邀请好友进群"]'),
                  '下次再说': (MobileBy.XPATH, '//*[@text ="下次再说"]'),
                  '立即分享': (MobileBy.XPATH, '//*[@text ="立即分享"]'),
                  "再次邀请": (MobileBy.XPATH, '//*[@text="还有人未进群,再次邀请"]'),
                  '群名片': (MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name'),
                  '群名称': (MobileBy.ID, 'com.chinasofti.rcs:id/group_name'),
                  "邀请微信或QQ好友进群": (MobileBy.ID, 'com.chinasofti.rcs:id/group_password_line'),
                  "设置你在群内显示的昵称": (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  '搜索结果列表': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
                  '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),

                  '删除联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_delete_contact'),
                  '群成员头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
                  '邀请微信或QQ好友进群小红点': (MobileBy.ID, 'com.chinasofti.rcs:id/group_password_red'),
                  '分享群口令框内容': (MobileBy.ID, 'com.chinasofti.rcs:id/cpntent_tv'),
                  '分享到QQ': (MobileBy.ID, 'com.chinasofti.rcs:id/qq_view'),
                  '分享到微信': (MobileBy.ID, 'com.chinasofti.rcs:id/wechat_view'),
                  '第一个群成员头像': (MobileBy.XPATH, '(//*[contains(@resource-id,"com.chinasofti.rcs:id/head_tv")])[1]'),
                  '删除成员': (MobileBy.XPATH, '(//*[contains(@resource-id,"com.chinasofti.rcs:id/iv_head")])[last()]'),
                  '移除群成员确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '不再提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_show_again'),
                  '快捷方式-确定添加': (MobileBy.ID, 'android:id/button1'),

                  }

    @TestLogger.log("获取控件数量")
    def get_element_count(self):
        els = self.get_elements(self.__locators["再次邀请"])
        return len(els)

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待群聊设置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("群聊设置")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_modify_groupname_load(self, timeout=8, auto_accept_alerts=True):
        """等待修改群名称页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("修改群名称")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_modify_mygroupname_load(self, timeout=8, auto_accept_alerts=True):
        """等待修改群名片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("修改群名片")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def _find_menu(self, locator):
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.swipe_by_direction(self.__locators['菜单区域'], 'up')
            if self._is_element_present(locator):
                return
            self.swipe_by_direction(self.__locators['菜单区域'], 'down')
            if self._is_element_present(locator):
                return
            raise AssertionError('页面找不到元素：{}'.format(locator))

    @TestLogger.log()
    def get_group_total_member(self):
        """获取群成员总人数"""
        self._find_menu(self.__class__.__locators['群成员(2人)'])
        el = self.get_element(self.__class__.__locators['群成员(2人)'])
        res = re.search(r"\d+", el.text)
        if res:
            return int(res.group())
        else:
            return 0

    @TestLogger.log()
    def click_group_member_show(self):
        """点击群成员展示>"""
        self._find_menu(self.__class__.__locators['群成员展开>'])
        self.click_element(self.__class__.__locators["群成员展开>"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_avetor_qq_wechat_friend(self):
        """点击邀请进群"""
        self.click_element(self.__class__.__locators["邀请微信或QQ好友进群"])

    @TestLogger.log()
    def click_add_member(self):
        """点击 '+ ': 添加成员"""
        self._find_menu((MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]'))
        self.driver.find_elements(MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]')[-2].click()



    @TestLogger.log()
    def click_del_member(self):
        """点击 '-': 删除成员"""
        self._find_menu((MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]'))
        self.driver.find_elements(MobileBy.XPATH, '//*[@resource-id ="com.chinasofti.rcs:id/tv_name"]')[-1].click()

    @TestLogger.log()
    def click_modify_group_name(self):
        """点击 修改群聊名称"""
        self._find_menu(self.__locators['修改群聊名称'])
        self.click_element(self.__locators['修改群聊名称'])

    @TestLogger.log()
    def click_modify_my_group_name(self):
        """点击 修改群名片"""
        self._find_menu(self.__locators['群名片'])
        self.click_element(self.__locators['群名片'])

    @TestLogger.log()
    def click_QRCode(self):
        """点击群二维码"""
        self.click_element(self.__locators['群二维码'])

    @TestLogger.log()
    def click_my_card(self):
        """点击我在本群的昵称"""
        self._find_menu(self.__locators['我在本群的昵称'])
        self.click_element(self.__locators['我在本群的昵称'])

    @TestLogger.log()
    def click_group_manage(self):
        """点击群管理"""
        self._find_menu(self.__locators['群管理'])
        self.click_element(self.__locators['群管理'])

    @TestLogger.log()
    def click_switch_undisturb(self):
        """点击消息免打扰开关"""
        self._find_menu(self.__locators['消息免打扰开关'])
        self.click_element(self.__locators['消息免打扰开关'])

    @TestLogger.log()
    def click_btn_logout(self):
        """点击消息免打扰开关"""
        self.click_element(self.__locators['退出'])

    @TestLogger.log()
    def get_switch_undisturb_status(self):
        """获取消息免打扰开关状态"""
        self._find_menu(self.__locators['消息免打扰开关'])
        el = self.get_element(self.__locators['消息免打扰开关'])
        return el.get_attribute("checked") == "true"

    @TestLogger.log()
    def get_chat_set_to_top_switch_status(self):
        """获取置顶聊天开关状态"""
        self._find_menu(self.__locators['置顶聊天开关'])
        el = self.get_element(self.__locators['置顶聊天开关'])
        return el.get_attribute("checked") == "true"

    @TestLogger.log()
    def click_chat_set_to_top_switch(self):
        """点击置顶聊天开关"""
        self._find_menu(self.__locators['置顶聊天开关'])
        self.click_element(self.__locators['置顶聊天开关'])

    @TestLogger.log()
    def click_find_chat_record(self):
        """点击查找聊天内容"""
        self._find_menu(self.__locators['查找聊天内容'])
        self.click_element(self.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_clear_chat_record(self):
        """点击清空聊天记录"""
        self._find_menu(self.__locators['清空聊天记录'])
        self.click_element(self.__locators['清空聊天记录'])

    @TestLogger.log()
    def click_clear_chat_record2(self):
        """群聊设置页面 点击清空聊天记录2"""
        self._find_menu(self.__locators['清空聊天记录2'])
        self.click_element(self.__locators['清空聊天记录2'])

    @TestLogger.log()
    def find_element_share2group_text(self):
        """分享至当前群"""
        self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)
        self._find_menu(self.__locators['分享至当前群(开启后将发送至当前群)'])
        el = self.get_element(self.__locators['分享至当前群(开启后将发送至当前群)'])
        return el.get_attribute("checked")

    @TestLogger.log()
    def find_element_daily2chat_text(self):
        """日志转聊天"""
        self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)
        self._find_menu(self.__locators['日志转聊天(开启后会将单聊消息发送给接收人)'])
        el = self.get_element(self.__locators['日志转聊天(开启后会将单聊消息发送给接收人)'])
        return el.get_attribute("checked")

    @TestLogger.log()
    def click_element_share2group_text(self):
        """分享至当前群"""
        # self._find_menu(self.__locators['分享至当前群(开启后将发送至当前群)'])
        self.swipe_by_percent_on_screen(50, 72, 50, 36, 800)
        time.sleep(1)
        el = self.get_element(self.__locators['分享至当前群(开启后将发送至当前群)'])
        el.click()
        time.sleep(3)
        print("---------- = " + str(el.get_attribute("checked")))
        return el.get_attribute("checked")

    @TestLogger.log()
    def click_delete_and_exit(self):
        """点击删除并退出"""
        self._find_menu(self.__locators['删除并退出'])
        self.click_element(self.__locators['删除并退出'])
        time.sleep(2)
        if self.get_elements(self.__locators["确定"]):
            self.click_element(self.__locators['确定'])
        time.sleep(3)

    @TestLogger.log()
    def click_dismiss(self):
        """解散群"""
        self.click_group_manage()
        time.sleep(2)
        self.click_group_manage_disband_button()
        time.sleep(2)
        self.click_sure()
        time.sleep(3)

    @TestLogger.log()
    def click_delete_and_exit2(self):
        """点击删除并退出"""
        self._find_menu(self.__locators['删除并退出'])
        self.click_element(self.__locators['删除并退出'])

    @TestLogger.log()
    def wait_clear_chat_record_confirmation_box_load(self, timeout=10, auto_accept_alerts=True):
        """等待 聊天记录清除确认框"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("是否清空聊天记录")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_text(self, text, timeout=10, auto_accept_alerts=True):
        """等待文字"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present(text)
            )
        except:
            message = "文字在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_exist_and_delete_confirmation_box_load(self, timeout=10, auto_accept_alerts=True):
        """等待 解散群成员确认框加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("解散群")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_confirm(self):
        """点击确认"""
        self.click_element(self.__locators['确认'])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__locators['取消'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['群聊设置'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log()
    def click_determine(self):
        """点击确定"""
        self.click_element(self.__locators['确定'])

    @TestLogger.log()
    def click_search_chat_record(self):
        """点击 查找聊天内容"""
        self._find_menu(self.__class__.__locators['查找聊天内容'])
        self.click_element(self.__class__.__locators['查找聊天内容'])

    @TestLogger.log()
    def click_add_member(self):
        """点击 “+”添加成员"""
        els = self.get_elements(self.__class__.__locators['群成员'])
        els[-2].click()

    @TestLogger.log()
    def clear_group_name(self):
        """清空群名称"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'))
        el.clear()

    @TestLogger.log()
    def is_enabled_of_group_name_save_button(self):
        """判断群名称保存按钮是否置灰"""
        return self._is_enabled(self.__class__.__locators['完成'])

    @TestLogger.log()
    def input_new_group_name(self, message):
        """输入新群名"""
        self.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'), message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def save_group_name(self):
        """保存新群名"""
        self.click_element(self.__class__.__locators['完成'])

    @TestLogger.log()
    def check_new_group_name(self, new_name):
        """确定新群名"""
        from unittest import TestCase
        return TestCase().assertEqual(self.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), new_name)

    @TestLogger.log()
    def is_enabled_of_save_group_name_button(self):
        """判断群名称保存按钮是否置灰"""
        return self._is_enabled(self.__class__.__locators['完成'])

    @TestLogger.log()
    def click_edit_group_name_back(self):
        """修改群名返回"""
        self.click_element(self.__class__.__locators['修改群名或群名片返回'])

    @TestLogger.log()
    def is_iv_delete_exit(self):
        """判断X按钮是否存在"""
        if self.get_element(self.__class__.__locators["X按钮"]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_iv_delete_button(self):
        """点击X按钮"""
        self.click_element(self.__class__.__locators["X按钮"])

    @TestLogger.log()
    def get_edit_query_text(self):
        """获取输入框文本"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'))
        text = el.get_attribute("text")
        return text

    @TestLogger.log()
    def click_edit_group_card_back(self):
        """修改群名片返回"""
        self.click_element(self.__class__.__locators['修改群名或群名片返回'])

    @TestLogger.log()
    def save_group_card_name(self):
        """保存新群名片名字"""
        self.click_element(self.__class__.__locators['群名片完成'])

    @TestLogger.log()
    def is_enabled_of_group_card_save_button(self):
        """判断群名片保存按钮是否置灰"""
        return self._is_enabled(self.__class__.__locators['群名片完成'])

    @TestLogger.log()
    def wait_for_qecode_load(self, timeout=15, auto_accept_alerts=True):
        """等待群二维码加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("该二维码7天内")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_qecode_share_button(self):
        """点击群二维码分享按钮"""
        times = 10
        while times > 0:
            time.sleep(1)
            if self.get_elements(self.__class__.__locators['二维码转发']):
                self.click_element(self.__class__.__locators['二维码转发'])
                break
            else:
                times -= 1
                if self.get_elements(self.__class__.__locators['二维码重置']):
                    self.click_element(self.__class__.__locators['二维码重置'])
                    time.sleep(1)

        return False

    @TestLogger.log()
    def click_qecode_download_button(self):
        """点击群二维码下载按钮"""
        times = 10
        while times > 0:
            time.sleep(1)
            if self.get_elements(self.__class__.__locators['二维码下载']):
                self.click_element(self.__class__.__locators['二维码下载'])
                break
            else:
                times -= 1
                if self.get_elements(self.__class__.__locators['二维码重置']):
                    self.click_element(self.__class__.__locators['二维码重置'])
                    time.sleep(1)

        return False

    @TestLogger.log()
    def click_qecode_back_button(self):
        """点击群二维码页面返回按钮"""
        self.click_element(self.__class__.__locators['二维码返回'])

    @TestLogger.log()
    def wait_for_group_manage_load(self, timeout=8, auto_accept_alerts=True):
        """等待群管理页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("群管理")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_group_manage_back_button(self):
        """点击群管理页面返回按钮"""
        self.click_element(self.__class__.__locators['群管理返回'])

    @TestLogger.log()
    def click_group_manage_transfer_button(self):
        """点击群主管理权转让按钮"""
        self.click_element(self.__class__.__locators['群主管理权转让'])

    @TestLogger.log()
    def click_group_manage_disband_button(self):
        """点击解散群按钮"""
        self.click_element(self.__class__.__locators['解散群'])

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log("点击添加成员")
    def click_add_number(self):
        els = self.get_elements(self.__locators["com.chinasofti.rcs:id/iv_avatar"])
        el = els[1]
        el.click()

    @TestLogger.log()
    def wait_for_share_group_load(self, timeout=15, auto_accept_alerts=True):
        """等待群管理页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("分享群口令邀请好友进群")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_my_group_name(self):
        """获取我的群聊名片名称"""
        el = self.get_element(self.__class__.__locators["群名片"])
        return el.text

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_say_next(self):
        """点击下次再说"""
        self.click_element(self.__class__.__locators["下次再说"])

    @TestLogger.log()
    def click_add_destop_link(self):
        """点击添加桌面快捷方式"""
        self._find_menu(self.__locators['添加桌面快捷方式'])
        self.click_element(self.__locators['添加桌面快捷方式'])
        time.sleep(1)

    @TestLogger.log()
    def check_element_for_add_destop_link(self):
        """添加桌面快捷方式元素校验"""
        self.page_should_contain_text("已尝试添加到桌面")
        self.page_should_contain_text("若添加失败，请在手机系统设置中为和飞信打开“创建桌面快捷方式”的权限")
        self.page_should_contain_text("我知道了")
        self.page_should_contain_text("不再提醒")

    @TestLogger.log()
    def click_iknow_but(self):
        """点击我知道"""
        self.click_element(self.__locators['我知道'])

    @TestLogger.log()
    def group_avatar_is_exist(self):
        """群头像存在性校验"""
        self.page_should_contain_element(self.__class__.__locators['com.chinasofti.rcs:id/iv_avatar'])

    @TestLogger.log()
    def group_name_is_exist(self):
        """群昵称存在性校验"""
        self.page_should_contain_element(self.__class__.__locators['com.chinasofti.rcs:id/tv_name'])

    @TestLogger.log()
    def group_chairman_tag_is_exist(self):
        """群昵称存在性校验"""
        self.page_should_contain_element(self.__class__.__locators['com.chinasofti.rcs:id/iv_group_chairman_tag'])

    @TestLogger.log()
    def check_group_nickname(self, name):
        """群昵称存在性校验"""
        from unittest import TestCase
        return TestCase().assertEqual(self.get_text(self.__class__.__locators['群名片']), name)

    @TestLogger.log()
    def click_group_avatars(self):
        """点击群二维码"""
        self.click_element(self.__class__.__locators["com.chinasofti.rcs:id/rl_group_avatars"])

    @TestLogger.log()
    def input_my_group_card_name(self, message):
        """输入你在群内显示的昵称"""
        self.input_text(self.__class__.__locators["设置你在群内显示的昵称"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def save_btn_is_enabled(self):
        """获取修改群名片完成按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["群名片完成"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['群聊设置'])
        if len(el) > 0:
            return True
        return False

    # @TestLogger.log('搜索结果是否存在')
    # def is_element_present_result(self):
    #     return self._is_element_present(self.__locators['搜索结果列表'])

    @TestLogger.log()
    def is_exist_present_result(self):
        """是否存在搜索结果"""
        el = self.get_elements(self.__locators['搜索结果列表'])
        if len(el) == 0:
            return False
        return True

    @TestLogger.log()
    def click_edit_query(self):
        """点击 输入关键词快速搜索"""
        self.click_element(self.__class__.__locators['输入关键词快速搜索'])

    @TestLogger.log()
    def input_search_message(self, message):
        """输入搜索信息"""
        self.input_text(self.__class__.__locators["输入关键词快速搜索"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def group_member_avatar_is_exist(self):
        """群成员头像存在性校验"""
        return self.page_should_contain_element(self.__class__.__locators['群成员头像'])

    @TestLogger.log()
    def click_group_member_avatar(self):
        """点击群成员头像"""
        self.click_element(self.__class__.__locators['群成员头像'])

    @TestLogger.log()
    def is_exist_invite_red_dot(self):
        """是否存在邀请微信或QQ好友进群小红点"""
        return self._is_element_present(self.__class__.__locators["邀请微信或QQ好友进群小红点"])

    @TestLogger.log()
    def click_share_now(self):
        """点击立即分享"""
        self.click_element(self.__class__.__locators['立即分享'])

    @TestLogger.log()
    def wait_for_share_group_password_invite_friend(self, timeout=10, auto_accept_alerts=True):
        """等待 分享群口令邀请好友进群"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("分享群口令邀请好友进群")
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_share_qq(self):
        """点击分享到QQ"""
        self.click_element(self.__class__.__locators['分享到QQ'])

    @TestLogger.log()
    def click_share_wechat(self):
        """点击分享到微信"""
        self.click_element(self.__class__.__locators['分享到微信'])

    @TestLogger.log()
    def click_first_group_member_avatar(self):
        """点击第一个群成员头像"""
        self.click_element(self.__class__.__locators['第一个群成员头像'])

    @TestLogger.log()
    def click_delete_member(self):
        """点击删除成员"""
        self.click_element(self.__class__.__locators['删除成员'])

    @TestLogger.log()
    def click_delete_member_sure(self):
        """点击移除群成员确定"""
        self.click_element(self.__class__.__locators['移除群成员确定'])

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators['确定'])

    @TestLogger.log()
    def click_no_show_again(self):
        """点击不再提醒"""
        self.click_element(self.__class__.__locators['不再提醒'])

    @TestLogger.log()
    def click_sure_add_desktop_shortcut(self):
        """点击确定添加快捷方式"""
        time.sleep(1)
        self.click_element(self.__locators["快捷方式-确定添加"])

    @TestLogger.log()
    def get_element_c(self, locator):
        return self.get_element(self.__locators[locator])

    @TestLogger.log()
    def is_element_present_c(self, locator):
        try:
            if self.get_element(self.__locators[locator]):
                return True
            else:
                return False
        except:
            return False
