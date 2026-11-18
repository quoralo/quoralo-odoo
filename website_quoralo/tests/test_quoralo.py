# Part of Quoralo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import ValidationError
from odoo.tests import HttpCase, TransactionCase, tagged

from odoo.addons.website_quoralo.models.website import extract_agent_id


def default_website(env):
    """The website a request on localhost is served by (no xmlid in Odoo 20)."""
    website = env["website"].search([], limit=1)
    assert website, "no website in the database"
    return website


SCRIPT_TAG = (
    '<script data-agent-ia src="https://www.quoralo.com/api/widget/my-agent" '
    "async></script>"
)


@tagged("post_install", "-at_install")
class TestQuoraloAgentId(TransactionCase):

    def test_extract_agent_id(self):
        self.assertEqual(extract_agent_id("my-agent"), "my-agent")
        self.assertEqual(extract_agent_id("  my-agent  "), "my-agent")
        self.assertEqual(extract_agent_id(SCRIPT_TAG), "my-agent")
        self.assertEqual(
            extract_agent_id("https://www.quoralo.com/c/cmwhsogxy00ebjp0841825d5m"),
            "cmwhsogxy00ebjp0841825d5m",
        )
        self.assertFalse(extract_agent_id(""))
        self.assertFalse(extract_agent_id(None))
        self.assertIsNone(extract_agent_id("not an agent!"))
        self.assertIsNone(extract_agent_id("https://example.com/page"))
        self.assertIsNone(extract_agent_id("a" * 81))

    def test_website_field_is_normalized(self):
        website = default_website(self.env)
        website.quoralo_agent_id = SCRIPT_TAG
        self.assertEqual(website.quoralo_agent_id, "my-agent")
        website.quoralo_agent_id = ""
        self.assertFalse(website.quoralo_agent_id)

    def test_invalid_value_is_refused(self):
        website = default_website(self.env)
        with self.assertRaises(ValidationError):
            website.quoralo_agent_id = "<script>alert(1)</script>"

    def test_settings_write_through(self):
        website = default_website(self.env)
        settings = self.env["res.config.settings"].create({
            "website_id": website.id,
            "quoralo_agent_id": "https://www.quoralo.com/c/my-agent",
        })
        settings.execute()
        self.assertEqual(website.quoralo_agent_id, "my-agent")

    def test_widget_html(self):
        website = default_website(self.env)
        website.quoralo_agent_id = "my-agent"
        html = str(website._quoralo_widget_html())
        self.assertIn('src="https://www.quoralo.com/api/widget/my-agent"', html)
        self.assertIn("data-agent-ia", html)
        self.assertIn("async", html)
        website.quoralo_agent_id = False
        self.assertEqual(website._quoralo_widget_html(), "")


@tagged("post_install", "-at_install")
class TestQuoraloWidgetOnPages(HttpCase):

    def test_no_bubble_without_agent(self):
        default_website(self.env).quoralo_agent_id = False
        # A distinct query string in each test avoids any cached copy of the page.
        response = self.url_open("/?quoralo_test=without")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("data-agent-ia", response.text)

    def test_bubble_on_public_pages(self):
        default_website(self.env).quoralo_agent_id = "my-agent"
        response = self.url_open("/?quoralo_test=with")
        self.assertEqual(response.status_code, 200)
        self.assertIn("https://www.quoralo.com/api/widget/my-agent", response.text)
        self.assertEqual(response.text.count("data-agent-ia"), 1)
        # The bubble goes at the end of the page, inside <body>.
        body = response.text.split("<body", 1)[1]
        self.assertIn("data-agent-ia", body)
