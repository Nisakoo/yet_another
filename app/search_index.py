import re
import json
from pathlib import Path
from collections import defaultdict

from django.conf import settings


# TODO: Перейти на Pickle
class SearchIndex:
    search_index_filename = "search_index.json"

    def __init__(self):
        self._index_file = Path(settings.BASE_DIR) / self.search_index_filename
        self._index = self._load_index()

    def _load_index(self):
        if self._index_file.exists():
            with open(self._index_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
    
    def _save_index(self):
        with open(self._index_file, "w", encoding="utf-8") as file:
            json.dump(self._index, file, ensure_ascii=False, indent=2)

    def tokenize(self, text):
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)

        stop_words = {'и', 'в', 'на', 'с', 'по', 'для', 'как', 'что', 'это', 
                      'the', 'is', 'a', 'an', 'in', 'on', 'at', 'to', 'for'}
        
        tokens = [w for w in words if len(w) > 2 and w not in stop_words]
        
        return tokens
    
    def build_index(self, queryset, fields):
        """ Запускать только в фоновых задачах. """

        self._index = defaultdict(set)

        for obj in queryset.iterator(chunk_size=500):
            combined_text = ' '.join(
                str(getattr(obj, field, ' '))
                for field in fields
            )

            tokens = self.tokenize(combined_text)

            for token in tokens:
                self._index[token].add(obj.id)

        self._index = {k: list(v) for k, v in self._index.items()}
        self._save_index()


    def search(self, query):
        tokens = self.tokenize(query)

        if not tokens:
            return []
        
        result_sets = []
        for token in tokens:
            ids = self._index.get(token, [])
            result_sets.append(set(ids))

        if result_sets:
            final_ids = set.intersection(*result_sets)
            return list(final_ids)
        
        return []

        