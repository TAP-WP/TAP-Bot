diff --git a/vitalarticles.py b/vitalarticles.py
index 5d5157d..da54630 100644
--- a/vitalarticles.py
+++ b/vitalarticles.py
@@ -1,13 +1,11 @@
 #!/usr/bin/python3
 
 import sys
+import re
 
 from ceterach.api import MediaWiki
-
 import mwparserfromhell as mwp
 
-import re
-
 allowed = mwp.nodes.Template, mwp.nodes.Wikilink
 
 def main():
@@ -55,10 +53,12 @@ class VitalArticleBot:
                 if len(icon_tl) > 1:
                     for icon_thing, template in zip(cls, icon_tl):
                         print(icon_thing, template)
+                        if template.get("1").value.lower() == icon_thing.lower(): break
                         template.get("1").value = icon_thing
                 else:
                     # Article is a delisted GA or FA and needs a new icon
-                    new_tl = mwp.nodes.Template("Icon", cls[1])
+                    new_tl = mwp.nodes.Template("Icon", [cls[1]])
+                    if icon_tl[0] == new_tl: continue # Duplicate icon template [[Kilogram]]
                     icon_tl += (new_tl,)
             else:
                 try:
@@ -81,7 +81,7 @@ class VitalArticleBot:
         for tl in code.filter_templates(recursive=True):
             for full_param in reversed(tl.params):
                 # GimmeBot puts the most recent action123blahs at the bottom
-                key, value = str(full_param.name), full_param.value.strip()
+                key, value = map(lambda e: e.strip(), [full_param.name, full_param.value])
                 if key == "class":
                     cls['class'] = value
                     got_cls = True
@@ -93,12 +93,13 @@ class VitalArticleBot:
                     if got_cls:
                         break
             if len(cls) == 2:
-                return [cls['class'], cls['delist']]
+                return list(map(lambda e: e.strip(), [cls['class'], cls['delist']]))
         else:
             if not cls:
                 print(WTF("No quality rating on " + repr(p.title)), file=sys.stderr)
-        return list(cls.values())
-		
+                return ['Unassessed']
+        return list(map(lambda e: e.strip(), cls.values()))
+
     def run(self):
         for va_page in self.list_vital_articles():
             print(va_page, "is being checked")
