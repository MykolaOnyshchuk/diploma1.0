import numpy as np
import cv2


class Line:
    def __init__(self, coords):
        self.__pts = np.array(coords, np.int32).reshape((- 1, 1, 2))
        self.__rect = cv2.boundingRect(self.__pts)
        self.__mask = None
        self.__count_mask_pixels = 0
        self.__color = (255, 255, 255)
        self.__final_size = (256, 256)
        self.__final_orig_size = (256, 256, 3)

    def __get_mask(self, shape):
        if self.__mask is not None:
            return self.__mask
        self.__mask = np.full((shape[0], shape[1]), 0, dtype=np.uint8)
        cv2.fillPoly(self.__mask, [self.__pts], self.__color)
        x, y, w, h = self.__rect
        self.__mask = self.__mask[y:y + h, x:x + w]
        self.__count_mask_pixels = cv2.countNonZero(self.__mask)
        return self.__mask

    def get_dataset_images(self, orig_image, res_image):
        return self.get_image(orig_image), self.get_image(res_image, False)
        # mask = self.__get_mask(orig_image.shape)
        # x, y, w, h = self.__rect
        #
        # orig_crop = orig_image[y:y + h, x:x + w]
        # final_orig_image = np.full(self.__final_orig_size, 0, dtype=np.uint8)
        # final_orig_image[0:h, 0:w] = cv2.bitwise_or(orig_crop, orig_crop, mask=mask)
        #
        # crop = res_image[y:y + h, x:x + w]
        # final_image = np.full(self.__final_size, 0, dtype=np.uint8)
        # final_image[0:h, 0:w] = cv2.bitwise_or(crop, crop, mask=mask)
        # return final_orig_image, final_image

    def get_image(self, image, orig=True):
        mask = self.__get_mask(image.shape)
        x, y, w, h = self.__rect
        orig_crop = image[y:y + h, x:x + w]
        final_image = np.full(self.__final_orig_size if orig is True else self.__final_size, 0, dtype=np.uint8)
        final_image[0:h, 0:w] = cv2.bitwise_or(orig_crop, orig_crop, mask=mask)
        return final_image

    def get_tlcr(self, image):
        return cv2.sumElems(image)[0] / self.__count_mask_pixels
