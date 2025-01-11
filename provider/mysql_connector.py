from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.mysql_connector import MySQLConnectorTool

class MySQLProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # for _ in MySQLConnectorTool.from_credentials(credentials).invoke(
            #     tool_parameters={"query": "SELECT 1"},
            # ):
            pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))