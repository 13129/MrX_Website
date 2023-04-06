SIMPLEUI_CONFIG = {
    'system_keep': False,  # 关闭系统菜单
    'menu_display': ['认证和授权', '工作记录', '数据管理工具', '扩展工具'],
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'app': 'auth',
        'name': '认证和授权',
        'icon': 'fas fa-shield-alt',
        'models': [{
            'name': '用户',
            'icon': 'far fa-user',
            'url': 'users/users/'
        }, {
            'name': '组',
            'icon': 'fas fa-users-cog',
            'url': 'auth/group/',
        }]
    }, {
        'app': 'blogs',
        'name': '工作记录',
        'icon': '',
        'models': [{
            'name': '记录分类',
            'icon': '',
            'url': 'blogs/category/'
        }, {
            'name': '记录信息',
            'icon': '',
            'url': 'blogs/blog/'
        }, {
            'name': '记录标签',
            'icon': '',
            'url': 'blogs/tag/'
        }]
    }, {
        'app': 'data_tools',
        'name': '数据管理工具',
        'icon': '',
        'models': [{
            'name': '目录关联管理',
            'icon': '',
            'url': 'data_tools/directorytable/'
        }, {
            'name': '目录管理',
            'icon': '',
            'url': 'data_tools/themedirectory/'
        }, {
            'name': '表管理',
            'icon': '',
            'url': 'data_tools/datasourcetable/'
        }, {
            'name': '字段管理',
            'icon': '',
            'url': 'data_tools/datasourcetablefield/'
        }, {
            'name': '数据源管理',
            'icon': '',
            'url': 'data_tools/datasource/'
        }, {
            'name': '数据源类型',
            'icon': '',
            'url': 'data_tools/datasourcetype/'
        }]
    }, {
        'app': 'extension_tools',
        'name': '扩展工具',
        'icon': '',
        'models': [{
            'name': '视频分类',
            'icon': '',
            'url': 'extension_tools/videocate/'
        }, {
            'name': '视频上传',
            'icon': '',
            'url': 'extension_tools/videoupload/'
        }, {
            'name': '访客信息',
            'icon': '',
            'url': 'extension_tools/tourist/'
        }, {
            'name': '友链接',
            'icon': '',
            'url': 'extension_tools/link/'
        }, {
            'name': '网站公告',
            'icon': '',
            'url': 'extension_tools/notice/'
        }]
    }]
}
