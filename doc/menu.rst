Selection menus
===============

This is Animanager's selection menu::

  0: (1852) Hidamari Sketch
  1: (2694) Hidamari no Ki
  2: (3165) Hidamari Sketch Specials
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  5: (7062) Hidamari Sketch x ☆☆☆
  6: (9563) Hidamari Sketch x ☆☆☆ Specials
  7: (11237) Hidamari Sketch x SP
  8: (11239) Hidamari Sketch x Honeycomb
  9: (17739) Hidamari Sketch: Sae Hiro Sotsugyou-hen
  10: (20391) Hidamari Sketch: Chou Hidamatsuri Special
  11: (26099) Hidamari no Ie
  12: (28911) Hidamari Sketch Recap
  13: (28913) Hidamari Sketch x 365 Recap
  14: (28915) Hidamari Sketch x ☆☆☆ Recap
  [-1]>

It is used in many places for making selections.  Simply enter the index of the
desired choice to select it.  The bracketed index indicates the default should
you press Enter without typing anything.

This index is a Python array index, so negative values are acceptable.  -1 means
the last choice, -2 means the second to last choice, and so on.

The selection menu also features simple commands.  You can view the built-in
help like so::

  [-1]> help

  Documented commands (type help <topic>):
  ========================================
  f  help  p  r

  Miscellaneous help topics:
  ==========================
  general

The ``f`` command lets you filter the selection menu::

  0: (1852) Hidamari Sketch
  1: (2694) Hidamari no Ki
  2: (3165) Hidamari Sketch Specials
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  5: (7062) Hidamari Sketch x ☆☆☆
  6: (9563) Hidamari Sketch x ☆☆☆ Specials
  7: (11237) Hidamari Sketch x SP
  8: (11239) Hidamari Sketch x Honeycomb
  9: (17739) Hidamari Sketch: Sae Hiro Sotsugyou-hen
  10: (20391) Hidamari Sketch: Chou Hidamatsuri Special
  11: (26099) Hidamari no Ie
  12: (28911) Hidamari Sketch Recap
  13: (28913) Hidamari Sketch x 365 Recap
  14: (28915) Hidamari Sketch x ☆☆☆ Recap
  [-1]> f sketch
  0: (1852) Hidamari Sketch
  2: (3165) Hidamari Sketch Specials
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  5: (7062) Hidamari Sketch x ☆☆☆
  6: (9563) Hidamari Sketch x ☆☆☆ Specials
  7: (11237) Hidamari Sketch x SP
  8: (11239) Hidamari Sketch x Honeycomb
  9: (17739) Hidamari Sketch: Sae Hiro Sotsugyou-hen
  10: (20391) Hidamari Sketch: Chou Hidamatsuri Special
  12: (28911) Hidamari Sketch Recap
  13: (28913) Hidamari Sketch x 365 Recap
  14: (28915) Hidamari Sketch x ☆☆☆ Recap
  [-1]> f 365
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  13: (28913) Hidamari Sketch x 365 Recap
  [-1]> 

The ``p`` command prints the current menu in case it is not on your screen and
you need to see it again::

  [-1]> p
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  13: (28913) Hidamari Sketch x 365 Recap
  [-1]> 

The ``r`` command resets all search filters::

  [-1]> r
  0: (1852) Hidamari Sketch
  1: (2694) Hidamari no Ki
  2: (3165) Hidamari Sketch Specials
  3: (3604) Hidamari Sketch x 365
  4: (6984) Hidamari Sketch x 365 Specials
  5: (7062) Hidamari Sketch x ☆☆☆
  6: (9563) Hidamari Sketch x ☆☆☆ Specials
  7: (11237) Hidamari Sketch x SP
  8: (11239) Hidamari Sketch x Honeycomb
  9: (17739) Hidamari Sketch: Sae Hiro Sotsugyou-hen
  10: (20391) Hidamari Sketch: Chou Hidamatsuri Special
  11: (26099) Hidamari no Ie
  12: (28911) Hidamari Sketch Recap
  13: (28913) Hidamari Sketch x 365 Recap
  14: (28915) Hidamari Sketch x ☆☆☆ Recap
  [-1]>


The ``q`` command lets you cancel or quit the current selection, only if it is
enabled for the current selection menu.  If quitting is enabled, a ``q`` will
appear in the prompt::

  [-1](q)>
