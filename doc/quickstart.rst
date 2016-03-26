Quickstart guide
================

This guide will help you start using Animanager to watch and track your anime.
However, as Animanager is geared toward advanced users, reading the rest of the
documentation is highly recommended.

Installation
------------

Install Animanager from PyPi::

  $ pip3 install --user animanager

Configuration
-------------

Copy ``config.ini`` to ``~/.animanager/config.ini`` and edit it as necessary.

In particular, you will want to set ``watchdir`` to the directory where you keep
your anime.

Running Animanager
------------------

Start Animanager::

  $ animanager anime
  INFO:animanager.animedb:Migration needed, backing up database
  INFO:animanager.animedb:Migrating database
  INFO:animanager.db.migrations:Migrating database from 0 to 1
  INFO:animanager.db.migrations:Migrating database from 1 to 2
  Animanager 0.10.0
  Copyright (C) 2015-2016  Allen Li

  This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
  This is free software, and you are welcome to redistribute it
  under certain conditions; type "gpl c" for details.
  A>

As you don't have a database yet, Animanager will create one automatically.

Getting help
------------

Animanager's command line provides basic help functionality::

  A> help

  Documented commands (type help <topic>):
  ========================================
  a         asearch  bump         gpl         quit      s       unregister
  add       ash      delete_rule  help        r         search  ur
  add_rule  ashow    f            purgecache  register  sh      w
  as        b        fetch        q           rules     show    watch

  A> help a
  Alias for add
  A> help add
  usage: add [-h] aid

  Add an anime or update an existing anime.

  positional arguments:
    aid

  optional arguments:
    -h, --help  show this help message and exit

Adding a series
---------------

Search AniDB for a series to add::

  A> asearch madoka
    #    AID  Title
  ---  -----  -----------------------------------------
    1   8069  Mahou Shoujo Madoka Magica
    2   8778  Gekijouban Mahou Shoujo Madoka Magica
    3  11793  Mahou Shoujo Madoka Magica: Concept Movie
  A> add 1

Checking anime status
---------------------

Check the status of an anime::

  A> search madoka
    #    AID  Title                       Type       Episodes    Complete    Available
  ---  -----  --------------------------  ---------  ----------  ----------  -----------
    1   8069  Mahou Shoujo Madoka Magica  TV Series  0/12
  A> show 1
  AID: 8069
  Title: Mahou Shoujo Madoka Magica
  Type: TV Series
  Episodes: 0/12
  Start date: 2011-01-07
  End date: 2011-04-22
  Complete: no

  A> show 1 -e
  AID: 8069
  Title: Mahou Shoujo Madoka Magica
  Type: TV Series
  Episodes: 0/12
  Start date: 2011-01-07
  End date: 2011-04-22
  Complete: no

  Number    Title                            min  Watched
  --------  -----------------------------  -----  ---------
  1         夢の中で会った, ような.....       25
  2         それはとっても嬉しいなって        25
  3         もう何も恐くない                  25
  4         奇跡も, 魔法も, あるんだよ        25
  5         後悔なんて, あるわけない          25
  6         こんなの絶対おかしいよ            25
  7         本当の気持ちと向き合えますか?     25
  8         あたしって, ほんとバカ            25
  9         そんなの, あたしが許さない        25
  10        もう誰にも頼らない                25
  11        最後に残った道しるべ              25
  12        わたしの, 最高の友達              25
  C1        Opening                            2
  C2        Ending 1                           2
  C3        Ending 2                           2
  C4        Ending 3                           2
  T1        CM動画1                            1
  T2        CM動画2                            1
  T3        CM動画3                            1
  T4        CM動画4                            1
  T5        CM動画5                            1
  T6        CM動画6                            1
  T7        CM動画7                            1
  T8        CM動画8                            1
  T9        CM動画9                            1
  T10       CM動画10                           1
  T11       BD CM 1                            1
  T12       BD CM 2                            1

Bumping watched episode code
----------------------------

You can bump the episode count manually::

  A> bump 1
  A> show 1
  AID: 8069
  Title: Mahou Shoujo Madoka Magica
  Type: TV Series
  Episodes: 1/12
  Start date: 2011-01-07
  End date: 2011-04-22
  Complete: no

Automatic watching
------------------

However, Animanager is designed for smarter watching than that!

You should have configured Animanager with the directory where you store your
anime.

First, set up a pattern for Animanager to find files for an anime.  Animanager's
default pattern works well::

  A> register 1
  A> show 1
  AID: 8069
  Title: Mahou Shoujo Madoka Magica
  Type: TV Series
  Episodes: 1/12
  Start date: 2011-01-07
  End date: 2011-04-22
  Complete: no
  Watching regexp: Mahou.*Shoujo.*Madoka.*Magica.*?\b(?P<ep>[0-9]+)(v[0-9]+)?

Or you can specify manually::

  A> register 1 madoka.*(?P<ep>[0-9]+).mkv
  A> show 1
  AID: 8069
  Title: Mahou Shoujo Madoka Magica
  Type: TV Series
  Episodes: 1/12
  Start date: 2011-01-07
  End date: 2011-04-22
  Complete: no
  Watching regexp: madoka.*(?P<ep>[0-9]+).mkv

Let's assume you have the next few episodes available in your anime directory
(``Mahou Shoujo Madoka Magica 02.mkv``)::

  A> search madoka
    #    AID  Title                       Type       Episodes    Complete    Available
  ---  -----  --------------------------  ---------  ----------  ----------  -----------
    1   8069  Mahou Shoujo Madoka Magica  TV Series  1/12                    2,3,4
  A> watch 1

Animanager will start your configured video player and you can start watching
immediately.

After the video player exits, you will be prompted to bump the episode count.
