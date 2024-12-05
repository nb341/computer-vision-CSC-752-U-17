import cv2
import os
from xml.dom import minidom

def crop_images_in_folders(images_dir, annotations_dir, output_dir='cropped'):
    """
    Crop all images in a directory based on annotations without extensions and save to an output folder.
    
    Args:
        images_dir (str): Path to the root directory containing subfolders with images.
        annotations_dir (str): Path to the root directory containing subfolders with annotations.
        output_dir (str): Path to save the cropped images, maintaining subfolder structure.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each subfolder in the images directory
    for subfolder in os.listdir(images_dir):
        image_subfolder = os.path.join(images_dir, subfolder)
        annotation_subfolder = os.path.join(annotations_dir, subfolder)
        
        # Check if subfolder exists in both directories
        if not os.path.isdir(image_subfolder) or not os.path.isdir(annotation_subfolder):
            print(f"Skipping {subfolder}: Subfolder missing in images or annotations.")
            continue

        # Create the corresponding subfolder in the output directory
        output_subfolder = os.path.join(output_dir, subfolder)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        # Process each image in the subfolder
        for image_file in os.listdir(image_subfolder):
            image_path = os.path.join(image_subfolder, image_file)
            annotation_file = os.path.splitext(image_file)[0]  # Match the image name
            annotation_path = os.path.join(annotation_subfolder, annotation_file)

            try:
                # Load image
                image_data = cv2.imread(image_path)
                if image_data is None:
                    print(f"Image {image_path} could not be loaded. Skipping.")
                    continue

                # Load and parse annotation
                if not os.path.exists(annotation_path):
                    print(f"Annotation file {annotation_path} not found. Skipping.")
                    continue

                annon_xml = minidom.parse(annotation_path)
                xmin = int(annon_xml.getElementsByTagName('xmin')[0].firstChild.nodeValue)
                ymin = int(annon_xml.getElementsByTagName('ymin')[0].firstChild.nodeValue)
                xmax = int(annon_xml.getElementsByTagName('xmax')[0].firstChild.nodeValue)
                ymax = int(annon_xml.getElementsByTagName('ymax')[0].firstChild.nodeValue)

                # Validate bounding box
                height, width = image_data.shape[:2]
                if xmin < 0 or ymin < 0 or xmax > width or ymax > height:
                    print(f"Invalid bounding box for {image_path}: ({xmin}, {ymin}, {xmax}, {ymax}). Skipping.")
                    continue

                # Crop the image
                cropped_image = image_data[ymin:ymax, xmin:xmax]

                # Save the cropped image in the corresponding output subfolder
                output_path = os.path.join(output_subfolder, image_file)
                cv2.imwrite(output_path, cropped_image)
                print(f"Cropped image saved to: {output_path}")

            except Exception as e:
                print(f"Error processing file {image_path}: {e}")

# How to use
images_dir = 'images/Images'
annotations_dir = 'C:/Users/narin/OneDrive/Documents/New folder (2)/annotation\Annotation'
output_dir = 'cropped'
crop_images_in_folders(images_dir, annotations_dir, output_dir)
