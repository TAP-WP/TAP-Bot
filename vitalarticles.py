#!/usr/bin/python3

import sys

from ceterach.api import MediaWiki

import mwparserfromhell as mwp

import re

allowed = mwp.nodes.Template, mwp.nodes.Wikilink

def main():
    api = MediaWiki()
    api.login("TAP_Bot", "password")
    bot = VitalArticleBot(api)
    if bot.is_allowed:
        bot.run()
    else:
        print("Check the bot's shutoff page!")
    api.logout()

class WTF(Exception): pass

class VitalArticleBot:
    def __init__(self, api, shutoff="User:TAP Bot/Shutoff"):
        self.api = api
        self.shutoff_page = api.page(shutoff)

    @property
    def is_allowed(self):
        return self.shutoff_page.content.lower() == "true"

    def list_vital_articles(self):
        for d in self.api.iterator(list='allpages',
                                   apprefix='Vital articles/',
                                   apnamespace=4,
                                   apfilterredir="nonredirects",
                                   limit=100):
            yield self.api.page(d['title'], follow_redirects=True)

    def process_vital_article(self, va_page):
        lines = va_page.content.splitlines(True)
        for i, line in enumerate(lines):
            if line[0] != "#":
                continue
            code_line = mwp.parse(line)
            *icon_tl, article = code_line.filter(forcetype=allowed)
            article_tp = self.api.page("Talk:" + str(article.title))
            cls = self.get_article_cls(article_tp)
            if len(cls) > 1:
                if len(icon_tl) > 1:
                    for icon_thing, template in zip(cls, icon_tl):
                        print(icon_thing, template)
                        template.get("1").value = icon_thing
                else:
                    # Article is a delisted GA or FA and needs a new icon
                    new_tl = mwp.nodes.Template("Icon", cls[1])
                    icon_tl += (new_tl,)
            else:
                icon_tl[0].get("1").value = cls
            if len(icon_tl) > 1:
                code_line.insert(2, " " + str(icon_tl[-1]))
            lines[i] = str(code_line)
        return "".join(lines)

    def get_article_cls(self, p):
        if not p.is_talkpage:
            p = p.toggle_talk()
        p = p.redirect_target if p.is_redirect else p
        code = mwp.parse(p.content)
        cls = {}
        got_cls, got_delist = False, False
        key_re = re.compile("action[0-9]+(result)")
        for tl in code.filter_templates(recursive=True):
            for full_param in reversed(tl.params):
                # GimmeBot puts the most recent action123blahs at the bottom
                key, value = str(full_param.name), full_param.value.strip()
                if key == "class":
                    cls['class'] = value
                    got_cls = True
                    if got_delist:
                        break
                elif key_re.search(key):
                    cls['delist'] = tl.get("currentstatus").value
                    got_delist = True
                    if got_cls:
                        break
            if len(cls) == 2:
                return [cls['class'], cls['delist']]
        else:
            if not cls:
                print(WTF("No quality rating on " + repr(p.title), file=sys.stderr)
        return list(cls.values())
		
    def run(self):
        for va_page in self.list_vital_articles():
            print(va_page, "is being checked")
            text = self.process_vital_article(va_page)
            if text != va_page.content:
                summary = "Updating qualities for vital articles"
                print(va_page.edit(text, summary, bot=True))

if __name__ == "__main__":
    main()