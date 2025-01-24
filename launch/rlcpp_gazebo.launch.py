import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    #File Paths
    pkg_share = FindPackageShare(package='robot_launcher_cpp').find('robot_launcher_cpp')
    urdf_model_path = os.path.join(pkg_share, 'urdf/wrv3/wrv3.xacro')
    sdf_model_path = os.path.join(pkg_share, 'models', 'wrv3', 'model2.sdf')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz_basic_settings.rviz')
    robot_description_raw = xacro.process_file(urdf_model_path).toxml()
    world = os.path.join(
        pkg_share,
        'worlds',
        'empty.world'
    )

    #Initializing Launch Configurations

    urdf_model = LaunchConfiguration('urdf_model', default=urdf_model_path)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    use_rviz = LaunchConfiguration('use_rviz', default='true')
    sdf_model = LaunchConfiguration('sdf_model', default=sdf_model_path)

    logger = LaunchConfiguration('log_level', default=["info"])
    gazebo_log = LaunchConfiguration('gazebo_log', default="false")

    #Declaring Launch Arguments

    declare_use_rviz_cmd = DeclareLaunchArgument(
        name='use_rviz',
        default_value='True',
        description='Flag to control use of RVIZ'
    )

    declare_logger_cmd = DeclareLaunchArgument(
        name='log_level',
        default_value="info",
        description='Indicates logging level of Nodes'
    )
        
    declare_gazebo_log_cmd = DeclareLaunchArgument(
        name='gazebo_log',
        default_value="true",
        description='Indicates gazebo verbosity'
    )

    declare_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value="true",
        description='On/Off Simulation time'
    )

    declare_x_pose_cmd = DeclareLaunchArgument(
        name='x_pose',
        default_value=x_pose,
        description="Position of robot along X axis"
    )

    declare_y_pose_cmd = DeclareLaunchArgument(
        name='y_pose',
        default_value=y_pose,
        description="Position of robot along Y axis"
    )

    robot_description = Command([FindExecutable(name='xacro'), ' ', urdf_model_path])

    #Initializing Other Launch Files
    #To change log level of the launch files add the following in launch_arguments:
    #'verbose': gazebo_log

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world,'verbose': gazebo_log}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_localization_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'robot_localization.launch.py')
        ),
    )

    #Creating Nodes
    #To control log level of nodes add the following to the node's Arguments:
    # '--ros-args','--log-level',logger

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[urdf_model_path],
        parameters=[{'use_sim_time': use_sim_time}],
        )

    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 
        'robot_description': robot_description}],
        arguments=['--ros-args','--log-level',logger]
    )

    start_gazebo_ros_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'WheelRobotv3',
            '-file', sdf_model_path,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01',
            '--ros-args','--log-level',logger
        ],
        output='screen',
    )

    start_rviz_cmd = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config_path]
    )

    ld = LaunchDescription()

    # Add the commands to the launch description
    #Launch Arguments
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_logger_cmd)
    ld.add_action(declare_gazebo_log_cmd)
    ld.add_action(declare_sim_time_cmd)
    ld.add_action(declare_x_pose_cmd)
    ld.add_action(declare_y_pose_cmd)

    #Launch Files
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(start_joint_state_publisher_cmd)
    #ld.add_action(ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'))
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_gazebo_ros_spawner_cmd)
    ld.add_action(robot_localization_cmd)
    ld.add_action(start_rviz_cmd)
    

    return ld