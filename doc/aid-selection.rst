AID Selection
=============

Many commands take an AID as an argument.  For convenience, Animanager provides
powerful facilities for specifying AIDs to make it faster for power users.

The primary way of specifying AIDs is by the result number from a search or
query command::

  show 12
  show 13

This will select the AID using the result number from the default results
domain.  Different search commands store their results under a domain, and
commands will use different results domains based on what would be most
convenient for each command.  You can also specify a specific results domain by
its key::

  show #db:12
  show #anidb:13

It is also common to reuse the last used AID, in which case simply use ``.``::

  show .

Finally, you can specify an AID explicitly::

  show aid:8069
