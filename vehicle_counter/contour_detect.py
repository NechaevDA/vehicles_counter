import cv2


class ContourDetect:
    bg_substractor = None
    contour_area_limit = 400
    border_line_y_top = 100
    border_line_y_bottom = 100

    def __init__(self, bg_substractor, border_line_y_top=100, border_line_y_bottom=100, contour_area_limit=400):
        self.border_line_y_bottom = border_line_y_bottom
        self.bg_substractor = bg_substractor
        self.contour_area_limit = contour_area_limit
        self.border_line_y_top = border_line_y_top

    def detect_contours(self, frame):
        fgmask = self.bg_substractor.apply(frame)

        # ядро функций эрозии, расширения, открытия и закрытия
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

        # Закрытие контуров
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        # Удаление шумов
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        # Расширение контуров для соединения соседей
        dilation = cv2.dilate(opening, kernel, iterations=2)

        verbose_image = dilation.copy()

        # Пороговое отсечение
        th = dilation[dilation < 240] = 0

        contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        valid_cntrs = []

        # Ограничение области распознавания
        for i, cntr in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cntr)
            if ((2 * y + h)/2 >= self.border_line_y_top and (2 * y + h)/2 <= self.border_line_y_bottom) & (cv2.contourArea(cntr) >= self.contour_area_limit):
                valid_cntrs.append(cntr)
                # valid_cntrs.append(cv2.boundingRect(cntr))

        return valid_cntrs, verbose_image
