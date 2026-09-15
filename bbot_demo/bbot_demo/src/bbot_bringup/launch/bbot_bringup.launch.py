from launch import LaunchDescription
from launch_ros.actions import Node
# 封装终端指令相关类--------------
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable
# 参数声明与获取-----------------
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration
# 文件包含相关-------------------
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
# 分组相关----------------------
# from launch_ros.actions import PushRosNamespace
# from launch.actions import GroupAction
# 事件相关----------------------
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import ExecuteProcess, RegisterEventHandler,LogInfo
# 获取功能包下share目录路径-------
from ament_index_python.packages import get_package_share_directory
import os


# 定义函数 generate_launch_description，这是 ROS 2 launch 系统的入口点
def generate_launch_description():
    # 定义变量 package_file_name，存储机器人描述功能包的名称
    package_file_name = 'bbot_description'
    
    # 创建一个包含其他 launch 文件的动作
    # IncludeLaunchDescription 用于将另一个 launch 文件的内容包含进来
    bbot = IncludeLaunchDescription(
        # PythonLaunchDescriptionSource 指定被包含的 launch 文件路径
        launch_description_source= PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory(package_file_name),  # 获取 bbot_description 包的 share 目录
                'launch',                                         # 进入 launch 子目录
                'bbot.launch.py'                                  # 指定要包含的 launch 文件名
            )
        ]),
        # launch_arguments 用于向被包含的 launch 文件传递参数（以键值对形式）
        # .items() 将字典转换为可迭代的键值对
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # 创建另一个包含动作，用于启动 Gazebo 仿真器（gazebo.launch.py）
    gazebo = IncludeLaunchDescription(
        launch_description_source= PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('gazebo_ros'),  # 获取 gazebo_ros 包的 share 目录
                'launch',                                   # launch 子目录
                'gazebo.launch.py'                          # Gazebo 的启动文件
            )
        ])
    )
    
    # 创建一个节点动作，用于在 Gazebo 中生成机器人实体
    spawn_entity = Node(
        package='gazebo_ros',                 # 节点所在的功能包
        executable='spawn_entity.py',         # 可执行文件名称（Python 脚本）
        arguments=[                           # 传递给可执行文件的命令行参数
            '-topic', 'robot_description',    # 指定机器人描述的话题名
            '-entity', 'bbot'                 # 指定生成的实体（模型）名称
        ],
        output='screen'                       # 将节点的标准输出打印到屏幕
    )
    
    # 创建一个节点动作，用于启动 joint_state 控制器生成器
    # 该节点会等待 controller_manager 服务，然后加载并激活 joint_state_broadcaster
    joint_broad_spawner = Node(
        package='controller_manager',         # controller_manager 功能包
        executable='spawner',                 # spawner 可执行文件
        arguments=['joint_state']             # 参数：要生成的控制器名称（对应 YAML 中的 joint_state）
    )
    
    # 创建一个节点动作，用于启动 diff_drive 控制器生成器
    diff_drive_spawner = Node(
        package='controller_manager',         # controller_manager 功能包
        executable='spawner',                 # spawner 可执行文件
        arguments=['diff_drive']              # 参数：要生成的控制器名称（对应 YAML 中的 diff_drive）
    )
    
    # 返回 LaunchDescription 对象，包含所有需要启动的动作
    # 注意：动作列表中的顺序会影响启动顺序（但不保证完全串行）
    return LaunchDescription([
        bbot,                 # 首先包含机器人描述 launch（通常发布 robot_description 并启动 robot_state_publisher）
        gazebo,               # 然后启动 Gazebo 仿真器（gazebo server 和 client）
        spawn_entity,         # 在 Gazebo 中生成机器人模型（依赖 robot_description 话题）
        diff_drive_spawner,   # 启动差速控制器生成器（等待 controller_manager 服务）
        joint_broad_spawner   # 启动关节状态发布器生成器
    ])