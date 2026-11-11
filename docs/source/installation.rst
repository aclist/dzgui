Installation
==================

.. note::
   Version 6 of DZGUI 6 has been fully replaced with DZGUI 7.
   Users on existing DZGUI 6 installations should migrate to the DZGUI 7 build.

In order to make the first-time setup experience easier for end-users, DZGUI 7 no longer requires
the tool to be installed from source code into a working Python environment. All necessary dependencies and the
runtime environment are built-in.

Turnkey installer
------------------------

- Visit the project's `Releases page <https://github.com/aclist/dzgui/releases/latest>`_.
- Download the DZGUI archive from the top of the **Assets** list. This file will be labeled ``dzgui-<VERSION>-x86_64-unknown-linux-musl.tar.gz``.
- Extract the archive's contents.
- From a terminal, run the command ``./dzgui`` or double click on the extracted file in a file explorer.
- Once the setup wizard opens, follow the steps at the bottom of this page.

UI dependencies (Python and PyGObject)
---------------------------------------
On most major distributions, GObject introspection libraries should be available by default.

If you receive an error about a missing ``libgirepository-2.0`` dependency, install it via your system's package manager.

On Debian-based distributions (Ubuntu, etc.), this package is not explicitly installed on the system.
You can install it via the following set of commands:

.. code:: console

   sudo apt update
   sudo apt install libgirepository-2.0-0

Next steps
---------------
Proceed to the :doc:`setup` section for setup instructions.
