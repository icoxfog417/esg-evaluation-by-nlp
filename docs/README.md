## Data Structure

### Documents

Elastic Searchに格納するドキュメントの構造

* `documentId`: ドキュメントのId
* `resouceId`: ドキュメントの大本であるファイルを特定するためのId
* `head`/`sections`: ドキュメント本文から見出しなどを明示的に取得できる場合、格納
* `attributes`: 検索を容易にするための構造情報
* `lang`: 言語 (キーワードを当てる際に特定する必要がある)

```
{
    documentId: 111,
    resouceId: 111,
    companyId: 111,
    fiscalYear: 2018,
    head: "title",
    sections: ["Our CSR"],
    body: "I want to improve climate change ...",
    attributes: {
        index: "C4"
    },
    lang: "ja"
}
```

### Standard

```
{
    standardId: 1,
    standardName: "TestStandard"
    standardItems: []
}
```


### Standard Item

```
{
    standardItemId: 2,
    subject: "E",
    theme: "Climate Change",
    keywords: [
        {
            standardItemKeywordId: 1,
            keyword: "気候変動リスク",
            query: "気候変動リスク"
        },
        {
            keywordId: 2,
            keyword: "TCFD board of directors",
            query: "TCFD 取締役会"
            index: {
                source: "CDP",
                index: "C1"
            }
        }
    ]
}
```

### Normalized Result


```
{
    normalizedResultId: 1,
    companyId: 1,
    fiscalYear: 9999,
    standardItemKeywordId: 1,
    standardItemId: 2,
    keyword: "気候変動リスク"
}
```

### Disclosure Score


```
{
    companyId: 1,
    fiscalYear: 9999,
    standardItemId: 11,
    hitCount: 3,
    numKeywords: 12
}
```
