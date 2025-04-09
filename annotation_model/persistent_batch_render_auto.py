import subprocess
import os
import argparse

import shutil
import multiprocessing

import pickle

def get_core_id():
    """Gets the core ID the process is currently running on (Linux only)."""
    with open("/proc/self/stat", "r") as f:
        stat_info = f.read().split()
        core_id = int(stat_info[38])  # The 39th field contains the core ID
    return core_id

def flatten_directory(source_directory, target_dir):
    # Walk through the source directory
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            # Check if the file is a .glb file
            if file.endswith(".glb"):
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Define the target path for the .glb file
                target_path = os.path.join(target_dir, file)
                # Move the file
                shutil.move(file_path, target_path)



def render_object(target_path, output_dir):
    command = [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        "-b",
        "-P",
        "persistent_blender_script.py",
        "--",
        "--object_path",
        target_path,
        "--output_dir",
        output_dir,
        "--engine",
        "CYCLES",
        "--scale",
        "0.8",
        "--num_images",
        "40",
        "--camera_dist",
        "1.2",
    ]

    # Run the Blender command
    subprocess.run(command)

def render_batch(object_files, target_path, output_dir, core_id):
    """Runs Blender to render a batch of objects."""
    #core_id = get_core_id()
    #set_affinity(core_id)
    command = [
        "taskset",
        "-c",
        str(core_id),
        "/mnt/2077AI/3d_model_labeller/Multiview_3D_model_classifier/labeller_model/blender-4.2.1-linux-x64/blender",
        "-b",
        "-P",
        "persistent_blender_script.py",
        "--",
        "--object_path",
        target_path,
        "--output_dir",
        output_dir,
        "--engine",
        "CYCLES",
        "--scale",
        "0.8",
        "--num_images",
        "40",
        "--camera_dist",
        "1.2",
    ]

    env = os.environ.copy()
    env['OBJECT_BATCH'] = ','.join(object_files)

    log_dir = os.getcwd() + "/correct_logs/" + object_files[0][:-4]
    log_file_path = log_dir + "_log.log"
    error_file_path = log_dir + "_error.log"
    
    with open(log_file_path, 'a') as log_file, open(error_file_path, 'a') as error_file:
        # Run the command and suppress the output (stdout and stderr) to the log file
        subprocess.run(command, env=env, stdout=log_file, stderr=error_file)

    #subprocess.run(command, env=env)

def split_batches(object_files, num_batches):
    """Split the list of object files into smaller batches."""
    batch_size = len(object_files) // num_batches
    #batch_size = 2
    return [object_files[i:i + batch_size] for i in range(0, len(object_files), batch_size)]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render objects in parallel.")
    parser.add_argument('--start_idx', type=int, required=True, help='Starting index for object files.')
    parser.add_argument('--end_idx', type=int, required=True, help='Ending index for object files.')
    parser.add_argument('--num_processes', type=int, required=True, help='num of proceses.')

    args = parser.parse_args()

    # Specify the root directory
    cwd = os.getcwd()
    # Folder containing the objects
    target_path = cwd + "/objaverse_models"
    os.makedirs(target_path, exist_ok=True)

    # Folder containing the objects
    output_dir = cwd + "/views"
    os.makedirs(output_dir, exist_ok=True)

    log_dir = cwd + "/correct_logs"
    os.makedirs(log_dir, exist_ok=True)

    # Define the number of processes (adjust this based on your CPU/GPU resources)
    #num_processes = multiprocessing.cpu_count()
    num_processes = args.num_processes

    # List all files in the folder
    object_files = []
    with open('to_render.txt', 'r') as file:
        object_files = [line.strip() + ".glb" for line in file]

    # Extract range of files based on input parameters
    object_files = object_files[args.start_idx:args.end_idx]

    # Split the list of object files into smaller batches
    batches = split_batches(object_files, num_processes)

    # Use multiprocessing to render each batch in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.starmap(render_batch, [(batch, target_path, output_dir, i % num_processes) for i, batch in enumerate(batches)])

    # Command to run Blender with the specified options
