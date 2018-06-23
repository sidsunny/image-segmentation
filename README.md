# Image Segmentation
Methods for segmenting images
1. thresholding - 4 methods (THRESH_BINARY", "THRESH_BINARY_INV", "THRESH_TRUNC", "THRESH_TOZERO", "THRESH_TOZERO_INV")
2. watershed  
  
  
  
## Image Filtering
Perform various linear or non-linear filtering operations on 2D images (represented as Mat()‘s). It means that for each pixel location (x,y) in the source image (normally, rectangular), its neighborhood is considered and used to compute the response. In case of a linear filter, it is a weighted sum of pixel values. In case of morphological operations, it is the minimum or maximum values, and so on. The computed response is stored in the destination image at the same location (x,y) . It means that the output image will be of the same size as the input image. Normally, the functions support multi-channel arrays, in which case every channel is processed independently. Therefore, the output image will also have the same number of channels as the input one.
Pyramid mean shift filtering - helps the accuracy of our thresholding step
  
  
  
## watershed.py
1. Segmentation using thresholding and drawing contours.
2. Segmentation using watershed algorithm

Run file as >> python main.py --image /path to your image


References:  
https://www.pyimagesearch.com  
https://docs.opencv.org/3.4/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576a147222a96556ebc1d948b372bcd7ac59  
https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#pyrmeanshiftfiltering  
https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html
