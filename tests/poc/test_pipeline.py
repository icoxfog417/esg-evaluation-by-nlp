import os
import unittest
import pandas as pd
from evaluator.models.document import Document
from evaluator.models.standard_item import StandardItem
from evaluator.models.standard_item_keyword import StandardItemKeyword
from evaluator.models.disclosure_score import DisclosureScore
from evaluator.models.normalized_result import NormalizedResult

from evaluator.normalizer.keyword_normalizer import KeywordNormalizer


class TestPipeline(unittest.TestCase):

    def test_pipeline(self):
        path = os.path.join(os.path.dirname(__file__), "../_data/evaluation_test.xlsx")
        documents = self.to_documents(pd.read_excel(path, sheet_name="documents"))
        standard_items = self.to_standard_items(pd.read_excel(path, sheet_name="standards"))
        normalized_result_df = pd.read_excel(path, sheet_name="normalized_result")

        normalizer = KeywordNormalizer(documents)
        ns = []
        ds = []
        for s in standard_items:
            normalized_results, disclosure_score = normalizer.normalize(
                                    company_id=9999,
                                    fiscal_year=9999, 
                                    standard_item=s)

            if len(normalized_results) > 0:
                ns += normalized_results
            if disclosure_score is not None:
                ds.append(disclosure_score)

            hit_count = normalized_result_df[
                            normalized_result_df["theme"] == s.theme]["hit_count"].values[0]
            self.assertEqual(hit_count, disclosure_score.hit_count)

        n_df = NormalizedResult.to_tables(ns)
        d_df = DisclosureScore.to_tables(ds)

    def to_documents(self, documents_df: pd.DataFrame) -> [dict]:
        documents = []
        for i, row in documents_df.iterrows():
            sections = row["section"].split("\n") if isinstance(row["section"], str) else []
            d = Document(
                    document_id=i,
                    resource_id=i,
                    company_id=9999,
                    fiscal_year=9999,
                    body=row["text"],
                    lang="ja",
                    head=row["chapter"],
                    sections=sections
            )
            documents.append(d)

        return documents

    def to_standard_items(self, standard_df: pd.DataFrame, lang="ja") -> [dict]:
        standard_items = []
        column = "keywords"
        if lang == "ja":
            column = "keywords_ja"

        for i, row in standard_df.iterrows():
            s = StandardItem(
                     standard_item_id=i,
                     subject=row["subject"],
                     theme=row["theme"],
                     keywords=[]
            )
            keywords = []
            ks = row[column].split("\n")
            for j, k in enumerate(ks):
                q = StandardItemKeyword(
                        standard_item_keyword_id=i * 100 + j,
                        keyword=k,
                        query=k
                )
                keywords.append(q)
            s.keywords = keywords
            standard_items.append(s)

        return standard_items
