from ultralytics import YOLO
import shutil
import os
from partition import combine_six_partitions

def run_model(model, run_name:str, conf):
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


model = YOLO('yolov5nu.pt')
conf = 0.2
run_name = 'test5_yolov5'

run_model(model=model, run_name=run_name, conf=conf)
