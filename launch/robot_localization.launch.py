import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    pkg_share = FindPackageShare(package='robot_launcher_cpp').find('robot_launcher_cpp')
    default_rob_loc_param_path = os.path.join(pkg_share, 'config/ekf.yaml')



    rlparam_path = LaunchConfiguration('rlparam_path', default='default_rob_loc_param_path')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    #LOGGER
    logger = LaunchConfiguration('log_level', default=["info"])

    declare_logger_cmd = DeclareLaunchArgument(
        name='log_level',
        default_value="info",
        description='Indicates logging level of Nodes')

    robot_localization_node = Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[default_rob_loc_param_path, {'use_sim_time':use_sim_time}],
       arguments=['--ros-args','--log-level',logger]
    )

    return LaunchDescription(
        [declare_logger_cmd,
        robot_localization_node]
    )