Setup
=========

DayZ license
-----------------

Prepare a Steam account with a DayZ license (i.e., own the game). From Steam's right-click menu for the game options, under ``Compatibility``, enable a Proton version ≥ ``6.8`` (or use Proton
Experimental for the latest version).

As of this writing, any recent version of Proton should work, and it is encouraged to use the most recent one.


API keys
-------------

You will need at a minimum a :ref:`Steam Web API key<steam_api>` in order to browse the server index.

.. _steam_api:

Steam Web API key
^^^^^^^^^^^^^^^^^^
**This step is required**.

Register for a `Steam Web API key <https://steamcommunity.com/dev/apikey>`_ (free) using your Steam account.

You will be asked for a unique URL for your app when registering. Typically, an API would send logs back to your URL in the form of callbacks.
However, since these API queries will be used for local consumption by a single user only, you can set a generic local identifier here like ``127.0.0.1`` to have the server discard them.

Once configured, you can insert this API key in the app when launching it for the first time.

.. note::
    If you are confused about this requirement, please refer to DZGUI Knowledge Base article :ref:`DZG-007<DZG-007>` for additional information.

Battlemetrics API key
^^^^^^^^^^^^^^^^^^^^^^
.. warning::

    This feature is no longer supported in DZGUI. Battlemetrics has switched to a paid service.

Choosing a Steam client
^^^^^^^^^^^^^^^^^^^^^^^^^
If multiple Steam clients are available (native Steam client/Flatpak Steam client), you will be
asked to choose which you want to use. Due to the way Steam's inter-process communication and internal URIs work,
if you choose one or the other, you should not run both clients simultaneously. This can lead DZGUI to send requests to the wrong one.

.. note::
   If you decide to switch to using a different Steam client with DZGUI, please uninstall fully (``dzgui -u``) and re-run the first time setup.


Next steps
--------------
Proceed to the next section for usage instructions.
