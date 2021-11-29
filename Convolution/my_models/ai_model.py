import cv2
import os
from Convolutional_NN import settings
# import matplotlib.pyplot as plt
# from glob import glob
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, BatchNormalization
# from tensorflow.keras.layers import Flatten, Dense
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
# import tensorflow as tf


def crop_one_picture(filename, cols=100, rows=100):
    ##Read the color image, the transparency of the image (alpha channel) is ignored, the default parameter;
    ##grayscale image; read the original image, including the alpha channel; can be expressed as 1, 0, -1
    path = settings.MEDIA_ROOT
    path2 = os.path.join(path, 'media')
    full_path = os.path.join(path2, filename)
    img = cv2.imread(full_path, -1)
    # img = cv2.imread(r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\media\tower2_to_twer3.jpg', -1)
    #     img = cv2.imread(r'D:\Mystuff\New folder\PROJECT L400\project\code\version 2\crop\tower3_to_twer4.jpg',-1)

    sum_rows = img.shape[0]  # height
    sum_cols = img.shape[1]  # width
    picture_path = os.path.join(path, 'pictures')
    save_path = picture_path + "\\crop_images\\"  # Saved path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("Cropped {0} column pictures, {1} row pictures.".format(int(sum_cols / cols), int(sum_rows / rows)))

    for i in range(int(sum_cols / cols)):
        for j in range(int(sum_rows / rows)):
            cv2.imwrite(
                save_path + os.path.splitext(filename)[0] + '_' + str(j) + '_' + str(i) + os.path.splitext(filename)[1],
                img[j * rows:(j + 1) * rows, i * cols:(i + 1) * cols, :])
            # print(path+"\crop\\"+os.path.splitext(filename)[0]+'_'+str(j)+'_'+str(i)+os.path.splitext(filename)[1])
    print("Cropping completed, get {0} pictures.".format(int(sum_cols / cols) * int(sum_rows / rows)))
    print("File saved in {0}".format(save_path))


filename = 'tower2_to_twer3.jpg'  # Image name to be cropped
cols = 200  # Width of small pictures (number of columns)
rows = 200  # Small picture height (number of lines)
# crop_one_picture(filename)

# cnn = load_model(r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\Convolution\my_models\WebModel_vxx.h5')
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

cnn = load_model(BASE_DIR / 'my_models/WebModel_vxx.h5')

# print("model loaded")


def Model_Predictions():
    # directory = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\crop_images'
    directory = BASE_DIR / '../media/pictures/crop_images'
    result_array = []
    for filename in os.listdir(directory):
        pred = ["House", "Land"]
        input_path = os.path.join(directory, filename)
        test_image = image.load_img(input_path, target_size=(128, 128, 3))
        # land_image = image.load_img(input_path, target_size=(128, 128, 3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = cnn.predict(test_image)

        print(result)
        result_value = pred[result.argmax()]
        if result_value == 'House':
            print('This is a house with stuff')
            ## show contours code
            img = cv2.pyrDown(cv2.imread(input_path, cv2.IMREAD_UNCHANGED))

            # threshold image
            ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                                              150, 255, cv2.THRESH_BINARY)
            # find contours and get the external one

            contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            i=0
            for c in contours:
                # get the bounding rect
                x, y, w, h = cv2.boundingRect(c)
                # draw a green rectangle to visualize the bounding rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

                # get the min area rect
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                # convert all coordinates floating point values to int
                box = np.int0(box)
                i=i+1

            print(len(contours))
            result_array.append(len(contours))
            # cv2.drawContours(img, contours, -1, (255, 255, 0), 1)
            # directory_img = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\image_test'
            directory_img = BASE_DIR / '../media/pictures/image_test'
            os.chdir(directory_img)

            # cv2.imshow("contours", img)
            cv2.imwrite(filename, img)
            # cv2.imshow("contours", img)
        ## end of contour code
        elif result_value == 'Land':
            print('This is a Bare Land')
            # directory_img = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\image_test'
            directory_img = BASE_DIR / '../media/pictures/image_test'
            os.chdir(directory_img)
            img = cv2.pyrDown(cv2.imread(input_path, cv2.IMREAD_UNCHANGED))
            # cv2.imshow("contours", img)
            cv2.imwrite(filename, img)
    # print(len(result_array))
    return result_array


# result_arrays =Model_Predictions()
# print("The amount of contours around are", len(result_arrays))

def file_name(root_path, picturetype):
    filename_root = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1] == picturetype:
                filename_root.append(os.path.join(root, file))
    return filename_root


def merge_picture(mergename, num_of_cols=12, num_of_rows=7):
    # merge_path = r"C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\image_test"
    merge_path = BASE_DIR / '../media/pictures/image_test'

    # The folder containing the small pictures to be merged
    filename_merge = file_name(merge_path, ".jpg")
    shape = cv2.imread(filename_merge[0]).shape  # Three-channel images need to change -1 to 1
    cols = shape[1]
    rows = shape[0]
    channels = shape[2]
    dst = np.zeros((rows * num_of_rows, cols * num_of_cols, channels), np.uint8)
    for i in range(len(filename_merge)):
        img = cv2.imread(filename_merge[i], -1)
        cols_th = int(filename_merge[i].split("_")[-1].split('.')[0])
        rows_th = int(filename_merge[i].split("_")[-2])
        roi = img[0:rows, 0:cols, :]
        dst[rows_th * rows:(rows_th + 1) * rows, cols_th * cols:(cols_th + 1) * cols, :] = roi
    # merge destination

    #     cv2.imwrite(merge_path+"merge.jpg",dst)
    # directory_merge = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\merge'
    directory_merge = BASE_DIR / '../media/pictures/merge'
    os.chdir(directory_merge)
    savemerge_name = mergename + "merge.jpg"
    cv2.imwrite(savemerge_name, dst)
    print('File merged and saved in {}'.format(directory_merge))

    return savemerge_name


# merge_path = r"D:\Mystuff\New folder\PROJECT L400\project\code\version 2\pictures\image_test"  # The folder containing the small pictures to be merged
# num_of_cols = 12  # Number of columns
# num_of_rows = 7  # Rows
# name='towr'
# merge_picture(name)
tower = "Tower3.jpg"
print(os.path.splitext(tower)[0])


def delete_files():
    # dir = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\crop_images'
    dir = BASE_DIR / '../media/pictures/crop_images'
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))

    # dir2 = r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\media\pictures\image_test'
    dir2 = BASE_DIR / '../media/pictures/image_test'

    for file in os.listdir(dir2):
        os.remove(os.path.join(dir2, file))

    print("Files Deleted")
