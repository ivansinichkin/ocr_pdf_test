import fitz


def write_to_pdf(docpdf, text1, text2):
    """
    Функция записывает полученные фрагменты текста на новую страницу в pdf, который получает на вход
    :param docpdf: Объект doc файла .pdf, открытый с помощью fitz
    :param text1: текст для записи в левую рамку
    :param text2: текст для записи в правую рамку
    :return:
    """
    font_file = r"times.ttf"

    page = docpdf.new_page()  # new page, or choose doc[n]
    page.insert_font(fontname="times", fontfile=font_file)
    r1 = fitz.Rect(25, 25, 290, 815)  # left rectangle
    r2 = fitz.Rect(295, 25, 585, 815)  # right rectangle

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


def write_to_txt(text_list: list, pathfile):
    """
    функция выполняет запись текста в текстовый файл
    :param text_list: список в котором хранятся строки текста
    :param filename: путь к файлу для записи
    :return:
    """
    with open(file=pathfile, mode='a', encoding='utf-8') as f:
        for text in text_list:
            f.write(text)
        f.close()
    print(f'Текст записан в файл {pathfile}')
