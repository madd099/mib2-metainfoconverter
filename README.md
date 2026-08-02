# Universal metainfo2.txt converter for MIB STD2 Technisat/Preh units

## Description
This program is created to help you to prepare the `metainfo2.txt` file from a target firmware (EU region) so it can be flashed onto a unit from any region or brand. It supports conversions such as ZR-to-ZR and PQ-to-PQ, as well as flashing ZR HMI firmware onto a PQ unit.
The program automatically selects the most suitable "Variant" from the `metainfo2.txt` file, replaces it with the one you specify, and creates the necessary links for your hardware. It also creates a backup.
The program includes built-in safeguards to prevent errors; for example, if you enter a Variant intended for a ZR unit but provide a `metainfo` file from PQ firmware, the program will display an error message.

## Usage
```
pip install PyQt5
python mibcongui.py
```
or download MIB2_Converter.zip with compiled .exe from "releases"

## Links

Screenshots and guides on [drive2.ru](https://www.drive2.ru/l/712304865233085471/)

____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# Универсальный конвертер metainfo2.txt для MIB STD2 Technisat/Preh

## Описание
Программа позволяет подготовить файл metainfo2.txt целевой прошивки (EU региона) для прошивки в юнит любого региона, бренда. Как для конвертаций ZR-ZR, PQ-PQ, так и для прошивки HMI ZR в PQ юнит.
Программа автоматически подберет наиболее подходящий Variant в файле metainfo2.txt и заменит его на введенный вами, а также создаст линки под ваше железо. Ну и бэкап сделает.
В программу встроена защита "от дурака", например, если вы введете Variant от ZR юнита и подсунете программе metainfo от PQ прошивки, вылезет соответствующая ошибка.

## Запуск
```
pip install PyQt5
python mibcongui.py
```
или MIB2_Converter.zip с готовым файлом .exe из вкладки "releases"

## Links

Инструкции и скрины на [drive2.ru](https://www.drive2.ru/l/712304865233085471/)
