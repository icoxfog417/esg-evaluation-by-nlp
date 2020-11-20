import pandas as pd
from evaluator.models.standard import Standard
from evaluator.models.standard_item import StandardItem
from evaluator.models.standard_item_keyword import StandardItemKeyword


class StandardReader():

    def __init__(self):
        pass

    def read(self, path, sheet_name, skiprows=0, lang="ja"):
        """
        Read Standard Data,
        sheet_name will be used as standard name.
        """
        sheet = pd.read_excel(path, sheet_name=sheet_name, skiprows=skiprows)
        sheet.dropna(subset=["standard_item_id"], inplace=True)
        ids = sheet["standard_item_id"].nunique()
        themes = sheet["standard_item_id"].nunique()

        if ids != themes:
            raise Exception("Number of ids and theme string does not match.")

        ids = sheet["standard_item_id"].unique()
        suffix = ""
        if lang:
            suffix = "_" + lang

        standard_items = []
        for _id in ids:
            if not _id:
                continue
            rows = sheet[sheet["standard_item_id"] == _id]
            s = None
            keywords = []
            for i, row in rows.iterrows():
                if s is None:
                    s = StandardItem(
                            standard_item_id=_id,
                            subject=row["subject" + suffix],
                            theme=row["theme" + suffix],
                            keywords=[]
                        )
                k = StandardItemKeyword(
                        standard_item_keyword_id=_id * 100 + i,
                        keyword=row["keyword" + suffix],
                        query=row["keyword" + suffix]
                )
                keywords.append(k)

            s.keywords = keywords
            standard_items.append(s)

        standard = Standard(sheet_name, standard_items)
        return standard
