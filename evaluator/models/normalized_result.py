import pandas as pd


class NormalizedResult():

    def __init__(self,
                 normalized_result_id,
                 company_id,
                 fiscal_year,
                 standard_item_keyword_id,
                 keyword
                 ):
        self.normalized_result_id = normalized_result_id
        self.company_id = company_id
        self.fiscal_year = fiscal_year
        self.standard_item_keyword_id = standard_item_keyword_id
        self.keyword = keyword

    def __str__(self):
        return "keyword: <{}>".format(self.keyword)

    @classmethod
    def to_tables(cls, normalized_results):
        data = []
        for n in normalized_results:
            nd = {
                "normalized_result_id": n.normalized_result_id,
                "company_id": n.company_id,
                "fiscal_year": n.fiscal_year,
                "standard_item_keyword_id": n.standard_item_keyword_id,
                "keyword": n.keyword
            }
            data.append(nd)

        return pd.DataFrame(data)
