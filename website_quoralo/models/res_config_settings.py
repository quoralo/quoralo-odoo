# Part of Quoralo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quoralo_agent_id = fields.Char(
        related="website_id.quoralo_agent_id",
        readonly=False,
    )
