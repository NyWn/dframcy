# coding: utf-8
from __future__ import unicode_literals

import spacy
import pandas as pd
from spacy.matcher import Matcher, PhraseMatcher


class DframCyMatcher(object):
    def __init__(self, nlp_model):
        self.nlp_model = nlp_model
        self._nlp = None
        self._matcher = None

    def __call__(self, doc):
        df_format_json = {}
        matches = self._matcher(doc)
        for match_id, start, end in matches:
            if "match_id" not in df_format_json:
                df_format_json["match_id"] = []
            else:
                df_format_json["match_id"].append(match_id)
            if "start" not in df_format_json:
                df_format_json["start"] = []
            else:
                df_format_json["start"].append(start)
            if "end" not in df_format_json:
                df_format_json["end"] = []
            else:
                df_format_json["end"].append(end)
            if "string_id" not in df_format_json:
                df_format_json["string_id"] = []
            else:
                df_format_json["string_id"].append(self._nlp.vocab.strings[match_id])
            if "span_text" not in df_format_json:
                df_format_json["span_text"] = []
            else:
                df_format_json["span_text"].append(doc[start:end].text)

        matches_dataframe = pd.DataFrame.from_dict(df_format_json)
        matches_dataframe.reindex(matches_dataframe["match_id"])
        matches_dataframe.drop(columns=["match_id"], inplace=True)

        return matches_dataframe

    def get_nlp(self):
        return self._nlp

    def get_matcher_object(self):
        return self._matcher

    @property
    def nlp(self):

        if not self._nlp:
            self._nlp = self.create_nlp_pipeline()
        return self._nlp

    def create_nlp_pipeline(self):
        try:
            nlp = spacy.load(self.nlp_model)
        except IOError:
            nlp = spacy.load("en")
        return nlp

    def get_matcher(self):
        if not self._nlp:
            self._nlp = self.create_nlp_pipeline()
        return Matcher(self._nlp.vocab)

    def add(self, pattern_name, callback, pattern):
        if not self._matcher:
            self._matcher = self.get_matcher()
        self._matcher.add(pattern_name, callback, pattern)

