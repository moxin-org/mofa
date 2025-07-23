import duckdb
from attrs import define, field
from typing import Dict, Any, List, Optional

@define
class LogEntry:
    node_name: str
    time: str                     # 可改为 datetime
    input_name: str
    input_value: Any = field(converter=str)
    output_name: str
    output_value: Any = field(converter=str)

@define
class DuckDBLogger:
    db_path: str = field(default='./logs/logs.duckdb')
    table_name: str = field(default='log_table')
    _con: duckdb.DuckDBPyConnection = field(init=False, repr=False)

    def __attrs_post_init__(self):
        self._con = duckdb.connect(self.db_path)
        self._con.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                node_name VARCHAR,
                time VARCHAR,
                input_name VARCHAR,
                input_value VARCHAR,
                output_name VARCHAR,
                output_value VARCHAR
            )
        """)  # 创建表仅执行一次，存在时不覆盖 :contentReference[oaicite:1]{index=1}

    def add_log_table_data(self, data: Dict[str, Any]) -> None:
        """接收 dict，插入一行记录。"""
        log = LogEntry(**data)
        self._con.execute(
            f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?)",
            (
                log.node_name,
                log.time,
                log.input_name,
                log.input_value,
                log.output_name,
                log.output_value
            )
        )

    def query(self, where: Optional[str] = None, params: Optional[List[Any]] = None) -> List[tuple]:
        """查询：可带 WHERE 条件与参数列表。"""
        sql = f"SELECT * FROM {self.table_name}"
        if where:
            sql += f" WHERE {where}"
        cur = self._con.execute(sql, params or [])
        return cur.fetchall()

    def update(self, set_clause: str, where: str, params: List[Any]) -> None:
        """更新：根据 set 和 where 条件进行更新。"""
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where}"
        self._con.execute(sql, params)

    def delete(self, where: str, params: List[Any]) -> None:
        """删除：根据 where 条件删除行。"""
        sql = f"DELETE FROM {self.table_name} WHERE {where}"
        self._con.execute(sql, params)

    def close(self):
        self._con.close()



if __name__ == "__main__":
    logger = DuckDBLogger(db_path='/Users/chenzi/project/zcbc/mofa/python/examples/hello_world/logs.duckdb', table_name='log_table')

    # # 新增一条记录
    # logger.add_log_table_data({
    #     'node_name': 'nodeA',
    #     'time': '2025-07-23T16:30:00',
    #     'input_name': 'temp',
    #     'input_value': 22.8,
    #     'output_name': 'status',
    #     'output_value': 'OK'
    # })

    # 查询所有
    print(logger.query())

    # 条件查询
    print(logger.query(where="input_name = ?", params=["temp"]))

    # 更新数据
    logger.update(
        set_clause="output_value = ?",
        where="node_name = ? AND input_name = ?",
        params=["BAD", "nodeA", "temp"]
    )

    # 删除记录
    logger.delete(
        where="node_name = ?",
        params=["nodeA"]
    )

    logger.close()
