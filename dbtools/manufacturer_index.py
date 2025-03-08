# -*- coding: utf-8 -*-

from pathlib import Path
import re
from rapidfuzz.fuzz import ratio, partial_ratio, token_sort_ratio


class ManufacturerIndex:
    tsv_path = Path(__file__).parent.joinpath('manufacturers.tsv')

    def __init__(self):
        self._false_names = {}
        self._true_name = {}
        with open(self.tsv_path, encoding='utf-8') as fh:
            manufacturers = [line.strip() for line in fh.read().strip().split('\n') if line.strip()]
        for manufacturer in manufacturers:
            names = manufacturer.split('\t')
            true_name = names[0]
            self._false_names[true_name] = names[1:]
            for name in names:
                self._true_name[name] = true_name

    def write(self):
        true_names = sorted(list(self._false_names.keys()), key=lambda x: x[0].lower())
        lines = []
        for true_name in true_names:
            lines.append('\t'.join([true_name] + self._false_names[true_name]))
        with open(self.tsv_path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines) + '\n')

    def find(self, name, ignore_case=True):
        """Finds manufacturer with a full headphone name

        Args:
            name: Full name of the headphone
            ignore_case: Match even if casing doesn't match?

        Returns:
            (True manufacturer name, matching part in the headphone name)
        """
        if not name:
            return None, None
        # Copy dict with lowercase key if ignoring case
        index = {key.lower(): val for key, val in self._true_name.items()} if ignore_case else self._true_name
        # Test substring of the headphone name made up of decreasing number of words, starting from the full length
        # and eliminating words one by one from the tail as long as a match is found
        # Sennheiser Electronic HD 800 (SDR mod)
        # Sennheiser Electronic HD 800 (SDR
        # Sennheiser Electronic HD 800
        # Sennheiser Electronic HD
        # Sennheiser Electronic --> Match false name "Sennheiser Electronic", finds true name "Sennheiser"
        words = name.split(' ')
        for n in range(len(words), 0, -1):
            candidate = ' '.join(words[:n])
            if ignore_case:
                candidate = candidate.lower()
            if candidate in index:
                return index[candidate], candidate
        return None, None

    def replace(self, old_name, ignore_case=True):
        manufacturer, match = self.find(old_name, ignore_case=ignore_case)
        if match is None:
            return old_name
        # Replace manufacturer with the match
        new_name = re.sub(f'^{re.escape(match)}', manufacturer, old_name, flags=re.IGNORECASE)
        return new_name

    def model(self, name, ignore_case=True):
        manufacturer, match = self.find(name, ignore_case=ignore_case)
        if match is None:
            return None
        # Replace manufacturer with the match
        return re.sub(f'^{match}', '', name, flags=re.IGNORECASE).strip()

    def search(self, name, threshold=80):
        """Search for manufacturer by name"""
        if not name:
            return []
        results = []
        for true_name in self._false_names.keys():
            # fuzz.ratio 대신 ratio 함수 직접 사용
            r = ratio(name.lower(), true_name.lower())
            if r >= threshold:
                results.append((true_name, r))
        # Sort by descending ratio
        results.sort(key=lambda x: x[1], reverse=True)
        return results


class UnknownManufacturerError(Exception):
    pass
