# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 22:36:05 2024

@author: pjwbu
"""

import os
import cv2
import matplotlib.pyplot as plt
"""
img_array = cv2.imread('C:/project/redfox.jpg')
rgb_img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
cv2.imwrite('C:/project/momo2.jpg',rgb_img_array)
"""

cv2_image = cv2.imread('redfox.jpg')

plt.figure(figsize = (10,10))
plt.imshow(cv2_image)
plt.show()