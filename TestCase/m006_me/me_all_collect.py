import re
import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.me.MeAboutChinasofti import MeAboutChinasoftiPage
from pages.me.MeHelpAndFeedback import MeHelpAndFeedbackPage
from pages.me.MeRecommendClient import MeRecommentdClienPage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        permission_list.click_permission_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        # if one_key.have_read_agreement_detail():
        #     one_key.click_read_agreement_detail()
        #     # 同意协议
        #     agreement = AgreementDetailPage()
        #     agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        if agreement.is_text_present("同意"):
            agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def make_already_in_message_page(reset=False):
        """确保应用在消息页面"""
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()

    @staticmethod
    def make_already_in_me_all_page():
        """确保应用在消息页面"""

        # 如果在消息页，不做任何操作
        mess = MessagePage()
        mep = MePage()
        if mep.is_on_this_page():
            return
        if mess.is_on_this_page():
            mess.open_me_page()
            mep.is_on_this_page()
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page(reset=False)
            mess.open_me_page()

    @staticmethod
    def make_already_set_message():
        """确保私人已经发送一条消息，且已收藏"""
        Preconditions.make_already_in_message_page()
        # 1.点击新建消息
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_add_icon()
        mess.click_new_message()
        # 2.选择联系人发送一条消息
        scp = SelectContactsPage()
        scp.wait_for_page_local_contact_load()
        scp.click_one_contact("给个红包1")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            bcp.click_i_have_read()
        infor = "测试工程师"
        bcp.input_message(infor * 30)
        bcp.send_message()
        # 3.点击该信息收藏
        mess.press_file_to_do("测试工程师", "收藏")
        if not bcp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        bcp.click_element(["id", 'com.chinasofti.rcs:id/back_arrow'])

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
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
        group_name = Preconditions.get_group_chat_name()
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
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        sog.click_back()
        time.sleep(1)
        sc.click_back()
        mess.wait_for_page_load()
        # 从本地联系人中选择成员创建群
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.click_one_contact(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "a" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_set_chart_group_message():
        """确保群聊已经发送一条消息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        infor = "我是测试工程师15918730974,www.otherpages.com "
        scp.input_message(infor * 40)
        scp.send_message()
        # 3.点击该信息收藏
        scp.press_file_to_do("我是测试工程师", "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        mess = MessagePage()
        scp.click_back()

    @staticmethod
    def make_already_set_chart_group_video(pic_video="video"):
        """确保群聊已经发送一条视频，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        time.sleep(2)
        if pic_video == "video":
            cpg.select_video_fk()
            cpg.click_send()
            time.sleep(3)
            scp.press_video()
        if pic_video == "pic":
            cpg.select_pic_fk()
            cpg.click_send()
            time.sleep(3)
            scp.press_pic()
        # 3.点击该信息收藏
        scp.click_collection()
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        scp.click_back()

    @staticmethod
    def make_already_set_chart_group_voice():
        """确保群聊已经发送一条语音，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_audio_btn()
        time.sleep(7)
        if scp.is_text_present("仅发送语音"):
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'仅发送语音')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'确定')]"], 15)
        if scp.is_text_present("无法识别，请重试"):
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'设置')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'仅发送语音')]"], 15)
            scp.click_element([MobileBy.XPATH, "//*[contains(@text,'确定')]"], 15)
        time.sleep(2)
        scp.click_send_btn()
        # 3.点击该信息收藏
        time.sleep(2.5)
        scp.press_voice_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        scp.click_back()

    @staticmethod
    def make_already_set_chart_group_name_card():
        """确保群聊已经发送一个名片，且已收藏"""
        Preconditions.enter_group_chat_page()
        Preconditions.delete_record_group_chat()
        # 1.点击新建消息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        time.sleep(3)
        scp.click_text("名片")
        time.sleep(1)
        ssp = SelectContactsPage()
        ssp.wait_for_page_local_contact_load()
        sogp = SelectOneGroupPage()
        sogp.select_contact_by_name("给个红包1")
        time.sleep(1)
        ssp.click_element([MobileBy.XPATH, "//*[contains(@text,'发送名片')]"], 15)
        time.sleep(3)
        # 3.点击该信息收藏
        scp.press_file_to_do("个人名片", "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        scp.click_back_by_android(2)

    @staticmethod
    def make_already_set_chart_group_location():
        """确保群聊已经发送一个位置信息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击更多位置信息
        mess = MessagePage()
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        mess.click_set_message("位置")
        clp = ChatLocationPage()
        clp.wait_for_page_load()
        clp.click_send()
        # 3.点击该信息收藏
        scp.press_message_to_do("收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        scp.click_back()

    @staticmethod
    def make_already_set_chart_group_file(file_type):
        """确保群聊已经发送一个文件信息，且已收藏"""
        Preconditions.enter_group_chat_page()
        # 1.点击更多位置信息
        scp = GroupChatPage()
        if scp.is_exist_dialog():
            scp.click_i_have_read()
        scp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        # 3.点击该信息收藏
        scp.press_file_to_do(file_type, "收藏")
        if not scp.is_toast_exist("已收藏"):
            raise AssertionError("没有此弹框")
        cmp.click_back()

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

    @staticmethod
    def delete_all_my_collection():
        """确保群聊已经发送一个文件信息，且已收藏"""
        mep = MePage()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_collection()
        for i in range(len(file_names)):
            mcp.press_and_move_left()
            if mcp.is_delete_element_present():
                mcp.click_delete_collection()
                mcp.click_sure_forward()
                # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    @staticmethod
    def delete_all_my_collection2():
        """确保群聊已经发送一个文件信息，且已收藏"""
        mep = MePage()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        els = mcp.get_all_collection2()
        for i in range(len(els)):
            mcp.press_and_move_left()
            if mcp.is_delete_element_present():
                mcp.click_delete_collection()
                mcp.click_sure_forward()
                # 4.点击返回
        mep.click_back()
        mep.open_message_page()


class MeAllCollect(TestCase):
    """我的_收藏"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_445(self):
        """收藏内容来自于个人私聊的展示"""
        Preconditions.make_already_set_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("今天", "今天")
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_445(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_446(self):
        """收藏内容来自于群聊的展示"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("我", Preconditions.get_group_chat_name())
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_446(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_447(self):
        """查看当天收藏内容的时间显示"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.element_contain_text("今天", "今天")
        mcp.element_contain_text("我", Preconditions.get_group_chat_name())
        # 3.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_447(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_451(self):
        """查看收藏内容为短视频的展示"""
        Preconditions.make_already_set_chart_group_video()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验是否有视频和播放时长（图片比例暂不做）
        flag = mcp.get_video_len("视频时长")
        self.assertIsNotNone(re.match(r'(\d\d:\d\d)', flag))
        mcp.page_should_contain_element([MobileBy.ID, 'com.chinasofti.rcs:id/iv_favorite_video_bg'])
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_451(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_452(self):
        """查看收藏内容为文字（含短信）的展示"""
        Preconditions.make_already_set_chart_group_message()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验收藏内容不超过三行
        self.assertEquals(mcp.get_width_of_collection("www.otherpages.com", 3), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_452(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_453(self):
        """查看收藏内容为语音消息的展示"""
        Preconditions.make_already_set_chart_group_voice()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验语音消息
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        flag = mcp.get_video_len("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口")
        self.assertIsNotNone(re.match(r'(\d+秒)', flag))
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_453(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_455(self):
        """查看收藏内容为名片的展示"""
        Preconditions.make_already_set_chart_group_name_card()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        flag1 = mcp.get_video_len("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口")
        # 名片名称最多显示两行
        self.assertEquals(mcp.get_width_of_collection("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", 2), True)
        flag2 = "[名片]" + "给个红包1" + "的个人名片"
        self.assertEquals(flag1, flag2)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_455(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_456(self):
        """查看收藏内容为位置信息的展示"""
        # 备注：位置无法加载
        try:
            Preconditions.make_already_set_chart_group_location()
            # 1.点击跳转到我的页面
            mess = MessagePage()
            mess.wait_for_page_load()
            # 进入群聊获取卡名
            mess.click_set_message('位置')
            scp = GroupChatPage()
            scp.wait_for_page_load()
            mess.click_back()
            time.sleep(1.8)
            # 2.点击我的收藏,进入收藏页面
            mess.open_me_page()
            mep = MePage()
            mep.is_on_this_page()
            mep.click_collection()
            mcp = MeCollectionPage()
            mcp.wait_for_page_load()
            # 3.校验名片格式
            mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
            # 位置信息最多显示2行
            self.assertEquals(mcp.get_width_of_collection("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", 2), True)
            # 4.点击返回
            mep.click_back()
            mep.open_message_page()
        except:
            pass

    def tearDown_test_me_zhangshuli_456(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_458(self):
        """查看收藏内容为未知文件的展示"""
        Preconditions.make_already_set_chart_group_file(".log")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        mcp.element_should_contain_text(["id", 'com.chinasofti.rcs:id/file_name'], ".log")
        # self.assertEquals(mcp.get_width_of_collection("文件名", 1), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_458(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_459(self):
        """查看收藏内容为已知文件的展示"""
        Preconditions.make_already_set_chart_group_file(".doc")
        Preconditions.make_already_set_chart_group_file(".txt")
        Preconditions.make_already_set_chart_group_file(".docx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".docx"), True)
        self.assertEquals(file_names[1].endswith(".txt"), True)
        self.assertEquals(file_names[2].endswith(".doc"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_459(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_460(self):
        """查看收藏内容为可识别的幻灯片格式"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        Preconditions.make_already_set_chart_group_file(".pptx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        for i in range(2):
            mcp.page_down()
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".pptx"), True)
        self.assertEquals(file_names[1].endswith(".ppt"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_460(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_461(self):
        """查看收藏内容为可识别的表格格式"""
        Preconditions.make_already_set_chart_group_file(".xls")
        Preconditions.make_already_set_chart_group_file(".xlsx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".xlsx"), True)
        self.assertEquals(file_names[1].endswith(".xls"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_461(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_462(self):
        """查看收藏内容为可识别的PDF格式"""
        Preconditions.make_already_set_chart_group_file(".pdf")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".pdf"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_462(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_464(self):
        """查看收藏内容为可识别的音频格式"""
        Preconditions.make_already_set_chart_group_file("18718.mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".mp3"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_464(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_466(self):
        """查看收藏内容为可识别的压缩格式"""
        Preconditions.make_already_set_chart_group_file(".rar")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_set_message('文件')
        scp = GroupChatPage()
        scp.wait_for_page_load()
        file_name1 = scp.get_file_info("文件名")
        file_size1 = scp.get_file_info("文件大小")
        mess.click_back()
        time.sleep(1.8)
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.校验名片格式
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/favorite_image_shortcut'])
        file_names = mcp.get_all_file_names()
        file_name2 = file_names[0]
        file_size2 = mcp.get_video_len("10.0KB")
        self.assertEquals(file_name1, file_name2)
        self.assertEquals(file_size1, file_size2)
        self.assertEquals(file_names[0].endswith(".rar"), True)
        # 4.点击返回
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_466(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_467(self):
        """查看收藏内容为短视频的展示"""
        Preconditions.make_already_set_chart_group_video()
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击该收藏内容
        mcp.click_collection_pic_video("收藏的视频")
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/sv_video'])
        # 4.点击返回
        mep.click_back_by_android(2)
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_467(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_468(self):
        """在收藏列表中打开音频文件"""
        Preconditions.make_already_set_chart_group_file(".mp3")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮
        mcp.click_collection_file_name()
        mcp.page_should_contain_text(file_name)
        # 4.点击返回
        mcp.click_back_by_android(2)
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_468(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_469(self):
        """查看收藏内容为图片的展示"""
        Preconditions.make_already_set_chart_group_video(pic_video="pic")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        # 2.点击我的收藏,进入收藏页面
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        # 3.点击该收藏内容
        mcp.click_collection_pic_video("收藏的图片")
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/favorite_title'])
        )
        mcp.page_should_contain_element(["id", 'com.chinasofti.rcs:id/iv_photo'])
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_469(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_470(self):
        """在收藏列表中打开文本文件"""
        Preconditions.make_already_set_chart_group_file(".txt")
        Preconditions.make_already_set_chart_group_file(".doc")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮,文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_470(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_471(self):
        """打开幻灯片格式为.ppt .pptx"""
        Preconditions.make_already_set_chart_group_file(".ppt")
        Preconditions.make_already_set_chart_group_file(".pptx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮(尝试两次),文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_471(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_472(self):
        """打开表格格式为.xls  .xlsx"""
        Preconditions.make_already_set_chart_group_file(".xls")
        Preconditions.make_already_set_chart_group_file(".xlsx")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        # 3.点击收藏的按钮,文本文件可以显示
        for i in range(len(file_names)):
            try:
                mcp.click_collection_file_name(i=i)
            except Exception:
                mcp.click_collection_file_name(i=i)
            mcp.wait_until(
                condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
            )
            file_name = file_names[i]
            mcp.page_should_contain_text(file_name)
            mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_472(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_473(self):
        """打开文件PDF格式为.pdf"""
        Preconditions.make_already_set_chart_group_file(".pdf")
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的收藏,进入收藏页面
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_collection()
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        file_names = mcp.get_all_file_names()
        file_name = file_names[0]
        # 3.点击收藏的按钮,文本文件可以显示
        mcp.click_collection_file_name()
        mcp.wait_until(
            condition=lambda d: current_mobile()._is_enabled(['id', 'com.chinasofti.rcs:id/title'])
        )
        mcp.page_should_contain_text(file_name)
        # 4.点击返回
        mep.click_back()
        mep.click_back()
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_473(self):
        Preconditions.make_already_in_me_all_page()
        Preconditions.delete_all_my_collection()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_476(self):
        """打开收藏的位置信息"""
        # 备注：位置无法加载
        try:
            Preconditions.make_already_set_chart_group_location()
            # 1.点击跳转到我的页面
            mess = MessagePage()
            mess.wait_for_page_load()
            # 2.点击我的收藏,进入收藏页面
            mess.open_me_page()
            mep = MePage()
            mep.is_on_this_page()
            mep.click_collection()
            mcp = MeCollectionPage()
            mcp.wait_for_page_load()
            # 3.点击收藏的按钮,文本文件可以显示
            mcp.open_location("位置")
            mcp.wait_for_location_page_load()
            mcp.page_contain_element("导航按钮")
            # 4.点击返回
            mep.click_back_by_android(2)
            mep.open_message_page()
        except:
            pass

    def tearDown_test_me_zhangshuli_476(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_477(self):
        """打开收藏的位置信息"""
        # 备注：位置无法加载
        try:
            Preconditions.make_already_set_chart_group_location()
            # 1.点击跳转到我的页面
            mess = MessagePage()
            mess.wait_for_page_load()
            # 2.点击我的收藏,进入收藏页面
            mess.open_me_page()
            mep = MePage()
            mep.is_on_this_page()
            mep.click_collection()
            mcp = MeCollectionPage()
            mcp.wait_for_page_load()
            # 3.点击收藏的按钮,文本文件可以显示
            mcp.open_location("位置")
            mcp.wait_for_location_page_load()
            mcp.page_contain_element("导航按钮")
            # 4.点击返回，检验是否在收藏位置页面
            mep.click_back()
            mcp.element_contain_text("[位置]广东省深圳市龙岗区居里夫人大道与环城路交叉口", "位置")
            # 5.点击返回
            mep.click_back_by_android(1)
            mep.open_message_page()
        except:
            pass

    def tearDown_test_me_zhangshuli_477(self):
        try:
            Preconditions.make_already_in_me_all_page()
            Preconditions.delete_all_my_collection()
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_486(self):
        """关于和飞信入口"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.校验关于和飞信页面
        mcp.wait_for_page_load_about()
        mcp.page_contain_el("产品logo")
        menu = {"和飞信V", "版本更新", "新手引导", "产品介绍"}
        self.assertEquals(mcp.page_contain_text(menu), True)
        # 4.点击返回
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    # @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    @unittest.skip("取决现网版本是否有跟新版本")
    def test_me_zhangshuli_487(self):
        """已是最新版本-检查更新弹窗"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        mcp.wait_for_page_load_about()
        # 3.点击检查更新
        mcp.click_check_update()
        mcp.wait_for_page_load_update()
        # 4.点击抢先下载
        mcp.click_update()
        if not mcp.is_toast_exist("已是最新版本"):
            raise AssertionError("不存在已是最新版本此弹框")
        # 5.点击返回
        mcp.click_back()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_506(self):
        """新手引导页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.关于和飞信页面，点击新手引导
        mcp.wait_for_page_load_about()
        mcp.click_new_guide()
        mcp.wait_for_page_new_guide()
        mcp.page_contain_el("返回1")
        menu1 = {"关键词", "即时消息", "消息必达", "拨号盘", "多方电话", "多方视频", "和通讯录"}
        self.assertEquals(mcp.page_contain_text(menu1), True)
        menu2 = {"消息篇", "通话篇", "通讯录", "工作台", "通用篇", "工作台"}
        self.assertEquals(mcp.page_contain_text(menu2), True)
        # 4.点击返回
        mcp.click_back_new()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_507(self):
        """关键词列表信息跳转到详情页验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.关于和飞信页面，点击新手引导
        mcp.wait_for_page_load_about()
        mcp.click_new_guide()
        mcp.wait_for_page_new_guide()
        time.sleep(3)
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mcp.click_current_msg("即时消息")
        # mcp.wait_for_page_new_guide_details()
        # mcp.page_should_contain_text("即时消息")
        # 4.点击返回
        # mcp.click_back_new()
        # time.sleep(1)
        # mcp.click_current_msg("即时消息")
        # mcp.wait_for_page_new_guide_details()
        # 5.点击关闭
        # mcp.click_close()
        # 6.点击返回
        # mcp.wait_for_page_load_about()
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_508(self):
        """新手引导页面关键词分类功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.关于和飞信页面，点击新手引导
        mcp.wait_for_page_load_about()
        mcp.click_new_guide()
        mcp.wait_for_page_new_guide()
        time.sleep(3)
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mcp.click_text("通话篇")
        # mcp.wait_for_page_new_guide_details()
        # mcp.page_should_contain_text("通话篇")
        # mcp.click_text("多方视频")
        # mcp.wait_for_page_new_guide_details()
        # 4.点击返回
        # mcp.click_back_new()
        # 5.点击关闭
        # mcp.click_close()
        # 6.点击返回
        # mcp.wait_for_page_load_about()
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_509(self):
        """产品介绍页面跳转验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.关于和飞信页面，点击产产品
        mcp.wait_for_page_load_about()
        mcp.click_product_introduction()
        # 产品介绍-id
        mcp.wait_for_page_new_guide_details()
        # 4.点击返回
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_510(self):
        """网络异常下，产品介绍页面跳转验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的关于和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        mcp = MeAboutChinasoftiPage()
        # 3.关于和飞信页面，点击产品介绍
        mcp.wait_for_page_load_about()
        mcp.set_network_status(0)
        mcp.click_product_introduction()
        self.assertEquals(mcp.is_toast_exist("网络不可用，请检查网络设置"), True)
        # 4.点击返回
        mcp.click_back_by_android()
        time.sleep(1)
        mcp.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @staticmethod
    def tearDown_test_me_zhangshuli_510():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_514(self):
        """通用版本（内陆/移动用户）-我页面文案检查"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        self.assertEquals(mep.is_text_present("推荐和飞信"), True)
        # self.assertEquals(mep._find_text_menu("分享和飞信"), False)
        # self.assertTrue(mep.wait_until(condition=lambda x: mep.is_text_present("推荐和飞信")))
        # self.assertFalse(mep.is_text_present("分享和飞信"))
        # 3.返回到我的页面
        mep.click_back_by_android()
        time.sleep(1)
        mep.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_515(self):
        """通用版本覆盖安装-推荐和飞信页面跳转验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        menu1 = {"推荐和飞信", "短信", "微信", "朋友圈", "QQ"}
        self.assertEquals(mrp.page_contain_text(menu1), True)
        # 3.返回到我的页面
        mep.click_back_by_android()
        time.sleep(1)
        mep.click_back_by_android()
        time.sleep(1)
        mep.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_529(self):
        """通用版本-短信入口-本地联系人列表"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # scp.click_one_contact("和飞信电话")
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_530(self):
        """通用版本-短信入口-本机已登录号码"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(1.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        # scp.click_one_contact(phone_number)
        # self.assertEquals(scp.is_toast_exist("该联系人不可选择"), True)
        # # 4.点击返回
        # scp.click_back()
        # mrp.click_back()
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_531(self):
        """通用版本-短信入口-搜索结果界面"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(1.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "12560"
        # scp.input_search_contact_message(phoneNumber)
        # info = "搜索团队联系人 : " + phoneNumber
        # scp.page_should_contain_text(info)
        # scp.page_should_contain_text("联系人")

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_532(self):
        """通用版本-短信入口-搜索结果大于3条"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(1.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "1"
        # scp.search(phoneNumber)
        # info = "搜索团队联系人 : " + phoneNumber
        # scp.page_should_contain_text(info)
        # scp.page_should_contain_text("联系人")
        # self.assertEquals(scp.result_is_more_tree(), True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_533(self):
        """通用版本-短信入口-搜索手机号"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "12560"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_534(self):
        """通用版本-短信入口-搜索姓名"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "和飞信电话"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_535(self):
        """通用版本-短信入口-搜索姓名"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "xili"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_535(self):
        """通用版本-短信入口-搜索姓名"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "xili"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_536(self):
        """通用版本-短信入口-搜索特殊符号"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "wa ss"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_538(self):
        """通用版本-短信入口-搜索+852开头"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "+85267656001"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_539(self):
        """通用版本-短信入口-搜索无本地联系人且为手机号"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # phoneNumber = "13537795364"
        # scp.input_search_contact_message(phoneNumber)
        # scp.click_one_local_contacts()
        # time.sleep(0.5)
        # scp.page_should_contain_text("免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验")
        # # 4.点击发送
        # mrp.click_send()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_540(self):
        """通用版本-短信入口-1期"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的推荐和飞信-点击短信
        mess.open_me_page()
        time.sleep(1)
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(2)
        mep.click_menu("关于和飞信")
        time.sleep(2)
        mep.click_menu("推荐和飞信")
        mrp = MeRecommentdClienPage()
        mrp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # time.sleep(0.8)
        # mrp.click_text("短信")
        # # 3.选择本地联系人
        # scp = SelectContactsPage()
        # scp.wait_for_page_local_contact_load()
        # # 4.点击返回
        # scp.click_back()
        # mrp.wait_for_page_load()
        # mrp.click_back()
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_580(self):
        """设置页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        # 3.检验设置列表页面展示
        sp = SettingPage()
        sp.wait_for_page_load()
        # 版本更新有修改
        # menu = {"短信设置", "消息通知", "来电管理", "副号管理", "联系人管理", "字体大小", "多语言", "参与体验改善计划", "退出", }
        menu = {"消息", "通话", "联系人", "通用", "帮助与反馈", "关于和飞信", "退出登录", }
        self.assertEquals(sp.page_contain_texts(menu), True)
        # 4.点击返回
        sp.click_back()
        mep.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_583(self):
        """验证我-设置-退出登录(正常网络)"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        # 3.点击退出登陆
        sp = SettingPage()
        sp.wait_for_page_load()
        sp.click_logout()
        sp.click_ok_of_alert()
        # 4.校验退出后在登陆页面
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        self.assertEquals(one_key.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_584(self):
        """验证我-设置-退出登录(异常网络)"""
        # 备注：退出登录暂时不验证
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.set_network_status(0)
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        # 3.点击退出登陆
        sp = SettingPage()
        sp.wait_for_page_load()
        sp.click_logout()
        sp.click_ok_of_alert()
        # 4.校验退出后在登陆页面
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        self.assertEquals(one_key.is_on_this_page(), True)
        # 5.退出后再点击一键登录有弹框提示
        one_key.click_one_key_login()
        if not one_key.is_toast_exist("一键登录失败"):
            raise AssertionError("一键登录失败")

    def tearDown_test_me_zhangshuli_584(self):
        # 1.打开网络
        try:
            mess = MessagePage()
            mess.set_network_status(6)
        except:
            pass

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_586(self):
        """设置-参与体验改善计划(异常网络)"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的设置
        mess.open_me_page()
        mep = MePage()
        mep.is_on_this_page()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("关于和飞信")
        time.sleep(1)
        # 3.点击参与体验改善计划
        mcp = MeAboutChinasoftiPage()
        mcp.click_plan()
        time.sleep(1)
        # 断网
        mess.set_network_status(0)
        sp = SettingPage()
        time.sleep(3)
        sp.click_menu("上传日志")
        if not sp.is_toast_exist("上传失败，请稍后重试"):
            raise AssertionError("没有此网络异常弹框")
        mess.click_back_by_android()
        time.sleep(1)
        mess.click_back_by_android()
        time.sleep(1)
        mess.click_back_by_android()
        time.sleep(1)
        mep.open_message_page()

    def tearDown_test_me_zhangshuli_586(self):
        # 1.打开网络
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_587(self):
        """帮助与反馈跳转功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        time.sleep(3)
        result = mfp.is_text_present("意见反馈")
        self.assertEqual(result, True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_588(self):
        """帮助与反馈页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈
        from pages.me.MeHelpAndFeedback import MeHelpAndFeedbackPage
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        menu = {"常见问题", "更多", "哪些人可以开通和使用和飞信", "如何登录及退出登录和飞信", "怎么开启和飞信同步手机通讯录的权限", "在线咨询", "客服热线", "企业专家服务", "论坛互动",
                "意见反馈"}
        self.assertEquals(mfp.page_contain_text(menu), True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_589(self):
        """常见问题列表信息跳转到详情页验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击常见问题列表信息
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        menu = {"常见问题", "更多", "哪些人可以开通和使用和飞信", "如何登录及退出登录和飞信", "怎么开启和飞信同步手机通讯录的权限", "在线咨询", "客服热线", "企业专家服务", "论坛互动",
                "意见反馈"}
        self.assertEquals(mfp.page_contain_text(menu), True)
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("哪些人可以开通和使用和飞信")
        # mfp.wait_for_page_load()
        # mfp.page_should_contain_text("哪些人可以开通和使用和飞信")
        # 4.点击返回
        # mfp.click_back()
        # self.assertEquals(mfp.page_contain_text(menu), True)

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_590(self):
        """常见问题更多跳转功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的更多,跳转到热点问题页面
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("更多")
        # mfp.wait_for_page_load()
        # mfp.page_should_contain_text("常见问题")
        # mfp.page_should_contain_text("问题分类")
        # # 4.点击返回
        # mfp.click_back()
        # mfp.click_back()
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_591(self):
        """常见问题更多页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的更多,跳转到热点问题页面
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("更多")
        # mfp.wait_for_page_load()
        # menu = {"常见问题", "问题分类", "消息篇", "通话篇", "通讯录", "工作台", "通用篇", "资费篇"}
        # self.assertEquals(mfp.page_contain_text(menu), True)
        # # 4.点击返回
        # mfp.click_back()
        # mfp.click_back()
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_592(self):
        """常见问题列表信息跳转到详情页验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击常见问题列表信息
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        menu = {"常见问题", "更多", "哪些人可以开通和使用和飞信", "如何登录及退出登录和飞信", "怎么开启和飞信同步手机通讯录的权限", "在线咨询", "客服热线", "企业专家服务", "论坛互动",
                "意见反馈"}
        self.assertEquals(mfp.page_contain_text(menu), True)
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("哪些人可以开通和使用和飞信")
        # mfp.wait_for_page_load()
        # mfp.page_should_contain_text("哪些人可以开通和使用和飞信")
        # # 4.点击返回
        # mfp.click_back()
        # self.assertEquals(mfp.page_contain_text(menu), True)
        # # 5.点击关闭
        # mfp.click_text_button("哪些人可以开通和使用和飞信")
        # mfp.wait_for_page_load()
        # mfp.click_text_button("X")
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_593(self):
        """常见问题页面问题分类功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的更多,跳转到热点问题页面
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("更多")
        # mfp.wait_for_page_load()
        # menu = {"常见问题", "问题分类", "消息篇", "通话篇", "通讯录", "工作台", "通用篇", "资费篇"}
        # self.assertEquals(mfp.page_contain_text(menu), True)
        # # 4.点击任意问题分类
        # mfp.click_text_button("资费篇1")
        # mfp.element_contain_text("资费篇", "资费篇")
        # mfp.page_should_contain_text("基本资费")
        # mfp.click_text_button("每月10GB定向流量套餐是什么")
        # mfp.element_contain_text("资费篇", "资费篇")
        # mfp.page_should_contain_text("每月10G流量包内定向流量仅适用于和飞信手机APP")
        # # 5.点击返回
        # mfp.click_back()
        # mfp.page_should_contain_text("基本资费")
        # # 6.点击关掉
        # mfp.click_text_button("X")
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_594(self):
        """在线咨询跳转功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的在线咨询
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("在线咨询")
        # mfp.wait_for_page_load()
        # mfp.page_contain_text("在线客服")
        # # 4.点击返回
        # mfp.click_text_button("X")
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_596(self):
        """企业专家服务跳转功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的客服热线
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("企业专家服务")
        # mfp.wait_for_page_load()
        # mfp.page_contain_text("预约")
        # # 5.点击返回
        # mfp.click_back()
        # mfp.click_back()
        # mess.open_message_page()

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_597(self):
        """论坛互动跳转功能验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的客服热线
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("论坛互动")
        # mfp.wait_for_page_load()
        # mfp.page_contain_text("和飞信社区")

    @tags('ALL', 'CMCC', 'me_all', 'debug_fk_me3')
    def test_me_zhangshuli_598(self):
        """意见反馈页面显示验证"""
        # 1.点击跳转到我的页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 2.点击我的帮助与反馈
        mess.open_me_page()
        mep = MePage()
        mep.click_setting_menu()
        time.sleep(1)
        mep.click_menu("帮助与反馈")
        time.sleep(3)
        # 3.点击进入帮助与反馈的客服热线
        mfp = MeHelpAndFeedbackPage()
        mfp.wait_for_page_load()
        # 备注：WebView加载的H5页面无法点击-华为note8手机
        # mfp.click_text_button("意见反馈")
        # mfp.wait_for_page_load()
        # menu = {"你想反馈的类型", "请补充详细问题和意见", "建议输入10个字以上的描述", "相册/相机", "提交"}
        # mfp.page_contain_text(menu)
        # # 5.点击返回
        # mfp.click_back()
        # mfp.click_back()
        # mess.open_message_page()
