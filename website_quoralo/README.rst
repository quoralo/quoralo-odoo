=========================
Quoralo AI Chat Agent
=========================

Adds the Quoralo AI chat agent to your Odoo website. The agent answers your
visitors at any hour, using only the information you gave it in your Quoralo
dashboard, and says when it does not know.

Features
========

* A **Quoralo AI chat agent** setting in *Website > Configuration > Settings*:
  no code to paste in the website editor.
* One agent per website (multi-website).
* The chat bubble is added at the end of every public page, and hidden while a
  page is being edited or translated.
* From Odoo 19, the bubble is handled like the code injected in the website
  editor, so the cookie bar settings apply to it in the same way.

Configuration
=============

#. In your Quoralo dashboard (in French), open your agent, click *Partager*
   and copy the script tag under *Widget pour votre site*. The agent ID or the
   agent's chat link also work.
#. In Odoo, go to *Website > Configuration > Settings*, find
   *Quoralo AI chat agent*, paste it and save. Only the agent ID is kept.
#. Open your website: the chat bubble appears on every page. Clear the field
   to remove it.

A Quoralo account and an agent are required.

Compatibility
=============

Odoo 18.0, 19.0 and 20.0 (Community and Enterprise). Odoo Online databases
cannot install third-party modules: there, paste the Quoralo script tag in the
website editor (Theme > Advanced > Code injection, ``</body>`` field).

Data and privacy
================

The chat bubble is loaded from Quoralo and your visitors' messages are
processed by Quoralo. Before their first message, visitors are told that they
are talking to an AI and how their messages are used. The module stores
nothing in Odoo except the agent ID.

Support
=======

contact@quoralo.com

License
=======

LGPL-3
