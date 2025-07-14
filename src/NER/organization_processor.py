import logging
import re
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.ExtOntology import ExtOntology
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.org.OrganizationReferent import OrganizationReferent


class OrganizationProcessor:
    """
    Отвечает за извлечение, фильтрацию и назначение ролей организациям из текста.
    """
    def __init__(self):
        self.logger = logging.getLogger("app." + __class__.__name__)
        self.org_types_full_names_map = {
            'АО': 'акционерное общество', 
            'ОАО': 'открытое акционерное общество',
            'ЗАО': 'закрытое акционерное общество',
            'ООО': 'общество с ограниченной ответственностью',
            'ИП': 'индивидуальный предприниматель', 
            'ПАО': 'публичное акционерное общество',
            'ОО': 'общественная организация',
            'НП': 'некоммерческое партнерство',
            'ГУП': 'государственное унитарное предприятие',
            'МУП': 'муниципальное унитарное предприятие',
            'ФГУП': 'федеральное государственное унитарное предприятие',
        }
        self.pullenti_formal_types = [ft.lower() for ft in self.org_types_full_names_map.values()]
        self.seller_key_words = ['продавец', 'с одной стороны', 'между']
        self.buyer_key_words = ['покупатель', 'с другой стороны']
        self.org_ontos = self._configure_org_ontology()

    def _clean_organization_name(self, raw_name: str) -> str:
        """Очищает название организации от ИНН/КПП и других лишних данных"""
        import re
        
        # Убираем различные варианты ИНН/КПП
        # Паттерн для "(ИНН цифры)" или ", ИНН цифры" или "ИНН/КПП цифры/цифры"
        patterns = [
            r'\s*\(\s*ИНН\s+[\d/]+.*?\)',  # (ИНН 1234567890) - убираем все до закрывающей скобки
            r',\s*ИНН/КПП\s+[\d/]+',       # , ИНН/КПП 1234567890/123456789
            r',\s*ИНН\s+[\d]+',            # , ИНН 1234567890
            r'\s+\(\s*ИНН\s+[\d]+.*',      # (ИНН 1234567890 - убираем все после (ИНН
        ]
        
        name = raw_name
        for pattern in patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Убираем лишние пробелы и запятые в конце
        name = name.strip().rstrip(',').strip()
        
        # Исправляем незакрытые кавычки
        name = self._fix_quotes(name)
        
        return name
    
    def _fix_quotes(self, text: str) -> str:
        """Исправляет незакрытые кавычки в названии организации"""
        if not text:
            return text
            
        # Подсчитываем открывающие и закрывающие кавычки
        opening_quotes = text.count('"')
        
        # Если количество кавычек нечетное, добавляем закрывающую кавычку
        if opening_quotes % 2 == 1:
            text += '"'
            
        return text

    def _configure_org_ontology(self) -> ExtOntology:
        """Настраивает онтологию организаций с предопределенными организациями"""
        org_ontos = ExtOntology()
        map_orgs = {
            'РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД': 'АО',
            'РУСАЛ АЧИНСКИЙ ГЛИНОЗЕМНЫЙ КОМБИНАТ': 'АО',
            'ОК РУСАЛ ТД': 'АО'
        }
        org_id_counter = 0
        for org_full_name, org_type in map_orgs.items():
            ontology_item_ref = OrganizationReferent()
            names_to_add_to_ontology = set()
            org_full_name_upper = org_full_name.upper()
            words = org_full_name_upper.split()
            names_to_add_to_ontology.add(org_full_name_upper)
            if len(words) > 1 and words[0] == "РУСАЛ":
                names_to_add_to_ontology.add(" ".join(words[1:]))
            if len(words) > 1:
                current_prefix_parts = []
                for i in range(len(words) - 1):
                    current_prefix_parts.append(words[i])
                    prefix_variant = " ".join(current_prefix_parts)
                    if not (prefix_variant == "РУСАЛ" and words[0] == "РУСАЛ" and len(words) > 1):
                        names_to_add_to_ontology.add(prefix_variant)
            if org_full_name_upper == "РУСАЛ": 
                names_to_add_to_ontology.add("РУСАЛ")
            
            for name_variant in names_to_add_to_ontology:
                ontology_item_ref.add_slot(OrganizationReferent.ATTR_NAME, name_variant, False)
            ontology_item_ref.add_slot(OrganizationReferent.ATTR_TYPE, org_type.upper(), False)
            org_ontos.add_referent(f"org_{org_id_counter}", ontology_item_ref)
            org_id_counter += 1
        return org_ontos

    def _extract_raw_organizations(self, analysis_result: AnalysisResult, txt: str) -> list[dict]:
        raw_orgs = []
        for ent in analysis_result.entities:
            
            if not isinstance(ent, OrganizationReferent): 
                continue
            
            current_org_ref, current_org_str = ent, str(ent)
            is_linked_to_custom_ontology = False
            if ent.ontology_items and isinstance(ent.ontology_items[0].referent, OrganizationReferent):
                current_org_ref = ent.ontology_items[0].referent
                current_org_str = str(current_org_ref)
                self.logger.debug(f"Entity '{str(ent)}' linked to ontology item: '{current_org_str}'")
                is_linked_to_custom_ontology = True
            
            self.logger.debug(f"Pullenti raw: {current_org_ref.type_name}: {current_org_str}")
            
            # Добавим детальное логирование для анализа типов
            org_types = []
            for slot in current_org_ref.slots:
                if slot.type_name == OrganizationReferent.ATTR_TYPE and isinstance(slot.value, str):
                    org_types.append(slot.value)
            
            self.logger.debug(f"Типы организации '{current_org_str}': {org_types}")
            
            is_primary_legal_entity = False
            # Если организация из нашей онтологии - всегда считаем её валидной
            if is_linked_to_custom_ontology:
                is_primary_legal_entity = True
                self.logger.debug(f"'{current_org_str}' принята (онтология)")
            else:
                # Для остальных проверяем тип
                for slot in current_org_ref.slots:
                    if slot.type_name == OrganizationReferent.ATTR_TYPE and isinstance(slot.value, str):
                        slot_val_upper = slot.value.upper()
                        slot_val_low = slot.value.lower()
                        
                        # Прямое сравнение с сокращениями
                        if slot_val_upper in self.org_types_full_names_map:
                            is_primary_legal_entity = True
                            self.logger.debug(f"'{current_org_str}' принята (тип: {slot.value})")
                            break
                        # Сравнение с полными названиями
                        elif slot_val_low in self.pullenti_formal_types:
                            is_primary_legal_entity = True
                            self.logger.debug(f"'{current_org_str}' принята (полный тип: {slot.value})")
                            break
                        # Дополнительная проверка для расширенного сопоставления
                        elif self.org_types_full_names_map.get(slot_val_upper, "").lower() in self.pullenti_formal_types:
                            is_primary_legal_entity = True
                            self.logger.debug(f"'{current_org_str}' принята (сопоставление: {slot.value})")
                            break
            
            if not is_primary_legal_entity: 
                self.logger.debug(f"'{current_org_str}' отклонена (не соответствует типам)")
                continue
                
            if not ent.occurrence:
                self.logger.warning(f"Org '{str(ent)}' no occurrence.") 
                continue
            
            occ = ent.occurrence[0]
            org_text_from_doc = txt[occ.begin_char:occ.end_char]
            can_names = [s.value.upper() for s in current_org_ref.slots if 
                        s.type_name == OrganizationReferent.ATTR_NAME and isinstance(s.value, str)]
            
            if not can_names and current_org_str:
                base_name = current_org_str.split(',')[0].strip().upper()
                if base_name: 
                    can_names.append(base_name)
            
            # Логирование для отладки проблемы с названиями
            self.logger.debug(f"Оригинальный текст из документа: '{org_text_from_doc}'")
            self.logger.debug(f"Pullenti str_repr: '{current_org_str}'")
            self.logger.debug(f"Canonical names: {can_names}")
            
            # Попытаемся использовать более корректное название
            base_name = current_org_str
            if not is_linked_to_custom_ontology:
                if org_text_from_doc and len(org_text_from_doc.strip()) > 0:
                    base_name = org_text_from_doc.strip()

            clean_name = self._clean_organization_name(base_name)
            # "Общество с ограниченной ответственностью" в "ООО"
            normalized_name = self._normalize_org_name(clean_name)
            # В конце убеждаемся, что формат соответствует "Имя, Тип"
            display_name = self._ensure_pullenti_format(normalized_name)

            self.logger.debug(f"Финальное название организации: '{display_name}'")
            raw_orgs.append({
                "text": org_text_from_doc, 
                "str_repr": display_name,  # Используем более корректное название
                "pullenti_str_repr": current_org_str,  # Сохраняем оригинальное от Pullenti для отладки
                "canonical_names": sorted(list(set(cn for cn in can_names if cn))),
                "window": txt[occ.end_char : min(occ.end_char + 70, len(txt))].lower(),
                "is_linked_to_custom_ontology": is_linked_to_custom_ontology, 
                "role": None
            })
            
            self.logger.debug(f"Добавлена организация: '{display_name}' (Pullenti: '{current_org_str}') (окно: '{txt[occ.end_char : min(occ.end_char + 30, len(txt))].lower()}')")
        
        return raw_orgs
    
    def _ensure_pullenti_format(self, name: str) -> str:
        """
        Проверяет, соответствует ли имя формату 'ТИП "НАЗВАНИЕ"',
        и если да, преобразует его в формат 'НАЗВАНИЕ, ТИП'.
        """
        if not name:
            return name

        # Создаем паттерн для поиска всех известных нам типов организаций в начале строки
        org_types_pattern = "|".join(re.escape(k) for k in self.org_types_full_names_map.keys())
        pattern = re.compile(r'^\s*(' + org_types_pattern + r')\s*"(.*?)"\s*$', re.IGNORECASE)
        
        match = pattern.match(name)
        
        # Если нашли соответствие формату 'ТИП "НАЗВАНИЕ"'
        if match:
            org_type = match.group(1).upper()  # "АО"
            org_name = match.group(2)          # "ЕВРОСИБЭНЕРГО"
            
            # Собираем в формате "НАЗВАНИЕ, ТИП"
            formatted_name = f'{org_name}, {org_type}'
            self.logger.debug(f"Название '{name}' переформатировано в '{formatted_name}'")
            return formatted_name
            
        # Если имя уже в нужном формате или в неизвестном, возвращаем как есть
        return name

    def _normalize_org_name(self, name: str) -> str:
        """Нормализует название организации, заменяя полные формы на сокращения."""
        if not name:
            return name
        
        # Создаем обратный словарь: {'полное имя в нижнем регистре': 'сокращение'}
        reversed_map = {v.lower(): k for k, v in self.org_types_full_names_map.items()}
        
        # Сортируем по длине, чтобы сначала заменять более длинные строки (например, "открытое акционерное общество" перед "акционерное общество")
        sorted_full_names = sorted(reversed_map.keys(), key=len, reverse=True)

        normalized_name = name
        for full_name in sorted_full_names:
            # Ищем полное имя в начале строки без учета регистра
            pattern = re.compile(r'^\s*' + re.escape(full_name) + r'\b', re.IGNORECASE)
            if pattern.search(normalized_name):
                abbreviation = reversed_map[full_name]
                # Заменяем найденное полное имя на сокращение
                normalized_name = pattern.sub(abbreviation, normalized_name, 1).strip()
                break  # После первой успешной замены выходим
                
        return normalized_name
    
    def _filter_subsumed_organizations(self, orgs_list: list[dict]) -> list[dict]:
        final_orgs = []
        for i, org_i in enumerate(orgs_list):
            is_subsumed = False
            if not org_i['is_linked_to_custom_ontology']:
                for j, org_j in enumerate(orgs_list):
                    if i == j or not org_j['is_linked_to_custom_ontology']: 
                        continue
                    if any(name_i in name_j and len(name_i) < len(name_j)
                           for name_i in org_i.get('canonical_names', [])
                           for name_j in org_j.get('canonical_names', [])):
                        self.logger.debug(f"'{org_i['str_repr']}' subsumed by '{org_j['str_repr']}' (ontology)")
                        is_subsumed = True
                        break
            if not is_subsumed: 
                final_orgs.append(org_i)
        return final_orgs

    def _assign_roles_by_keywords_and_rusal_logic(self, orgs_list: list[dict]) -> None:
        for org in orgs_list:
            win_text = org['window']
            if any(kw in win_text for kw in self.seller_key_words):
                org['role'] = 'продавец'
            elif any(kw in win_text for kw in self.buyer_key_words): 
                org['role'] = 'покупатель'
            
            if org['role'] is None and \
               (any("РУСАЛ" in cn for cn in org.get('canonical_names', [])) or \
                "РУСАЛ" in org['str_repr'].split(',')[0].strip().upper()):
                org['role'] = 'покупатель'
                self.logger.debug(f"'{org['str_repr']}' -> 'покупатель' (РУСАЛ logic).")

    def _assign_mutual_roles(self, orgs_list: list[dict]) -> None:
        # Найти организации с уже назначенными ролями
        sellers = [org for org in orgs_list if org['role'] == 'продавец']
        buyers = [org for org in orgs_list if org['role'] == 'покупатель']
        unassigned = [org for org in orgs_list if org['role'] is None]
        
        self.logger.debug(f"Перед взаимным назначением: продавцы={len(sellers)}, покупатели={len(buyers)}, неназначенные={len(unassigned)}")
        
        # Если есть покупатель, но нет продавца - назначить неназначенную организацию продавцом
        if buyers and not sellers and len(unassigned) >= 1:
            unassigned[0]['role'] = 'продавец'
            self.logger.debug(f"'{unassigned[0]['str_repr']}' назначена продавцом (mutual logic)")
        
        # Если есть продавец, но нет покупателя - назначить неназначенную организацию покупателем  
        elif sellers and not buyers and len(unassigned) >= 1:
            unassigned[0]['role'] = 'покупатель'
            self.logger.debug(f"'{unassigned[0]['str_repr']}' назначена покупателем (mutual logic)")
        
        # Исходная логика для случая с 2 организациями
        elif len(orgs_list) == 2:
            o1, o2 = orgs_list[0], orgs_list[1]
            if o1['role'] == 'покупатель' and o2['role'] is None: 
                o2['role'] = 'продавец'
                self.logger.debug(f"'{o2['str_repr']}' назначена продавцом (2 orgs logic)")
            elif o2['role'] == 'покупатель' and o1['role'] is None: 
                o1['role'] = 'продавец'
                self.logger.debug(f"'{o1['str_repr']}' назначена продавцом (2 orgs logic)")
            elif o1['role'] == 'продавец' and o2['role'] is None: 
                o2['role'] = 'покупатель'
                self.logger.debug(f"'{o2['str_repr']}' назначена покупателем (2 orgs logic)")
            elif o2['role'] == 'продавец' and o1['role'] is None: 
                o1['role'] = 'покупатель'
                self.logger.debug(f"'{o1['str_repr']}' назначена покупателем (2 orgs logic)")

    def _log_final_organization_roles(self, orgs_list: list[dict]) -> None:
        
        if not orgs_list: 
            self.logger.warning("Организации для назначения ролей не найдены.")
            return
        self.logger.info("Итоговые организации и их роли:")
        
        for org in orgs_list:
            role = org.get('role', 'Не определена')
            log_entry = f"{role.upper()} - {org['str_repr']}"
            if not org['is_linked_to_custom_ontology']: 
                log_entry += f" (Исходный: '{org['text']}')"
            if 'pullenti_str_repr' in org and org['pullenti_str_repr'] != org['str_repr']:
                log_entry += f" (Pullenti: '{org['pullenti_str_repr']}')"
            self.logger.info(log_entry)

    def process_text(self, text: str) -> list[dict]:
        self.logger.debug(f"Поиск организаций в тексте (начало): {text}...")
        with ProcessorService.create_specific_processor(OrganizationAnalyzer.ANALYZER_NAME) as proc:
            res = proc.process(SourceOfAnalysis(text), self.org_ontos)
        
        orgs = self._extract_raw_organizations(res, text)
        if not orgs: 
            self.logger.info("Первичное извлечение не дало организаций.")
            return []
        
        orgs = self._filter_subsumed_organizations(orgs)
        if not orgs: 
            self.logger.info("После фильтрации поглощенных организаций список пуст.")
            return []
        
        self._assign_roles_by_keywords_and_rusal_logic(orgs)
        self._assign_mutual_roles(orgs)

        return orgs