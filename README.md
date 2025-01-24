## robot_launcher_cpp
Launch robot in Gazebo and Rviz2.
Hello there, this is a package that can be used to launch your robot in both Gazebo and Rviz. Here are the steps:
1. Create your robot description files and save them in a folder inside the "urdf" folder.
2. Save your meshes in a folder in the "meshes" folder.
3. Create a folder with your robot's name in the "models" folder. This is where you would save the .sdf files for Gazebo Simulation.
4. Add the meshes in a meshes folder inside your robot model folder. This would be required for the Gazebo Simulation.
5. Use these lines to create your SDF files:
   cd to your "urdf" file
   xacro <file_name>.xacro > <file_name>.urdf
   gz sdf -p <file_name>.urdf > ../../models/<folder_name>/model.sdf
6. Make sure that the urdf file has an empty link named "world".

## More updates coming soon


