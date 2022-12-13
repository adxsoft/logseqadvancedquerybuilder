# data used for test cases

# TODO Test and Add each query in LogseqTestGraph from QueryExample05 onwards

QueryTestCases = [

    # test 1
    """title: pages command - select all pages
- pages
    - *
#+BEGIN_QUERY
{
:title [:b "pages command - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
""",

    # test 2
    """title: pages command - specific pages
- pages
    - testpage001
    - testpage002
#+BEGIN_QUERY
{
:title [:b "pages command - specific pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[?block :block/name "testpage001"]
[?block :block/name "testpage002"]
)
]
}
#+END_QUERY
""",

    # test 3
    """title: pages command - pages by wildcards
- pages
    - testpage00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
""",

    # test 4
    """title: pages command - pages by wildcards
- pages
    - *002
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "002")]
]
}
#+END_QUERY
""",

    # test 5
    """title: pages command - pages by wildcards
- pages
    - *page00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/includes? ?pagename "page00")]
]
}
#+END_QUERY
""",

    # test 6
    """title: pages command - ignore pages (including wildcards)
- pages
    - not testpage*
    - not Queries*
#+BEGIN_QUERY
{
:title [:b "pages command - ignore pages (including wildcards)"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "testpage")])
(not [(clojure.string/starts-with? ?pagename "Queries")])
]
}
#+END_QUERY
""",

    # test 7
    """title: blocks command - ignore blocks using wildcards
- blocks
    - not And sir dare view*
    - not *here leave merit enjoy forth.
    - not *roof gutters*
#+BEGIN_QUERY
{
:title [:b "blocks command - ignore blocks using wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not [(clojure.string/ends-with? ?blockcontent "And sir dare view")])
(not [(clojure.string/starts-with? ?blockcontent "here leave merit enjoy forth.")])
(not [(clojure.string/includes? ?blockcontent "roof gutters")])
]
}
#+END_QUERY
""",

    # test 8
    """title: blocktags - select and exclude block level tags
- blocks
    - *
- blocktags
    - tagA
    - tagD
    - not tagB
#+BEGIN_QUERY
{
:title [:b "blocktags - select and exclude block level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "taga")
(page-ref ?block "tagd")
)
(not (page-ref ?block "tagb"))
]
}
#+END_QUERY
""",
    """title: blocktags and pages don't mix
- pages
    - testpage00*
- blocktags
    - tagA
    - not tagB
#+BEGIN_QUERY

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages don't mix"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
""",

    # test 10
    """title: pagetags - page level tags
- pages
    - testpage*
- pagetags
    - classA
#+BEGIN_QUERY
{
:title [:b "pagetags - page level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
[?block :block/journal? false]
(page-tags ?block #{"classa"})
]
}
#+END_QUERY
""",

    # test 11
    """title: pagetags and pages
- pages
    - *dynamics*
- pagetags
    - classB
#+BEGIN_QUERY
{
:title [:b "pagetags and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/includes? ?pagename "dynamics")]
[?block :block/journal? false]
(page-tags ?block #{"classb"})
]
}
#+END_QUERY
""",

    # test 12
    """title: select and exclude task types
- tasks
    - TODO
    - not DOING
#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "select and exclude task types"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
""",

    """title: select and exclude task types
- pages
    - testpage00*
- tasks
    - TODO
    - not DOING
#+BEGIN_QUERY

;; **ERROR: tasks not valid with pages command use blocks command instead

{
:title [:b "select and exclude task types"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
""",

    # test 14
    """title: select and exclude pages with page properties
- pages
    - *
- pageproperties
    - pagetype, "p-major"
    - pagetype, "p-minor"
    - not pagetype, "p-advanced"
#+BEGIN_QUERY
{
:title [:b "select and exclude pages with page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "p-major")
(page-property ?block :pagetype "p-minor")
)
(not (page-property ?block :pagetype "p-advanced"))
]
}
#+END_QUERY
""",

    # test 15
    """title: select and exclude blocks with block properties
- blocks
    - *
- blockproperties
    - category, "b-thriller"
    - category, "b-western"
    - grade, "b-fiction"
#+BEGIN_QUERY
{
:title [:b "select and exclude blocks with block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :category "b-thriller")
(property ?block :category "b-western")
(property ?block :grade "b-fiction")
)
]
}
#+END_QUERY
""",

    # test 16
    """title: only search pages in specific namespace
- pages
    - *
- namespace
    - physics
#+BEGIN_QUERY
{
:title [:b "only search pages in specific namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(namespace ?block "physics")
]
}
#+END_QUERY
""",

    # test 17
    """title: find block properties in a namespace
- blocks
    - *
- namespace
    - tech/python
- blockproperties
    - grade, "b-fiction"
#+BEGIN_QUERY
{
:title [:b "find block properties in a namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "tech/python")
(property ?block :grade "b-fiction")
]
}
#+END_QUERY
""",

    # test 18
    """title: find scheduled blocks in a namespace
- blocks
    - *
- namespace
    - physics
- scheduled
#+BEGIN_QUERY
{
:title [:b "find scheduled blocks in a namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "physics")
[?block :block/scheduled ?scheduleddate]
]
}
#+END_QUERY
""",

    # test 19
    """title: scheduled - find scheduled blocks in a date range
- blocks
    - *
- scheduledbetween
    - :720d-before :700d-after
#+BEGIN_QUERY
{
:title [:b "scheduled - find scheduled blocks in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/scheduled ?scheduleddate]
[(>= ?scheduleddate ?startdate)]
[(<= ?scheduleddate ?enddate)]
]
:inputs [:720d-before :700d-after]
}
#+END_QUERY
""",

    # test 20
    """title: find blocks with deadlines
- blocks
    - *
- deadline
#+BEGIN_QUERY
{
:title [:b "find blocks with deadlines"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/deadline ?deadlinedate]
]
}
#+END_QUERY
""",

    # test 21
    """title: find blocks with deadlines in a date range
- blocks
    - *
- deadlinebetween
    - :120d-before :30d-after
#+BEGIN_QUERY
{
:title [:b "find blocks with deadlines in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/deadline ?deadlinedate]
[(>= ?deadlinedate ?startdate)]
[(<= ?deadlinedate ?enddate)]
]
:inputs [:120d-before :30d-after]
}
#+END_QUERY
""",

    # test 22
    """title: find journals
- pages
    - *
- journalonly
#+BEGIN_QUERY
{
:title [:b "find journals"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? true]
]
}
#+END_QUERY
""",

    # test 23
    """title: find journal in a date range
- pages
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "find journal in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/name ?pagename]
[?block :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
""",

    # test 24
    """title: find journals between dates
- blocks
    - *
- journalsbetween
    - :30d-before :today
#+BEGIN_QUERY
{
:title [:b "find journals between dates"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:30d-before :today]
}
#+END_QUERY
""",

    # test 25
    """title: collapse results
- pages
    - testpage00*
- collapse
#+BEGIN_QUERY
{
:title [:b "collapse results"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:collapsed? true
}
#+END_QUERY
""",

    # test 26
    """title: expand results
- pages
    - testpage00*
- expand
#+BEGIN_QUERY
{
:title [:b "expand results"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:collapsed? false
}
#+END_QUERY
""",

    # test 27
    """title: show breadcrumbs
- pages
    - testpage00*
- showbreadcrumb
#+BEGIN_QUERY
{
:title [:b "show breadcrumbs"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:breadcrumb-show? true
}
#+END_QUERY
""",

    # test 28
    """title: hide breadcrumbs
- pages
    - testpage00*
- hidebreadcrumb
#+BEGIN_QUERY
{
:title [:b "hide breadcrumbs"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:breadcrumb-show? false
}
#+END_QUERY
""",

    # test 29
    """title: find journal in a date range using blocks
- blocks
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "find journal in a date range using blocks"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
""",
    # test 30
    """title: All blocks - test access to parent pages tags, journal
- blocks
    - *
- tasks
    - TODO
- pagetags
    - classC
#+BEGIN_QUERY
{
:title [:b "All blocks - test access to parent pages tags, journal"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
[?page :block/journal? false]
(page-tags ?page #{"classc"})
]
}
#+END_QUERY
""",
    # test 31
    """title: Pages only - Access page properties
- pages
    - *
- pageproperties
    - pagetype, "p-minor"
#+BEGIN_QUERY
{
:title [:b "Pages only - Access page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "p-minor")
]
}
#+END_QUERY
""",
    # test 32
    """title: Pages only - access multiple property values
- pages
    - *
- pageproperties
    - pagetype, "p-minor"
    - pagetype, "p-major"
#+BEGIN_QUERY
{
:title [:b "Pages only - access multiple property values"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "p-minor")
(page-property ?block :pagetype "p-major")
)
]
}
#+END_QUERY
""",
    # test 33
    """title: Page blocks only - pagetags
- pages
    - *
- pagetags
    - classC
#+BEGIN_QUERY
{
:title [:b "Page blocks only - pagetags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
(page-tags ?block #{"classc"})
]
}
#+END_QUERY
""",
    # test 34
    """title: Pages only - select all pages
- pages
    - *
#+BEGIN_QUERY
{
:title [:b "Pages only - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
""",
    # test 35
    """title: pages command - specific pages
- pages
    - testpage001
    - testpage002
#+BEGIN_QUERY
{
:title [:b "pages command - specific pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[?block :block/name "testpage001"]
[?block :block/name "testpage002"]
)
]
}
#+END_QUERY
""",
    # test 36
    """title: pages command - pages by wildcards
- pages
    - testpage00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
""",
    # test 37
    """title: pages command - pages by wildcards
- pages
    - *002
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "002")]
]
}
#+END_QUERY
""",
    # test 38
    """title: journalsbetween defaulting to blocks retrieval
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "journalsbetween defaulting to blocks retrieval"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
""",
    # test 39
    """title: journalsbetween using pages retrieval
- pages
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "journalsbetween using pages retrieval"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/name ?pagename]
[?block :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
""",
    # test 40
    """title: page property combinations using and and or
- pages
    - *
- pageproperties
    - pagecategory, "p-minor"
    - or pagecategory, "p-minimum"
    - and pagetype, "p-type1"
#+BEGIN_QUERY
{
:title [:b "page property combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagecategory "p-minor")
(page-property ?block :pagecategory "p-minimum")
)
(page-property ?block :pagetype "p-type1")
]
}
#+END_QUERY
""",
    # test 41
    """title: page tag combinations using and and or
- pages
    - *
- pagetags
    - classA
    - or classB
    - and classH
#+BEGIN_QUERY
{
:title [:b "page tag combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
( or 
(page-tags ?block #{"classa"})
(page-tags ?block #{"classb"})
)
(page-tags ?block #{"classh"})
]
}
#+END_QUERY
""",
    # test 42
    """title: block property combinations using and and or
- blocks
    - *
- blockproperties
    - category, "b-fiction"
    - or grade, "b-western"
    - and category, "b-travel"
#+BEGIN_QUERY
{
:title [:b "block property combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :category "b-fiction")
(property ?block :grade "b-western")
)
(property ?block :category "b-travel")
]
}
#+END_QUERY
""",
    # test 43
    """title: block tag combinations using and and or
- blocks
    - *
- blocktags
    - tagA
    - or tagB
    - and tagD
#+BEGIN_QUERY
{
:title [:b "block tag combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "taga")
(page-ref ?block "tagb")
)
(page-ref ?block "tagd")
]
}
#+END_QUERY
""",
    # test 44
    """title: task and or combintions
- blocks
    - *
- tasks
    - TODO
    - and WAITING
    - or LATER
    - not DOING
#+BEGIN_QUERY
{
:title [:b "task and or combintions"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
( or 
[(contains? #{"TODO"} ?marker)]
[(contains? #{"LATER"} ?marker)]
)
[(contains? #{"WAITING"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
""",
    # test 45
    """title: select blocks with links to pages
- blocks
    - *
- pagelinks
    - gardening
    - vegetables
    - not turnips
#+BEGIN_QUERY
{
:title [:b "select blocks with links to pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[?block :block/path-refs [:block/name "gardening"]]
[?block :block/path-refs [:block/name "vegetables"]]
)
(not [?block :block/path-refs [:block/name "turnips"]])
]
}
#+END_QUERY
""",
    # test 46
    """title: select blocks with links to journals
- blocks
    - *
- pagelinks
    - Dec 25th, 2022
    - Jan 1st, 2019
#+BEGIN_QUERY
{
:title [:b "select blocks with links to journals"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[?block :block/path-refs [:block/name "dec 25th, 2022"]]
[?block :block/path-refs [:block/name "jan 1st, 2019"]]
)
]
}
#+END_QUERY
"""



]

# print('No of test cases = '+str(len(QueryTestCases)))
