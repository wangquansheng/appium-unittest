from TestCase.m001_login.login import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


class TeamTest(TestCase):
    """工作台->团队创建"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """进入创建团队页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_create_team_page()
            return
        team = CreateTeamPage()
        if team.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_create_team_page()

    def default_tearDown(self):
        pass

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0001(self):
        """检查创建团队界面是否正确返回到工作台主界面"""
        # 1、点击最底部的“创建团队”
        # 2、点击左上角【<】返回
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC1",'workbench')
    def test_TDCJ_0002(self):
        """创建团队"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0003(self):
        """创建团队-团队名称为空"""
        team = CreateTeamPage()
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请输入团队名称")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0004(self):
        """创建团建-所在地为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请选择所在地")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0005(self):
        """创建团建-行业为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请选择行业")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0006(self):
        """创建团建-姓名为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.choose_industry()
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("管理员姓名不能为空")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL',"CMCC", 'workbench')
    def test_TDCJ_0007(self):
        """创建团建-邮箱为空"""
        team = CreateTeamPage()
        team.input_team_name("测试团队")
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        team.input_email('')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("请输入邮箱地址")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()


@unittest.skip("过滤")
class WorkbenchGGXXTest(TestCase):
    """工作台->公告信息"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    @staticmethod
    def setUp_test_workbench_GGXX_0005():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.create_team_message("天气预报","晴天转多云")
        time.sleep(1)

    @tags('ALL',"CMCC", 'Login', "workbench")
    def test_workbench_GGXX_0005(self):
        '验证公告信息首页搜索是否正确'
        pg = CreateTeamPage()
        pg.click_enter_search()
        pg.input_search_text()
        pg.is_text_present('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0005():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL',"CMCC", 'Login', "workbench")
    def test_workbench_GGXX_0006(self):
        '验证未发公告页搜索是否正确'
        pg = CreateTeamPage()
        pg.click_no_publish()
        pg.click_enter_search()
        pg.input_search_text()
        pg.is_text_present('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0006():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0007():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.create_team_message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL',"CMCC", 'Login', "workbench")
    def test_workbench_GGXX_0007(self):
        '已发布公告下线'
        pg = CreateTeamPage()
        pg.click_list_message()
        pg.click_remove_message()
        time.sleep(2)
        pg.page_should_not_contain_text('天气预报')

    @staticmethod
    def tearDown_test_workbench_GGXX_0007():
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0008():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL',"CMCC", 'Login', "workbench")
    def test_workbench_GGXX_0008(self):
        '公告存草稿'
        pg = CreateTeamPage()
        pg.click_no_publish()
        time.sleep(1)
        pg.page_should_contain_text("天气预报")

    @staticmethod
    def tearDown_test_workbench_GGXX_0008():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_0009():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL',"CMCC", 'Login', "workbench")
    def test_workbench_GGXX_0009(self):
        """
        发布未发布中公告
        :return:
        """
        pg = CreateTeamPage()
        pg.click_no_publish()
        time.sleep(1)
        pg.click_list_message()
        pg.click_publish()
        pg.click_sure()
        time.sleep(2)
        pg.page_should_contain_text("天气预报")
        time.sleep(1)

    @staticmethod
    def tearDown_test_workbench_GGXX_0009():
        # 恢复网络连接
        oklp = OneKeyLoginPage()
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)

    @staticmethod
    def setUp_test_workbench_GGXX_00010():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        pg = CreateTeamPage()
        pg.click_workbeanch_button()
        time.sleep(5)
        pg.page_up()
        pg.click_public_message()
        pg.save_team__message("天气预报", "晴天转多云,风云多变")
        time.sleep(1)

    @tags('ALL', "CMCC",'Login', "workbench")
    def test_workbench_GGXX_00010(self):
        """
        删除,公告中草稿
        """
        pg = CreateTeamPage()
        time.sleep(1)
        pg.click_no_publish()
        time.sleep(1)
        pg.remove_message()
        time.sleep(2)
        flag=pg.page_should_not_contain_text("天气预报")

    @staticmethod
    def tearDown_test_workbench_GGXX_00010():
        oklp = OneKeyLoginPage()
        time.sleep(10)
        pg = CreateTeamPage()
        pg.remove_message()
        oklp.press_home_key(3)


class TeamTestAll(TestCase):
    """工作台->团队创建"""

    @classmethod
    def setUpClass(cls) -> None:
        import warnings
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """进入创建团队页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_create_team_page()
            return
        team = CreateTeamPage()
        if team.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_create_team_page()

    def default_tearDown(self):
        pass

    @tags('ALL',"CMCC", 'workbench','CJTD')
    def test_CJTD_0002(self):
        """企业名称少于3个字"""
        # 1.在移动端创建团队页面，企业名称输入少于3个字，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我")
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        if not team.is_text_present("团队名称不能少于3个字"):
            raise AssertionError("没有提示团队名称不少于3个字")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0003(self):
        """企业名称长度在3-50个字之间"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0004(self):
        """企业名称大于50个字"""
        # 1.在移动端创建团队页面，企业名称输入大于50个字点【提交注册】
        team = CreateTeamPage()
        name="我"*51
        team.input_team_name(name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(1)
        team.page_should_contain_text("团队名称不能超过50个字")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0006(self):
        """地区只选择省，不选择市"""
        #1.在移动端创建团队页面，其他信息填写完成，地区只选择省，不选择市，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_industry()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("请选择所在地")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0007(self):
        """地区选择完成"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0009(self):
        """地区只选一级行业，不选二级行业"""
        #1.在移动端创建团队页面，其他信息填写完成，地区只选一级行业，不选二级行业，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.input_real_name('admin')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("请选择行业")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0010(self):
        """行业类型选择完成"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0012(self):
        """管理员姓名少于2位"""
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        team.input_real_name('a')
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("管理员姓名不得少于2位")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0013(self):
        """管理员姓名超过20个汉字"""
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name="好"*21
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("姓名不能超过20个汉字或60个字母")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0014(self):
        """管理员姓名超过60个字母"""
        #1.在移动端创建团队页面，其他信息填写完成，管理员姓名输入超过60个字母，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name = "a" * 61
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("姓名不能超过20个汉字或60个字母")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0015(self):
        """管理员姓名输入非法字符"""
        #1.在移动端创建团队页面，其他信息填写完成，管理员姓名输入非汉字、字母数字和空格，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name = "*" * 3
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("只许输入中文、字母、数字或空格")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0016(self):
        """管理员姓名输入1位+空格"""
        #1.在移动端创建团队页面，其他信息填写完成，管理员姓名输入管理员姓名输入1位+空格，点【提交注册】
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name = "a "
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("管理员姓名不得少于2位")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    # @tags('ALL', "CMCC", 'workbench')
    @unittest.skip("过")
    def test_CJTD_0017(self):
        """管理员姓名输入2位+空格"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = "CJTD_0017"
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team(default_team_name,user_name="aa ")
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    #@tags('ALL', "CMCC", 'workbench')
    @unittest.skip("过")
    def test_CJTD_0018(self):
        """管理员姓名输入20个汉字或60个字母"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = "CJTD_0018"
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        user_name="哈"*20
        Preconditions.create_team(default_team_name, user_name)
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0019(self):
        """账号为大陆手机号邮箱地址自动填写"""
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        # user_name = "哈" * 20
        # Preconditions.create_team(default_team_name, user_name)
        email=team.get_email_text()
        a = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        b=a+"@139.com"
        if not email==b:
            raise AssertionError("邮箱地址没有自动填写")
        #创建团队
        team = CreateTeamPage()
        team.input_team_name(default_team_name)
        team.choose_location()
        team.choose_industry()
        team.input_real_name("admin")
        # 立即创建团队
        team.click_immediately_create_team()
        # 点击完成设置工作台
        team.wait_for_setting_workbench_page_load()
        team.click_finish_setting_workbench()
        team.wait_for_create_team_success_page_load()
        # 进入工作台
        team.click_enter_workbench()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0021(self):
        """输入无效的邮箱地址格式"""
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name = "admin"
        team.input_real_name(name)
        team.input_email("123456")
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("请输入正确的邮箱地址")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0022(self):
        """输入正确的邮箱地址"""
        #1.在移动端创建团队页面，其他信息填写完成，输入正确的邮箱地址，点【提交注册】
        team = CreateTeamPage()
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        # 有默认的团队，就不创建
        default_team_name = Preconditions.get_team_name()
        workbench.click_enterprise_name_triangle()
        time.sleep(1)
        teams = workbench.get_team_names()
        current_mobile().back()
        if default_team_name in teams:
            print("当前已有团队:" + default_team_name + ",未再创建！")
            workbench.click_create_team()
            team.wait_for_page_load()
            return
        # 点击最底部的“创建团队”
        workbench.click_create_team()
        team.wait_for_page_load()
        Preconditions.create_team()
        # 回到创建团队页面
        workbench.click_create_team()
        team.wait_for_page_load()

    # @tags('ALL', "CMCC", 'workbench', 'CJTD')
    @unittest.skip("过")
    def test_CJTD_0024(self):
        """同一个账号一天内注册三家企业"""
        #1.在移动端创建团队页面，同一个账号一天内注册三家企业
        #前提是在这一天内没有创建过其他团队和已经创建的团队数量没有达到上限
        a=0
        while a<3:
            team = CreateTeamPage()
            team.click_back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            # 有默认的团队，就不创建
            param="aa"+str(a)
            default_team_name = param
            workbench.click_enterprise_name_triangle()
            time.sleep(1)
            teams = workbench.get_team_names()
            current_mobile().back()
            if default_team_name in teams:
                print("当前已有团队:" + default_team_name + ",未再创建！")
                workbench.click_create_team()
                team.wait_for_page_load()
                return
            # 点击最底部的“创建团队”
            workbench.click_create_team()
            team.wait_for_page_load()
            Preconditions.create_team(default_team_name, user_name=param)
            # 回到创建团队页面
            workbench.click_create_team()
            team.wait_for_page_load()
            a+=1
            time.sleep(2)

    # @tags('ALL', "CMCC", 'workbench', 'CJTD')
    @unittest.skip("过")
    def test_CJTD_0025(self):
        """同一个账号一天内注册第四家企业"""
        #1.在移动端创建团队页面，同一个账号一天内注册第四家企业
        #前提是当天已经创建了3家企业
        team = CreateTeamPage()
        team.input_team_name("我我我")
        team.choose_location()
        team.choose_industry()
        name = "admin"
        team.input_real_name(name)
        # team.input_email("123456")
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("您今天创建的团队已达上限")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC1", 'workbench', 'CJTD')
    def test_CJTD_0027(self):
        """敏感词检验 -- 企业名称检查"""
        # 1、企业名称输入敏感词：如法论功组织等
        # 2、其他正常信息正常填写
        team = CreateTeamPage()
        team.input_team_name("法轮功")
        team.choose_location()
        team.choose_industry()
        name = "admin"
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("311")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0028(self):
        """敏感词检验 -- 管理员检查"""
        # 1、依次填写企业名称、选择所在地、行业
        # 2、管理员姓名输入敏感词：如法论功等
        team = CreateTeamPage()
        team.input_team_name("test_CJTD_0028")
        team.choose_location()
        team.choose_industry()
        name = "法轮功"
        team.input_real_name(name)
        # 立即创建团队
        team.click_immediately_create_team()
        time.sleep(2)
        team.page_should_contain_text("315")
        team.click_sure()
        # 清除输入数据
        team.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.click_create_team()
        team.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'CJTD')
    def test_CJTD_0029(self):
        """企业切换"""
        # 1.点击界面左上角显示的企业
        # 2.点击与当前企业不同的任一企业
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.click_element_("当前团队名称")
        time.sleep(2)
        workbench.click_element_("第二个团队")
        time.sleep(3)
        workbench.click_element_("当前团队名称")
        time.sleep(2)
        workbench.click_element_("第一个团队")
