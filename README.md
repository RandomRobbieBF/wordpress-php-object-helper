# wordpress-php-object-helper

About
---

Got Know a plugin has a php object exploit but need to find which lib to use?

This will bruteforce all plugins and then find a plugin that is using a known lib that could help.

It's not perfect but it's better than nothing!

Example Output
----

```
$ python3 plugins.py -u http://wordpress.lan -f wp-plugins.lst
Processing URLs: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 26/26 [00:00<00:00, 26.74it/s]
Found the following plugins:
http://wordpress.lan/wp-content/plugins/updraftplus/readme.txt
Checking Wordpress SVN for vendor folder.
Vendor Folder found at http://plugins.svn.wordpress.org/updraftplus/trunk/vendor/
Checking for known libraries for phpgcc inside vendor folder.
You may be able to use the following Guzzle with this updraftplus plugin.
You may be able to use the following Symfony with this updraftplus plugin.
You may be able to use the following PHPSecLib with this updraftplus plugin.
```
