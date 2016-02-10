dnl -*- mode: web -*-
define(`TITLE', `Animanager')dnl
include(header.m4)dnl

<h1>Animanager</h1>

<p>Animanager is a command line anime and manga Swiss army knife.</p>

<section>
  <h2>Source code</h2>

  <a href="https://github.com/darkfeline/animanager">GitHub</a>
</section>

<section>
  <h2>Documentation</h2>

  <a href="http://animanager.readthedocs.org/">Read the Docs</a>
</section>

<section>
  <h2>News</h2>

  <section>
    <h3>2016-02-10</h3>

    <p>
      Animanager is currently undergoing a large rewrite.  The rewrite includes two
      major changes: moving from MyAnimeList to AniDB and rewriting Animanager's
      user interface.
    </p>

    <p>
      The first change, moving to AniDB, was motivated by the following factors:
    </p>

    <ul>
      <li>MyAnimeList is inaccurate and messy (no standard for how to deal with OVAs
        and specials, no standard for how to name series).</li>
      <li>AniDB contains more detailed information.</li>
    </ul>

    <p>
      This necessitates the following other changes:
    </p>

    <ul>
      <li>Database format will be changed completely to compensate for the extra
        information and different information format of AniDB.</li>
    </ul>

    <p>
      The second change, rewriting the user interface, involves moving to a
      shell-like command line interface, from the old process command based model.
      This was motivated by the following factors:
    </p>

    <ul>
      <li>Python's startup time, coupled with Animanager's own startup time, is very
        slow.</li>
      <li>By maintaining a CLI session, Animanager can keep an in-memory cache to
        speed up operations.</li>
      <li>Animanager's new database schema (motivated by the AniDB switch) is less
        efficient for certain operatings, necessitating caching.</li>
      <li>Animanager usage fits better with the CLI model.  Comparatively, the old
        model was better for scripting, which is a smaller use case for Animanager.
        The new model will still support scripting.</li>
    </ul>

    <p>
      Information about database migration will be included in the final 0.8
      release, which will be published once 0.9.0 is finalized.
    </p>
  </section>
</section>

include(footer.m4)dnl
