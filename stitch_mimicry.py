from imgstitch.panorama import Stitcher
from imgstitch.brightness import merge_brightness
from imutils import resize
from cv2 import imread, imshow, waitKey, imwrite
from sys import argv
'''
USAGE
python stitch_mimicry.py -r[resize_width] left.png right.png out.png
'''
if __name__ == "__main__":
    if len(argv) == 5:
        w = int(argv[1][2:])
        imageL = argv[2]
        imageR = argv[3]
        imageO = argv[4]
    else:
        w = 0
        imageL = argv[1]
        imageR = argv[2]
        imageO = argv[3]

    # 为加快处理速度，加载两图片后缩放宽度为w
    imageL = imread(imageL)
    imageR = imread(imageR)
    if w > 0:
        imageL = resize(imageL, width=w)
        imageR = resize(imageR, width=w)
    imageL, imageR = merge_brightness([imageL, imageR])
    imshow("tmpL", imageL)
    imshow("tmpR", imageR)
    waitKey(0)

    # 调用类方法拼接图片
    result, vis = Stitcher().stitch([imageL, imageR], showMatches=True)

    # 展示图片
    imshow("Image L", imageL)
    imshow("Image R", imageR)
    imshow("Keypoint Matches", vis)
    imshow("Result", result)
    waitKey(0)
    imwrite(imageO, result)
