import asyncio
import aiomysql
from ast import literal_eval


# insert 전용
async def test_example_execute(loop):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                      user='root', password='root1234', db='container_weight', loop=loop)
        cur = await conn.cursor()

        query = "UPDATE member SET drive_cnt = '1233' WHERE (index = '3');"
        result = await cur.execute(query)
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


@asyncio.coroutine
def test_example(loop):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='container_weight',
                                       loop=loop)

    cur = yield from conn.cursor()
    yield from cur.execute("UPDATE ")
    r = yield from cur.fetchall()
    for i in r:
        print(i[1], end=" ")
    print(" ")

    yield from cur.close()
    conn.close()

    return r


@asyncio.coroutine
def query_operator(loop):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                       db='container_weight', loop=loop)
    cursor = yield from conn.cursor(aiomysql.DictCursor)

    query = "select * from container;"
    yield from cursor.execute(query)

    tuple = yield from cursor.fetchall()
    conn.close()
    return tuple


# 4번 요청에서 사용하는 함수
# 새로운 컨테이너 아이디를 만들기 위해 사용
@asyncio.coroutine
def get_last_container_idx(loop):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                       db='container_weight', loop=loop)
    cursor = yield from conn.cursor(aiomysql.DictCursor)

    query = "select max(idx) from container;"
    yield from cursor.execute(query)

    tuple = yield from cursor.fetchall()
    conn.close()

    return tuple


# 4번 요청에서 사용하는 함수
# 새로운 컨테이너 삽입
async def insert_new_container(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                      user='root', password='root1234', db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)

        new_container_idx = data_dict['idx']
        current_container_key = data_dict['container_key']

        query = "INSERT INTO container(idx, container_key) VALUES (" + "'" + new_container_idx + "'" + "," + "'" + current_container_key + "');"
        result = await cur.execute(query)
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 4번 요청에서 사용하는 함수
# 테이블 새로 생성하는 함수
# 테이블 이름은 컨테이너 아이디로 생성함
async def create_table_function(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                      db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)
        table_id = "CONT" + str(data_dict['table_id'])

        # query example
        # CREATE TABLE dept (dept_no INT(11) unsigned NOT NULL, dept_name VARCHAR(32) NOT NULL, PRIMARY KEY (dept_no) );
        await cur.execute(
            """CREATE TABLE """ + table_id + """(object_id int AUTO_INCREMENT, object_weight VARCHAR(255), PRIMARY KEY (object_id));""")
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 6번 요청에서 사용하는 함수
# 해시값을 토대로 id를 찾아오는 함수
@asyncio.coroutine
def find_id_from_hash(loop, data):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                       db='container_weight', loop=loop)
    cursor = yield from conn.cursor(aiomysql.DictCursor)

    data_dict = literal_eval(data)
    table_id = str(data_dict['target_container'])

    query = "SELECT idx FROM container WHERE container_key =" + "'" + table_id + "'" + ";"
    yield from cursor.execute(query)

    tuple = yield from cursor.fetchall()
    conn.close()

    return tuple


# 6번 요청에서 사용하는 함수
# 테이블 삭제하는 함수
async def delete_target_container(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                      db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)
        table_id = "CONT" + str(data_dict['target_container_name'])

        # query example
        await cur.execute("DROP TABLE " + table_id + ";")
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 6번 요청에서 사용하는 함수
# 컨테이너의 칼럼을 삭제하는 함수
async def delete_target_container_column(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                      db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)
        table_id = str(data_dict['target_container_idx'])

        # query example
        await cur.execute("DELETE FROM container WHERE idx = " + "'" + table_id + "';")
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 8번 요청에서 사용하는 함수
# 해당 컨테이너에 데이터를 삽입함
async def insert_new_object(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                      user='root', password='root1234', db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)

        cont_table_name = data_dict['table_name']
        cont_table_name = str(cont_table_name).lower()
        object_weight = data_dict['object_weight']

        query = "INSERT INTO " + cont_table_name + "(object_weight) VALUES (" + "'" + str(object_weight) + "');"

        result = await cur.execute(query)
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 10번 요청에서 사용하는 함수
# 해당 컨테이너에 있는 모든 데이터를 조회한후 반환하는 함수
@asyncio.coroutine
def get_all_object(loop, data):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234',
                                       db='container_weight', loop=loop)
    cursor = yield from conn.cursor(aiomysql.DictCursor)

    data_dict = literal_eval(data)

    cont_table_name = data_dict['table_name']
    cont_table_name = str(cont_table_name).lower()

    query = "select object_id, object_weight from " + str(cont_table_name) + ";"

    yield from cursor.execute(query)

    result = yield from cursor.fetchall()
    conn.close()

    return result


async def del_target_object(loop, data):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                      user='root', password='root1234', db='container_weight', loop=loop)
        cur = await conn.cursor()

        data_dict = literal_eval(data)

        cont_table_name = data_dict['table_name']
        cont_table_name = str(cont_table_name).lower()

        del_target_object_id = data_dict['del_target_id']

        query = "DELETE FROM " + cont_table_name + " WHERE object_id = " + "'" + str(del_target_object_id) + "'" + ";"

        result = await cur.execute(query)
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result