# logseq query builder unit tests
#
# use 'ut' snippet to generate a testcase

import logseqquerybuilder as lqb
import unittest
import QueryTestDB as td
import queryDB as db
import sys
import logging as log


def gettestcommands(testno):
    testdata = td.QueryTestCases[testno].split("#+BEGIN")
    return testdata[0]


def gettestexpectedresults(testno):
    testdata = td.QueryTestCases[testno].split("#+BEGIN")
    return "#+BEGIN"+testdata[1]


class Test_negative_manual_tests(unittest.TestCase):

    # ------------------------------------
    def test_bad_title(self):
        commands = """title pages command - select all pages
- pages
    - *
"""
        result = """#+BEGIN_QUERY
;; WARNING: title line should start with title:
{
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
"""

        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_missing_pages_and_blocks_commands_1(self):
        commands = """title: missing pages and blocks commands"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "missing pages and blocks commands"]
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

    def test_missing_pages_and_blocks_all_commands(self):

        results = ''
        for command in db.commandsDict:
            commands = 'title: test missing pages and blocks\n- '+command+'\n'
            result = lqb.testQueryBuild(commands)
            results += '\nRESULT for '+command+'\n\n'+result+'\n\n'

        expectedresults = """
RESULT for blocks

#+BEGIN_QUERY
{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY



RESULT for blockproperties

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY



RESULT for blocktags

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY



RESULT for deadline

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/deadline ?deadlinedate]
]
}
#+END_QUERY



RESULT for deadlinebetween

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
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
}
#+END_QUERY



RESULT for journalsbetween

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
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
}
#+END_QUERY



RESULT for journalonly

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? true]
]
}
#+END_QUERY



RESULT for namespace

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY



RESULT for pages

#+BEGIN_QUERY
{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY



RESULT for pageproperties

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY



RESULT for pagetags

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? false]
]
}
#+END_QUERY



RESULT for tasks

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
]
}
#+END_QUERY



RESULT for scheduled

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/scheduled ?scheduleddate]
]
}
#+END_QUERY



RESULT for scheduledbetween

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
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
}
#+END_QUERY



RESULT for collapse

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:collapsed? true
}
#+END_QUERY



RESULT for expand

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:collapsed? false
}
#+END_QUERY



RESULT for showbreadcrumb

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
:breadcrumb-show? true
}
#+END_QUERY



RESULT for hidebreadcrumb

#+BEGIN_QUERY
;; WARNING: Must have \'pages\' command or \'blocks\' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "test missing pages and blocks"]
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
        self.assertEqual(expectedresults, results)

    def test_bad_commands(self):
        commands = """title: bad commands
- badcommand1
- badcommand2
forgottenthedash
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

;; WARNING: '- badcommand1' is not valid command.
;;          Either a mispelt command or no leading dash
;; WARNING: '- badcommand2' is not valid command.
;;          Either a mispelt command or no leading dash
;; WARNING: forgottenthedash has no leading hypen eg '- pages'
{
:title [:b "bad commands"]
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

    def test_equal_rather_than_dash(self):
        commands = """title: equal sign used instead of dash
- pages
    = testpage00*
= pagetags
"""
        result = """#+BEGIN_QUERY
;; WARNING:     = testpage00* has no leading hypen eg '- pages'
;; WARNING: = pagetags has no leading hypen eg '- pages'
{
:title [:b "equal sign used instead of dash"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

    def test_only_an_argument_line(self):
        commands = """title: missing command
    - testpage00*
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "missing command"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/ends-with? ?blockcontent "testpage00")]
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)


class Test_positive_manual_tests(unittest.TestCase):

    # ------------------------------------
    def test_pages1(self):
        commands = """title: pages command - select all pages
- pages
    - *
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pages command - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
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
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
(not [?block :block/name "testpage3"])
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocks1(self):
        commands = """title: blocks command - blocks by wildcards
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

        commands = """title: blocktags command - test 1
- blocktags
    - tag1
    - tag2
    - not tag3
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

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
        commands = """title: blocktags and pages command combined - test 2
- pages
    - test*
    - *an
- blocktags
    - tag1
    - tag2
"""
        result = """#+BEGIN_QUERY

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages command combined - test 2"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "an")]
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocktags3(self):
        commands = """title: blocktags and pages command combined - test 3
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

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages command combined - test 3"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "2")]
)
(not [(clojure.string/ends-with? ?pagename "age1")])
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blocktags4(self):
        commands = """title: multiple blocks tags
- blocks
    - *
- blocktags
    - tag1 tag2 tag3
    - not tag2
"""
        result = """#+BEGIN_QUERY
{
:title [:b "multiple blocks tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-ref ?block "tag1")
(page-ref ?block "tag2")
(page-ref ?block "tag3")
(not (page-ref ?block "tag2"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pagetags1(self):
        commands = """title: pagetags - test 1
- pagetags
    - pagetag1
    - pagetag2
    - not pagetag4
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "pagetags - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? false]
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
        commands = """title: pagetags and pages combined - test 1
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
[?block :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "age7")])
[?block :block/journal? false]
( or 
(page-tags ?block #{"pagetag1"})
(page-tags ?block #{"pagetag2"})
)
(not (page-tags ?block #{"pagetag4"}))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pagetags3(self):
        commands = """title: pages with multiple tags
- pages
    - *
- pagetags
    - classA  classB
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pages with multiple tags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
(page-tags ?block #{"classa"})
(page-tags ?block #{"classb"})
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_tasks1(self):
        commands = """title: tasks - select and exclude task types
- tasks
    - TODO
    - not DOING
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "tasks - select and exclude task types"]
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
        commands = """title: tasks and pages
- pages
    - *7
- tasks
    - TODO
    - not DOING
"""
        result = """#+BEGIN_QUERY

;; **ERROR: tasks not valid with pages command use blocks command instead

{
:title [:b "tasks and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "7")]
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties1(self):
        commands = """title: pageproperties - pagetype only missing pages command
- pages
    - *
- pageproperties
    - pagetype, "testA"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype only missing pages command"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "testA")
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties2(self):
        commands = """title: pageproperties - pagetype testA and testB
- pages
    - *
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA and testB"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "testA")
(page-property ?block :pagetype "testB")
)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties3(self):
        commands = """title: pageproperties - pagetype testA not testB
- pages
    - *
- pageproperties
    - pagetype, "testA"
    - not pagetype, "testB"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA not testB"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "testA")
(not (page-property ?block :pagetype "testB"))
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_pageproperties4(self):
        commands = """title: pageproperties - missing pages command
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
    - not pagekey, 1
"""
        result = """#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "pageproperties - missing pages command"]
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
        commands = """title: blockproperties - pagetype only
- blocks
    - *
- pageproperties
    - pagetype, "testA"
"""
        result = """#+BEGIN_QUERY
{
:title [:b "blockproperties - pagetype only"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-property ?page :pagetype "testA)
]
}
#+END_QUERY
"""
        self.assertEqual(lqb.testQueryBuild(commands), result)

# ------------------------------------
    def test_blockproperties1(self):
        commands = """title: blockproperties - blockprop3 b1
- blocks
    - *
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
- blocks
    - *
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
- blocks
    - *
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
- blocks
    - *
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
- blocks
    - *
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
- blocks
    - *
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
- blocks
    - *
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
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

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
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

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
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

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
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "find journals in a date range"]
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
[?block :block/name ?pagename]
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
[?block :block/name ?pagename]
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
[?block :block/name ?pagename]
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
[?block :block/name ?pagename]
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

    def setUp(self) -> None:
        lqb.querygroup = 'RUBBISH'
        return super().setUp()

    def test_1(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_2(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_3(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_4(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_5(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_6(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_7(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_8(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_9(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_10(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_11(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_12(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_13(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_14(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_15(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_16(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_17(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_18(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_19(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_20(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_21(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_22(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_23(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_24(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_25(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_26(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_27(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_28(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_29(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_30(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_31(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_32(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_33(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_34(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_35(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_36(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_37(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_38(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))

    def test_39(self):
        functionname = sys._getframe().f_code.co_name
        testno = int(functionname.split("_")[1])-1
        theresult = lqb.testQueryBuild(gettestcommands(testno))
        self.assertEqual(theresult, gettestexpectedresults(testno))
