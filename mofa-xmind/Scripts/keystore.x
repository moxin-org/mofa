#
# Copyright (C) 2024 The XLang Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# <END>

from xlang_sqlite import sqlite

def create_db():
    pushWritepad(sqlite)
    # Create a KV.db database
    %USE ../config/keystore;
    %key_store_if = SELECT name FROM sqlite_master WHERE type='table' AND name='key_store';
    re = key_store_if.fetch()
    if re == None:
        %CREATE TABLE key_store (key TEXT PRIMARY KEY, value TEXT);
    popWritepad()

def query(key):
    pushWritepad(sqlite)
    %USE ../config/keystore;
    %kv_query = SELECT value FROM key_store WHERE key = ${key};
    results = kv_query.fetch()
    popWritepad()
    if results != None:
        return results[0]
    else:
        return None
    
def store(key, value):
    pushWritepad(sqlite)
    %USE ../config/keystore;
    %INSERT OR REPLACE INTO key_store (key, value) VALUES (${key}, ${value});
    popWritepad()

def remove(key):
    pushWritepad(sqlite)
    %USE ../config/keystore;
    %DELETE FROM key_store WHERE key = ${key};
    popWritepad()

def test():
    create_db()
    store('openai_key1', 'put key here')
    val = query('openai_key1')
    remove('openai_key1')
    val_again = query('openai_key1')
    print("Done!")

create_db()

# test()
