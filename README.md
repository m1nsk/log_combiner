# log_combiner
## log_generate.py 
* Генерирует файл generated_log.txt, содержащий все сгенерированные строки логов.Количество строк можно указать через интерфейс консоли.
* Сгенерированные строки логов распределяются по N файлам логов в случайном порядке. Количество файлов можно указать через интерфейс консоли. Имена сгенерированных файлом : log{N}.txt где n порядковый номер файла

    
## log_join.py
  * Скрипт, который объединяет записи нескольких лог файлов. Через интерфейс консоли можно указать файлы логов, которые необходимо объединить. Объединенный список строк логов будет выведен в файл test_log.txt
    
## log_compare_test.py
  * Скрипт сравнивающий идентичность двух тестовых файлов логов.
