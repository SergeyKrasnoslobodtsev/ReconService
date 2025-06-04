import logging
import re
import typing
from datetime import datetime

from .utils import format_currency_value
from .utils import extract_quarter_via_regex 
from .utils import extract_dates_via_pullenti
from .utils import select_best_date_candidate

from ..PDFExtractor.base_extractor import Cell, Document

class ReconciliationActExtractor:
    """
    Извлекает данные из таблиц актов сверки.
    """
    def __init__(self, doc: Document, logger: logging.Logger):
        self.doc = doc
        self.logger = logger

    def _extract_date_from_text(self, txt: str, context_year: typing.Optional[int] = None) -> typing.Optional[dict]:
        """
        Извлекает дату из текста, используя regex и Pullenti, с приоритезацией.
        """

        potential_dates_info = []

        # 1. Попытка извлечь квартал с помощью Regex
        if context_year and context_year > 0: # Для regex квартала нужен год
            regex_quarter_date = extract_quarter_via_regex(txt, context_year)
            if regex_quarter_date:
                potential_dates_info.append(regex_quarter_date)
                # В оригинале был break, если regex нашел квартал.
                # Если мы хотим, чтобы Pullenti все равно отработал для поиска более точной полной даты,
                # то этот флаг found_quarter_by_regex и break не нужны здесь.
                # Вместо этого, приоритезация решит.
                # Если же regex-квартал должен полностью отменять Pullenti, то можно вернуть его сразу.
                # Судя по комментариям в оригинале "Pullenti может найти более точную полную дату",
                # лучше собирать все и потом выбирать.

        # 2. Извлечение дат с помощью Pullenti
        pullenti_extracted_dates = extract_dates_via_pullenti(txt, context_year)
        if pullenti_extracted_dates:
            potential_dates_info.extend(pullenti_extracted_dates)

        if not potential_dates_info:
            self.logger.debug(f"Для текста '{txt}' не найдено потенциальных дат (regex и Pullenti).")
            return None

        self.logger.debug(f"Все потенциальные кандидаты дат для '{txt}': {potential_dates_info}")

        # Выбор наилучшей даты
        best_date_components = select_best_date_candidate(potential_dates_info, context_year)

        
        # Форматирование и возврат
        if best_date_components and best_date_components.get('year'):
            final_day = best_date_components['day']
            final_month = best_date_components['month']
            final_year = best_date_components['year']
            
            formatted_str = f"{final_day:02d}.{final_month:02d}.{final_year:04d}"
            self.logger.debug( 
                    f"Извлечена дата: {formatted_str} из '{txt}' (тип: {best_date_components['type']})"
                )
            
            return {
                    'day': final_day, 
                    'month': final_month, 
                    'year': final_year, 
                    'formatted_str': formatted_str,
                    'source_type': best_date_components['type'] 
                }
        else:
            self.logger.debug(f"Не удалось окончательно определить дату из '{txt}'. Лучший кандидат: {best_date_components}, Контекстный год: {context_year}")
            return None

    def _find_debit_credit_columns_under_header(
            self, table_cells: list[Cell], 
            parent_row: int, parent_col: int, parent_colspan: int,
            debit_kw: str = "дебет", credit_kw: str = "кредит"
    ) -> tuple[int, int]:
        debit_idx, credit_idx = -1, -1
        sub_header_row = parent_row + 1
        for cell in table_cells:
            # Используем self.logger вместо глобального logger
            self.logger.debug(f'text cell: {cell.text} - {cell.row}:{cell.col}')
            if cell.row == sub_header_row and parent_col <= cell.col < (parent_col + parent_colspan):
                text_low = cell.text.lower().strip() if cell.text else ""
                if debit_kw in text_low and debit_idx == -1: 
                    debit_idx = cell.col
                if credit_kw in text_low and credit_idx == -1 and cell.col != debit_idx: 
                    credit_idx = cell.col
        return debit_idx, credit_idx

    def extract_for_seller(self, seller_info: dict) -> dict:
        debit_entries_for_service = []  
        credit_entries_for_service = [] 
        valid_dates_for_period = []  

        seller_names = set()
        # ... (логика определения seller_names остается прежней) ...
        if sr := seller_info.get('str_repr'):
            sr_low = sr.lower()
            seller_names.add(sr_low)
            seller_names.add(sr_low.split(',')[0].strip())
            seller_names.update(m.strip() for m in re.findall(r'\(([^,)]+)', sr_low) if m.strip() and len(m.strip()) > 1)
        seller_names.update(cn.lower() for cn in seller_info.get('canonical_names', []))
        
        if raw_txt := seller_info.get('text'):
            raw_low = raw_txt.lower()
            core_raw = raw_low.split(',')[0].strip()
            seller_names.add(core_raw)
            if qm := re.search(r'["«“]([^"»”]+)["»”]', core_raw): 
                seller_names.add(qm.group(1).strip())
            seller_names.update(m.strip() for m in re.findall(r'\(([^,)]+)', raw_low) if m.strip() and len(m.strip()) > 1)
        
        sorted_seller_names = sorted([name for name in seller_names if name], key=len, reverse=True)
        self.logger.debug(f"Варианты имени продавца для поиска: {sorted_seller_names}")

        for tbl_idx, tbl in enumerate(self.doc.get_tables()):
            self.logger.info(f"Анализ таблицы {tbl_idx + 1} для акта сверки продавца.")
            main_hdr_cell: typing.Optional[Cell] = None
            # ... (логика поиска main_hdr_cell остается прежней) ...
            for cell in tbl.cells:
                if not cell.text: 
                    continue
                cell_txt_low = cell.text.lower().strip()
               
                if "по данным продавца" in cell_txt_low: 
                    main_hdr_cell = cell 
                    break
               
                if "по данным" in cell_txt_low and any(v in cell_txt_low for v in sorted_seller_names):
                    main_hdr_cell = cell
                    break

            if not main_hdr_cell:
                self.logger.debug(f"Заголовок продавца не найден в табл. {tbl_idx + 1}.")
                continue
            
            self.logger.debug(f"Найден заголовок продавца: '{main_hdr_cell.text}' R{main_hdr_cell.row}C{main_hdr_cell.col}")

            debit_col, credit_col = self._find_debit_credit_columns_under_header(
                tbl.cells, main_hdr_cell.row, main_hdr_cell.col, main_hdr_cell.colspan)

            cols_ok = (debit_col != -1 and (main_hdr_cell.colspan < 2 or credit_col != -1))
            if not cols_ok:
                self.logger.warning(f"Не удалось идентифицировать Д/К колонки в табл. {tbl_idx + 1}.")
                continue
            
            self.logger.info(f"Колонки продавца: Дебет(C{debit_col})" + (f", Кредит(C{credit_col})" if credit_col!=-1 else ""))
            
            rows_map: typing.Dict[int, typing.Dict[int, str]] = {}
            # ... (логика заполнения rows_map остается прежней) ...
            for cell in tbl.cells:
                if cell.row not in rows_map: 
                    rows_map[cell.row] = {}
                rows_map[cell.row][cell.col] = cell.text.strip() if cell.text else ""

            data_start_row = main_hdr_cell.row + 2
            last_known_year_in_table: typing.Optional[int] = None

            for r_idx in sorted(rows_map.keys()):
                if r_idx < data_start_row: 
                    continue
                
                row_data = rows_map[r_idx]
                desc = " ".join(filter(None, (row_data.get(c_idx, "") for c_idx in range(debit_col)))).strip()

                date_val_str = None 
                if desc:
                    date_info = self._extract_date_from_text(desc, context_year=last_known_year_in_table)
                    if date_info:
                        date_val_str = date_info['formatted_str']
                        if date_info.get('year') and date_info['year'] > 0:
                            last_known_year_in_table = date_info['year']
                
                if date_val_str:
                    try:
                        dt_obj = datetime.strptime(date_val_str, "%d.%m.%Y").date()
                        valid_dates_for_period.append(dt_obj)
                    except ValueError:
                        self.logger.warning(f"Не удалось разобрать строку с датой: {date_val_str} для расчета периода в T{tbl_idx}R{r_idx}. Ожидаемый формат ДД.ММ.ГГГГ")

                raw_debit_text = row_data.get(debit_col, "")
                formatted_debit_str = format_currency_value(raw_debit_text)
                debit_value = 0.0
                if formatted_debit_str and formatted_debit_str != "0,00":
                    try:
                        debit_value = float(formatted_debit_str.replace(',', '.').replace(' ', ''))
                    except ValueError:
                        self.logger.warning(f"Не удалось преобразовать значение дебета '{formatted_debit_str}' в число для T{tbl_idx}R{r_idx}. Используется 0.0.")
                
                raw_credit_text = row_data.get(credit_col, "") if credit_col != -1 else ""
                formatted_credit_str = format_currency_value(raw_credit_text)
                credit_value = 0.0
                if formatted_credit_str and formatted_credit_str != "0,00":
                    try:
                        credit_value = float(formatted_credit_str.replace(',', '.').replace(' ', ''))
                    except ValueError:
                        self.logger.warning(f"Не удалось преобразовать значение кредита '{formatted_credit_str}' в число для T{tbl_idx}R{r_idx}. Используется 0.0.")
                
                if desc: # Создаем запись только если есть описание

                    debit_entries_for_service.append({
                        "ner_table_idx": tbl_idx,
                        "ner_row_idx": r_idx, 
                        "record": desc,
                        "date": date_val_str, 
                        "value": debit_value 
                    })
                    self.logger.info(f"  Т{tbl_idx}R{r_idx}: Оп='{desc}', Дата={date_val_str or 'None'}, Д={debit_value:.2f} (исходн: '{formatted_debit_str}')")
                    credit_entries_for_service.append({
                        "ner_table_idx": tbl_idx, 
                        "ner_row_idx": r_idx, 
                        "record": desc,
                        "date": date_val_str, 
                        "value": credit_value 
                    })
                    self.logger.info(f"  Т{tbl_idx}R{r_idx}: Оп='{desc}', Дата={date_val_str or 'None'}, К={credit_value:.2f} (исходн: '{formatted_credit_str}')")
    
        min_date_str: typing.Optional[str] = None
        max_date_str: typing.Optional[str] = None
        
        if valid_dates_for_period: # Используем собранные даты
            min_dt = min(valid_dates_for_period)
            max_dt = max(valid_dates_for_period)
            min_date_str = min_dt.strftime("%d.%m.%Y")
            max_date_str = max_dt.strftime("%d.%m.%Y")
            self.logger.info(f"Рассчитанный период для продавца: с {min_date_str} по {max_date_str}")
        else:
            self.logger.info("Не найдено валидных дат в операциях продавца для определения периода.")

        return {
            "debit_entries_data": debit_entries_for_service,
            "credit_entries_data": credit_entries_for_service,
            "period_from": min_date_str,
            "period_to": max_date_str
        }
    
    def extract_for_buyer(self, buyer_info: dict) -> dict:
        """
        Извлекает значения дебета и кредита для покупателя по всем таблицам.
        Возвращает структуру аналогичную extract_for_seller:
        {
            "debit_entries_data": [...],
            "credit_entries_data": [...]
        }
        Каждый элемент содержит: индекс таблицы, строки, колонки, описание, дату, значение.
        """
        debit_entries_for_service = []
        credit_entries_for_service = []
        buyer_names = set()
        
        if sr := buyer_info.get('str_repr'):
            sr_low = sr.lower()
            buyer_names.add(sr_low)
            buyer_names.add(sr_low.split(',')[0].strip())
            buyer_names.update(m.strip() for m in re.findall(r'\(([^,)]+)', sr_low) if m.strip() and len(m.strip()) > 1)
        buyer_names.update(cn.lower() for cn in buyer_info.get('canonical_names', []))
        
        if raw_txt := buyer_info.get('text'):
            raw_low = raw_txt.lower()
            core_raw = raw_low.split(',')[0].strip()
            buyer_names.add(core_raw)
            if qm := re.search(r'["«“]([^"»”]+)["»”]', core_raw): 
                buyer_names.add(qm.group(1).strip())
            buyer_names.update(m.strip() for m in re.findall(r'\(([^,)]+)', raw_low) if m.strip() and len(m.strip()) > 1)
        
        sorted_buyer_names = sorted([name for name in buyer_names if name], key=len, reverse=True)
        self.logger.debug(f"Варианты имени покупателя для поиска: {sorted_buyer_names}")

        for tbl_idx, tbl in enumerate(self.doc.get_tables()):
            self.logger.info(f"Анализ таблицы {tbl_idx + 1} для акта сверки покупателя.")
            main_hdr_cell: typing.Optional[Cell] = None
            for cell in tbl.cells:
                if not cell.text: 
                    continue
                cell_txt_low = cell.text.lower().strip()
               
                if "по данным покупателя" in cell_txt_low: 
                    main_hdr_cell = cell 
                    break
                if "по данным клиента" in cell_txt_low: 
                    main_hdr_cell = cell 
                    break
                if "по данным" in cell_txt_low and any(v in cell_txt_low for v in sorted_buyer_names):
                    main_hdr_cell = cell
                    break
            
            if not main_hdr_cell:
                self.logger.debug(f"Заголовок покупателя не найден в табл. {tbl_idx + 1}.")
                continue
            
            self.logger.debug(f"Найден заголовок покупателя: '{main_hdr_cell.text}' R{main_hdr_cell.row}C{main_hdr_cell.col}")

            debit_col, credit_col = self._find_debit_credit_columns_under_header(
                tbl.cells, main_hdr_cell.row, main_hdr_cell.col, main_hdr_cell.colspan)

            cols_ok = (debit_col != -1 and (main_hdr_cell.colspan < 2 or credit_col != -1))
            
            if not cols_ok:
                self.logger.warning(f"Не удалось идентифицировать Д/К колонки в табл. {tbl_idx + 1}.")
                continue
            
            self.logger.info(f"Колонки покупателя: Дебет(C{debit_col})" + (f", Кредит(C{credit_col})" if credit_col!=-1 else ""))

            rows_map: typing.Dict[int, typing.Dict[int, str]] = {}
            for cell in tbl.cells:
                if cell.row not in rows_map: 
                    rows_map[cell.row] = {}
                rows_map[cell.row][cell.col] = cell.text.strip() if cell.text else ""

            data_start_row = main_hdr_cell.row + 2

            for r_idx in sorted(rows_map.keys()):
                if r_idx < data_start_row: 
                    continue
                row_data = rows_map[r_idx]
                desc = " ".join(filter(None, (row_data.get(c_idx, "") for c_idx in range(debit_col)))).strip()
                date_val_str = None  # Можно доработать извлечение даты, если потребуется

                # Дебет
                raw_debit_text = row_data.get(debit_col, "")
                formatted_debit_str = format_currency_value(raw_debit_text)
                debit_value = 0.0
                if formatted_debit_str and formatted_debit_str != "0,00":
                    try:
                        debit_value = float(formatted_debit_str.replace(',', '.').replace(' ', ''))
                    except ValueError:
                        self.logger.warning(f"Не удалось преобразовать значение дебета '{formatted_debit_str}' в число для T{tbl_idx}R{r_idx}. Используется 0.0.")
                
                debit_entries_for_service.append({
                    "ner_table_idx": tbl_idx,
                    "ner_row_idx": r_idx,
                    "ner_col_idx": debit_col,
                    "record": desc,
                    "date": date_val_str,
                    "value": debit_value
                })
                self.logger.info(f"Добавлена запись дебета для T{tbl_idx}R{r_idx}: {debit_value}")

                # Кредит
                raw_credit_text = row_data.get(credit_col, "") if credit_col != -1 else ""
                formatted_credit_str = format_currency_value(raw_credit_text)
                credit_value = 0.0
                if formatted_credit_str and formatted_credit_str != "0,00":
                    try:
                        credit_value = float(formatted_credit_str.replace(',', '.').replace(' ', ''))
                    except ValueError:
                        self.logger.warning(f"Не удалось преобразовать значение кредита '{formatted_credit_str}' в число для T{tbl_idx}R{r_idx}. Используется 0.0.")
                
                credit_entries_for_service.append({
                    "ner_table_idx": tbl_idx,
                    "ner_row_idx": r_idx,
                    "ner_col_idx": credit_col,
                    "record": desc,
                    "date": date_val_str,
                    "value": credit_value
                })
                self.logger.info(f"Добавлена запись кредита для T{tbl_idx}R{r_idx}: {credit_value}")

        return {
            "debit_entries_data": debit_entries_for_service,
            "credit_entries_data": credit_entries_for_service
        }