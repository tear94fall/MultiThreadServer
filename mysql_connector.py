import asyncio
import aiomysql

loop = asyncio.get_event_loop()


@asyncio.coroutine
def test_example():
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='test',
                                       loop=loop)

    cur = yield from conn.cursor()
    yield from cur.execute("SELECT * FROM captcha2")
    r = yield from cur.fetchall()
    for i in r:
        print(i[1], end=" ")
    print(" ")

    yield from cur.close()
    conn.close()

    return r
