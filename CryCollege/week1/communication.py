import socket


def send_receive(ip_dst, port_dst, msg, maxsize=1000):
    """
    Send one package via udp and receive one package.
    :param ip_dst: ip where to send the data
    :param port_dst: port to send the data to
    :param msg: data to send
    :return data: the data you received
    :return addr: the address you received the data from
    """

    raise NotImplementedError("TODO: Implement me plx")
    return data, addr


if __name__ == '__main__':
    print(send_receive("127.0.0.1", 1337, b"Huhu!"))