<h2>OCR PDF</h2>
Данный скрипт создан для распознавания текста из PDF документа, в котором содержится отсканированный текст на двух языках в двух колонках.
В качестве основных инструментов выбраны две библиотеки: PyMuPDF для работы с PDF файлом и PyTesseract для распознавания текста.
PyMuPDF предоставляет широкий набор инструментов для чтения и записи PDF файлов, а также имеет встроенный метод для распознавания текста на основе PyTesseract.
PyTesseract имеет различные настройки для более точного распознавания текста, а также множество предобученных моделей для различных языков. В данном случае было важно, чтобы библиотека имела возможность работы с казахским языком.

___

<h4>Проблемы</h4>

___

* На странице две колонки текста. Если производить распознавание всей страницы, на выходе получим перемешанные строки на двух языка.
* Отсканированные изображения повернуты не строго верткально. В общем случае для распознавания это небольшая проблема, так как углы поворота небольшие. Однако, в данном случае это мешает точному разделению страницы на две части поскольку текст расположен вплотную к линии разделяющей колонки.
* Изображения имеют разные размеры, что не дает их легко разделить по колонкам.

___

<h4>Алгоритм действий</h4>

___

1. Извлекаем с каждой страницы PDF изображение отксканированной страницы и сохраняем.<br>
Функция __extract_png_page__
2. Производим предобработку изображений:
   * Находим оптимальный угол поворота, чтобы строки располагались горизонтально, а разделительная линия между колонками вертикально, и поворачиваем изображение.<br>
   Функция __rotate_image__
   * Находим координаты вертикальной разделительной линии с помощью алгоритма Хафа для нахождения линий. Используется алгоритм из библиотеки OpenCV.<br>
   Функция __detect_dividing_line__
   * Разрезаем изображение по вертикали на два отдельных.<br>
   Функция __cut_image__
3. С помощью PeTesseract производим распознавание текста на изображениях. Используем конфигурацию "Automatic page segmentation with OSD".<br>
Функция __text_recognition_pyt__
4. Записываем полученный текст в PDF файл по колонкам, как в исходном документе, либо в два TXT файла отдельно по языкам, либо используем два варианта одновременно.<br>
Функции __write_to_pdf__, __write_to_txt__

___

<h4>Модули и Функции</h4>

____

* Модуль __extract_image_from_pdf(pdf_path)__
    * __extract_png_page__<br>
    Функция выполняет проход по всем страницам PDF документа и извлекает все изображения с каждой страницы. Изображения сохраняются в папку data/extrd_images/ с названием {xref}.png, также названия всех изображений возвращаются функцией в виде списка.<br>
    __Параметры__
        * pdf_path(str) - путь к PDF файлу<br>
        
        __Возваращаемое значение__<br>
    Список c названиями всех извлеченных изображений.
    
* Модуль __image_preprocessing__
    * __rotate_image(img)__<br>
    Функция получает на вход изображение страницы с текстом, подбирает оптимальный угол поворота и выполняет поворот изображения. Изображение поворачивается на углы от -3° до 3° с шагом 0.2°. Предварительно изображение переводится в градации серого и затем бинаризуется.<br>
    __Параметры__
        * img(np.array) - массив, получаемый при чтении изображения с помощью OpenCV<br>
    
        __Возвращаемое значение__<br>
    Numpy массив, содержащий бинаризованное изображение.
    
    * __detect_dividing_line(img)__<br>
    Функция с помощью алгоритма Хафа выполняет поиск разделительной линии между колнками текста. На вход алгоритма Хафа передается только небольшая область изображения размером 100 пикселей по горизонтали с центром в середине изображения и половина высоты изображения по вертикали. Предварительно данная область изображения размывается, а затем производиться детектирование краев методом Канни. <br>
    __Параметры__
        * img(np.array) - Numpy массив, содержащий бинаризованное изображение<br>
        
        __Возвращаемое значение__<br>
    Целое число со значением x координаты разделительной линии.
    * __cut_image(img, x_cut)__<br>
    Функция разделяет изображение на две части по вертикали.<br>
    __Параметры__
        * img(np.array) - Numpy массив, содержащий бинаризованное изображение
        * x_cut(int) - x координата, по которой производится разделение изображения<br>
    
        __Возвращаемое значение__<br>
    Кортеж с двумя бинаризованными изображениями, под индексом 0 левая часть, под индексом 1 правая.
    
* Модуль __recognition_pytes__
    * __text_recognition_pyt(img, language)__<br>
    Функция с помощью бибилиотеки PyTesseract выполняет распознавание текста на изображении. Используемая конфигурация: Page segmentation mode - 1    Automatic page segmentation with OSD; OCR Engine mode - 3    Default, based on what is available.
    __Параметры__
        * img(np.array) - Numpy массив, содержащий изображение<br>
        * language(str) - язык распознаваемого текста, например 'kaz', 'rus', 'kaz+rus'<br>
            
        __Возвращаемое значение__<br>
        Строка содержащая, распознанный текст.
        
* Модуль __write_result__
    * __write_to_pdf(docpdf, text1, text2)__<br>
    Функция записывает полученные фрагменты текста на новую страницу в PDF, который получает на вход. В документе PDF создается новая страница, на ней рисуются две колонки (рамки) для текста, в которые текст записывается. После окончания работы функции необходимо выполнить сохранение документа.<br>
    __Параметры__
        * docpdf(object Document) - объект документа, открытый или созданный с помощью PyMuPDF
        * text1(str) - строка текста, которая записывается в левую колонку
        * text2(str) - строка текста, которая записывается в правую колонку<br>
        
        __Возвращаемое значение__<br>
        None
        
    * __write_to_txt(text_list: list, pathfile)__<br>
    Функция записывает полученный список строк в TXT файл.<br>
    __Параметры__
        * text_list(list) - список строк
        * pathfile(str) - путь к TXT файлу<br>
        
        __Возвращаемое значение__<br>
        None
