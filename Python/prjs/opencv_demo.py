# coding : cp1251
import cv2

image = cv2.imread("d:\dump\clouds.jpg")

gray_image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
cv2.imshow("Over the clouds", image )
cv2.imshow("Over the clouds - gray", gray_image )
cv2.waitKey(0)
cv2.destroyAllWindows()

