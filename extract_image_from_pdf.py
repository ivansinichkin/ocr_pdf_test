import fitz


def extract_png_page(pdf_path):
    """
    Функция сохраняет все изображения из pdf файла
    :param pdf_path: путь к pdf файлу
    :return xref_list: список названий сохраненных файлов
    """
    pdf = fitz.open(pdf_path)
    xref_list = []
    for i in range(pdf.page_count):
        image_page = pdf.get_page_images(i)
        for image in image_page:
            xref = image[0]
            xref_list.append(f'{xref}.png')
            pix = fitz.Pixmap(pdf, xref)
            if pix.n < 5:
                pix.save(f'data/extrd_images/{xref}.png')
            else:
                pix1 = fitz.open(fitz.csRGB, pix)
                pix1.writePNG(f'data/extrd_images/{xref}.png')
                pix1 = None
    return xref_list
