from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


"""
The below function gets the latest messages from the server and inserts it into the Listbox object.
If the window has somehow been closed abruptly, we remove the user.
"""
def receive():
    stop = False
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE).decode('utf8')
            msgList.insert(tkinter.END,msg)
        except OSError:
            cleanAndClose()
            break

"""
The below function sends the messages of the user to the server to be broadcast, 
if the exit sequence is entered, user's data is purged, and the window is closed.
"""
def send(event=None):
    msg = myMsg.get()
    myMsg.set("")
    clientSocket.send(bytes(msg,'utf8'))
    if msg is "'exit'":
        clientSocket.close()
        cleanAndClose()
        top.quit()

"""
If the exit sequence is entered, this function is executed.
"""
def cleanAndClose(event=None):
    myMsg.set("'exit'")
    send()
    top.destroy()
    stop = True

if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('Bite Wise')
    top.configure(bg='#F2F2F2')
    messageFrame = tkinter.Frame(top, bg='#F2F2F2')
    scrollbar = tkinter.Scrollbar(messageFrame)
    top.state('zoomed')

    # msgList = tkinter.Listbox(messageFrame, width = 200, yscrollcommand = scrollbar.set)
    # scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    # msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    # msgList.pack(fill = tkinter.X)
    # messageFrame.pack()

    msgList = tkinter.Listbox(messageFrame, width=200, height=20, yscrollcommand=scrollbar.set, bg='#FFFFFF')
    msgList.configure(font=('Arial', 12))
    scrollbar.config(command=msgList.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    messageFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=10)

    myMsg = tkinter.StringVar()
    # myMsg.set("Click to type")
    # entryField = tkinter.Entry(top,textvariable = myMsg, width=100)
    # entryField.bind("<Return>", send)
    # entryField.pack()
    entryField = tkinter.Entry(top, textvariable=myMsg, width=70, bg='#FFFFFF')
    entryField.configure(font=('Arial', 12))
    entryField.bind("<Return>", send)
    entryField.pack(side=tkinter.LEFT, padx=10, pady=10, fill=tkinter.X, expand=True)
    # sendButton = tkinter.Button(top, text = 'Send', command = send, height = 1, width = 7)
    # sendButton.pack()
    sendButton = tkinter.Button(top, text='Send', command=send, width=10, height=2, bg='#4CAF50', fg='#FFFFFF')
    sendButton.configure(font=('Arial', 12, 'bold'))
    sendButton.pack(side=tkinter.LEFT, padx=10, pady=10)

    top.protocol("WM_DELETE_WINDOW", cleanAndClose)

    #HOST = input('Enter HOST IP Address: ')
    HOST = '127.0.0.1'
    PORT = 5545
    # PORT = input('Enter PORT number: ')
    PORT = 5545 if not PORT else int(PORT)

    BUFFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    receiveThread = Thread(target=receive)
    receiveThread.start()
    tkinter.mainloop()
    receiveThread.join()