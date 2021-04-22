# USAGE
# python stitch_mimicry.py left.png right.png

from imgstitch.panorama import Stitcher
from imgstitch.brightness import merge_brightness
from imutils import resize
from cv2 import imread, imshow, waitKey, imwrite
from sys import argv

if __name__ == "__main__":
    imageL = argv[1]
    imageR = argv[2]
    imageO = argv[3]

    # load the two images and resize them to have a width of 400 pixels
    # (for faster processing)
    imageL = imread(imageL)
    imageR = imread(imageR)
    imageL = resize(imageL, width=400)
    imageR = resize(imageR, width=400)
    imageL, imageR = merge_brightness([imageL, imageR])
    imshow("tmp", imageL)
    imshow("tmp", imageR)
    waitKey(0)

    # stitch the images together to create a panorama
    stitcher = Stitcher()
    result, vis = stitcher.stitch([imageL, imageR], showMatches=True)

    # show the images
    imshow("Image L", imageL)
    imshow("Image R", imageR)
    imshow("Keypoint Matches", vis)
    imshow("Result", result)
    waitKey(0)
    imwrite(imageO, result)
