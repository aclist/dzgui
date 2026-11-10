# History of the project
This file collects notable milestones and events related to DZGUI, mainly around DZGUI as a framework and the history of development.
A chronological summary of features can be found in CHANGELOG.md.

## 2021
### 2021-12-03: DayZ adds support for Battleye over Proton
DayZ was among a handful of games with whitelisted anti-cheat support under Valve's emerging WINE-based Proton compatibility layer.
While adding anti-cheat compatibility at a technical level, this change did not actually allow the client to connect to servers running complex modlists.

Development of the precursor to DZGUI began at around this time.

### 2021-12-12: initial version of DZTUI is created
DZTUI, a Bash script and terminal user interface, was the precursor to DZGUI.
This was an initial attempt at bootstrapping the Steam client to handle mods correctly when launching DayZ.
Due to user interest, features continued to be added. This early tool is archived under the 'dztui' branch.

## 2022
### 2022-05-09: addition of zenity GUI and project name change (DZGUI)
With the introduction of the Steam Deck, more users wanted a graphical user interface
to interact with DZTUI. Being that DZTUI was purely a Bash script, a method of
drawing menus was needed, so the "zenity" package was used to create prefabricated dialogs.
While this met the minimum requirement to show prompts and selectable options, no rich customization was possible.

The introduction of zenity as a dependency marked the shift from "DZTUI" to "DZGUI".

Throughout 2022, the limits of zenity for DZGUI's purposes were tested, particularly in the context of SteamOS.
This led to the discovery of a number of bugs in zenity, GTK, and SteamOS, which were reported up to their respective channels.
While this was improving the SteamOS user experience, it started to become clear that a fully custom UI was needed.

This barebones version of DZGUI sufficed for some time, with the Bash script and some standalone Python modules doing the heavy lifting,
and this period served to surface a number of bugs and interesting interactions with the Steam client.

## 2023
### 2023-11-23: Python 3.10 dependency
Prior to this time, DZGUI open-endedly allowed you to use any Python version for its modules, without any significant handling for
the idiosyncrasies of different versions. A minimum requirement of Python 3.10 was thus instituted to normalize expected behavior.

Throughout 2023, various features related to server browsing were added, such as filters and more granular search parameters.

There were still a lot of unknowns at this time, so things were being resolved through trial and error.

## 2024
### 2024-01-31: DZGUI 5 API introduces GTK UI
Using zenity as a simple GUI had exposed some bugs and limitations in that package, particularly when trying to push huge lists of server records
into tables and sorting them in a performant manner.

Around this time it became clear that a more robust UI framework was needed. While keeping the original Bash script and Python modules for
background processing, PyGObject (GTK) was added to the project in order to ship a custom UI that could be designed from the ground up.

However, it should be noted that at this point, the DZGUI logic itself was still a (increasingly large) Bash script to which a GTK UI had been stitched on.
These were totally separate components, with UI actions on the GTK side triggering calls to Bash functions in an overly complex helper file.
The UI was basically a thin client around the old Bash logic, but this was still a far cry from an integrated application with proper signals and dedicated components.

Effectively, DZGUI 5 through 6 were a stepping stone that set the groundwork to go from DZGUI 4 (pure Bash script) to
DZGUI 7 (standalone Python application). Today, little of DZGUI 5's original logic remains outside of the basic UI grid.

### 2024-10-15: Frostline DLC released, widespread parsing problems
DayZ's first DLC introduced a new format for server responses that packed extra metadata into the A2S_RULES format.
Upon its release, all third-party DayZ launchers and server listing web sites were unable to parse the mod information being returned from Frostline servers.

For a period of two weeks, this remained unsolved and various attempts were made to understand the updated specification.

### 2024-10-30: DZGUI hotfix adds support for Frostline servers
DZGUI was the first third-party tool to fix parsing for Frostline servers and restore functionality.
This was a small milestone, because it meant DZGUI was evolving from a "dumb" launcher to a featureful tool
touching upon and improving all aspects of the end-to-end DayZ experience.

Particularly around this time, the sheer diversity of needs of modders, server operators, and players started to become clear.
Users had highly specific and diverse use cases for setting up their game environment, and requested a number of features to support that on
the DZGUI side.

## 2025
### 2025-01-17: DZGUI 6 API
With DZGUI 6, the difficult decision to enforce a Python 3.13 dependency was made.
While the previous dependency was Python 3.10+, it was deemed better to develop against and target identical versions.

However, due to the vagaries of managing Python environments on end-user systems, this change added unnecessary complexity and frustration.
Users had to properly set up virtual environments, install the relevant dependencies, and create a wrapper script to run this version, whereas
previous versions had essentially been point and click.

### 2025-10-23: DZGUI 7 API and the "Ship of Theseus"
It had become clear that the situation above was untenable and the legacy Bash script was unmaintainable given the project's enlarged scope.
The lack of a robust testing or typehinting framework made it difficult to diagnose rare bugs.

Shipping a standalone, turnkey application with zero or minimal dependencies was the most urgent priority.
DZGUI was still carrying around small bits and pieces of the old Bash script logic, so the decision was made to
refactor the application into a pure Python + GTK tool. This would effectively be a total rewrite of all logic,
only preserving the most minimal skeleton of the original UI layout as a reference.

Over the course of a year, a wholesale "Ship of Theseus" rewrite took place.
Nearly every component of DZGUI 6, both API and UI side, was taken apart and replaced.

A soft alpha and beta phase were used to iterate on this concept further. DZGUI 7 was increasingly recommended to users
as the preferred choice. This allowed for keeping the established userbase on the (relatively) stable DZGUI 6 spec, while building up
the new spec and making it available to more users as features were elaborated.

Through late 2025, several LLM-generated applications that recycled significant parts of DZGUI's code without the applicable GPL license were found.
The maintainers of those projects were advised to excise the offending segments or apply the necessary GPL licenses.

## 2026
### 2026-05-17: Switch to standalone releases
The DZGUI 7 beta starts shipping standalone glibc builds with an integrated setup wizard and installer.

DZGUI 6 had relied on "over the air" updates delivered via either a "stable" or "testing" branch
(archived respectively under the "dzgui" and "testing" branches). Effectively, the script would bootstrap itself and
fetch raw files directly from the repository. This was prone to problems because updates were monolithic, not giving
an easy escape hatch if the user needed to rollback in the event of a regression.

This was changed to atomic, tagged releases. In addition to updating directly through DZGUI, these prebuilt releases can be
downloaded manually as needed, and rollbacks are available for all prior versions under the DZGUI 7 specification.

### 2026-10-27: 500 tickets closed
The milestone of 500 tickets/PRs being closed was reached.

2026 was by far DZGUI's most intensive year by commits, perhaps suggesting the scope of the rewrite:

- 2021: 16
- 2022: 434
- 2023: 322
- 2024: 347
- 2025: 426
- 2026: 1300

DZGUI 7 is scheduled to release as a stable version within the year.
