import cv2
from random import randint


def draw_information(image, verbose, paths, count_f, count_b, line_y, line_x, offset_y, im_width, im_height):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if verbose:
        for k, v in paths.items():
            cv2.putText(image,
                        str(k),
                        v[0],
                        font,
                        .7,
                        (255, 255, 0),
                        2)
            for p in v:
                color = (randint(127, 255), randint(127, 255), randint(127, 255))
                cv2.circle(image, p, 5, color)

    cv2.line(image, (0, line_y), (im_width, line_y), (255, 0, 0), 1)
    cv2.line(image, (line_x, 0), (line_x, im_height), (255, 0, 0), 1)
    if verbose:
        cv2.line(image, (0, line_y - offset_y), (im_width, line_y - offset_y), (255, 0, 255), 1)
        cv2.line(image, (0, line_y + offset_y), (im_width, line_y + offset_y), (255, 0, 255), 1)
    cv2.putText(image,
                'Forward {0}; Backward {1}'.format(count_f, count_b),
                (50, 50),
                font,
                1,
                (255, 255, 0),
                2)
