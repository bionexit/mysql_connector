import pymysql
from pymysql.err import MySQLError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from typing import Any, Generator
import json

class MySQLConnectorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 获取凭据
            host = tool_parameters["mysql_host"]
            user = tool_parameters["mysql_user"]
            password = tool_parameters["mysql_password"]
            database = tool_parameters["mysql_database"]
            port = tool_parameters["mysql_port"]

            # 连接 MySQL 数据库
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,  # 使用端口号
                cursorclass=pymysql.cursors.DictCursor
            )

            if connection.open:
                cursor = connection.cursor()
                query = tool_parameters["query"]
                cursor.execute(query)
                results = cursor.fetchall()
                if len(results) > 0:
                    output = {"data":results,"length":len(results)}
                    yield self.create_json_message(output)
                else:
                    yield self.create_text_message("Query returned no results")
        except MySQLError as e:
            yield self.create_text_message(f"Database connection error: {e}")
        except Exception as e:
            yield self.create_text_message(f"Dify error: {e}")
        finally:
            if connection.open:
                cursor.close()
                connection.close()