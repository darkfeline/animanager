Commands reference
==================

Global options
--------------

These go before any commands.

--config=PATH   Specify an alternate configuration file to use.
                Default is ``~/.animanager/config.ini``.
--db=PATH       Specify an alternate database file to use.
                Default is ``~/.animanager/database.db``.

Make judicious use of the ``--help`` option::

  $ animanager --help
  $ animanager anime --help
  $ animanager anime add --help

Anime commands
--------------

These commands track and manage anime::

  $ animanager anime <command>

I suggest you make an alias for your shell; for Bash, put this in your
``.bashrc``::

  alias anime="animanager anime"

.. _add:

add
^^^

::

   $ animanager anime add "series name search"

Add a series.

You provide a string to search for, Animanager will search for it on MAL and
prompt you for a series to add.  You can add it with an initial status of "plan
to watch", "watching", or "finished".  In the case of "finished", Animanager
will also set the watched episode count, and ask if you want to set the start
and finished dates to today.  In the case of "watching", Animanager will also
register the show (see :ref:`register`).

bump
^^^^

::

   $ animanager anime bump "series name search"

Animanager will selectively bump the episode watched count of one show.  By
default Animanager will only search "watching" shows; use the option ``--all``
to search from all shows, including "plan to watch" and "dropped".

Animanager will set the show to watching, update start and end date, and update
completion status automagically.

clean
^^^^^

::

   $ animanager anime clean

Cleans up registered series in the config (see :ref:`register`).

Removes all registered series in the config file that have been completed.

hold
^^^^

::

   $ animanager anime hold "series name search"

Animanager will set the status of one series to "on hold".  By
default Animanager will only search "watching" shows; use the option ``--all``
to search from all incomplete shows, including "plan to watch" and "dropped".

.. _register:

register
^^^^^^^^

::

   $ animanager anime register

Register a series.

Registering series is used for the :ref:`watch` command.  These are added to the
configuration file under the ``[series]`` section.

Here is an example::

  [series]
  877 = .*Overlord.*?(?P<ep>[0-9]+)(v(?P<ver>[0-9]+))?

These map the internal ID of a series in the database to a regular expression
pattern that is used by Animanager to match files to series.

The ``(?P<ep>[0-9]+)`` group captures the episode number of the file.

The ``(?P<ver>[0-9]+)`` group captures the version of the file.  If this group
doesn't match or isn't present, the version defaults to 1.

The ``register`` command will add a default regular expression pattern that
should work most of the time.  Depending on how your files are named, you may
need to edit this pattern by hand in the configuration file.

The patterns are tried sequentially.  That means that for the following example,
the second line will never match because the first line will match instead::

  [series]
  1 = .*Overlord.*?(?P<ep>[0-9]+)(v(?P<ver>[0-9]+))?
  2 = .*Overlord.*?Special.*?(?P<ep>[0-9]+)(v(?P<ver>[0-9]+))?

Refer to the Python documentation for more information about Python's regular
expression syntax.

Adding a series as "watching" (see :ref:`add`) will register it automatically.
In the case where you added as series as "plan to watch" or otherwise do not
have a series registered in your config, this command can be used.

search
^^^^^^

::

   $ animanager anime search "series name search"

Print the databasea data for all series that match the given term.  Example::

  $ animanager anime search yuusha
    id  name                                                                         type      ep_watched    ep_total  status    date_started    date_finished      animedb_id
  ----  ---------------------------------------------------------------------------  ------  ------------  ----------  --------  --------------  ---------------  ------------
   108  Densetsu no Yuusha no Densetsu                                               TV                24          24  complete                                           8086
   158  Hagure Yuusha no Estetica                                                    TV                12          12  complete                                          13161
   291  Maoyuu Maou Yuusha                                                           TV                12          12  complete                  2013-03-30              14833
   526  Yuusha ni Narenakatta Ore wa Shibushibu Shuushoku wo Ketsui Shimashita.      TV                12          12  complete  2013-10-08      2013-12-22              18677
   601  Yuusha ni Narenakatta Ore wa Shibushibu Shuushoku wo Ketsui Shimashita. OVA  OVA                1           1  complete  2014-03-14      2014-03-14              20545
   739  Yuuki Yuuna wa Yuusha de Aru                                                 TV                12          12  complete  2014-10-17      2014-12-26              25519
   856  Rokka no Yuusha                                                              TV                12          12  complete  2015-07-20      2015-09-20              28497

stats
^^^^^

::

   $ animanager anime stats

Print database statistics.  Example::

  $ animanager anime stats
  By status:
  - complete: 638
  - on hold: 0
  - dropped: 165
  - watching: 22
  - plan to watch: 61
  Total: 886
  Episodes watched: 8715

update
^^^^^^

::

   $ animanager anime update

Update series data in database.

This command queries MAL for updated series information to use to update
Animanager's database.

This command works on all series that do not have total episode count
information yet or have status "watching".

Information that may be updated is the name of the series and total episode
count.

.. _watch:

watch
^^^^^

::

   $ animanager anime watch

Watch anime.

This is Animanager's main command.  All you have to do is run this command and
watch anime; Animanager will update the database automagically.

It takes the list of registered series and matches it against all the files in
the current directory, presenting you with a menu of series to watch::

  0: (900) Hidamari Sketch x 365 (cur. 1, avail. 12)
  1: (877) Overlord (cur. 12, avail. 1)
  [-1]> 

After selecting a series, your selected video player will open automatically.
After it terminates, Animanager will prompt you to update your tracking
information and return to the initial menu.

To exit, use CTRL-C or equivalent command to send SIGTERM in your terminal.

watching
^^^^^^^^

::

   $ animanager anime watching

Print the databasea data for all currently watching series.

Manga commands
--------------

Animanager doesn't support manga yet.
