#ธารา ศรีธราดล 6509681141
import socket # libraly socket
import os # เอาไว้ทำงานกับไฟล์

HOST = ''  # ให้ server ทำงานบนทุก Ip
PORT = 5141  # กำหนด port เป็น 5000 + 141 จาก 6509681141

# สร้าง socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # สร้าง socket, AF_INET คือ IPv4 SOCKET_STREAM คือ TCP
    # ให้ socket ทำงานกับ host และ port ที่ตั้งไว้
    server_socket.bind((HOST, PORT)) 
    # รอการเชื่อมต่อจาก client
    server_socket.listen() 

    print(f"Server is running on port {PORT}") # print ว่า server รันอยู่ port ไหน

    running = True
    while running: # loop ให้ server ทำงานตลอด
        conn, addr = server_socket.accept() #conn คือ socket addr คือ address ของ client
        with conn:
            print(f"Connected by {addr}\n") #

            # อ่านข้อมูลจาก client
            request = conn.recv(2048).decode() # รับข้อมูลสูงสุดได้ 2048 byte และ decode เพื่อแปลงเป็น string
            #print("Request received:")
            #print(request)

            # วิเคราะห์ HTTP request
            try:
                request_line = request.splitlines()[0] # แยกบรรทัดแรกออกมาเดี่ยว ๆ
                method, path, _ = request_line.split() # แบ่งส่วน
                
                if method == 'GET':
                    if path == '/mypage.html':
                        if os.path.exists('mypage.html'): # เช็คว่ามีไฟล์ชื่อนี้มั้ย
                            with open('mypage.html', 'rb') as f: # เปิดไฟล์ในรูปแบบ byte แทนด้วย f
                                response_body = f.read()
                            response = 'HTTP/1.0 200 OK\r\n'
                            response += 'Content-Type: text/html\r\n'
                            response += f'Content-Length: {len(response_body)}\r\n'
                            response += '\r\n'
                            response = response.encode() + response_body
                        else:
                            response = 'HTTP/1.0 404 Not Found\r\n\r\nFile Not Found'
                            response = response.encode()

                    elif path == '/myimage.gif':
                        if os.path.exists('myimage.gif'):
                            with open('myimage.gif', 'rb') as f:
                                response_body = f.read()
                            response = 'HTTP/1.0 200 OK\r\n'
                            response += 'Content-Type: image/gif\r\n'
                            response += f'Content-Length: {len(response_body)}\r\n'
                            response += '\r\n'
                            response = response.encode() + response_body
                            running = False
                        else:
                            response = 'HTTP/1.0 404 Not Found\r\n\r\nFile Not Found'
                            response = response.encode()

                    else: #path อื่น ๆ
                        response = 'HTTP/1.0 404 Not Found\r\n\r\nFile Not Found'
                        response = response.encode()
                else: #ไม่ใช่ get
                    response = 'HTTP/1.0 405 Method Not Allowed\r\n\r\nMethod Not Allowed'
                    response = response.encode()

                conn.sendall(response) #ตอบกลับ

            except Exception as e:
                print(f"Error processing request: {e}")

print("Connection closed.\n")
