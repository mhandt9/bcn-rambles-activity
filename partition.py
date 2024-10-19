import os
from PIL import Image

"""
Partitions ALL images in images/raw into a folder with 6 partitions (two rows, three columns)
"""

def partition_into_six(img):
    """Takes image and saves 6 partitions (two rows, three columns) in a folder with the same filename as the original."""
    width, height = img.size

    # Determine the dimensions for each partition
    partition_width = width // 3  # 3 columns
    partition_height = height // 2  # 2 rows

    filename = img.filename.split('raw\\')[1].replace('.png', '')

    # Make a folder for the partitions
    os.mkdir('images/partitioned/'+filename)

    # Loop through each row and column to create partitions
    pnum = 0

    for row in range(2):
        for col in range(3):
            left = col * partition_width
            upper = row * partition_height
            right = (col + 1) * partition_width
            lower = (row + 1) * partition_height

            pnum += 1

            # Crop the image
            partition = img.crop((left, upper, right, lower))

            # Save the 6 partitions to their folder with this format as name: 'images/partitions/date_time_temperatre_humiditiy_pnum.png
            partition.save('images/partitioned/'+filename+'/'+filename+'_p'+str(pnum)+'.png')

def combine_six_partitions(partition_folder, output_path):
    """Combines six partitions (two rows, three columns) back into a single image."""

    print(os.listdir(partition_folder))
    
    # List all partition files in the folder
    partition_files = sorted([f for f in os.listdir(partition_folder) if f.endswith('.jpg')])

    if len(partition_files) != 6:
        raise ValueError("There must be exactly 6 partition files in the folder.")
    
    # Open the first partition to get dimensions
    partition_1 = Image.open(os.path.join(partition_folder, partition_files[0]))
    partition_width, partition_height = partition_1.size

    # Create a new blank image with the combined dimensions (3 columns, 2 rows)
    combined_image = Image.new('RGB', (partition_width * 3, partition_height * 2))

    # Iterate over the partitions and paste them into the correct location
    pnum = 0
    for row in range(2):
        for col in range(3):
            # Open the corresponding partition
            partition = Image.open(os.path.join(partition_folder, partition_files[pnum]))
            
            # Calculate the position where this partition will be pasted
            left = col * partition_width
            upper = row * partition_height

            # Paste the partition into the combined image
            combined_image.paste(partition, (left, upper))
            
            pnum += 1

    # Save the combined image
    combined_image.save(output_path+'.png')
    print(f"Combined image saved to {output_path}'.png'")

if __name__ == "__main__":

    # Partitions every image in images/raw/
    for image_name in os.listdir('images/raw'):
        image = Image.open('images/raw/'+image_name)

        partition_into_six(img=image)