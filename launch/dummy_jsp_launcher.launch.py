import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    pkg_share = FindPackageShare(package='robot_launcher_cpp').find('robot_launcher_cpp')
 
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz_basic_settings.rviz')

    default_urdf_model_path = os.path.join(pkg_share, 'urdf/wrv3/wrv3.xacro')

    urdf_model = LaunchConfiguration('urdf_model', default=default_urdf_model_path)
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    #declare_urdf_model_path_cmd = DeclareLaunchArgument(
    #    name='urdf_model', 
    #    default_value=default_urdf_model_path, 
    #    description='Absolute path to robot urdf file')

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        name='rviz_config_file',
        default_value=default_rviz_config_path,
        description='Full path to the RVIZ config file to use')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')

    print("urdf: ", urdf_model)

    logger = LaunchConfiguration('log_level', default=["debug"])

    #condition=UnlessCondition(gui),
    #condition=IfCondition(gui),
    #condition=IfCondition(use_robot_state_pub),
    #condition=IfCondition(use_rviz),
    #Command(['xacro ', urdf_model])}],
    #    arguments=[default_urdf_path])
    #Actions
    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
        )

    start_joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui')

    start_robot_state_publisher_cmd = Node(
        condition= IfCondition(use_sim_time),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': True, 
        'robot_description': Command(['xacro ', urdf_model])}],
        arguments=[default_urdf_model_path])

    start_rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file])

#Add Gazebo
    #gazebo = DeclareLaunchArgument(
    #    PythonLaunchDescriptionSource(os.path.join(
    #        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    #    )
    #)

    #spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                arguments=['-entity', 'my_bot',
    #                        '-file', default_urdf_model_path,
    #                        '-x', '0',
    #                        '-y', '0',
    #                        '-z', '0'
    #                            ],
    #                output='screen')

    ld = LaunchDescription()

    #ld.add_action(declare_urdf_model_path_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_use_sim_time_cmd)

    ld.add_action(start_joint_state_publisher_cmd)
    ld.add_action(start_joint_state_publisher_gui_node)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)

    return ld

