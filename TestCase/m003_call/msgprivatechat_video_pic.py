import random
import time
import re
import warnings

from library.core.common.simcardtype import CardType
from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from pages.components import BaseChatPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.utils.testcasefilter import tags
from pages import *
import unittest

class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def make_already_have_my_picture():
        """确保当前页面已有图片"""

        # 1.点击输入框左上方的相册图标
        scp = SingleChatPage()
        cpp = ChatPicPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        if scp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            scp.click_picture()
            cpp.wait_for_page_load()
            cpp.select_pic_fk(1)
            cpp.click_send()
            time.sleep(5)

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_single_chat():
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入单聊转发图片"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            scp = SingleChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            single_name = "大佬1"
            Preconditions.enter_single_chat_page(single_name)
            scp.forward_pic()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    #多人群聊前置条件
    @staticmethod
    def select_one_mobile(moible_param):
        """选择指定的设备连接，并确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        # 消息页面
        Preconditions.make_in_message_page(moible_param,reset=False)

    @staticmethod
    def make_in_message_page(moible_param,reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile(moible_param, reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def build_one_new_group_with_number(puhone_number,group_name):
        """新建一个指定成员和名称的群，如果已存在，不建群"""
        # 消息页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return True
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        #添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        slc.click_one_contact("飞信电话")
        # a = 0
        # names = {}
        # while a < 3:
        #     names = slc.get_contacts_name()
        #     num = len(names)
        #     if not names:
        #         raise AssertionError("No contacts, please add contacts in address book.")
        #     if num == 1:
        #         sog.page_up()
        #         a += 1
        #         if a == 3:
        #             raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
        #     else:
        #         break
        # # 选择成员
        # for name in names:
        #     slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()
        return False

    @staticmethod
    def get_group_chat_name_double():
        """获取多人群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "多机" + phone_number[-4:]
        return group_name

    @staticmethod
    def go_to_group_double(group_name):
        """从消息列表进入双机群聊，前提：已经存在双机群聊"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # # 群名
        # group_name = Preconditions.get_group_chat_name_double()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有找到双机群聊，请确认是否创建")
        sog.click_element_("群聊名")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def change_mobile(moible_param):
        """转换设备连接并且确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        current_mobile().hide_keyboard_if_display()
        current_mobile().launch_app()
        Preconditions.make_in_message_page(moible_param)


class MsgPrivateChatVideoPicTest(TestCase):
    """
    模块：消息->单聊视频,图片
    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-单聊视频,图片
    """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0001(self):
        """单聊会话页面，不勾选相册内图片点击发送按钮"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片时，发送按钮是否置灰展示并且不可点击
        flag = cpg.send_btn_is_enabled()
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0002(self):
        """单聊会话页面，勾选相册内一张图片发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右下角高亮展示的发送按钮，发送此照片
        cpg.select_pic()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0003(self):
        """单聊会话页面，预览相册内图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0004(self):
        """单聊会话页面，预览相册内图片，不勾选原图发送"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3.直接点击发送按钮
        cppp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0005(self):
        """单聊会话页面，预览相册数量与发送按钮数量一致"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择多张照片，点击左下角的预览按钮
        cpp.select_pic(n=3)
        cpp.click_preview()
        pic_preview = ChatPicPreviewPage()
        pic_preview.wait_for_page_load()
        # 3.查看发送按钮数字
        send_num = pic_preview.get_pic_send_num()
        self.assertEqual(send_num, '3')
        pic_preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_edit_pic():
        """图片编辑操作"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右上角编辑按钮，进行涂鸦、马赛克、文本编辑
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        pic = ChatPicEditPage()
        # 涂鸦
        pic.click_doodle()
        pic.do_doodle()
        # 马赛克
        pic.click_mosaic()
        pic.do_mosaic()
        # 文本编辑
        pic.click_text_edit_btn()
        pic.input_pic_text()
        # 完成
        pic.click_save()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0006(self):
        """单聊会话页面，编辑图片发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存按钮
        pic.click_save()
        # 4.点击发送
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0007(self):
        """单聊会话页面，编辑图片不保存发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 4.点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0008(self):
        """单聊会话页面，编辑图片中途直接发送"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击发送
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0009(self):
        """单聊会话页面，编辑图片保存"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存
        pic.click_save()
        flag = pic.is_toast_exist("保存成功")
        if not flag:
            raise AssertionError("保存编辑图片时没有弹出“保存成功”提示")
        # 返回单聊会话页面
        pic.click_cancle()
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0010(self):
        """单聊会话页面，取消编辑图片"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 返回单聊会话页面
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0011(self):
        """单聊会话页面，取消编辑图片，点击发送按钮"""
        self.public_edit_pic()
        chat = SingleChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 4.点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0012(self):
        """单聊会话页面，发送相册内的图片 """
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，直接点击当前选中的图片，放大展示当前图片
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        preview_info = cppp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', preview_info))
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    # @tags('ALL', 'SMOKE', 'CMCC')
    @unittest.skip('用例发生改变，点击图片编辑没有弹窗')
    def test_msg_xiaoliping_C_0013(self):
        """单聊会话页面，预览已选中的图片，隐藏编辑按钮 """
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2、选择2张照片后，点击左下角的预览按钮
        cpg.select_pic(n=2)
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        flag = cppp.is_toast_exist("仅支持勾选单张图片时进行编辑")
        if not flag:
            raise AssertionError("勾选多张图片时编辑按钮没有隐藏")
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0014(self):
        """单聊会话页面，勾选9张相册内图片发送"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择9张图片，点击发送
        cpg.select_pic(n=9)
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0015(self):
        """单聊会话页面，勾选超9张相册内图片发送"""
        # 1.在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择超9张图片
        cpp.select_pic(n=10)
        flag = cpp.is_toast_exist("最多只能选择9张照片")
        if not flag:
            raise AssertionError("选择超过9张图片时无‘最多只能选择9张照片’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0016(self):
        """单聊会话页面，同时发送相册中的图片和视屏"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择图片和视频
        cpp.select_pic()
        cpp.select_video()
        flag = cpp.is_toast_exist("不能同时选择照片和视频")
        if not flag:
            raise AssertionError("同时选择照片和视频时无‘不能同时选择照片和视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0017(self):
        """单聊会话页面，使用拍照功能并发送照片"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击“√”
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0018(self):
        """单聊会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"发送"
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0019(self):
        """单聊会话页面，使用拍照功能拍照之后编辑并保存"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_text_edit_btn()
        pic.input_pic_text(text="VideoPic_0019")
        # 点击完成
        pic.click_save()
        # 3.点击"保存"
        pic.click_save()
        # 4.点击"发送"
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0020(self):
        """单聊会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"取消"
        pic.click_cancle()
        # 4.点击“发送”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0021(self):
        """单聊会话页面，打开拍照，立刻返回会话窗口"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        # 2、打开照相机，点击“∨”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0022(self):
        """单聊会话页面，打开拍照，拍照之后返回会话窗口"""
        # 1、在当前聊天会话页面，点击富媒体行拍照图标
        chat = SingleChatPage()
        chat.click_take_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        # 2、打开照相机，点击“返回图标”
        cpp.click_back()
        cpp.take_photo_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_pic():
        """在聊天会话页面发送一张图片"""
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一张照片发送
        cpp.select_pic_fk()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0044(self):
        """单聊会话页面，转发自己发送的图片给本地联系人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        if names:
            slcp.select_one_member_by_name(list(names)[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0047(self):
        """单聊会话页面，转发自己发送的图片给和通讯录联系人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 4.在搜索框输入多种字符
        shc.input_search("大佬1")
        # 5.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 6.点击确认转发
        shc.click_sure_forward()
        flag = chat.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘已转发’提示")
        if not chat.is_on_this_page():
            raise AssertionError("当前页面不在单聊页面")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0050(self):
        """单聊会话页面，转发自己发送的图片给陌生人"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        times = 500
        while times > 0:
            tel = "147752" + str(random.randint(10000, 99999))
            scp.search(tel)
            # 构造陌生号码发送
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0060(self):
        """单聊会话页面，删除自己发送的图片"""
        self.public_send_pic()
        # 1、在当前聊天会话页面，长按自己发送的图片
        chat = SingleChatPage()
        chat.press_pic()
        # 2、点击 删除
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0062(self):
        """单聊会话页面，收藏自己发送的照片"""
        # 1、在当前聊天会话页面，长按自己发送的图片
        self.public_send_pic()
        chat = SingleChatPage()
        chat.press_pic()
        # 2.收藏该图片
        chat.click_collection()
        flag = chat.is_toast_exist("已收藏")
        if not flag:
            raise AssertionError("收藏图片没有‘已收藏’提示")
        chat.wait_for_page_load()
        time.sleep(1)
        # 3.在我模块中的收藏是否可见
        chat.click_back_by_android(3)
        time.sleep(1)
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        flag = mcp.have_collection_pic()
        if not flag:
            raise AssertionError("收藏图片后，在我的收藏中不可见")



    @staticmethod
    def public_send_video():
        """在聊天会话页面发送一个视频"""
        chat = SingleChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一个视频发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0066(self):
        """单聊会话页面，转发自己发送的视频给本地联系人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("转发消息无‘已转发’提示")
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0067(self):
        """单聊会话页面，转发自己发送的视频给和通讯录联系人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            time.sleep(1)
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选择", timeout=3)
                time.sleep(1)
                if not flag:
                    break
            # 3、点击确定
            time.sleep(1)
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发", timeout=8)
            if not flag2:
                raise AssertionError("转发消息无‘已转发’提示")
        else:
            print("WARN: Please create a team and add m005_contacts.")
            shcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0068(self):
        """单聊会话页面，转发自己发送的视频给陌生人"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        times = 500
        while times > 0:
            tel = "147752" + str(random.randint(10000, 99999))
            scp.search(tel)
            # 构造陌生号码发送
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0070(self):
        """单聊会话页面，删除自己发送的视频"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2、点击 删除
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0072(self):
        """单聊会话页面，收藏自己发送的视频"""
        self.public_send_video()
        # 1、在当前聊天会话页面，长按自己发送的视频
        chat = SingleChatPage()
        chat.press_video()
        # 2.收藏该视频
        chat.click_collection()
        flag = chat.is_toast_exist("已收藏")
        if not flag:
            raise AssertionError("收藏视频没有‘已收藏’提示")
        chat.wait_for_page_load()
        # 3.在我模块中的收藏是否可见
        cdp = ContactDetailsPage()
        chat.click_back_by_android(3)
        mess = MessagePage()
        mess.open_me_page()
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        flag = mcp.have_collection_video()
        if not flag:
            raise AssertionError("收藏视频后，在我的收藏中不可见")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0073(self):
        """单聊会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选择一个视屏
        cpp.select_video()
        flag = cpp.send_btn_is_enabled()
        if not flag:
            raise AssertionError("选择视频，发送按钮不可点击")
        times = cpp.get_video_times()
        res = re.match(r'\d+:\d+', times[0])
        if not res:
            raise AssertionError("视频显示时长格式错误，不是‘00:00’类型")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0074(self):
        """在单聊聊天会话页面，发送相册内一个视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视屏，点击发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()
        # 3、发送成功，会话窗口可见可播放
        chat.play_video()
        chat.wait_for_play_video_page_load()
        chat.close_video()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0075(self):
        """在单聊聊天会话页面，发送相册内多个视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中多个视屏
        cpp.select_video(n=0)
        cpp.select_video(n=1)
        # toast提示“最多只能选择一个视频”
        flag = cpp.is_toast_exist("最多只能选择1个视频")
        if not flag:
            raise AssertionError("选择多个视频时无‘最多只能选择1个视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0076(self):
        """在单聊聊天会话页面，同时发送相册内视频和图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视频和一个图片
        cpp.select_video()
        cpp.select_pic()
        # toast提示“不能同时选择照片和视频”
        flag = cpp.is_toast_exist("不能同时选择照片和视频", 5)
        if not flag:
            raise AssertionError("选中一个视频和一个图片时无‘不能同时选择照片和视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0077(self):
        """在单聊聊天会话页面，发送视频时预览视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标
        chat = SingleChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选中一个视频点击预览
        cpp.select_video()
        cpp.click_preview()
        # 3、可正常预览
        preview = ChatPicPreviewPage()
        preview.wait_for_video_preview_load()
        preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def delete_media_msg():
        """删除在单聊会话窗的图片，gif消息"""
        chat = SingleChatPage()
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            chat.wait_for_page_load()
            if not chat.is_exist_pic_msg():
                break
            chat.press_pic()
            chat.click_delete()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0165(self):
        """在单聊会话窗，验证点击趣图搜搜入口"""
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 进入趣图选择页面
        if not gif.is_gif_exist():
            raise AssertionError("趣图页面无gif趣图")
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0166(self):
        """在单聊会话窗，网络正常发送表情搜搜"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、选择表情点击发送
        gif.send_gif()
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        if not chat.is_exist_pic_msg():
            raise AssertionError("发送表情后，在单聊会话窗无表情趣图存在")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0167(self):
        """在单聊会话窗，断网情况下发送表情搜搜"""
        # 断网
        current_mobile().set_network_status(0)
        # 点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        # 提示：“网络异常，请重新设置网络”
        if not chat.is_toast_exist("请检查网络设置", timeout=10):
            raise AssertionError("断网情况下点击GIF无含有 ‘请检查网络设置’的提示")
        chat.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0167():
        """恢复网络"""
        current_mobile().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0168(self):
        """在单聊会话窗，搜索数字关键字选择发送趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入数字
        nums = ['1', '2', '6', '666', '8']
        for msg in nums:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                # 3、点击选择表情
                gif.send_gif()
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                if not chat.is_exist_pic_msg():
                    raise AssertionError("发送gif后，在单聊会话窗无gif")
                chat.wait_for_page_load()
                return


    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0169(self):
        """在单聊会话窗，搜索特殊字符关键字发送趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入特殊字符 @ ? ...
        chars = ['@', '?', '...']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                # 3、点击选择表情
                gif.send_gif()
                if not chat.is_exist_pic_msg():
                    raise AssertionError("发送gif后，在单聊会话窗无gif")
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        raise AssertionError("搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0170(self):
        """在单聊会话窗，搜索特殊字符关键字发送趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        chars = ['appium', 'xxxx', 'a', '123456', '*']
        # 提示无搜索结果，换个关键词试试
        for msg in chars:
            gif.input_message(msg)
            if gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        # raise AssertionError("搜索框输入关键字" + "、".join(chars) + "有gif搜索结果，请换输入关键字试试")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_xiaoliping_C_0171(self):
        """在单聊会话窗，搜索趣图过程中返回至消息列表重新进入"""
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字匹配到对应结果后点击返回
        chars = ['ok', 'o', '哈哈', 'no', 'yes']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                chat.click_back()
                # 3、再次进入该会话页面
                cdp = ContactDetailsPage()
                cdp.click_message_icon()
                gif.input_message("")
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                if gif.is_gif_exist():
                    raise AssertionError("在单聊会话窗，gif搜索到对应结果后点击返回,再次进入该会话页面时gif存在")
                return
        raise AssertionError("在单聊会话窗，搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0172(self):
        """在单聊会话窗，趣图发送成功后搜索结果依然保留"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字匹配到对应结果后点击发送
        chars = ['ok', 'o', '哈哈', 'no', 'yes']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                gif.send_gif()
                if not chat.is_exist_pic_msg():
                    raise AssertionError("在单聊会话窗,发送gif后，在标签分组会话窗无gif")
                if not gif.is_gif_exist():
                    raise AssertionError("gif发送后，gif的搜索内容不存在")
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        raise AssertionError("在单聊会话窗,搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0174(self):
        """在单聊会话窗，关闭GIF搜索框"""
        # 1、点击GIF图标
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、点击搜索框左方×
        gif.close_gif()
        if gif.is_gif_exist():
            raise AssertionError("点击左方× gif关闭后趣图页面还存在")
        current_mobile().hide_keyboard_if_display()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0195(self):
        """转发聊天内容中的已下载的图片（缩略图）"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个图片，点击转发
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_pic_to_do("转发")
        # 调起联系人选择器
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 返回聊天页面
        scp.click_back()
        pv.click_back()
        record.click_back()
        set_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0196(self):
        """转发聊天内容中的已下载的图片（放大图）"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.点开放大一张图片，长按点击转发
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.click_pic()
        pv.wait_for_pic_preview_page_load()
        pv.press_preview_pic_to_do("转发")
        # 调起联系人选择器
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_back()
        pv.close_pic_preview()
        pv.click_back()
        record.click_back()
        set_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0197(self):
        """转发聊天内容中的已下载的图片给任意对象"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个图片，点击转发
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_pic_to_do("转发")
        # 5.选择任意对象
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if "本机" in names:
            names.remove("本机")
        if not names:
            raise AssertionError("WARN: There is no linkman.")
        slcp.select_one_member_by_name(names[0])
        slcp.click_sure_forward()
        flag = slcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("转发聊天内容中的已下载的图片无‘已转发’提示")
        if pv.is_on_this_page():
            pv.click_back()
        # 回到消息页面
        record.click_back_by_android(6)
        cdp = ContactDetailsPage()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()
        # 在转发人的聊天界面可查看转发内容
        mess.look_detail_news_by_name(names[0])
        chat.wait_for_page_load()
        if not chat.is_exist_pic_msg():
            raise AssertionError("转发图片时在转发人的聊天界面无转发的图片")
        chat.click_back()
        mess.wait_for_page_load()
        # 从消息页面进入单聊页面
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        chat = SingleChatPage()
        contacts.select_people_by_name(names[0])
        cdp.wait_for_page_load()
        # 点击消息进入单聊会话页面
        cdp.click_message_icon()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0200(self):
        """转发聊天内容中的已下载的视频（缩略图）"""
        self.public_send_video()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个视频，点击转发
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_video_to_do("转发")
        # 调起联系人选择器
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 返回聊天页面
        scp.click_back()
        pv.click_back()
        record.click_back()
        set_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0201(self):
        """转发聊天内容中的已下载的视频（放大图）"""
        self.public_send_video()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.点开放大一张视频，长按点击转发
        pv = PicVideoPage()
        pv.click_video()
        pv.wait_for_play_video_page_load()
        pv.press_preview_video_to_do("转发")
        # 调起联系人选择器
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_back()
        pv.close_video()
        if pv.is_on_this_page():
            pv.click_back()
        record.click_back()
        set_page.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0202(self):
        """转发聊天内容中的已下载的视频给任意对象"""
        self.public_send_video()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个视频，点击转发
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_video_to_do("转发")
        # 5.选择任意对象
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if "本机" in names:
            names.remove("本机")
        if not names:
            raise AssertionError("WARN: There is no linkman.")
        slcp.select_one_member_by_name(names[0])
        slcp.click_sure_forward()
        flag = slcp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("转发聊天内容中的已下载的视频无‘已转发’提示")
        if pv.is_on_this_page():
            pv.click_back()
        # 回到消息页面
        record.click_back_by_android(6)
        cdp = ContactDetailsPage()
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()
        # # 在转发人的聊天界面可查看转发内容
        # mess.look_detail_news_by_name(names[0])
        # chat.wait_for_page_load()
        # if not chat.is_exist_video_msg():
        #     raise AssertionError("转发视频时在转发人的聊天界面无转发的视频")
        # chat.click_back()
        # mess.wait_for_page_load()
        # # 从消息页面进入单聊页面
        # mess.open_contacts_page()
        # contacts = ContactsPage()
        # time.sleep(3)
        # names = contacts.get_contacts_name()
        # chat = SingleChatPage()
        # contacts.select_people_by_name(names[0])
        # cdp.wait_for_page_load()
        # # 点击消息进入单聊会话页面
        # cdp.click_message_icon()
        # # 如果弹框用户须知则点击处理
        # flag = chat.is_exist_dialog()
        # if flag:
        #     chat.click_i_have_read()
        # chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0204(self):
        """收藏聊天内容中的已下载的图片"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个图片，点击收藏
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_pic_to_do("收藏")
        # toast提醒“已收藏”
        if not pv.is_toast_exist("已收藏"):
            raise AssertionError("收藏聊天记录中的图片无‘已收藏’提示")
        # 回到我页面
        pv.click_back_by_android(6)
        cdp = ContactDetailsPage()
        mess = MessagePage()
        mess.open_me_page()
        # 我模块收藏列表可见
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.have_collection_pic():
            raise AssertionError("收藏图片后，在我的收藏中不可见")
        # # 回到单聊会话页面
        # mcp.click_back()
        # mess.open_contacts_page()
        # contacts = ContactsPage()
        # time.sleep(3)
        # names = contacts.get_contacts_name()
        # contacts.select_people_by_name(names[0])
        # cdp.wait_for_page_load()
        # cdp.click_message_icon()
        # flag = chat.is_exist_dialog()
        # if flag:
        #     chat.click_i_have_read()
        # chat.wait_for_page_load()

    @staticmethod
    def clear_PicVideo_Record():
        """清除聊天内容中的图片与视频记录"""
        chat = SingleChatPage()
        chat.click_setting()
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        record = FindChatRecordPage()
        record.click_pic_video()
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.clear_record()
        pv.click_back()
        record.click_back()
        set_page.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0205(self):
        """删除聊天内容中的图片"""
        self.clear_PicVideo_Record()
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.长按任意一个图片，点击删除
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.press_pic_to_do("删除")
        # 无任何提醒
        if pv.is_toast_exist("删除", timeout=3):
            raise AssertionError("删除聊天记录中的图片有toast‘删除’提示")
        nums = pv.get_record_nums()
        if nums != 0:
            raise AssertionError("聊天记录中的图片删除失败，删除后依然存在")
        pv.click_back_by_android(3)
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG1')
    def test_msg_xiaoliping_C_0206(self):
        """保存聊天内容中的图片到本地"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.点击任意一个图片放大后，长按选择保存图片
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.click_pic()
        pv.wait_for_pic_preview_page_load()
        msg = "在单聊设置查找聊天内容的图片与视频页面,放大图片后,长按选择保存图片"
        times = 10
        while times > 0:
            pv.press_preview_pic_to_do("保存")
            # toast提醒"正在保存...","保存成功"
            flag1 = pv.is_toast_exist("正在保存", timeout=4)
            flag2 = pv.is_toast_exist("保存成功", timeout=4)
            if flag1 and flag2:
                break
            times = times - 1
        if times == 0:
            return AssertionError(msg + "无‘正在保存’或者 ‘保存成功’提示！")
        pv.close_pic_preview()
        pv.click_back()
        record.click_back()
        set_page.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0207(self):
        """保存聊天内容中的视频到本地"""
        self.public_send_video()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.点击任意一个视频放大后，长按选择保存视频
        pv = PicVideoPage()
        pv.click_video()
        pv.wait_for_play_video_page_load()
        pv.press_preview_video_to_do("保存视频")
        # toast提醒“视频已保存”
        msg = "在单聊设置查找聊天内容的图片与视频页面,放大视频后,长按选择保存视频"
        if not pv.is_toast_exist("视频已保存"):
            raise AssertionError(msg + "无‘视频已保存’提示！")
        pv.close_video()
        if pv.is_on_this_page():
            pv.click_back()
        record.click_back()
        set_page.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_xiaoliping_C_0208(self):
        """编辑聊天内容中的图片，并发送"""
        self.public_send_pic()
        # 1.在聊天会话页面，点击右上角设置图标
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击查找聊天内容
        set_page = SingleChatSetPage()
        set_page.search_chat_record()
        # 3.点击图片与视频
        record = FindChatRecordPage()
        record.click_pic_video()
        # 4.点击任意一个图片放大后，长按选择编辑
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.click_pic()
        pv.wait_for_pic_preview_page_load()
        pv.press_preview_pic_to_do("编辑")
        # 可对图片涂鸦、马赛克、文本
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        pic.click_mosaic()
        pic.do_mosaic()
        pic.click_text_edit_btn()
        pic.input_pic_text("VideoPic_0140")
        pic.click_save()
        # 5.点击发送按钮,调起联系人选择器
        pic.click_send()
        scp = SelectContactsPage()
        try:
            scp.wait_for_page_load()
        except:
            raise AssertionError("编辑图片后，发送图片未跳转到选择联系人界面")
        scp.click_back()
        pv.close_pic_preview()
        pv.click_back()
        record.click_back()
        set_page.click_back()
        chat.wait_for_page_load()


class MsgPrivateChatVideoPicAllTest(TestCase):
    """
    模块：单聊-图片、视频、GIF
    文件位置：1.1.3全量测试用例->113全量用例--肖立平.xlsx
    表格：单聊-图片、视频、GIF
    Author:刘晓东
    """

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        # Preconditions.select_mobile('Android-移动')
        # # 导入测试联系人、群聊
        # fail_time1 = 0
        # flag1 = False
        # import dataproviders
        # while fail_time1 < 3:
        #     try:
        #         required_contacts = dataproviders.get_preset_contacts()
        #         conts = ContactsPage()
        #         current_mobile().hide_keyboard_if_display()
        #         Preconditions.make_already_in_message_page()
        #         conts.open_contacts_page()
        #         try:
        #             if conts.is_text_present("发现SIM卡联系人"):
        #                 conts.click_text("显示")
        #         except:
        #             pass
        #         for name, number in required_contacts:
        #             # 创建联系人
        #             conts.create_contacts_if_not_exits(name, number)
        #         required_group_chats = dataproviders.get_preset_group_chats()
        #         conts.open_group_chat_list()
        #         group_list = GroupListPage()
        #         for group_name, members in required_group_chats:
        #             group_list.wait_for_page_load()
        #             # 创建群
        #             group_list.create_group_chats_if_not_exits(group_name, members)
        #         group_list.click_back()
        #         conts.open_message_page()
        #         flag1 = True
        #     except:
        #         fail_time1 += 1
        #     if flag1:
        #         break
        #
        # # 导入团队联系人
        # fail_time2 = 0
        # flag2 = False
        # while fail_time2 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
        #         Preconditions.create_he_contacts(contact_names)
        #         flag2 = True
        #     except:
        #         fail_time2 += 1
        #     if flag2:
        #         break
        #
        # # 确保有企业群
        # fail_time3 = 0
        # flag3 = False
        # while fail_time3 < 5:
        #     try:
        #         Preconditions.make_already_in_message_page()
        #         Preconditions.ensure_have_enterprise_group()
        #         flag3 = True
        #     except:
        #         fail_time3 += 1
        #     if flag3:
        #         break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """

        Preconditions.select_mobile('Android-移动')
        name = "大佬1"
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_single_chat_page(name)
            return
        scp = SingleChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0041(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        contact_name = "大佬1"
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        scp.click_back()
        # 返回时做一个判断，避免被别的模块影响执行
        mp = MessagePage()
        if not mp.is_on_this_page():
            cdp = ContactDetailsPage()
            cdp.click_back_icon()
            cp = ContactsPage()
            time.sleep(1)
            cp.wait_for_contacts_page_load()
            mp.open_message_page()
            Preconditions.enter_single_chat_page(contact_name)
            scp.click_picture()
            cpp.wait_for_page_load()
            cpp.select_pic_fk(1)
            cpp.click_send()
            time.sleep(5)
            scp.click_back()
        Preconditions.enter_single_chat_page(contact_name)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0042(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口时失败"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0042():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0043(self):
        """单聊会话页面，转发自己发送的图片到当前会话窗口时点击取消转发"""

        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 给当前会话页面发送一张图片,确保最近聊天中有记录
        cpp = ChatPicPage()
        time.sleep(2)
        scp.click_picture()
        cpp.wait_for_page_load()
        cpp.select_pic_fk(1)
        cpp.click_send()
        time.sleep(5)
        # 解决发送图片后，最近聊天窗口没有记录，需要退出刷新的问题
        scp.click_back()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        scg.select_recent_chat_by_name(contact_name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0044(self):
        """单聊会话页面，转发自己发送的图片给手机联系人"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        slc.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        if not mp.is_on_this_page():
            cdp = ContactDetailsPage()
            cdp.click_back_icon()
            cp = ContactsPage()
            cp.wait_for_page_load()
            cp.open_message_page()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0045(self):
        """单聊会话页面，转发自己发送的图片到手机联系人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 确定转发
        slc.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0045():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0046(self):
        """单聊会话页面，转发自己发送的图片到手机联系人时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择本地联系人”菜单
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        name = "大佬2"
        # 3.选择一个手机联系人
        slc.selecting_local_contacts_by_name(name)
        # 取消转发
        slc.click_cancel_forward()
        # 4.等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        # 返回单聊会话页面
        slc.click_back()
        scg.wait_for_page_load()
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0047(self):
        """单聊会话页面，转发自己发送的图片给团队联系人"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0048(self):
        """单聊会话页面，转发自己发送的图片到团队联系人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        time.sleep(1)
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0048():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0049(self):
        """单聊会话页面，转发自己发送的图片到团队联系人时点击取消转发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择和通讯录联系人”菜单
        scg.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        # 等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 3.选择一个团队联系人
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_single_chat()
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人->和通讯录联系人 页面加载
        shc.wait_for_he_contacts_page_load()
        # 返回单聊会话页面
        shc.click_back()
        shc.click_back()
        scg.wait_for_page_load()
        scg.click_back()
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0050(self):
        """单聊会话页面，转发自己发送的图片给陌生人"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的陌生联系人
        mp.choose_chat_by_name(number)
        time.sleep(2)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0051(self):
        """单聊会话页面，转发自己发送的图片到陌生人时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 确定转发
        scg.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0051():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0052(self):
        """单聊会话页面，转发自己发送的图片到陌生人时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        number = "13855558888"
        # 输入陌生手机号码
        scg.input_search_keyword(number)
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # 3.选择陌生号码转发
        scg.click_unknown_member()
        # 取消转发
        scg.click_cancel_forward()
        # 4.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0053(self):
        """单聊会话页面，转发自己发送的图片到普通群"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 5.验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0054(self):
        """单聊会话页面，转发自己发送的图片到普通群时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        group_name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(group_name)
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0054():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0055(self):
        """单聊会话页面，转发自己发送的图片到普通群时点击取消转发"""

        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        name = "群聊1"
        # 3.选择一个普通群
        sog.selecting_one_group_by_name(name)
        # 取消转发
        sog.click_cancel_forward()
        # 4.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0056(self):
        """单聊会话页面，转发自己发送的图片到企业群"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 3.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 4.选择一个企业群
        name = sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 5.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        time.sleep(2)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 选择刚发送消息的聊天页
        mp.choose_chat_by_name(name)
        time.sleep(2)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        # 返回消息页
        scp.click_back()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0057(self):
        """单聊会话页面，转发自己发送的图片到企业群时失败"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        scp.click_back()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        contact_name = "大佬1"
        Preconditions.enter_single_chat_page(contact_name)
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 设置手机网络断开
        scp.set_network_status(0)
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 3.选择一个企业群
        sog.select_one_enterprise_group()
        # 确定转发
        sog.click_sure_forward()
        # 4.是否提示已转发,等待单聊页面加载
        self.assertEquals(scp.is_exist_forward(), True)
        scp.wait_for_page_load()
        # 返回到消息页
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_C_0057():
        """恢复网络"""

        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_C_0058(self):
        """单聊会话页面，转发自己发送的图片到企业群时点击取消转发"""

        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 确保当前聊天页面已有图片
        Preconditions.make_already_have_my_picture()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        # 1.长按自己发送的图片并转发
        scp.forward_pic()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 点击“选择一个群”菜单
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 3.选择一个企业群
        sog.select_one_enterprise_group()
        # 取消转发
        sog.click_cancel_forward()
        # 4.等待“选择一个群”页面加载
        sog.wait_for_page_load()
        sog.click_back()
        # 等待选择联系人页面加载
        scg.wait_for_page_load()
        # 返回单聊会话页面
        scg.click_back()

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0023(self):
        """单聊会话页面，转发他人发送的图片到当前会话窗口"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击转发
        # 3、在最近聊天中选择当前会话窗
        # 4、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_element_("消息图片")
        time.sleep(6)
        scp.press_xy()
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text(phone_number2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0035(self):
        """单聊会话页面，转发他人发送的图片到普通群"""
        # 1、在当前会话窗口长按他人发送的文件消息
        # 2、点击转发
        # 3、点击选择一个群，选择任意普通群
        # 4、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_element_("消息图片")
        time.sleep(6)
        scp.press_xy()
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword("给个红包1")
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有给个红包1群，请创建后重试")
        sog.click_element_("群聊名")
        time.sleep(2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text("给个红包1")
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do('给个红包1', "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0038(self):
        """单聊会话页面，转发他人发送的图片到企业群"""
        # 1、在当前会话窗口长按他人发送的文件消息
        # 2、点击转发
        # 3、点击选择一个群，选择任意企业群
        # 4、点击发送按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_element_("消息图片")
        time.sleep(6)
        scp.press_xy()
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text("选择一个群")
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword("测试企业群")
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有测试企业群，请创建后重试")
        sog.click_element_("群聊名")
        time.sleep(2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        current_mobile().back()
        Preconditions.change_mobile('Android-移动-移动')
        mess.click_text("测试企业群")
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.press_file_to_do("测试企业群", "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0059(self):
        """单聊会话页面，删除他人发送的图片"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2、点击删除
        # 3、点击确定
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.press_element_("消息图片", 3000)
        scp.click_text("删除")
        time.sleep(2)
        if scp.is_element_exit_("消息图片"):
            raise AssertionError("删除图片不成功")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0061(self):
        """单聊会话页面，收藏他人发送的照片"""
        # 1、在当前聊天会话页面，长按他人发送的图片
        # 2.收藏该图片
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一张相片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk()
        # 4.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 5.点击发送,
        cpp.click_send()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.press_element_("消息图片", 3000)
        scp.click_text("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.is_element_exit_("收藏的图片"):
            raise AssertionError("收藏的图片不可见")
        # 左滑收藏消息体
        mcp.press_and_move_left()
        # 判断是否有删除按钮
        if mcp.is_delete_element_present():
            mcp.click_delete_collection()
            mcp.click_sure_forward()
            if not mcp.is_toast_exist("取消收藏成功"):
                raise AssertionError("不可以删除收藏的消息体")
            time.sleep(1)
            mcp.click_back()
            mess.open_message_page()
        else:
            raise AssertionError("没有删除收藏按钮")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0063(self):
        """单聊会话页面，转发他人发送的视频给手机联系人"""
        # 1、在当前聊天会话页面，长按他人发送的视频
        # 2、点击转发
        # 3、选择任意手机联系人
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一段视频
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_element_("消息视频")
        time.sleep(2)
        if scp.is_element_exit_("关闭视频"):
            scp.press_xy()
        else:
            # 点击后等待视频加载成功
            scp.wait_for_video_load()
            scp.press_element_("消息视频", 3000)
        scp.click_text("转发")
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        sc.click_text(phone_number2)
        scp.click_element_("确定")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("转发失败")
        time.sleep(2)
        if scp.is_element_exit_("关闭视频"):
            current_mobile().back()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_C_0069(self):
        """单聊会话页面，删除他人发送的视频"""
        # 1、在当前聊天会话页面，长按他人发送的视频
        # 2、点击删除
        # 3、点击确定
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_picture()
        # 3.进入相片页面,选择一段视频
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        cpg.click_send()
        time.sleep(5)
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.press_element_("消息视频", 3000)
        scp.click_text("删除")
        time.sleep(2)
        if scp.is_element_exit_("消息视频"):
            raise AssertionError("删除视频不成功")
        Preconditions.change_mobile('Android-移动-移动')
        mess.press_file_to_do(phone_number2, "删除聊天")
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx', 'yx')
    def test_msg_xiaoliping_C_0080(self):
        """分享相册内图片给手机联系人"""
        # 1、成功登陆和飞信
        # 2、进入手机本地相册
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击发送，长按图片转发
        cpg.click_send()
        scp.press_last_picture_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击选择手机联系人
        select_contacts.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        # 5.在搜索框点击搜索到的手机联系人
        slcp.search_and_select_contact("大佬2")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("没有已转发的弹框提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在单聊页面")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx', 'yx')
    def test_msg_xiaoliping_C_0092(self):
        """分享相册内视频给手机联系人"""
        # 1、成功登陆和飞信
        # 2、进入手机本地相册
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        # 2.进入相片页面,选择视频
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        # 3.点击发送，长按视频转发
        cpg.click_send()
        scp.press_last_video_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 4.点击选择手机联系人
        select_contacts.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        # 5.在搜索框点击搜索到的手机联系人
        slcp.search_and_select_contact("大佬2")
        if not scp.is_toast_exist("已转发"):
            raise AssertionError("没有已转发的弹框提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在单聊页面")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx', 'yx')
    def test_msg_xiaoliping_C_0095(self):
        """分享相册内视频给团队联系人"""
        # 1、成功登陆和飞信
        # 2、进入手机本地相册
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        # 2.进入相片页面,选择视频
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_video_fk(1)
        # 3.点击发送，长按视频转发
        cpg.click_send()
        scp.press_last_video_to_do("转发")
        select_contacts = SelectContactsPage()
        select_contacts.wait_for_page_load()
        # 5.点击“选择团队联系人”菜单
        select_contacts.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 6.选择团队
        shc.click_department_name("测试团队1")
        # 7.在搜索框输入联系人名字
        shc.input_search("大佬1")
        # 8.点击搜索的团队联系人
        shc.click_search_team_contacts()
        # 9.点击确认转发
        shc.click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("没有已转发的弹框提示")
        if not scp.is_on_this_page():
            raise AssertionError("当前页面不在单聊页面")

