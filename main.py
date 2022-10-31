from extract_image_from_pdf import extract_png_page
from image_preprocessing import rotate_image, cut_image, detect_dividing_line
from recognition_pytes import text_recognition_pyt, write_to_txt
import cv2

# извлекаем изображения из pdf, изображения сохраняем в data/extrd_pages, также получаем их названия списком
pdf_path = 'data/sample.pdf'
xref_list = extract_png_page(pdf_path)

for img in xref_list:
    # открываем изображение, поворачиваем, находим x-координату для разделения изоюражения
    # получаем левую часть на казахском языке и правую на русском
    img = cv2.imread(f'data/extrd_images/{img}')
    img_rotated = rotate_image(img)
    div_x_coor = detect_dividing_line(img_rotated)
    img_left, img_right = cut_image(img_rotated, div_x_coor)
    # производим распознавание текста на каждой отдельной части изображения и записываем в два разных файла
    text_kaz = text_recognition_pyt(img_left, language='kaz')
    text_rus = text_recognition_pyt(img_right, language='rus')
    write_to_txt(text_kaz, 'data/result_kaz.txt')
    write_to_txt(text_rus, 'data/result_rus.txt')
