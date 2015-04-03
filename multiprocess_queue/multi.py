import multiprocessing
import Queue
import Tkinter
tk = Tkinter.Tk()
import time

class MyFancyClass(multiprocessing.Process):
    
    def __init__(self, parent_queue,child_queue):
        self.counter = 0
        multiprocessing.Process.__init__(self)
        self.parent_queue = parent_queue
        self.child_queue = child_queue
        button = Tkinter.Button(tk,text="Blue",command=lambda: self.printit())
        button.pack()

        canvas = Tkinter.Canvas(tk, width=400, height=400, bg="white")
        canvas.pack()

        tk.after(100,self.do_something)

    def printit(self):
        print(self.counter)
        self.child_queue.put("ok")

    def run(self):
        tk.mainloop()
        #self.do_something()

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        msg = self.parent_queue.get()
        self.counter = msg["matt"]
        print 'Doing something fancy in %s for %d!' % (proc_name, self.counter )
        tk.after(1000,self.do_something)

"""
def worker(q):
    obj = q.get()
    obj.do_something()
"""

if __name__ == '__main__':
    parent = multiprocessing.Queue()
    child = multiprocessing.Queue()

    work = MyFancyClass(parent,child)
    #p = multiprocessing.Process(target=work(), args=(queue,))
    print("starting thread")
    work.start()
    counter = 0
    
    while work.is_alive():
        parent.put({"matt":counter})
        try:
            print(child.get(False))
        except Queue.Empty:
            print("no message")
        time.sleep(1)
        counter += 1
    
    # Wait for the worker to finish
    print("waiting for end")
    parent.close()
    parent.join_thread()
    child.close()
    child.join_thread()
    work.join()
    print("done")
