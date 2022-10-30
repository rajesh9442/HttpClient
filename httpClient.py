import sys
import socket

def retrieve_url(url):
    domain = url_split(url)
    if domain is None:
        return None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((domain[0], domain[2]))
        domain[0]=bytes(domain[0],'utf-8')
        domain[1]=bytes(domain[1],'utf-8')
        s.send(b"GET " + domain[1] +
               b" HTTP/1.1\r\nHost:" + domain[0] +
               b"\r\nConnection: close\r\n\r\n")
    except socket.error:
        return None
    data_packets = []
    while True:
        data = None
        try:
            data = s.recv(4096)
            if data:
                data_packets+=[data]
                continue
            else:
                break
        except socket.error:
            return None
    data = b"".join(data_packets)
    if data.find(b"200 OK") != -1:
        new_data = data.split(b"\r\n\r\n", 1)
        return new_data[1]


def url_split(url):
    link=url
    if "http://" in url:
        link=link[7:]
        if '/' in link:
            link=link.split('/',1)
            for i in range(len(link)-1):
                i=i+1
                link[i]='/'+link[i]
            link+=[80]
            return link
        else:
            link=link.split()
            link+=['/']
            link+=[80]
            return link
    elif "https://" in url:
        link=link[8:]
        if '/' in link:
            link=link.split('/',1)
            for i in range(len(link)-1):
                i=i+1
                link[i]='/'+link[i]
            link+=[80]
            return link
        else:
            link=link.split()
            link+=['/']
            link+=[80]
            return link
    else:
        return None

if __name__ == "__main__":
    # pylint: disable=no-member
    sys.stdout.buffer.write(retrieve_url(sys.argv[1]))
