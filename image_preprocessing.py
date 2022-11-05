import numpy as np
import cv2


def rotate_image(img):
    """
    Функция получает на вход изображение страницы с текстом, подбирает оптимальный угол поворота
     и выполняет поворот изображения
    :param img: объект изображения
    :return img_rotation: повернутое изображение
    """
    # сперва переведём изображение из RGB в чёрно серый
    # значения пикселей будут от 0 до 255
    img_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

    # а теперь из серых тонов, сделаем изображение бинарным
    th_box = int(img_gray.shape[0] * 0.007) * 2 + 1
    img_bin_ = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, th_box, th_box)

    img_bin = img_bin_.copy()
    num_rows, num_cols = img_bin.shape[:2]

    best_zero, best_angle = None, 0
    # итеративно поворачиваем изображение на пятую часть градуса
    for my_angle in range(-15, 16, 1):
        rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), my_angle / 5, 1)
        img_rotation = cv2.warpAffine(img_bin, rotation_matrix, (num_cols, num_rows),
                                      borderMode=cv2.BORDER_CONSTANT,
                                      borderValue=255)

        img_01 = np.where(img_rotation > 127, 0, 1)
        sum_y = np.sum(img_01, axis=1)
        th_ = int(img_bin_.shape[0] * 0.005)
        sum_y = np.where(sum_y < th_, 0, sum_y)

        num_zeros = sum_y.shape[0] - np.count_nonzero(sum_y)

        if best_zero is None:
            best_zero = num_zeros
            best_angle = my_angle

        # лучший поворот запоминаем
        if num_zeros > best_zero:
            best_zero = num_zeros
            best_angle = my_angle

    print('Best angle: ' + str(best_angle / 5))
    if best_angle != 0:
        rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), best_angle / 5, 1)
        img_rotation = cv2.warpAffine(img_bin, rotation_matrix, (num_cols, num_rows),
                                      borderMode=cv2.BORDER_CONSTANT,
                                      borderValue=255)
    else:
        return img_bin

    return img_rotation


def cut_image(img, x_cut):
    """
    Функция разрезает изображение по вертикали, как отдельные колонки текста
    :param img: объект ихображения
    :param x_cut: x-координата, по которой будет выполнено разрезание
    :return img_left, img_right: две части изображения
    """
    img_shape = img.shape
    h, w = img_shape[0], img_shape[1]
    img_left = img[0: h, 0: x_cut + 10]
    img_right = img[0: h, x_cut - 10: w]
    return img_left, img_right


def detect_dividing_line(img_bin):
    """
    Функция для обнаружения разделительной линии между колонками текста
    :param img: объект изоражения
    :return x_coor_line: x-координата разделительной линии
    """
    # Search is performed in a specific part of the image
    img_shape = img_bin.shape
    h, w = img_shape[0], img_shape[1]
    img_cut = img_bin[0: h // 2, w // 2 - 50: w // 2 + 50]
    # Convert the img to grayscale
    # gray = cv2.cvtColor(img_cut, cv2.COLOR_BGR2GRAY)

    # Apply edge detection method on the image
    blurred_image = cv2.GaussianBlur(img_cut, (9, 9), 0)
    edges = cv2.Canny(blurred_image, 50, 150, apertureSize=3)

    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 50, np.pi / 1, 300)
    print('Количество найденных линий: ', str(len(lines)))

    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
        # x0 stores the value rcos(theta)
        x0 = a * r
        # y0 stores the value rsin(theta)
        y0 = b * r
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000 * (-b))
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000 * a)
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000 * (-b))
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000 * a)

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        # cv2.line(img_bin, (x1, y1), (x2, y2), (0, 0, 255), 10)

        x1_img = int(w // 2 - 50 + x1)
        x2_img = int(w // 2 - 50 + x2)
        if x1_img == x2_img:
            x_coor_line = x1_img

    return x_coor_line
