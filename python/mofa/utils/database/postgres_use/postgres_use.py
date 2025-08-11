import psycopg2
from psycopg2 import sql
from attrs import define, field
from typing import Dict, Any, Optional
import os
from datetime import datetime


@define
class LogEntry:
    node_name: str
    time: str  # 保持字符串，或改为 datetime
    input_name: str
    input_value: Any = field(converter=str)
    output_name: str
    output_value: Any = field(converter=str)


@define
class PostgreSQLDBLogger:
    host: str = field(default=os.getenv('PG_HOST', 'localhost'))
    port: int = field(default=int(os.getenv('PG_PORT', 5433)))
    database: str = field(default=os.getenv('PG_DATABASE', 'mofa_logs'))
    user: str = field(default=os.getenv('PG_USER', 'mofa_user'))
    password: str = field(default=os.getenv('PG_PASSWORD', 'mofa_pwd'))  # 确保这里使用实际密码
    table_name: str = field(default='log_table')

    _con: psycopg2.extensions.connection = field(init=False, repr=False)

    def __attrs_post_init__(self):
        try:
            self._con = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self._con.autocommit = True
            print(f"Connected to PostgreSQL database: {self.database} at {self.host}:{self.port}")

            # 创建表 (如果不存在)
            with self._con.cursor() as cur:
                cur.execute(sql.SQL("""
                                    CREATE TABLE IF NOT EXISTS {}
                                    (
                                        id
                                        SERIAL
                                        PRIMARY
                                        KEY,               -- 添加主键，方便管理
                                        node_name
                                        TEXT,              -- 更改为 TEXT 类型
                                        log_time
                                        TIMESTAMP
                                        WITH
                                        TIME
                                        ZONE
                                        DEFAULT
                                        CURRENT_TIMESTAMP, -- 使用实际时间戳类型
                                        input_name
                                        TEXT,              -- 更改为 TEXT 类型
                                        input_value
                                        TEXT,              -- 保持 TEXT 类型
                                        output_name
                                        TEXT,              -- 更改为 TEXT 类型
                                        output_value
                                        TEXT               -- 保持 TEXT 类型
                                    )
                                    """).format(sql.Identifier(self.table_name)))

        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL or creating table: {e}")
            raise  # 抛出异常，让上层知道连接失败

    def add_log_table_data(self, data: Dict[str, Any]) -> None:
        """接收 dict，插入一行记录。"""
        log = LogEntry(**data)
        try:
            with self._con.cursor() as cur:
                cur.execute(
                    sql.SQL(
                        "INSERT INTO {} (node_name, log_time, input_name, input_value, output_name, output_value) VALUES (%s, %s, %s, %s, %s, %s)").format(
                        sql.Identifier(self.table_name)
                    ),
                    (
                        log.node_name,
                        datetime.fromisoformat(log.time) if isinstance(log.time, str) else log.time,
                        log.input_name,
                        log.input_value,
                        log.output_name,
                        log.output_value
                    )
                )
        except psycopg2.Error as e:
            print(f"Error inserting log data: {e}")

    def query(self, where: Optional[str] = None, params: Optional[list] = None) -> list:
        """查询：可带 WHERE 条件与参数列表。"""
        sql_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name))
        if where:
            sql_query = sql.SQL("SELECT * FROM {} WHERE {}").format(sql.Identifier(self.table_name), sql.SQL(where))

        with self._con.cursor() as cur:
            cur.execute(sql_query, params)
            return cur.fetchall()

    def close(self):
        """关闭数据库连接。"""
        if self._con:
            self._con.close()
            print("PostgreSQL connection closed.")


# 可以在此处添加一个简单的测试，但通常会在MofaAgent中调用
if __name__ == "__main__":
    # 确保设置了环境变量，或者修改PostgreSQLDBLogger的默认值以匹配你的DB
    # os.environ['PG_HOST'] = 'localhost'
    # os.environ['PG_PORT'] = '5433' # 如果你修改了 Docker Compose 的端口映射
    # os.environ['PG_DATABASE'] = 'mofa_logs'
    # os.environ['PG_USER'] = 'mofa_user'
    # os.environ['PG_PASSWORD'] = 'mofa_pwd'

    logger = None
    try:
        logger = PostgreSQLDBLogger()
        print("Logger initialized.")

        # 新增一条记录
        logger.add_log_table_data({
            'node_name': 'test_node_A_with_long_name_that_exceeds_varchar255_limit_if_it_were_still_varchar',
            'time': datetime.now().isoformat(),
            'input_name': 'test_input_with_long_description_for_analysis_purposes',
            'input_value': "This is a very long input value that could contain JSON, XML, or any other large text data that needs to be stored without truncation. It demonstrates the use of the TEXT data type in PostgreSQL, which can handle strings of virtually unlimited length (up to 1 GB). This is crucial for logging arbitrary data structures or large messages from various nodes in a distributed system like Dora-RS. The TEXT type is highly recommended for fields where the maximum length is unknown or can vary significantly.",
            'output_name': 'test_output_result_summary',
            'output_value': "This is the corresponding output value, also potentially very long. For example, it could be a serialized object, a large error stack trace, or a detailed report generated by the node. Using TEXT ensures that no information is lost due to arbitrary length limits. The flexibility of TEXT makes the logging system robust against changes in data structure or verbosity."
        })
        print("Added a log entry.")

        # 查询所有记录
        print("\nAll logs:")
        for row in logger.query():
            print(row)

        # 条件查询
        print("\nLogs for 'test_node_A_with_long_name_that_exceeds_varchar255_limit_if_it_were_still_varchar':")
        for row in logger.query(where="node_name = %s", params=[
            "test_node_A_with_long_name_that_exceeds_varchar255_limit_if_it_were_still_varchar"]):
            print(row)

    except Exception as e:
        print(f"An error occurred during test: {e}")
    finally:
        if logger:
            logger.close()
