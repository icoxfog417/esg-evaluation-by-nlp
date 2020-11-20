import pandas as pd


class DisclosureScore():

    def __init__(self,
                 company_id,
                 fiscal_year,
                 standard_item_id,
                 num_keywords,
                 hit_count
                 ):
        self.company_id = company_id
        self.fiscal_year = fiscal_year
        self.standard_item_id = standard_item_id
        self.num_keywords = num_keywords
        self.hit_count = hit_count

    def __str__(self):
        return "{} hit / {}".format(self.hit_count, self.num_keywords)

    @classmethod
    def to_tables(cls, disclosure_scores):
        data = []
        for d in disclosure_scores:
            dd = {
                "company_id": d.company_id,
                "fiscal_year": d.fiscal_year,
                "standard_item_id": d.standard_item_id,
                "num_keywords": d.num_keywords,
                "hit_count": d.hit_count,
            }
            data.append(dd)

        return pd.DataFrame(data)
