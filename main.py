import cv2

# Load an image
img = cv2.imread('AimTrainer.jpg')
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
