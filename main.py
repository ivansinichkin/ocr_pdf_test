from extract_image_from_pdf import extract_png_page
from image_preprocessing import rotate_image, cut_image, detect_dividing_line
from recognition_pytes import text_recognition_pyt
from write_result import write_to_txt, write_to_pdf
import fitz
import cv2


def main():
    # извлекаем изображения из pdf, изображения сохраняем в data/extrd_pages, также получаем их названия списком
    pdf_path = 'data/sample.pdf'
    out_pdf_path = 'data/result.pdf'
    xref_list = extract_png_page(pdf_path)

    # создадим два списка, в которые постранично сложим текст на каждом языке для дальнейшей записи в пдф
    text_list_kaz = []
    text_list_rus = []

    for img in xref_list:
        # открываем изображение, поворачиваем, находим x-координату для разделения изоюражения
        # получаем левую часть на казахском языке и правую на русском
        img = cv2.imread(f'data/extrd_images/{img}')
        img_rotated = rotate_image(img)
        div_x_coor = detect_dividing_line(img_rotated)
        img_left, img_right = cut_image(img_rotated, div_x_coor)
        # производим распознавание текста на каждой отдельной части изображения и записываем в два разных файла
        text_kaz = text_recognition_pyt(img_left, language='kaz')
        text_list_kaz.append(text_kaz)
        text_rus = text_recognition_pyt(img_right, language='rus')
        text_list_rus.append(text_rus)

    # запись полученного текста в PDF или TXT
    writing_flag = 9
    while writing_flag not in [0, 1, 2]:
        try:
            writing_flag = int(input('Куда записать результаты распознавания текста?\n'
                                     'Введите число:\n'
                                     '0 - запись в PDF файл\n'
                                     '1 - запись в TXT файл\n'
                                     '2 - запись и в PDF, и в TXT\n'))
        except ValueError as ve:
            print(ve)
            print('Введите число от 0 до 2')
            writing_flag = 9

    if writing_flag == 0:
        doc = fitz.open()
        for text_k, text_r in zip(text_list_kaz, text_list_rus):
            write_to_pdf(doc, text_k, text_r)
        doc.save(out_pdf_path)
        print(f'Текст записан в файл {out_pdf_path}')
    elif writing_flag == 1:
        write_to_txt(text_list_kaz, 'data/result_kaz.txt')
        write_to_txt(text_list_rus, 'data/result_rus.txt')
    elif writing_flag == 2:
        doc = fitz.open()
        for text_k, text_r in zip(text_list_kaz, text_list_rus):
            write_to_pdf(doc, text_k, text_r)
        doc.save(out_pdf_path)
        print(f'Текст записан в файл {out_pdf_path}')
        write_to_txt(text_list_kaz, 'data/result_kaz.txt')
        write_to_txt(text_list_rus, 'data/result_rus.txt')


if __name__ == '__main__':
    main()
