#!/usr/bin/env python

"""
Copyright (C) 2012 Thine Antique Pen

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import sys
import pywikibot

site = pywikibot.Site()
REDIRECT = '#REDIRECT [[%s]]'
def create(year):
    target = str(year)+' in Mandatory Palestine'
    pg1 = pywikibot.Page(site, str(year)+' of the Mandatory Palestinian territories')
    pg2 = pywikibot.Page(site, str(year)+' in the Mandatory Palestinian territories')
    pg3 = pywikibot.Page(site, str(year)+' in the Mandatory Palestinian National Authority')
    pg4 = pywikibot.Page(site, str(year)+' of the Mandatory Palestinian National Authority')
    pg5 = pywikibot.Page(site, str(year)+' of Mandatory Palestine')
    for page in [pg1, pg2, pg3, pg4, pg5]:
        if page.exists():
            continue
        print 'Creating %s' % page.title(asLink=True)
        page.put(REDIRECT % target, 'Bot: Creating redirect to [[%s]]' % target)
        talk = page.toggleTalkPage()
        if not talk.exists():
            print 'Creating %s' % talk.title(asLink=True)
            tag = '{{WikiProject Palestine|class=Redirect}}'
            summary = 'Bot: tagging article talk page with [[Wikipedia:WikiProject Palestine]]'
            talk.put(tag, summary)
def main():
    year = 1920
    while year < 1948:
        create(year)
        year += 1


if __name__ == "__main__":
    pywikibot.handleArgs()
    main()
