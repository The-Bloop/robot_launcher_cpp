## robot_launcher_cpp
# Launch Robot in Gazebo and Rviz2

This package allows you to launch your robot in both Gazebo and Rviz. Follow the steps below to set it up:

## Steps

1. **Create Robot Description Files**  
   - Save your robot description files in a folder inside the `urdf` folder.

2. **Save Meshes**  
   - Save your meshes in a folder inside the `meshes` folder.

3. **Create a Robot Model Folder**  
   - Create a folder with your robot's name in the `models` folder.  
   - Save the `.sdf` files for Gazebo simulation in this folder.

4. **Add Meshes for Gazebo**  
   - Add the meshes in a `meshes` folder inside your robot model folder. This is required for Gazebo simulation.

5. **Generate SDF Files**  
   Use the following commands to create your SDF files:  
   ```bash
   # Navigate to the "urdf" folder
   cd <path_to_urdf_folder>

   # Convert .xacro to .urdf
   xacro <file_name>.xacro > <file_name>.urdf

   # Convert .urdf to .sdf and save in the models folder
   gz sdf -p <file_name>.urdf > ../../models/<folder_name>/model.sdf


## More updates coming soon


