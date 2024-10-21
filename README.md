# Activity detection in les Rambles, popular street in Barcelona

This repo contains:
- Scraping of images from a webcam located a the Museu d'Arts Santa Mònica
- Partitioning of image to force model to focus on different parts
- Script to run Ultralytics YOLO models on the partitions and combining them back together


![Example Prediction](https://github.com/mhandt9/bcn-rambles-activity/blob/main/example_imgs/example_result.png)


## Usage

### Scraping
Scraping the newest image from the webcam:

```
python scrape_image.py
```

Scraping images every hour:

```
python scrape_image.py --schedule
```

### Running model

You can specify the YOLO model to be used, the minimum confidence level at which predictions are displayed and the run name.

To use it without any other changes, the folder images/partitioned cannot be empty, therefore scrape_image.py has to have been run at least once.

For example:

```
python model.py --model yolov8n.pt --conf 0.5 --run_name custom_run_name
```
This will save predictions of every partition in the folder images/partitioned under runs/run_name and the restored predictions of the full images in results/run_name.
