from cv2 import imread, imwrite, Stitcher_create, STITCHER_OK, STITCHER_PANORAMA
from sys import argv
from glob import glob
'''
Usage: <match_ext_name> <input_dir> <output_file>
eg: python3 ./stitch_official.py jpg './i' './o.jpg'
'''
if __name__ == "__main__":
    if len(argv) == 4:
        imgd = argv[2]
        if imgd[-1] != '/': imgd += '/'
        imgs = glob(imgd + "*." + argv[1])
        print("Imgs to stitch:", imgs)
        sticher = Stitcher_create(STITCHER_PANORAMA)
        status, pano = sticher.stitch([imread(img) for img in imgs])
        if status != STITCHER_OK:
            print("Can't stitch images, error code = %d" % status)
        else:
            imwrite(argv[3], pano)
            print("stitching completed successfully.")
