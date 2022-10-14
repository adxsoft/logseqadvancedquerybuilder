# data used for test cases

QueryTestCases = [
    {
        # --------- Test Case 1 ------------
        "name": "pages - select all pages",
        "commands": [
                "title: pages command - pages by wildcards",
                "- pages",
                "    - *"
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 2------------
        "name": "pages - select specific pages",
        "commands": [
            "title: pages command - specific pages",
            "- pages",
            "    - testpage001",
            "    - testpage002"
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - specific pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[?page :block/name "testpage001"]
[?page :block/name "testpage002"]
)
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 3 ------------
        "name": "pages - using wildcards (*)",
        "commands": [
            "title: pages command - pages by wildcards",
            "- pages",
            "    - testpage00*",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 4 ------------
        "name": "pages - using wildcards (*)",
        "commands": [
            "title: pages command - pages by wildcards",
            "- pages",
            "    - *002",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "002")]
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 5 ------------
        "name": "pages - using wildcards (*)",
        "commands": [
            "title: pages command - pages by wildcards",
            "- pages",
            "    - *page00*",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/includes? ?pagename "page00")]
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 6 ------------
        "name": "pages - ignore various pages",
        "commands": [
            "title: pages command - ignore pages (including wildcards)",
            "- pages",
            "    - not testpage*",
            "    - not Queries*"
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pages command - ignore pages (including wildcards)"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "testpage")])
(not [(clojure.string/starts-with? ?pagename "Queries")])
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 7 ------------
        "name": "blocks - by wildcards",
        "commands": [
            "title: blocks command - ignore blocks using wildcards",
            "- pages",
            "    - not And sir dare view*",
            "    - not *here leave merit enjoy forth.",
            "    - not *roof gutters*",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "blocks command - ignore blocks using wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "And sir dare view")])
(not [(clojure.string/ends-with? ?pagename "here leave merit enjoy forth.")])
(not [(clojure.string/includes? ?pagename "roof gutters")])
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 8 ------------
        "name": "blocktags - select and exclude block level tags",
        "commands": [
            "title: blocktags - select and exclude block level tags",
            "- blocktags",
            "    - tagA",
            "    - tagD",
            "    - not tagB",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "blocktags - select and exclude block level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "tagA")
(page-ref ?block "tagD")
)
(not (page-ref ?block "tagB"))
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 9 ------------
        "name": "blocktags and pages",
        "commands": [
            "title: blocktags and pages example",
            "- pages",
            "    - testpage00*",
            "- blocktags",
            "    - tagA",
            "    - not tagB",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "blocktags and pages example"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
(page-ref ?block "tagA")
(not (page-ref ?block "tagB"))
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 10 ------------
        "name": "pagetags - page level tags",
        "commands": [
            "title: pagetags - page level tags",
            "- pages",
            "    - testpage*",
            "- pagetags",
            "    - p-minor",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pagetags - page level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
(page-tags ?page #{"p-minor"})
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 11 ------------
        "name": "pagetags - with pages selection",
        "commands": [
            "title: pagetags and pages",
            "- pages",
            "    - *dynamics*",
            "- pagetags",
            "    - p-major",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "pagetags and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/includes? ?pagename "dynamics")]
(page-tags ?page #{"p-major"})
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 12 ------------
        "name": "tasks - select and exclude task types",
        "commands": [
            "title: select and exclude task types",
            "- tasks",
            "    - TODO",
            "    - not DOING",
        ],
        "query": """#+BEGIN_QUERY
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
"""
    },
    {
        # --------- Test Case 13 ------------
        "name": "tasks - tasks and pages",
        "commands": [
            "title: select and exclude task types",
            "- pages",
            "    - testpage01*",
            "- tasks",
            "    - TODO",
            "    - not DOING",
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "select and exclude task types"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage01")]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 14 ------------
        "name": "page properties - select pages using page property",
        "commands": [
            "title: select and exclude pages with page properties",
            "- pageproperties",
            '    - pagetype, "p-major"',
            '    - pagetype, "p-minor"',
            '    - not pagetype "p-advanced"',
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "select and exclude pages with page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-property ?page :pagetype "p-major")
(page-property ?page :pagetype "p-minor")
)
(not (page-property ?page :pagetype "p-advanced" $$ARG2))
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 15 ------------
        "name": "block properties - select blocks using block property",
        "commands": [
            "title: select and exclude blocks with block properties",
            "- blockproperties",
            '    - category, "b-thriller"',
            '    - category, "b-western"',
            '    - grade "b-fiction"',
        ],
        "query": """#+BEGIN_QUERY
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
(property ?block :grade "b-fiction" $$ARG2)
)
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 16 ------------
        "name": "namespace - only search in specific namespace",
        "commands": [
            "title: only search in specific namespace",
            "- namespace",
            '    - physics',
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "only search in specific namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "physics")
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 17 ------------
        "name": "namespace - find block properties in a namespace",
        "commands": [
            "title: find block properties in a namespace",
            "- namespace",
            '    - physics',
            '- blockproperties',
            '    - grade, "b-fiction"',
        ],
        "query": """#+BEGIN_QUERY
{
:title [:b "find block properties in a namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "physics")
(property ?block :grade "b-fiction")
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 18 ------------
        "name": "scheduled - find scheduled blocks in a namespace",
        "commands": [
            "title: find scheduled blocks in a namespace",
            "- namespace",
            '    - physics',
            '- scheduled',
        ],
        "query": """#+BEGIN_QUERY
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
"""
    },
    {
        # --------- Test Case 19 ------------
        "name": "scheduled - find scheduled blocks in a date range",
        "commands": [
            "- scheduledbetween",
            "    - :120d-before :90d-after",
        ],
        "query": """#+BEGIN_QUERY
{
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
:inputs [:120d-before :90d-after]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 20 ------------
        "name": "deadline - find blocks with deadlines",
        "commands": [
            "title: find blocks with deadlines",
            '- deadline',
        ],
        "query": """#+BEGIN_QUERY
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
"""
    },
    {
        # --------- Test Case 21 ------------
        "name": "deadline - find deadline blocks in a date range",
        "commands": [
            "- deadlinebetween",
            "    - :120d-before :30d-after",
        ],
        "query": """#+BEGIN_QUERY
{
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
"""
    },
    {
        # --------- Test Case 22 ------------
        "name": "journalonly - find journals only (not pages)",
        "commands": [
            "- journalonly",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? true]
]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 23 ------------
        "name": "journalsbetween - find future journals in a date range",
        "commands": [
            "- journalsbetween",
            "    - :today :30d-after",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? true]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 24 ------------
        "name": "journalsbetween - find past journals in a date range",
        "commands": [
            "- journalsbetween",
            "    - :30d-before :today",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? true]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:30d-before :today]
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 25 ------------
        "name": "collapse - collapse all found blocks",
        "commands": [
            "- collapse",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:collapsed? true
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 26 ------------
        "name": "expand - expand all found blocks",
        "commands": [
            "- expand",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:collapsed? false
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 27 ------------
        "name": "showbreadcrumb - show breadcrumbs for all found blockss",
        "commands": [
            "- showbreadcrumb",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:breadcrumb-show? true
}
#+END_QUERY
"""
    },
    {
        # --------- Test Case 28 ------------
        "name": "hidebreadcrumb - hide breadcrumbs for all found blockss",
        "commands": [
            "- hidebreadcrumb",
        ],
        "query": """#+BEGIN_QUERY
{
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:breadcrumb-show? false
}
#+END_QUERY
"""
    },
]

print('No of test cases = '+str(len(QueryTestCases)))
