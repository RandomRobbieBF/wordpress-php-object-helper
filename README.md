# wordpress-php-object-helper

About
---

You have a Known plugin with a PHP object exploit?, but you need to determine which library to use to exploit the issue and run with phpggc.

This should help you out.

Example Output
----

```
$ python3 finder.py -u http://wordpress.lan -f wp-plugins.lst
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
