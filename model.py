from ultralytics import YOLO
import shutil
import os
from partition import combine_six_partitions
import argparse

def run_model(model, run_name: str, conf):
    """Runs provided YOLO model, saves predicted partitions under folder in runs/run_name and provides resulting final image in results/run_name"""

    partitions_folders = ['images/partitioned/'+x for x in os.listdir('images/partitioned')]

    os.mkdir('runs/'+run_name)

    for folder in partitions_folders:
        results = model(source=folder, show=False, conf=conf, save=True, project='runs', name=folder.split('partitioned/')[1])
        shutil.move(src='runs/'+folder.split('partitioned/')[1], dst='runs/'+run_name)
        print('Results moved to runs/'+run_name+'/'+folder.split('partitioned/')[1])

    os.mkdir('results/'+run_name)

    for partitioned_results in os.listdir('runs/'+run_name):
        combine_six_partitions(partition_folder='runs/'+run_name+'/'+partitioned_results, output_path='results/'+run_name+'/'+partitioned_results)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run YOLO model on partitioned images")
    
    # Add command-line arguments
    parser.add_argument('--model', type=str, default='yolov5nu.pt', help='Path to YOLO model weights')
    parser.add_argument('--conf', type=float, default=0.2, help='Confidence threshold for YOLO model')
    parser.add_argument('--run_name', type=str, default='test_run', help='Name of the run (used for saving results)')

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the YOLO model with the provided model path
    model = YOLO(args.model)

    # Run the model with the provided parameters
    run_model(model=model, run_name=args.run_name, conf=args.conf)

