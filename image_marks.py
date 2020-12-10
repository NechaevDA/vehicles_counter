# importing the module
import cv2

# здесь поменять на папку, где фотки лежат
BASE_DIR = 'D:\\Study\\CV\\Lab\\'
SCALE_FACTOR = 5
points = []
ctr = 0
# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    global ctr
    global points
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(scale(x), ' ', scale(y))

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        ctr += 1
        points.append((scale(x), scale(y)))
        # file
        cv2.putText(img, str(ctr), (scale(x + 12), scale(y + 5)), font,
                    5, (255, 0, 0), 5)
        cv2.circle(img, (scale(x), scale(y)), 40, (255, 0, 0), 5)
        # window
        cv2.putText(imS, str(ctr), (x + 15, y + 5), font,
                    1, (255, 0, 0), 2)
        cv2.circle(imS, (x, y), 10, (255, 0, 0), 2)
        cv2.imshow('image', imS)

        # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)


def scale(num):
    return num * SCALE_FACTOR


def save_points(name):
    global points, BASE_DIR
    f = open('{0}{1}.txt'.format(BASE_DIR, name), 'w+')
    f.write('{0}\n'.format(len(points)))
    for point in points:
        f.write('{0} {1}\n'.format(point[0], point[1]))
    f.close()


# driver function
if __name__ == "__main__":

    # тут вводить название результирующих файлов тхт и жпг
    name = input('Result Name: ')
    # тут поменять название фотки
    image_name = 'cam2.jpg'

    # reading the image
    img = cv2.imread('{0}{1}'.format(BASE_DIR, image_name), 1)

    # scale
    (h, w) = img.shape[:2]
    imS = cv2.resize(img, (int(w / SCALE_FACTOR), int(h / SCALE_FACTOR)))

    # displaying the image
    cv2.imshow('image', imS)

    # setting mouse hadler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # Filename
    filename = '{0}{1}.jpg'.format(BASE_DIR, name)

    # Using cv2.imwrite() method
    # Saving the image
    cv2.imwrite(filename, img)
    save_points(name)

    # close the window
    cv2.destroyAllWindows()