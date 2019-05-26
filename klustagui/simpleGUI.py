from tkinter import *
from tkinter import filedialog
import os, glob
env_loc = os.getcwd()
class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      self.picks = picks
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return [self.picks[i] for i in range(len(self.picks)) if self.vars[i].get()==1]

window = Tk()
Ready = False

def change_file_names(path):
    file_list = glob.glob('"'+path+'*.dat"')
    correct_list = []
    for file in file_list:
        if file[0:2]=='amp':
            if file[4]!= 'A':
                new_name = 'amp-A-'+file[6:]
                correct_list.append(new_name)
            else:
                correct_list.append(file)
    os.chdir( path )
    for i in range(len(file_list)):
        os.system('rename '+file_list[i]+' '+correct_list[i])

def process_to_klusta(path,file_list=0):
    global Ready
    global env_loc
    change_file_names(path)
    cur = env_loc
    os.chdir(cur+'/extra_files')
    os.system('COPY "1chan28.prb"'+' "'+path+'"')
    os.system('COPY "unRAR.exe"'+' "'+path+'"')
    os.system('COPY "amp-A 3-10 clusters big chunk.rar"' + ' "' + path +
              '/clusters_big_chunk.rar"')
    os.chdir( path )
    os.system('unRAR e clusters_big_chunk.rar')
    from moran_lab import multi_klusta
    multi_klusta.run_klusta(CAR=False,move_files=False,start_val=file_list)
    multi_klusta.run_kwik_gui()
    Ready = True
    print('processing finished')

def sort(path, events):
    if Ready:
        os.chdir(path)
        os.system('activate klusta')
        from moran_lab import spike_sort
        local_name = spike_sort.All_electrodes(get_laser=False,get_events=True,event_list=events)
        local_name.show_all_psth(save=True,tastes=events)
        return True

def ask_path():
    global filename
    filename = filedialog.askdirectory()

L1 = Label(window,text="Choose file directory")
L1.pack()
B1 = Button(window,text='Choose',command=ask_path)
B1.pack()
L2 = Label(window,text="choose events")
L2.pack()
option_box = Checkbar(window,['Water','Sugar','Tone','Shock'])
option_box.pack()
L3 = Label(window,text='choose channel list(optional)')
L3.pack()
channels = Checkbar(window,[i for i in range(1,33)])
channels.pack()
B2 = Button(window,text='process data',command=lambda : process_to_klusta(filename,channels.state()))
B2.pack()
B3 = Button(window,text='sort spikes',command=lambda : sort(filename,option_box.state))
B3.pack()

window.mainloop()