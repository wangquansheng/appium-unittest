from operator import eq
from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class GroupChatPage(BaseChatPage):
    """群聊天页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  'com.chinasofti.rcs:id/back_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '返回2': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
                  '返回3': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  '关闭返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_close_actionbar'),
                  '群聊001(2)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '消息免打扰': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_slient'),
                  '多方通话': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  '14:58': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'frank': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '[呲牙1]': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '呵呵': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'mobile0489': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  'APP test': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '选择名片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  '文件发送成功标志': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '选择照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '发送失败标识': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '编辑': (MobileBy.XPATH, "//*[contains(@text, '编辑')]"),
                  '发送': (MobileBy.XPATH, "//*[contains(@text, '发送')]"),
                  '保存图片': (MobileBy.XPATH, "//*[contains(@text, '保存图片')]"),
                  '我知道了': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok'),
                  '勾': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '重发消息确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '位置返回': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
                  '表情按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/gv_expression'),
                  '表情': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_expression_image'),
                  '输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  '关闭表情页': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression_keyboard'),
                  '多选返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '多选计数': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_count'),
                  '多选选择框': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_check'),
                  '多选删除': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_delete'),
                  '多选转发': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_forward'),
                  '删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消删除已选信息': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  "返回上一级": (MobileBy.ID, "com.chinasofti.rcs:id/left_back"),
                  "文本发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_send"),
                  "语音小红点": (MobileBy.ID, "com.chinasofti.rcs:id/ib_record_red_dot"),
                  "粘贴": (MobileBy.ID, "com.chinasofti.rcs:id/ib_pic"),
                  "照片选择框": (MobileBy.ID, "com.chinasofti.rcs:id/iv_select"),
                  "更多小红点": (MobileBy.ID, "com.chinasofti.rcs:id/id_more_red_dot"),
                  "预览文件_返回": (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '预览文件_更多': (MobileBy.ID, 'com.chinasofti.rcs:id/menu'),
                  '定位_地图': ('id', 'com.chinasofti.rcs:id/location_info_view'),
                  '始终允许': (MobileBy.XPATH, "//*[contains(@text, '始终允许')]"),
                  '文本消息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '群成员': (MobileBy.XPATH, "//*[contains(@text, '群成员')]"),
                  '搜索成员输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                  '群成员头像': (MobileBy.ID, 'com.chinasofti.rcs:id/head_tv'),
                  '已读动态': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_has_read'),
                  '置顶聊天': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_set_to_top_switch'),
                  '移除群成员减号': (MobileBy.XPATH,
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[4]/android.view.View"),
                  '确定移除': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消移除': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  '富媒体拍照': ('id', 'com.chinasofti.rcs:id/ib_take_photo'),
                  '语音按钮': ('id', 'com.chinasofti.rcs:id/ib_audio'),
                  '加入群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/group_qr_apply_enter'),
                  '添加群成员加号': (MobileBy.XPATH,
                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]/android.view.View"),
                  '文件': ('id', 'com.chinasofti.rcs:id/ib_file'),
                  '超过20M图片': ('id', 'com.chinasofti.rcs:id/layout_loading'),
                  '放大的图片': (
                      MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/vp_preview"]/android.widget.ImageView'),
                  '关闭视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_close'),
                  '视频播放': (MobileBy.ID, 'com.chinasofti.rcs:id/video_play'),
                  '群聊拍照': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  '企业群成员头像': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_icon'),
                  '飞信电话(免费)': (MobileBy.XPATH, '//*[@text="飞信电话（免费）"]'),
                  '多方视频': (MobileBy.XPATH, '//*[@text="多方视频"]'),
                  '多方视频接听': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAnswer'),
                  '多方视频挂断': (MobileBy.ID, 'com.chinasofti.rcs:id/ivCancel'),
                  '结束多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/end_video_call_btn'),
                  '多方视频缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_hide'),
                  '消息根节点': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]/*'),
                  '下拉菜单箭头': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/drop_down_image"]'),
                  '下拉菜单选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/albumTitle"]'),
                  '列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]'),
                  '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]/*['
                                          '@resource-id="com.chinasofti.rcs:id/rl_img"]'),
                  '选择': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_select"]'),
                  '原图': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/cb_original_photo"]'),
                  '预览': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_preview"]'),
                  '结束双人视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_term'),
                  '设置小红点': (MobileBy.ID, 'com.chinasofti.rcs:id/red_view'),
                  '群短信': (MobileBy.XPATH, '//*[@text="群短信"]'),
                  '名片': (MobileBy.XPATH, '//*[@text="名片"]'),
                  '位置': (MobileBy.XPATH, '//*[@text="位置"]'),
                  '红包': (MobileBy.XPATH, '//*[@text="红包"]'),
                  '飞信电话': (MobileBy.XPATH, '//*[@text="飞信电话"]'),

                  '飞信电话缩放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/smart_multi_call_hide'),
                  '飞信电话会控加号': (MobileBy.ID, 'com.chinasofti.rcs:id/ivAvatar'),
                  '飞信电话会控全员禁音': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_group_mute'),
                  '挂断和飞信电话': (MobileBy.ID, 'com.chinasofti.rcs:id/ivDecline'),
                  '同时发送语音+文字(语音识别)': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_and_text'),
                  '语音发送模式确定': (MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'),
                  '发送者姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/text_name'),
                  '信息体': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  '切换': (MobileBy.ID, 'android:id/button1'),
                  '不切换': (MobileBy.ID, 'android:id/button2'),
                  # 审批页面
                  # '请假': (MobileBy.ID, 'android:id/button2'),
                  # '加班': (MobileBy.ID, 'android:id/button2'),
                  # '外出': (MobileBy.ID, 'android:id/button2'),
                  # '出差': (MobileBy.ID, 'android:id/button2'),
                  # '报销': (MobileBy.ID, 'android:id/button2'),
                  # '备用金': (MobileBy.ID, 'android:id/button2'),
                  # '用车': (MobileBy.ID, 'android:id/button2'),
                  # '物品领用': (MobileBy.ID, 'android:id/button2'),
                  # '采购': (MobileBy.ID, 'android:id/button2'),
                  # '用章': (MobileBy.ID, 'android:id/button2'),
                  # '通用审批': (MobileBy.ID, 'android:id/button2'),
                  }

    @TestLogger.log()
    def click_collection(self):
        """点击保存图片"""
        self.click_element(self.__class__.__locators["收藏"])

    @TestLogger.log()
    def click_muti_select(self):
        """点击保存图片"""
        self.click_element(self.__class__.__locators["多选"])

    def is_on_this_page_631(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['选择照片'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def close_pic_preview(self):
        """退出图片阅览"""
        self.click_element(self.__class__.__locators['放大的图片'])

    @TestLogger.log()
    def click_selection_forward(self):
        """点击转发"""
        self.click_element(self.__class__.__locators["转发"])

    @TestLogger.log()
    def click_save_picture(self):
        """点击保存图片"""
        self.click_element(self.__class__.__locators["保存图片"])

    @TestLogger.log()
    def click_file(self):
        """点击文件"""
        self.click_element(self.__class__.__locators["文件"])

    @TestLogger.log()
    def click_network_switch(self):
        self.click_element(self.__class__.__locators["切换"])

    @TestLogger.log()
    def click_send_failed(self):
        """点击发送失败标识"""
        self.click_element(self.__class__.__locators["发送失败标识"])

    @TestLogger.log()
    def click_edit(self):
        """点击编辑"""
        self.click_element(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def is_exist_btn(self, text):
        """是否存在各个功能按钮"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def is_exist_edit_page(self):
        """长按消息"""
        for option in ["收藏", "转发", "多选", "编辑", "删除"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True

    @TestLogger.log()
    def is_exist_picture_edit_page(self):
        """长按消息"""
        for option in ["转发", "编辑", "保存图片"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True

    @TestLogger.log()
    def click_picture_msg(self):
        """点击消息"""
        els = self.get_elements(self.__locators['超过20M图片'])
        els[-1].click()

    @TestLogger.log()
    def press_picture(self):
        """长按消息"""
        els = self.get_elements(self.__locators['超过20M图片'])
        self.press(els[-1])

    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__locators['消息视频'])
        return len(el) > 0

    def is_multi_show(self):
        """判断当前是否聚合展示"""
        el = self.get_elements(self.__locators['com.chinasofti.rcs:id/svd_head'])
        return len(el) == 1

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def click_msg_image(self, number):
        """点击图片消息"""
        els = self.get_elements(self.__class__.__locators["消息图片"])
        els[number].click()

    @TestLogger.log()
    def is_exists_group_by_name(self, name):
        """是否存在指定群聊名"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/title" and contains(@text, "%s")]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_collection(self):
        """是否存在消息已收藏"""
        return self.is_toast_exist("已收藏")

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def click_take_picture(self):
        """点击选择富媒体拍照"""
        self.click_element(self.__class__.__locators["富媒体拍照"])

    @TestLogger.log()
    def click_take_picture2(self):
        """点击-群聊拍照"""
        self.click_element(self.__class__.__locators["群聊拍照"])

    @TestLogger.log()
    def is_send_sucess(self):
        """当前页面是否有发送失败标识"""
        el = self.get_elements(self.__locators['发送失败标识'])
        if len(el) > 0:
            return False
        return True

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def click_setting(self):
        """点击设置"""
        self.click_element(self.__class__.__locators["设置"])
        time.sleep(1)

    @TestLogger.log()
    def is_exist_setting_btn(self):
        """是否存在 设置按钮"""
        return self.is_element_exit_("设置")

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待群聊页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方通话"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['多方通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_profile(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_back2(self):
        """点击返回按钮(审批页面)"""
        self.click_element(self.__class__.__locators["返回2"])

    @TestLogger.log()
    def click_close_back(self):
        """点击返回按钮(审批页面)"""
        self.click_element(self.__class__.__locators["关闭返回"])

    @TestLogger.log()
    def is_exist_undisturb(self):
        """是否存在消息免打扰标志"""
        return self._is_element_present(self.__class__.__locators["消息免打扰"])

    @TestLogger.log()
    def click_more(self):
        """点击更多富媒体按钮"""
        self.click_element(self.__class__.__locators["更多"], default_timeout=8)
        time.sleep(1)

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_file(self, file):
        """长按指定文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)

    @TestLogger.log()
    def is_address_text_present(self):
        """判断位置信息是否在群聊页面发送"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def press_message_to_do(self, text):
        """长按指定信息进行操作"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def wait_for_message_down_file(self, timeout=20, auto_accept_alerts=True):
        """等待消息发送成功"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["勾"])
            )
        except:
            message = "消息在{}s内，没有发送成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_exist_network(self):
        """是否存网络不可用"""
        return self.is_toast_exist("网络不可用，请检查网络设置")

    @TestLogger.log()
    def click_send_again(self):
        """点击重新发送gif"""
        self.click_element(self.__class__.__locators["发送失败标识"])
        self.click_element(self.__class__.__locators["重发消息确定"])

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """判断是否有重发按钮"""
        el = self.get_elements(self.__locators['重发按钮'])
        return len(el) > 0

    @TestLogger.log()
    def click_msg_send_failed_button(self):
        """点击重发按钮"""
        self.click_element(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_resend_confirm(self):
        """点击重发消息确定"""
        self.click_element(self.__class__.__locators["重发消息确定"])

    @TestLogger.log()
    def click_clean_video(self):
        """点击删除消息视频"""
        try:
            el = self.get_element(self.__class__.__locators["消息视频"])
            self.press(el)
            self.click_element(self.__class__.__locators["删除"])
        except:
            pass
        return self

    @TestLogger.log()
    def press_voice_message_to_do(self, text):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_message_longclick(self):
        """长按消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)

    @TestLogger.log()
    def press_message_longclick2(self):
        """长按文本消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        self.press(el)

    @TestLogger.log()
    def press_the_message_by_text(self, text):
        """长按指定文本消息"""
        els = self.get_elements(self.__class__.__locators["信息体"])

        if els:
            for el in els:
                print("------------" + el.text)
                if el.text == text:
                    print("------------" + el.text)
                    tmpel = el
                    break
        self.press(tmpel)

    @TestLogger.log()
    def click_message(self, text):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def get_width_of_msg_of_text(self):
        """获取文本信息框的大小"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        rect = el.rect
        return rect["width"]

    @TestLogger.log()
    def is_call_page_load(self):
        """判断是否可以发起呼叫"""
        el = self.get_element((MobileBy.ID, 'com.android.incallui:id/endButton'))
        if el:
            return True
        else:
            return False

    @TestLogger.log()
    def click_end_call_button(self):
        """点击结束呼叫按钮 """
        self.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @TestLogger.log()
    def click_location_back(self):
        """点击位置页面返回 """
        self.click_element(self.__class__.__locators['位置返回'])

    @TestLogger.log()
    def click_expression_button(self):
        """点击表情按钮"""
        self.click_element(self.__class__.__locators["表情按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_exist_expression_page(self):
        """是否存在表情页"""
        return self._is_element_present(self.__class__.__locators["表情页"])

    @TestLogger.log()
    def click_expression_page_close_button(self):
        """点击表情页关闭"""
        if self._is_element_present(self.__class__.__locators["关闭表情页"]):
            self.click_element(self.__class__.__locators["关闭表情页"])

    @TestLogger.log()
    def get_expressions(self):
        """获取表情包"""
        els = self.get_elements(self.__locators['表情'])
        return els

    @TestLogger.log()
    def get_input_box(self):
        """获取输入框"""
        el = self.get_element(self.__locators['输入框'])
        return el

    @TestLogger.log()
    def click_input_box(self):
        """获取输入框"""
        self.click_element(self.__locators['输入框'])

    @TestLogger.log()
    def is_enabled_of_send_button(self):
        """发送按钮状态"""
        flag = self._is_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'))
        return flag

    @TestLogger.log()
    def is_exist_multiple_selection_back(self):
        """是否存在多选【×】关闭按钮"""
        return self._is_element_present(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_count(self):
        """是否存在多选计数"""
        return self._is_element_present(self.__class__.__locators["多选计数"])

    @TestLogger.log()
    def get_multiple_selection_select_box(self):
        """获取多选选择框"""
        els = self.get_elements(self.__class__.__locators["多选选择框"])
        if els:
            return els
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def get_check_all_not_selected(self):
        """勾选所有未勾选的内容"""
        els = self.get_elements(self.__class__.__locators["多选选择框"])
        if els:
            for el in els:
                if eq(el.get_attribute('checked'), 'false'):
                    el.click()
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def is_enabled_multiple_selection_delete(self):
        """判断多选删除是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def is_enabled_multiple_selection_forward(self):
        """判断多选转发是否高亮展示"""
        return self._is_enabled(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def click_multiple_selection_back(self):
        """点击多选返回"""
        self.click_element(self.__class__.__locators["多选返回"])

    @TestLogger.log()
    def is_exist_multiple_selection_select_box(self):
        """是否存在多选选择框"""
        return self._is_element_present(self.__class__.__locators["多选选择框"])

    @TestLogger.log()
    def click_multiple_selection_delete(self):
        """点击多选删除"""
        self.click_element(self.__class__.__locators["多选删除"])

    @TestLogger.log()
    def click_multiple_selection_delete_cancel(self):
        """点击取消删除已选信息"""
        self.click_element(self.__class__.__locators["取消删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_delete_sure(self):
        """点击确定删除已选信息"""
        self.click_element(self.__class__.__locators["删除已选信息"])

    @TestLogger.log()
    def click_multiple_selection_forward(self):
        """点击多选转发"""
        self.click_element(self.__class__.__locators["多选转发"])

    @TestLogger.log()
    def press_audio_to_do(self, text):
        """长按语音消息体进行操作"""
        els = self.get_elements(self.__class__.__locators["语音消息体"])
        if els:
            self.press(els[0])
            self.click_element(self.__class__.__locators[text])
        else:
            raise AssertionError("没有找到语音消息体")

    @TestLogger.log()
    def press_audio(self):
        """长按语音消息体进行操作"""
        els = self.get_elements(self.__class__.__locators["语音消息体"])
        if els:
            self.press(els[0])
        else:
            raise AssertionError("没有找到语音消息体")

    @TestLogger.log()
    def get_group_name(self):
        """在群聊页面获取群聊名称"""
        return self.get_element(self.__class__.__locators['群聊001(2)']).text

    @TestLogger.log()
    def get_multiple_selection_count(self):
        """获取多选计数框"""
        el = self.get_element(self.__class__.__locators["多选计数"])
        if el:
            return el
        else:
            raise AssertionError("没有找到多选选择框")

    @TestLogger.log()
    def press_voice_message(self):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/linearlayout_msg_content'))
        self.press(el)

    @TestLogger.log()
    def press_text_message(self):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        self.press(el)

    @TestLogger.log()
    def get_text_message(self):
        """长按语言消息体"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        return el.text

    @TestLogger.log()
    def click_return(self):
        """返回上一级"""
        self.click_element(self.__class__.__locators["返回上一级"])

    @TestLogger.log()
    def return_btn_is_exist(self):
        """返回上一级"""
        self.page_should_contain_element(self.__class__.__locators["返回上一级"])

    @TestLogger.log()
    def get_height_of_msg_of_text(self):
        """获取文本信息框的大小"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        rect = el.rect
        return rect["height"]

    @TestLogger.log()
    def get_msg_of_text(self):
        """获取文本信息框的信息"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'))
        text = el.text
        return text

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["输入框"], message)
        return self

    @TestLogger.log()
    def send_text(self):
        """发送文本"""
        self.click_element(self.__class__.__locators["文本发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_exist_red_dot(self):
        """是否存在语音小红点"""
        return self._is_element_present(self.__class__.__locators["语音小红点"])

    @TestLogger.log()
    def click_long_copy_message(self):
        """输入文本信息"""
        self.click_element(self.__locators["输入框"])
        el = self.get_element(self.__locators["输入框"])
        self.press(el)
        time.sleep(1.8)
        self.click_element(self.__locators["粘贴"])

    @TestLogger.log()
    def click_long_message(self):
        """输入文本信息"""
        el = self.get_elements(self.__locators["呵呵"])
        el = el[-1]
        el.click()

    @TestLogger.log()
    def click_mutilcall(self):
        """点击多方通话"""
        self.click_element(self.__class__.__locators["多方通话"])

    @TestLogger.log()
    def select_picture(self):
        """选择照片"""
        self.click_element(self.__class__.__locators["照片选择框"])

    @TestLogger.log("文件是否发送成功")
    def check_message_resend_success(self):
        return self._is_element_present(self.__class__.__locators['文件发送成功标志'])

    @TestLogger.log("当前页面是否有发文件消息")
    def is_exist_msg_file(self):
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        return len(el) > 0

    @TestLogger.log("删除当前群聊发送的文件")
    def delete_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['删除'])
        else:
            print('当前窗口没有可以删除的消息')

    @TestLogger.log("撤回文件")
    def recall_file(self, file):
        el = self.wait_until(
            condition=lambda x: self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file)))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log("点击发送的最后的文件")
    def click_last_file_send_fail(self):
        ele_list = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        ele_list[-1].click()

    @TestLogger.log("点击预览文件返回")
    def click_file_back(self):
        self.click_element(self.__locators['预览文件_返回'])

    @TestLogger.log("预览文件里的更多按钮是否存在")
    def is_exist_more_button(self):
        return self.wait_until(condition=lambda x: self._is_element_present(self.__locators['预览文件_更多']))

    @TestLogger.log("点击预览文件里的更多按钮")
    def click_more_button(self):
        self.click_element(self.__locators['预览文件_更多'])

    @TestLogger.log("检查预览文件选项是否可用")
    def check_options_is_enable(self):
        text_list = ['转发', '收藏', '其他应用打开']
        for text in text_list:
            if not self._is_enabled(('xpath', '//*[contains(@text, "{}")]'.format(text))):
                return False
        return True

    @TestLogger.log("通过文本点击元素")
    def click_element_by_text(self, text):
        ele = ('xpath', '//*[contains(@text, "{}")]'.format(text))
        self.click_element(ele)

    @TestLogger.log("当前页面是否有发地图消息")
    def is_exist_loc_msg(self):
        el = self.get_elements(self.__locators['定位_地图'])
        return len(el) > 0

    @TestLogger.log("撤回文件")
    def recall_file(self, file):
        el = self.wait_until(
            condition=lambda x: self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file)))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log("撤回位置消息")
    def recall_loc_msg(self):
        el = self.wait_until(
            condition=lambda x: self.get_elements(self.__locators['定位_地图']))
        self.press(el[-1])
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_message_text_by_number(self, number):
        """点击消息文本"""
        els = self.get_elements(self.__class__.__locators["文本消息"])
        els[number].click()

    @TestLogger.log()
    def press_message_text_by_number(self, number):
        """按压消息文本"""
        els = self.get_elements(self.__class__.__locators["文本消息"])
        self.press(els[number])

    @TestLogger.log()
    def is_exists_message_by_text(self, name):
        """是否存在指定文本消息"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and text="%s"]' % name)
        return self._is_element_present(locator)

    @TestLogger.log()
    def input_member_message(self, message):
        """输入搜索成员文本信息"""
        self.input_text(self.__class__.__locators["搜索成员输入框"], message)
        return self

    @TestLogger.log()
    def is_exist_msg_has_read_icon(self):
        """判断是否有已读动态标志"""
        el = self.get_elements(self.__locators['已读动态'])
        return len(el) > 0

    @TestLogger.log()
    def click_has_read_icon(self):
        """点击已读动态标志"""
        els = self.get_elements(self.__class__.__locators["已读动态"])
        els[-1].click()

    @TestLogger.log()
    def press_element_by_text(self, text, times):
        """依靠text长按元素"""
        locator = (MobileBy.XPATH, "//*[contains(@text, '%s')]" % text)
        el = self.get_element(locator)
        self.press(el, times)

    @TestLogger.log()
    def get_message_text_by_number(self, number=0):
        """按压消息文本"""
        els = self.get_elements(self.__class__.__locators["文本消息"])
        return els[number].get_attribute("text")

    @TestLogger.log()
    def press_element_(self, text, times):
        """长按元素"""
        el = self.get_element(self.__class__.__locators[text])
        self.press(el, times)

    @TestLogger.log()
    def wait_for_video_load(self, timeout=60, auto_accept_alerts=True):
        """等待群聊视频加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["视频播放"])
            )
        except:
            message = "视频在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('点击飞信电话(免费)')
    def click_hf_tel(self):
        """点击飞信电话(免费)"""
        self.click_element(self.__locators['飞信电话(免费)'])

    @TestLogger.log('点击多方视频')
    def click_multi_videos(self):
        """点击多方视频"""
        self.click_element(self.__locators['多方视频'])

    @TestLogger.log('点击始终允许')
    def click_always_allow(self):
        """点击始终允许"""
        self.click_element(self.__locators['始终允许'])

    @TestLogger.log()
    def press_last_file(self):
        """长按最后一个文件"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))[-1]
        self.press(el)

    @TestLogger.log()
    def press_last_message(self):
        """长按最后一个文本消息"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/tv_message'))[-1]
        self.press(el)

    @TestLogger.log()
    def press_last_message_to_do(self, text):
        """长按最后一个文本消息进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/tv_message'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_last_file_to_do(self, text):
        """长按最后一个文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_last_picture_to_do(self, text):
        """长按最后一个图片文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/layout_loading'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_last_video_to_do(self, text):
        """长按最后一个视频文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/video_thumb'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def is_exist_file_by_type(self, file_type):
        """是否存在指定类型文件"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and contains(@text,"%s")]' % file_type)
        return self._is_element_present(locator)

    @TestLogger.log('等待消息在指定时间内状态变为“加载中”、“发送失败”、“发送成功”中的一种')
    def wait_for_msg_send_status_become_to(self, expected, max_wait_time=3, most_recent_index=1):
        self.wait_until(
            condition=lambda d: self.get_msg_status(msg=self.__locators['消息根节点'],
                                                    most_recent_index=most_recent_index) == expected,
            timeout=max_wait_time
        )

    @TestLogger.log('获取消息发送状态')
    def get_msg_status(self, msg, most_recent_index=1):
        """
        获取消息的发送状态，如：
            1、加载中
            2、已发送
            3、发送失败
        如果传入的是定位器，默认寻找最新一条消息，没有则抛出 NoSuchElementException 异常
        :param msg: 消息（必须传入消息根节点元素或者元素的定位器）
        :param most_recent_index: 消息在列表中的序号，从消息列表底部往上数，从1开始计数
        :return:
        """
        if not isinstance(msg, WebElement):
            msgs = self.get_elements(msg)
            if msgs:
                msg = msgs[-most_recent_index]
            else:
                raise NoSuchElementException('找不到元素：{}'.format(msg))
        # 找加载中
        if msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/progress_send_small"]'):
            return '加载中'
        elif msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/imageview_msg_send_failed"]'):
            return '发送失败'
        else:
            return '发送成功'

    @TestLogger.log('切换到指定文件夹')
    def switch_to_given_folder(self, path):
        import re
        if not self.get_elements(self.__locators['下拉菜单选项']):
            self.click_element(self.__locators['下拉菜单箭头'])
        menu_list = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]']
        self.swipe_by_direction(menu_list, 'down', 600)
        menu_item = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]/*']
        for i in self.mobile.list_iterator(menu_list, menu_item):
            del i
            menus = self.get_elements(self.__locators['下拉菜单选项'])
            for menu in menus:
                menu_text = menu.text
                assert re.match(r'.+\(\d+\)', menu_text), r'Assert menu text match Regex:."+\(\d+\)"'
                display_name, total = re.findall(r'(.+)\((\d+)\)', menu_text)[0]
                if len(display_name) > 3:
                    result = re.findall(r'(.+)([.]{3})$', display_name)
                    if result:
                        if path.find(result[0][0]) == 0:
                            menu.click()
                            return result[0][0], int(total)
                    else:
                        if path.find(display_name) == 0:
                            menu.click()
                            return display_name, int(total)
                else:
                    if display_name == path:
                        menu.click()
                        return path, int(total)
        raise NoSuchElementException('下拉菜单没有找到名称为"{}"的目录'.format(path))

    @TestLogger.log('选择指定序号的图片（视频）')
    def select_items_by_given_orders(self, *orders):
        orders = sorted(list(set(orders)))
        offset = 1
        for i in self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项']):
            if offset in orders:
                if not self.is_list_item_selected(i):
                    el = i.find_element(*self.__locators['选择'])
                    el.click()
                orders.remove(offset)
            offset += 1
            if not orders:
                break

    @TestLogger.log('获取列表项已选状态')
    def is_list_item_selected(self, item):
        if isinstance(item, (list, tuple)):
            item = self.get_element(item)
        elif isinstance(item, WebElement):
            pass
        else:
            raise ValueError('参数类型错误')

        selector = item.find_element(*self.__locators['选择'])
        color = self.get_coordinate_color_of_element(selector, 5, 50, True)
        white = (255, 255, 255, 255)
        blue = (21, 124, 248, 255)
        if color == white:
            # 未选择状态为不透明白色
            return False
        elif color == blue:
            # 已选状态为不透明蓝色
            return True
        else:
            raise RuntimeError('RGBA颜色{}无法识别勾选状态'.format(color))

    @TestLogger.log()
    def click_original_photo(self):
        """点击原图"""
        self.click_element(self.__class__.__locators["原图"])

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        # 发送图片需要时间
        time.sleep(times)

    @TestLogger.log('点击预览')
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__locators['预览'])

    @TestLogger.log()
    def click_group_setting_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回3"])

    @TestLogger.log()
    def is_exist_setting_red_dot(self):
        """是否存在设置小红点"""
        return self._is_element_present(self.__class__.__locators["设置小红点"])

    @TestLogger.log()
    def click_group_sms(self):
        """点击群短信"""
        self.click_element(self.__class__.__locators["群短信"])

    @TestLogger.log()
    def is_exist_more_page(self):
        """是否存在更多选项"""
        for option in ["飞信电话", "多方通话", "群短信", "名片", "位置", "红包"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True

    @TestLogger.log()
    def click_i_know(self):
        """点击我知道了"""
        self.click_element(self.__class__.__locators["我知道了"])

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
