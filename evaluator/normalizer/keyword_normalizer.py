from evaluator.models.standard_item import StandardItem
from evaluator.models.document import Document
from evaluator.models.normalized_result import NormalizedResult
from evaluator.models.disclosure_score import DisclosureScore


class KeywordNormalizer():

    def __init__(self, documents: [Document]):
        self.documents = documents

    def normalize(self, company_id, fiscal_year, standard_item) -> [NormalizedResult, DisclosureScore]:
        normalized_results = self.search_keywords(
                                company_id, fiscal_year, standard_item)
        disclosure_score = None
        if len(normalized_results) > 0:
            # hit_countの計算: 同じキーワードのヒットは1として扱う必要がある
            hit_count = len(set([n.standard_item_keyword_id for n in normalized_results]))
            num_keywords = len(standard_item.keywords)
            disclosure_score = DisclosureScore(
                company_id=company_id,
                fiscal_year=fiscal_year,
                standard_item_id=standard_item.standard_item_id,
                num_keywords=num_keywords,
                hit_count=hit_count
            )

        return normalized_results, disclosure_score

    def filter_documents(self, company_id, fiscal_year):
        filtered = []
        for d in self.documents:
            if d.company_id == company_id and d.fiscal_year == fiscal_year:
                filtered.append(d)

        return filtered

    def search_keywords(self, company_id: int, fiscal_year: int,
                        standard_item: StandardItem):
        filtered = self.filter_documents(company_id, fiscal_year)

        ns = []
        for k in standard_item.keywords:
            for i, d in enumerate(filtered):
                if k.query in d.body:
                    n = NormalizedResult(
                        normalized_result_id=k.standard_item_keyword_id * 100 + i,
                        company_id=company_id,
                        fiscal_year=fiscal_year,
                        standard_item_keyword_id=k.standard_item_keyword_id,
                        keyword=k.keyword
                    )
                    ns.append(n)

        return ns
