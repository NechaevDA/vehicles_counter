import cv2
import numpy as np
from vehicle_counter.display import draw_information
from vehicle_counter.contour_detect import ContourDetect
from vehicle_counter.counter import Counter

border_line_y = 300
border_line_x = 450
offset_y = 70
great_britain = False # Вечно у британцев все наперекосяк
step = 0 # 0 - borders, 1 - offset


def click_event(event, x, y, flags, params):
    global border_line_y
    global border_line_x
    global offset_y
    global great_britain
    global step
    disp_f = frame.copy()
    if step == 0:
        cv2.putText(disp_f, 'Set zones', (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.line(disp_f, (0, y), (width, y), (255, 0, 0), 1)
        cv2.line(disp_f, (x, 0), (x, height), (255, 0, 0), 1)
    elif step == 1:
        cv2.putText(disp_f, 'Set contour detection offset', (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.line(disp_f, (0, border_line_y), (width, border_line_y), (255, 0, 0), 1)
        cv2.line(disp_f, (border_line_x, 0), (border_line_x, height), (255, 0, 0), 1)
        tmp_offset = abs(border_line_y - y)
        cv2.line(disp_f, (0, border_line_y - tmp_offset), (width, border_line_y - tmp_offset), (255, 0, 255), 1)
        cv2.line(disp_f, (0, border_line_y + tmp_offset), (width, border_line_y + tmp_offset), (255, 0, 255), 1)
    elif step == 2:
        cv2.line(disp_f, (0, border_line_y), (width, border_line_y), (255, 0, 0), 1)
        cv2.line(disp_f, (border_line_x, 0), (border_line_x, height), (255, 0, 0), 1)
        cv2.line(disp_f, (0, border_line_y - offset_y), (width, border_line_y - offset_y), (255, 0, 255), 1)
        cv2.line(disp_f, (0, border_line_y + offset_y), (width, border_line_y + offset_y), (255, 0, 255), 1)
        cv2.putText(disp_f, 'Click on the BACKWARD Side (cars moving TOWARD camera)', (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    else:
        cv2.putText(disp_f, 'Setup completed, press any key...', (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if step == 0:
            border_line_x = x
            border_line_y = y
        if step == 1:
            offset_y = abs(border_line_y - y)
        if step == 2:
            great_britain = x < border_line_x
        step += 1

    cv2.imshow('Setup', disp_f)


def train_bg_subtractor(inst, cap, num=500):
    '''
        BG substractor need process some amount of frames to start giving result
    '''
    print ('Training BG Subtractor...')
    i = 0
    while i < num:
        ret, frame = cap.read()
        inst.apply(frame, None, 0.001)
        i += 1
    cap.release()


if __name__ == '__main__':
    # настройки прогона, можно забирать из аргументов
    file_name = 'videos/traffic1.avi'
    verbose = True  # отображать ли информацию о работе
    contour_area_limit = 400

    # информация о видеоролике
    cap = cv2.VideoCapture(file_name)
    fps = cap.get(cv2.cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_info = 'FPS: {0} Dimenstions(HxW): {1}x{2}'.format(fps, height, width)
    print(vid_info)

    # настройка зон
    ret, frame = cap.read()
    cv2.imshow('Setup', frame)
    cv2.setMouseCallback('Setup', click_event)
    cv2.waitKey(0)

    frame_counter = 0

    # создаем вычитатель фона
    background_substractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True, history=500)
    train_bg_subtractor(background_substractor, cap, num=500)
    cv2.destroyAllWindows()
    # логика детектирования контуров
    contour_detect = ContourDetect(background_substractor,
                                   border_line_y - offset_y,
                                   border_line_y + offset_y,
                                   contour_area_limit)

    # счетчик
    counter = Counter(count_line_y=border_line_y,
                      count_line_x=border_line_x,
                      max_dist=40,
                      max_path=10,
                      great_britain=great_britain)

    # найденные пути
    paths = {}
    dilated_image = None

    # ресетим видеоролик после тренировки вычитателя
    cap = cv2.VideoCapture(file_name)

    while cap.isOpened():
        frame_counter += 1
        ret, current_image = cap.read()

        display_image = current_image.copy()

        if frame_counter % 2 == 0:
            contours, dilated_image = contour_detect.detect_contours(current_image)

            paths = counter.analyze_contours(contours)

        draw_information(display_image,
                         verbose,
                         paths,
                         counter.forward_count,
                         counter.backward_count,
                         border_line_y,
                         border_line_x,
                         offset_y,
                         width,
                         height)

        if verbose:
            if dilated_image is not None:
                dilated_cvt = cv2.cvtColor(dilated_image, cv2.COLOR_GRAY2BGR)
                numpy_horizontal = np.hstack((display_image, dilated_cvt))
                cv2.imshow('Video', numpy_horizontal)
        else:
            cv2.imshow('Video', display_image)
        if cv2.waitKey(int(fps)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
