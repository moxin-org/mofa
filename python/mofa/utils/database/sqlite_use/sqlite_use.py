import sqlite3
import os
from os import mkdir

from attrs import define, field
from typing import Dict, Any, List, Optional
from datetime import datetime # 假设您使用datetime对象

from mofa.utils.files.dir import make_dir


@define
class LogEntry:
    node_name: str
    time: str
    input_name: str
    input_value: Any = field(converter=str)
    output_name: str
    output_value: Any = field(converter=str)

@define
class SQLiteLogger:
    db_path: str = field(default='./logs/logs.sqlite')
    table_name: str = field(default='log_table')
    _con: sqlite3.Connection = field(init=False, repr=False)

    def __attrs_post_init__(self):
        if self.db_path == '':
            self.db_path = 'logs.sqlite'
        print('这个是 db  path : ',self.db_path)
        make_dir(self.db_path)
        self._con = sqlite3.connect(self.db_path)
        # 开启 WAL 模式，大大改善并发读写性能
        self._con.execute("PRAGMA journal_mode=WAL;")
        self._con.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                node_name TEXT,
                time TEXT,
                input_name TEXT,
                input_value TEXT,
                output_name TEXT,
                output_value TEXT
            )
        """)
        self._con.commit() # 提交 CREATE TABLE 事务

    def add_log_table_data(self, data: Dict[str, Any]) -> None:
        log = LogEntry(**data)
        # 每次写入都使用一个事务，确保原子性
        try:
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
            self._con.commit()
        except sqlite3.OperationalError as e:
            # 这通常意味着数据库被锁住，例如另一个进程正在写入
            print(f"SQLite Write Error (OperationalError): {e}. Retrying or handling...")
            self._con.rollback() # 回滚当前事务
            # 在实际应用中，您可能需要实现一个重试机制或者将日志推送到一个内存队列稍后写入
        except Exception as e:
            print(f"SQLite Write Error: {e}")
            self._con.rollback()


    def query(self, where: Optional[str] = None, params: Optional[List[Any]] = None) -> List[tuple]:
        sql = f"SELECT * FROM {self.table_name}"
        if where:
            sql += f" WHERE {where}"
        cur = self._con.execute(sql, params or [])
        return cur.fetchall()

    def update(self, set_clause: str, where: str, params: List[Any]) -> None:
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where}"
        self._con.execute(sql, params)
        self._con.commit()

    def delete(self, where: str, params: List[Any]) -> None:
        sql = f"DELETE FROM {self.table_name} WHERE {where}"
        self._con.execute(sql, params)
        self._con.commit()

    def close(self):
        self._con.close()

# MofaAgent 中的使用方式
# 在 MofaAgent 的 __attrs_post_init__ 中初始化：
# self.log_db = SQLiteLogger(db_path=os.getenv('LOG_DB_PATH', './logs.sqlite'), table_name=os.getenv('LOG_DB_TABLE_NAME', 'log_table'))
#
# 在 write_log 方法中：
# if log_data is not None:
#     # 每次写入都直接使用已经初始化好的 self.log_db 实例
#     self.log_db.add_log_table_data(data=log_data)
#
# 在 MofaAgent 进程结束前调用 self.log_db.close()