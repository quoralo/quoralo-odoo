# Part of Quoralo. See LICENSE file for full copyright and licensing details.
import re

from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

WIDGET_URL = "https://www.quoralo.com/api/widget/"

# An agent ID found inside a pasted chat link or script tag:
#   https://www.quoralo.com/c/my-agent
#   <script data-agent-ia src="https://www.quoralo.com/api/widget/my-agent" async></script>
_AGENT_IN_URL = re.compile(r"/(?:c|api/widget)/([a-z0-9-]{1,80})", re.IGNORECASE)
# A bare agent ID.
_AGENT_ID = re.compile(r"^[a-z0-9-]{1,80}$", re.IGNORECASE)


def extract_agent_id(value):
    """Return the Quoralo agent ID contained in ``value``.

    ``value`` may be the agent ID itself, the agent's chat link or the whole
    script tag copied from the Quoralo dashboard. Returns ``False`` when
    ``value`` is empty and ``None`` when no valid agent ID can be found.
    """
    value = (value or "").strip()
    if not value:
        return False
    match = _AGENT_IN_URL.search(value)
    if match:
        return match.group(1)
    if _AGENT_ID.match(value):
        return value
    return None


class Website(models.Model):
    _inherit = "website"

    quoralo_agent_id = fields.Char(
        string="Quoralo Agent",
        help="The ID of your Quoralo agent. You can also paste its chat link "
             "or the script tag from the Quoralo dashboard (Partager > "
             "Widget pour votre site).",
    )

    @api.model
    def _quoralo_normalize_vals(self, vals):
        if "quoralo_agent_id" in vals:
            agent = extract_agent_id(vals["quoralo_agent_id"])
            if agent is None:
                raise ValidationError(_(
                    "This is not a valid Quoralo agent. Paste the agent ID, "
                    "its chat link or the script tag from the Quoralo "
                    "dashboard (Partager > Widget pour votre site)."
                ))
            vals["quoralo_agent_id"] = agent
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._quoralo_normalize_vals(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._quoralo_normalize_vals(vals)
        return super().write(vals)

    def _quoralo_widget_html(self):
        """Script tag that loads the Quoralo chat bubble on this website."""
        self.ensure_one()
        agent = self.quoralo_agent_id
        if not agent or not _AGENT_ID.match(agent):
            return ""
        script = Markup(
            '<script data-agent-ia="" src="%s" async="async"></script>'
        ) % (WIDGET_URL + agent)
        # Since Odoo 19, the website controls third-party scripts when the
        # cookie bar blocks third-party domains: treat the chat bubble exactly
        # like the code injected in the website editor.
        control = getattr(self, "_control_third_party_trackers_in_html", None)
        return control(script) if control else script
