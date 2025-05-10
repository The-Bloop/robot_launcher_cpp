import os
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
    robot_name = 'WheelRobot'
    # model_name = 'wrv4'
    pkg_share = FindPackageShare(package='robot_launcher_cpp').find('robot_launcher_cpp')
    urdf_model_path = os.path.join(pkg_share, 'urdf/wrv4/wrv4.urdf.xacro')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz_basic_settings.rviz')
    world = os.path.join(
        pkg_share,
        'worlds',
        'turtlebot3_world.world'
    )

    #Initializing Launch Configurations

    model_name = LaunchConfiguration('model_name', default='wrv4')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-0.5')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')
    use_rviz = LaunchConfiguration('use_rviz', default='true')

    logger = LaunchConfiguration('log_level', default=["info"])
    gazebo_log = LaunchConfiguration('gazebo_log', default="false")

    #Declaring Launch Arguments

    model_name_arg = DeclareLaunchArgument(
        name='model_name',
        default_value='wrv4',
        description='Enter Version name of Robot'
    )

    use_rviz_arg = DeclareLaunchArgument(
        name='use_rviz',
        default_value='True',
        description='Flag to control use of RVIZ'
    )

    logger_arg = DeclareLaunchArgument(
        name='log_level',
        default_value="info",
        description='Indicates logging level of Nodes'
    )
        
    gazebo_log_arg = DeclareLaunchArgument(
        name='gazebo_log',
        default_value="false",
        description='Indicates gazebo verbosity'
    )

    sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value="true",
        description='On/Off Simulation time'
    )

    x_pose_arg = DeclareLaunchArgument(
        name='x_pose',
        default_value=x_pose,
        description="Position of robot along X axis"
    )

    y_pose_arg = DeclareLaunchArgument(
        name='y_pose',
        default_value=y_pose,
        description="Position of robot along Y axis"
    )

    # print(x_pose)
    # print(model_name.variable_name[0].perform())
    # file_name = 'urdf/' + model_name + '/' + model_name + '.urdf.xacro'
    # print(file_name)

    robot_description = Command([FindExecutable(name='xacro'), ' ', urdf_model_path])

    #Initializing Other Launch Files
    #To change log level of the launch files add the following in launch_arguments:
    #'verbose': gazebo_log

    gzserver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world,'verbose': gazebo_log}.items()
    )

    gzclient_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'robot_localization.launch.py')
        ),
    )

    #Creating Nodes
    #To control log level of nodes add the following to the node's Arguments:
    # '--ros-args','--log-level',logger

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[urdf_model_path],
        parameters=[{'use_sim_time': use_sim_time}],
        )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 
        'robot_description': robot_description}],
        arguments=['--ros-args','--log-level',logger]
    )

    gazebo_ros_spawner_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', robot_name,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01',
            '--ros-args','--log-level',logger
        ],
        output='screen',
    )

    rviz_node = Node(
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
    ld.add_action(model_name_arg)
    ld.add_action(use_rviz_arg)
    ld.add_action(logger_arg)
    ld.add_action(gazebo_log_arg)
    ld.add_action(sim_time_arg)
    ld.add_action(x_pose_arg)
    ld.add_action(y_pose_arg)

    #Launch Files
    ld.add_action(gzserver_launch)
    ld.add_action(gzclient_launch)
    ld.add_action(joint_state_publisher_node)
    #ld.add_action(ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'))
    ld.add_action(robot_state_publisher_node)
    ld.add_action(gazebo_ros_spawner_node)
    ld.add_action(robot_localization_launch)
    ld.add_action(rviz_node)
    

    return ld