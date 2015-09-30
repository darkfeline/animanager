Quickstart
==========

This guide provides an example of basic Animanager usage.

Adding a series
---------------

First, add a series to track::

  $ animanager anime add "hidamari sketch"

Animanager will search MAL for series::

  0: (1852) Hidamari Sketch
  1: (3165) Hidamari Sketch Specials
  2: (3604) Hidamari Sketch x 365
  3: (6984) Hidamari Sketch x 365 Specials
  4: (7062) Hidamari Sketch x ☆☆☆
  5: (9563) Hidamari Sketch x ☆☆☆ Specials
  6: (11237) Hidamari Sketch x SP
  7: (11239) Hidamari Sketch x Honeycomb
  8: (17739) Hidamari Sketch: Sae Hiro Sotsugyou-hen
  9: (20391) Hidamari Sketch: Chou Hidamatsuri Special
  10: (28911) Hidamari Sketch Recap
  11: (28913) Hidamari Sketch x 365 Recap
  12: (28915) Hidamari Sketch x ☆☆☆ Recap
  [-1]> 

This is Animanager's selection interface, which you will see a lot.  The
``[-1]`` means the default choice is -1, or the last item (in this case, 12).
Another common default is ``[0]``, which indicates the first item.  You can pick
an item by typing its number and pressing Enter, or simply press Enter to pick
the default choice.

Next, choose the initial status::

  0: plan to watch
  1: watching
  2: complete
  [0]>

For this guide, here we pick ``watching``.

Searching your database
-----------------------

We can search our database to check our information::

  $ animanager anime search hidamari
    id  name                      type       ep_watched    ep_total  status      date_started  date_finished      animedb_id
  ----  ------------------------  -------  ------------  ----------  --------  --------------  ---------------  ------------
     1  Hidamari Sketch x 365     TV                  0          13  watching                                           3604

This shows all of the information Animanager tracks.

Watching shows
--------------

Navigate to the directory where your files are::

  $ cd anime
  $ ls
  [SpoonSubs] Hidamari Sketch x365 - 01 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 02 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 03 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 04 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 05 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 06 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 06 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 07 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 08 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 09 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 09 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 10 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 11 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 12 (DVD).mkv
  [SpoonSubs] Hidamari Sketch x365 - 13 (DVD).mkv

Now we can use Animanager to automatically watch our series::

  $ animanager anime watch
  0: (900) Hidamari Sketch x 365 (cur. 0, avail. 13)
  [-1]> 

Animanager presents the choices for series to watch.  Right now we only have one
series, but we can add multiple and they will appear here provided that episodes
are available.

We see that we have currently watched no episodes and have 13 available to
watch.

Press Enter to select the default and only choice.  Your configured video player
will start and you can watch the episode.

After the episode is over, the video player will close (provided that you are
using an ``mpv``-like player)::

  Bump? [Y/n]

Animanager will prompt whether you want to bump your currently watched episode
count.  The default is yes, so just hit Enter.  Alternatively, you can type
``n`` to keep your currently watched episode at 0.

Next, Animanager will prompt whether you want to delete the file.  Again, the
default is yes::

  Delete? [Y/n]

Now we're back at the menu::

  0: (900) Hidamari Sketch x 365 (cur. 1, avail. 12)
  [-1]> 

You can keep watching, or quit using CTRL-C.  We quit to continue the tutorial.

Let's check our database::

  $ animanager anime search hidamari
    id  name                      type       ep_watched    ep_total  status      date_started  date_finished      animedb_id
  ----  ------------------------  -------  ------------  ----------  --------  --------------  ---------------  ------------
     1  Hidamari Sketch x 365     TV                  1          13  watching  2015-09-29                               3604

The episode count has been updated automatically, and the start date has been
set as well.

View stats
----------

Just for fun, Animanager also lets you view basic statistics::

  $ animanager anime stats
  By status:
  - complete: 638
  - on hold: 0
  - dropped: 165
  - watching: 22
  - plan to watch: 61
  Total: 886
  Episodes watched: 8715

Other features
--------------

Here's an overview of some of Animanager's features:

- Version detection.  Animanager will delete older versions of an episode and
  watch the latest version.
- Date tracking of when you started and finished a series.
- Updating series data via MAL (for example, if the total number of episodes for
  a series changes).

I highly recommend you read through all of the documentation, which contains
more information about Animanager's features.
