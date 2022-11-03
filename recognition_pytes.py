import pytesseract
import fitz

'''Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.
       
       OCR Engine modes:
  0    Legacy engine only.
  1    Neural nets LSTM engine only.
  2    Legacy + LSTM engines.
  3    Default, based on what is available.'''


def text_recognition_pyt(img, language):
    """
    функция выполянет распознавние текста на изображении
    :param img: объект изображения
    :param language: строка вида 'rus' или 'rus+kaz' в случае нескольих языков
    :return text: распознанный текст в виде строки
    """
    myconfig = r'--psm 1 --oem 3'
    print('Распознавание текста на изображении...')
    text = pytesseract.image_to_string(img, lang=language, config=myconfig,)
    return text


def write_to_pdf(docpdf, text1, text2):
    """
    :param docpdf: Объект doc файла .pdf, открытый с помощью fitz
    :param text1: текст для записи в левую рамку
    :param text2: текст для записи в правую рамку
    :return:
    """
    font_file = r"times.ttf"

    page = docpdf.new_page()  # new page, or choose doc[n]
    page.insert_font(fontname="times", fontfile=font_file)
    r1 = fitz.Rect(25, 25, 290, 815)  # a 50x50 rectangle
    r2 = fitz.Rect(295, 25, 585, 815)  # 2nd rect

    black = (0, 0, 0)

    shape = page.new_shape()  # create Shape
    shape.draw_rect(r1)  # draw rectangles
    shape.draw_rect(r2)  # giving them

    shape.finish(width=0.3, color=black)
    # Now insert text in the rectangles.
    # A return code rc < 0 indicates insufficient space (not checked here).
    font_size = 8
    rc1 = shape.insert_textbox(r1, text1, encoding=2, color=black, fontsize=font_size, fontname='times', align=3)
    print(rc1)
    rc2 = shape.insert_textbox(r2, text2, encoding=2, color=black, fontsize=font_size, fontname='times', align=3)
    print(rc2)

    shape.commit()  # write all stuff to page /Contents
    print('Текст записан в pdf')


def write_to_txt(text, filename):
    """
    функция выполняет запись текста в текстовый файл
    :param text: текст в виде строки
    :param filename: путь к файлу для записи
    :return:
    """
    with open(file=filename, mode='a', encoding='utf-8') as f:
        f.write(text)
        f.close()
