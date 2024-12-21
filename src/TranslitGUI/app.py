import toga
import toga_android
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from typing import Dict, Union
from toga.platform import get_platform_factory
import platform
import json
import os
from pathlib import Path

# Define transliteration tables
translit_table_rus_to_lat: Dict[str, Union[str, tuple]] = {
    ',': ',', 'а': 'a', 'б': 'p', 'в': 'v', 'г': 'k', 'д': 't',
    'ӑ': 'o', 'ă': 'o', 'е': ('e', 'ye'), 'ж': 'ş', 'з': 's',
    'ĕ': 'ö', 'ӗ': 'ö', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
    'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
    'ç': 'c', 'ҫ': 'c', 'т': 't', 'у': 'u', 'ӳ': 'ü', 'ÿ': 'ü',
    'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ç', 'щ': 'şç', 'ш': 'ş', 'ы': 'ı',
    'э': 'e', 'ю': 'yu', 'я': 'ya', 'ь': '′', 'ъ': '', '?': '?',
    'А': 'A', 'Б': 'P', 'В': 'V', 'Г': 'K', 'Д': 'T', 'Ă': 'O',
    'Ӑ': 'O', 'Е': 'E', 'Ĕ': 'Ö', 'Ӗ': 'Ö', 'Ж': 'Ş', 'З': 'S',
    'И': 'İ', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Ç': 'C', 'Ҫ': 'C',
    'Т': 'T', 'У': 'U', 'Ӳ': 'Ü', 'Ÿ': 'Ü', 'Ф': 'F', 'Х': 'X',
    'Ц': 'Ts', 'Ч': 'Ç', 'Щ': 'Şç', 'Ш': 'Ş', 'Ы': 'I', 'Э': 'E', 'Ю': 'Yu',
    'Я': 'Ya', 'Ь': '′', 'Ъ': '', '?': '?'
}

translit_table_rus_to_ar: Dict[str, str] = {
    ';': '؛', ',': '،', 'а': 'ا', 'б': 'پ', 'в': 'ۋ', 'ӑ': 'أ', 'ă': 'أ',
    'е': 'ە', 'з': 'س', 'ĕ': 'ۀ', 'ӗ': 'ۀ', 'и': 'ې', 'й': 'ي',
    'к': 'ك', 'л': 'ل', 'м': 'م', 'н': 'ن', 'о': 'و', 'п': 'پ',
    'р': 'ر', 'с': 'س', 'ç': 'ج', 'ҫ': 'ج', 'т': 'ت', 'у': 'و',
    'ӳ': 'ۆ', 'ф': 'ف', 'х': 'خ', 'ц': 'تس', 'ч': 'چ', 'ш': 'ش',
    'ы': 'ى', 'э': 'ە', 'ю': 'يو', 'я': 'يا', 'ь': 'ٰ', 'ъ': '', '?': '؟',
    'А': 'ا', 'Б': 'پ', 'В': 'ۋ', 'Ă': 'أ', 'Ӑ': 'أ', 'Е': 'ە',
    'Ĕ': 'ۀ', 'Ӗ': 'ۀ', 'З': 'س', 'И': 'ې', 'Й': 'ي', 'К': 'ك',
    'Л': 'ل', 'М': 'م', 'Н': 'ن', 'О': 'و', 'П': 'پ', 'Р': 'ر',
    'С': 'س', 'Ç': 'ج', 'Ҫ': 'ج', 'Т': 'ت', 'У': 'و', 'Ӳ': 'ۆ',
    'Ф': 'ف', 'Х': 'خ', 'Ц': 'تس', 'Ч': 'چ', 'Ш': 'ش', 'Ы': 'ى',
    'Э': 'ە', 'Ю': 'يو', 'Я': 'يا', 'Ь': 'ٰ', 'Ъ': '', '?': '؟'
}

translit_table_ar_to_lat = {
    'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 'th', 'ج': 'j', 'چ': 'ch',
    'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's',
    'ش': 'sh', 'ص': 's', 'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh',
    'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h',
    'و': 'w', 'ي': 'y', 'ى': 'a', 'ء': "'", 'ئ': 'y', 'ؤ': 'w', 'ة': 'h',
    'آ': 'a', 'أ': 'a', 'إ': 'i', 'ؤ': 'u', 'ئ': 'i', 'ى': 'a', 'ة': 'h'
}

# Reverse transliteration tables
translit_table_lat_to_rus: Dict[str, str] = {v: k for k, v in translit_table_rus_to_lat.items()}
translit_table_ar_to_rus: Dict[str, str] = {v: k for k, v in translit_table_rus_to_ar.items()}
translit_table_lat_to_ar = {v: k for k, v in translit_table_ar_to_lat.items()}

def transliterate(text: str, table: Dict[str, Union[str, tuple]]) -> str:
    result = []
    for char in text:
        if char in table:
            translit_value = table[char]
            if isinstance(translit_value, tuple):
                result.append(translit_value[0])  # Use the first variant
            else:
                result.append(translit_value)
        else:
            result.append(char)
    return ''.join(result)

def reverse_transliterate(text: str, table: Dict[str, str]) -> str:
    result = []
    for char in text:
        result.append(table.get(char, char))
    return ''.join(result)

class TransliterationApp(toga.App):
    def startup(self):
        # Create modern-styled main window
        self.main_window = toga.MainWindow(
            title=self.name,
            size=(600, 400)  # Optimal default window size
        )

        # Styled input field with clear visual hierarchy
        input_container = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER))
        input_label = toga.Label(
            'Input Text',
            style=Pack(padding=(0, 0, 10, 0), font_weight='bold', font_size=14)
        )
        self.input_box = toga.MultilineTextInput(
            placeholder='Add text',
            style=Pack(flex=1, padding=10, height=120, font_size=12)
        )
        input_container.add(input_label)
        input_container.add(self.input_box)

        # Controls section with direction selector and translate button
        controls = toga.Box(style=Pack(direction=ROW, padding=(20, 20), alignment=CENTER))
        self.language_select = toga.Selection(
            items=[
                'Cyrillic → Latin',
                'Cyrillic → Arabic',
                'Latin → Cyrillic',
                'Arabic → Cyrillic',
                'Arabic → Latin',
                'Latin → Arabic'
            ],
            style=Pack(flex=1, padding=(0, 10, 0, 0), font_size=12)
        )
        self.translit_button = toga.Button(
            'Translate',
            on_press=self.transliterate_text,
            style=Pack(width=120, padding=10, background_color='#4a90e2', color='white')
        )
        
        self.clear_button = toga.Button(
            'Clear',
            on_press=self.clear_output,
            style=Pack(width=120, padding=10, background_color='#e24a4a', color='white')
        )
        controls.add(self.language_select)
        controls.add(self.translit_button)
        controls.add(self.clear_button)

        # Output section
        output_container = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER))
        output_label = toga.Label(
            'Result',
            style=Pack(padding=(0, 0, 10, 0), font_weight='bold', font_size=14)
        )
        self.output_box = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, padding=10, height=120, font_size=12)
        )
        output_container.add(output_label)
        output_container.add(self.output_box)

        # Main container with modern spacing
        main_container = toga.Box(
            children=[
                input_container,
                controls,
                output_container
            ],
            style=Pack(
                direction=COLUMN,
                padding=30,
                background_color='#f5f5f5',
                alignment=CENTER
            )
        )

        self.main_window.content = main_container
        self.main_window.show()

    def transliterate_text(self, widget):
        input_text = self.input_box.value
        if not input_text:
            self.output_box.value = 'Add text'
            return

        if not self.language_select.value:
            self.output_box.value = 'Select a translation direction'
            return

        translation_map = {
            'Cyrillic → Latin': (transliterate, translit_table_rus_to_lat),
            'Cyrillic → Arabic': (transliterate, translit_table_rus_to_ar),
            'Latin → Cyrillic': (reverse_transliterate, translit_table_lat_to_rus),
            'Arabic → Cyrillic': (reverse_transliterate, translit_table_ar_to_rus),
            'Arabic → Latin': (transliterate, translit_table_ar_to_lat),
            'Latin → Arabic': (reverse_transliterate, translit_table_lat_to_ar)
        }

        func, table = translation_map[self.language_select.value]
        self.output_box.value = func(input_text, table)

    def clear_output(self, widget):
        self.input_box.value = ''
        self.output_box.value = ''

def main():
    def main():

     factory = get_platform_factory()
    current_platform = platform.system().lower()

    if current_platform == 'android':
        return TransliterationApp('TranslitGUI', 'org.example.translit', factory=factory)
    else:
        return TransliterationApp('TranslitGUI', 'org.example.translit')
