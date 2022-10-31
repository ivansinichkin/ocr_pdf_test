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
    text = pytesseract.image_to_string(img, lang=language, config=myconfig,)
    return text


def write_to_pdf(text):
    doc = fitz.open()  # new or existing PDF
    page = doc.new_page()  # new page, or choose doc[n]
    r1 = fitz.Rect(25, 25, 290, 815)  # a 50x50 rectangle
    r2 = fitz.Rect(295, 25, 585, 815) # 2nd rect

    t1 = "text with rotate = 0."  # the texts we will put in
    t2 = "text with rotate = 90."

    black = (0, 0, 0)
    """We use a Shape object (something like a canvas) to output the text and
    the rectangles surrounding it for demonstration.
    """
    shape = page.new_shape()  # create Shape
    shape.draw_rect(r1)  # draw rectangles
    shape.draw_rect(r2)  # giving them

    shape.finish(width=0.3, color=black)
    # Now insert text in the rectangles. Font "Helvetica" will be used
    # by default. A return code rc < 0 indicates insufficient space (not checked here).
    # как быть с кодировкой...
    rc = shape.insert_textbox(r1, text.encode('utf-8').decode("Cyrillic"), color=black, fontsize=6,
                              fontname='HELV',
                              align=3)
    print(rc)
    # rc = shape.insert_textbox(r2, text, color=black)

    shape.commit()  # write all stuff to page /Contents
    doc.save("result.pdf")


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
