# logseq query builder unit tests
#
# use 'ut' snippet to generate a testcase

import logseqquerybuilder as lqb
import unittest
import QueryTestDB as td
import sys


class Test_manual_tests(unittest.TestCase):

    # ------------------------------------
    def test_pages1(self):
        commands = """title: pages command - All Pages
- pages
    - *
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pages command - All Pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY
"""

        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pages2(self):
        commands = """title: pages command - pages by wildcards
- pages
    - abc*
    - *de*
    - not 2*
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or
[(clojure.string/starts-with? ?pagename "abc")]
[(clojure.string/includes? ?pagename "de")]
)
(not [(clojure.string/starts-with? ?pagename "2")])
]
}
#+END_QUERY
"""

# ------------------------------------
    def test_pages3(self):
        commands = """title: pages - wildcards but exclude specific page
- pages
    - testpage*
    - not testpage3
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pages - wildcards but exclude specific page"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
(not [?page :block/name "testpage3"])
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocks1(self):
        commands = """
title: blocks command - blocks by wildcards
- blocks
    - testblock*
    - *123*
    - 6*
    - not *456*
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blocks command - blocks by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/ends-with? ?blockcontent "testblock")]
[(clojure.string/includes? ?blockcontent "123")]
[(clojure.string/ends-with? ?blockcontent "6")]
)
(not [(clojure.string/includes? ?blockcontent "456")])
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocktags1(self):

        commands = """
title: blocktags command - test 1
- blocktags
    - tag1
    - tag2
    - not tag3
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blocktags command - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag2")
)
(not (page-ref ?block "tag3"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocktags2(self):
        commands = """
title: blocktags and pages command combined - test 2
- pages
    - test*
    - *an
- blocktags
    - tag1
    - tag2
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blocktags and pages command combined - test 2"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "an")]
)
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag2")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocktags3(self):
        commands = """
title: blocktags and pages command combined - test 3
- pages
    - test*
    - *2
    - not *age1
- blocktags
    - tag1
    - not tag2
    - tag3
    - not tag4
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blocktags and pages command combined - test 3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "2")]
)
(not [(clojure.string/ends-with? ?pagename "age1")])
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag3")
)
(not (page-ref ?block "tag2"))
(not (page-ref ?block "tag4"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pagetags1(self):
        commands = """
title: pagetags - test 1
- pagetags
    - pagetag1
    - pagetag2
    - not pagetag4
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pagetags - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-tags ?page #{"pagetag1"})
(page-tags ?page #{"pagetag2"})
)
(not (page-tags ?page #{"pagetag4"}))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pagetags2(self):
        commands = """
title: pagetags and pages combined - test 1
- pages
    - not age7*
- pagetags
    - pagetag1
    - pagetag2
    - not pagetag4
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pagetags and pages combined - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "age7")])
( or 
(page-tags ?page #{"pagetag1"})
(page-tags ?page #{"pagetag2"})
)
(not (page-tags ?page #{"pagetag4"}))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_tasks1(self):
        commands = """
title: tasks
- tasks
    - TODO
    - not DOING
"""
        result = """#+BEGIN_QUERY
{
:title [:b "tasks"]
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
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_tasks2(self):
        commands = """
title: tasks and pages
- pages
    - *7
- tasks
    - TODO
    - not DOING
"""
        result = """#+BEGIN_QUERY
{
:title [:b "tasks and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "7")]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties1(self):
        commands = """
title: pageproperties - pagetype only
- pageproperties
    - pagetype, "testA"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype only"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-property ?page :pagetype "testA")
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties2(self):
        commands = """
title: pageproperties - pagetype testA and testB
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA and testB"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-property ?page :pagetype "testA")
(page-property ?page :pagetype "testB")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties3(self):
        commands = """
title: pageproperties - pagetype testA not testB
- pageproperties
    - pagetype, "testA"
    - not pagetype, "testB"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA not testB"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-property ?page :pagetype "testA")
(not (page-property ?page :pagetype "testB"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties4(self):
        commands = """
title: pageproperties - pagetype testA and testB not pagekey 1
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
    - not pagekey, 1
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA and testB not pagekey 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-property ?page :pagetype "testA")
(page-property ?page :pagetype "testB")
)
(not (page-property ?page :pagekey 1))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_blockproperties1(self):
        commands = """
title: blockproperties - pagetype only
- pageproperties
    - pagetype, "testA"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype only"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-property ?page :pagetype "testA")
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blockproperties1(self):
        commands = """title: blockproperties - blockprop3 b1
- blockproperties
    - blockprop3, "b1"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(property ?block :blockprop3 "b1")
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blockproperties2(self):
        commands = """title: blockproperties - blockprop3 b1 and b2 and b3
- blockproperties
    - blockprop3, "b1"
    - blockprop3, "b2"
    - blockprop3, "b3"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1 and b2 and b3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :blockprop3 "b1")
(property ?block :blockprop3 "b2")
(property ?block :blockprop3 "b3")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blockproperties3(self):
        commands = """title: blockproperties - blockprop3 b1 and b2 not b3
- blockproperties
    - blockprop3, "b1"
    - blockprop3, "b2"
    - not blockprop3, "b3"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1 and b2 not b3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :blockprop3 "b1")
(property ?block :blockprop3 "b2")
)
(not (property ?block :blockprop3 "b3"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_namespace1(self):
        commands = """title: namespace1 block properties
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "namespace1 block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_namespace2(self):
        commands = """title: not namespace1 block properties
- namespace
    - not namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "not namespace1 block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not (namespace ?page "namespace1"))
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_scheduled1(self):
        commands = """title: namespace1 block properties that are scheduled
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
    - ns1p3blocktype, "nsp3blockvalue"
- scheduled
"""
        result = """#+BEGIN_QUERY
{
:title [:b "namespace1 block properties that are scheduled"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
(property ?block :ns1p3blocktype "nsp3blockvalue")
)
[?block :block/scheduled ?scheduleddate]
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_deadline1(self):
        commands = """title: namespace1 block properties that have a deadline
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
    - ns1p3blocktype, "nsp3blockvalue"
    - ns1p4blocktype, "nsp4blockvalue"
    - ns1p5blocktype, "nsp5blockvalue"
- deadline
"""
        result = """#+BEGIN_QUERY
{
:title [:b "namespace1 block properties that have a deadline"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
(property ?block :ns1p3blocktype "nsp3blockvalue")
(property ?block :ns1p4blocktype "nsp4blockvalue")
(property ?block :ns1p5blocktype "nsp5blockvalue")
)
[?block :block/deadline ?deadlinedate]
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_scheduledbetween1(self):
        commands = """title: scheduled blocks in date range
- scheduledbetween
    - :today :30d-after
"""
        result = """#+BEGIN_QUERY
{
:title [:b "scheduled blocks in date range"]
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
:inputs [:today :30d-after]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_deadlinebetween1(self):
        commands = """title: deadline blocks in date range
- deadlinebetween
    - :today :30d-after
"""
        result = """#+BEGIN_QUERY
{
:title [:b "deadline blocks in date range"]
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
:inputs [:today :30d-after]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_journalonly(self):
        commands = """title: journal pages only
- journalonly
"""
        result = """#+BEGIN_QUERY
{
:title [:b "journal pages only"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_journalsbetween(self):
        commands = """title: find journals in a date range
- journalsbetween
    - :today :30d-after
"""
        result = """#+BEGIN_QUERY
{
:title [:b "find journals in a date range"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_collapse(self):
        commands = """title: collapse found blocks
- pages
    - *
- collapse
"""
        result = """#+BEGIN_QUERY
{
:title [:b "collapse found blocks"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_expand(self):
        commands = """title: expand found blocks
- pages
    - *
- expand
"""
        result = """#+BEGIN_QUERY
{
:title [:b "expand found blocks"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_showbreadcrumb(self):
        commands = """title: show breadcrumb for found blocks
- pages
    - *
- showbreadcrumb
"""
        result = """#+BEGIN_QUERY
{
:title [:b "show breadcrumb for found blocks"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_hidebreadcrumb(self):
        commands = """title: hide breadcrumbs for found blocks
- pages
    - *
- hidebreadcrumb
"""
        result = """#+BEGIN_QUERY
{
:title [:b "hide breadcrumbs for found blocks"]
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
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(lqb.testQueryBuild(commands), result)


# Automated Tests
class Test_Automated_Tests(unittest.TestCase):
    # Uses test data from the QueryTestDB module
    # Each test is numbered from 1 to the number of tests in QueryTestDB.py

    def test_1(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_2(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_3(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_4(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_5(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_6(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_7(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_8(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_9(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_10(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_11(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_12(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_13(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_14(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_15(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_16(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_17(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_18(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_19(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_20(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_21(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_22(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_23(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_24(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_25(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_26(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_27(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)

    def test_28(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        print('test no '+str(testno)+' - ' +
              td.QueryTestCases[testno]['commands'][0])
        commands = '\n'.join(td.QueryTestCases[testno]['commands'])
        expectedresult = td.QueryTestCases[testno]['query']
        theresult = lqb.testQueryBuild(commands)
        self.assertEqual(theresult, expectedresult)
