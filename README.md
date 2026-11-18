# Quoralo for Odoo

Odoo module that adds the [Quoralo](https://www.quoralo.com) AI chat agent to an Odoo website.

The agent answers visitors at any hour, using only the information the business gave it, and says when it does not know. This module adds a **Quoralo AI chat agent** setting in *Website > Configuration > Settings*: paste the agent ID, its chat link or the script tag from the Quoralo dashboard, and the chat bubble appears on every public page.

| Branch | Odoo version |
|---|---|
| `18.0` | Odoo 18 |
| `19.0` | Odoo 19 |
| `20.0` | Odoo 20 |

The module is in the [`website_quoralo`](website_quoralo) folder. See its [README](website_quoralo/README.rst) for the setup steps.

## Tests

Each branch installs the module in the official Odoo Docker image of its version and runs the module's tests (GitHub Actions, `.github/workflows/tests.yml`).

## Other platforms

Quoralo also has official extensions for WordPress, PrestaShop, Joomla and Drupal, and step-by-step guides for 15 platforms: https://www.quoralo.com/integrations

## License

LGPL-3.0. See [LICENSE](LICENSE).

## Contact

contact@quoralo.com
