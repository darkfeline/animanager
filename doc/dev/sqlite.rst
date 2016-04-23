:mod:`animanager.sqlite` --- SQLite package
===========================================

:mod:`animanager.sqlite.db` --- SQLite database
-----------------------------------------------

.. automodule:: animanager.sqlite.db

.. autoclass:: SQLiteDB

   .. automethod:: connect

   .. automethod:: enable_foreign_keys
   .. automethod:: disable_foreign_keys
   .. automethod:: check_foreign_keys

   .. attribute:: version

      :class:`SQLiteDB` provides access to SQLite's database user version PRAGMA
      via the :attr:`version` property.

      >>> db = SQLite(':memory:')
      >>> db.version = 3
      >>> db.version
      3

.. autoexception:: DatabaseError
   :show-inheritance:

.. autoexception:: SQLiteError
   :show-inheritance:

:mod:`animanager.sqlite.utils` --- SQLite utilities
---------------------------------------------------

.. automodule:: animanager.sqlite.utils
   :members:

:mod:`animanager.sqlite.migrations` --- Simple migrations
---------------------------------------------------------

.. automodule:: animanager.sqlite.migrations

.. autoclass:: MigrationManager

   .. automethod:: register
   .. automethod:: migration

   .. automethod:: needs_migration
   .. automethod:: check_version
   .. automethod:: migrate

.. autoclass:: Migration(from_ver, to_ver, migrate_func)
   :members:

.. autoexception:: MigrationError
   :show-inheritance:

.. autoexception:: VersionError
   :show-inheritance:

:mod:`animanager.sqlite.cachetable` --- Temporary cache tables
--------------------------------------------------------------

.. automodule:: animanager.sqlite.cachetable

.. autoclass:: CacheTableManager

   .. automethod:: setup
   .. automethod:: cleanup

.. autoclass:: CacheTable
   :members:
