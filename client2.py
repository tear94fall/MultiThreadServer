import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('localhost', 8888, loop=loop)
    message = str(message)

    print('데이터를 보냄 : %s ' % message)

    writer.write(message.encode())

    data = await reader.read(1024)
    print('데이터를 받아옴 : %s ' % data.decode())

    writer.close()


# 비동기 함수를 반복 수행하는 함수
async def main():
    # print("전송할 데이터를 입력해주세요>>", end="")
    # message = str(input())
    message = 1
    # 아무것도 입력되지 않았을 경우를 처리하는 로직 추가
    while True:
        if not message:
            print("아무것도 입력되지 않았습니다.")
            pass
        else:
            await tcp_echo_client(message, loop)
        message += 1


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
