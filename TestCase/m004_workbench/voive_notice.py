import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.Workbench import WorkbenchPage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
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
        # one_key.click_read_agreement_detail()
        #
        # # 同意协议
        # agreement = AgreementDetailPage()
        # agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
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
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()


class VoiceNoticeTest(TestCase):
    """工作台->语音通知"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        wbp = WorkbenchPage()
        if mess.is_on_this_page():
            mess.open_workbench_page()
            return
        if wbp.is_on_this_page():
            return
        else:
            # current_mobile().reset_app()
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            mess.open_workbench_page()

    @tags('ALL', 'CMCC', 'workbench', 'debug_fk')
    def test_YYTZ_0001(self):
        """正常查看使用该指引"""
        # 0.进入语音通知页面
        wbp = WorkbenchPage()
        wbp.click_voice_notice()
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads("创建语音通知")
        # 1.点击点击右上角【？】
        vnp.click_enter_more()
        vnp.wait_for_page_loads("语音通知使用指引")
        # 2.上下滑动浏览页面
        for i in range(3):
            vnp.swipe_half_page_up()
        self.assertEquals(vnp.find_els_h5("接听通知"), True)
        vnp.swipe_half_page_down()
        # 3.点击返回
        vnp.click_back()
        vnp.click_back()

    @tags('ALL', 'CMCC', 'workbench', 'debug_fk')
    def test_YYTZ_0015(self):
        """点击顶部关闭按钮"""
        # 0.进入语音通知页面
        wbp = WorkbenchPage()
        wbp.click_voice_notice()
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads("创建语音通知")
        # 1.点击点击右上角【？】
        vnp.click_enter_more()
        vnp.wait_for_page_loads("语音通知使用指引")
        # 2.在其他有关闭按钮页面，点击顶部【x】
        vnp.click_close_more()
        time.sleep(3)
        self.assertEquals(wbp.is_on_this_page(), True)

    @tags('ALL', 'CMCC', 'workbench', 'debug_fk')
    def test_cjhy_0001(self):
        """查看超级会议使用说明"""
        # 0.进入超级会议页面页面
        wbp = WorkbenchPage()
        wbp.click_super_meeting()
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads("超级会议")
        # 1.点击点击右上角【？】
        vnp.click_enter_more()
        vnp.wait_for_page_loads("超级会议使用说明")
        # 2.上下滑动浏览页面
        for i in range(3):
            vnp.swipe_half_page_up()
        self.assertEquals(vnp.find_els_h5("会场管理"), True)
        vnp.swipe_half_page_down()
        # 3.点击返回
        vnp.click_back()
        vnp.click_back()

    @tags('ALL', 'CMCC', 'workbench', 'debug_fk')
    def test_TCTD_0002(self):
        """主管理员-工作台团队列表退出团队"""
        mess = MessagePage()
        # 1.点击左上角的企业名称的倒三角，长按企业名称
        wbp = WorkbenchPage()
        wbp.click_press_enterprise_name()
        wbp.page_should_contain_text("解散团队")
        # 2.点击【解散团队】
        wbp.click_cancel_team()
        wbp.page_should_contain_text("请您根据指引完成操作")
        # 3.点击确定
        wbp.click_sure()
        wbp.page_should_not_contain_text("请您根据指引完成操作")
        wbp.click_back_team()
        wbp.is_on_this_page()

