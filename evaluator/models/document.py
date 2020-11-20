class Document():

    def __init__(self,
                 document_id,
                 resource_id,
                 company_id,
                 fiscal_year,
                 body,
                 lang="ja",
                 head="",
                 sections=(),
                 attributes=()
                 ):
        self.document_id = document_id
        self.resource_id = resource_id
        self.company_id = company_id
        self.fiscal_year = fiscal_year
        self.body = body
        self.lang = lang
        self.head = head
        self.sections = list(sections)
        self.attributes = list(attributes)
