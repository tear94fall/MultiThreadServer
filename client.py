import asyncio
from buffer import Buffer

server_addr = 'localhost'
server_port = 8888


async def tcp_echo_client(message, loop):
    try:
        reader, writer = await asyncio.open_connection(server_addr, server_port, loop=loop)
        print('서버와 연결에 성공했습니다.')

        writer.write(message.encode())
        print('보낸 데이터 : %s ' % message)

        data = await reader.read(1024)
        print('받은 데이터 : %s ' % data.decode())

        writer.close()
        print('연결을 종료 합니다.')
    except Exception as err:
        print(err)


# 비동기 함수를 반복 수행하는 함수
async def main():
    buffer = Buffer()
    buffer.insert_data("name", "임준섭")
    buffer.insert_data("tel", "010-1234-5678")

    message = buffer.get_all_data()
    message = str(message)
    # 아무것도 입력되지 않았을 경우를 처리하는 로직 추가
    if not message:
        print("아무것도 입력되지 않았습니다.")
        pass
    else:
        await tcp_echo_client(message, loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
