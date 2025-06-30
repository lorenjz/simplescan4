import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd
import SetSpike
from tkinter import filedialog
from urllib.request import urlopen
from tkinter import messagebox
import xml.etree.ElementTree as ET
import webcolors

global global_df
global global_table

class MyTable(Table):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-2>", self.handle_cell_click)

    def handle_cell_click(self, event):
        row = self.get_row_clicked(event)
        col = self.get_col_clicked(event)
        print(col)
        if row != -1 and col != -1:
            value = self.model.getValueAt(row, col)
            print(f"Clicked cell: Row {row}, Column {col}, Value: {value}")
            if col == 0:
                button_click(str(value))

    def updatemystuff(self):
        self.update
    
        

def button_click(chnl_freq):
   #link = "http://192.168.2.3/?spike"
   #f = urlopen(link)
   #print("Asked spike to come forward")
   e_text=entry.get() #ip address
   width = 5
   width_no = int(width)
   freq_start = float(chnl_freq) - (float(width_no) /2)
   freq_stop = float(chnl_freq) + (float(width_no) /2)
   frequency_list = []
   for index, row in global_df.iterrows():
        if is_between(float(row['freq']), freq_start, freq_stop):
            

            #print(f"{index}:  {row['freqName']}, Frequency:  {row['freq']}" )
            frequency_list.append(row['freq'])
   SetSpike.set_wrls_chnl(e_text,chnl_freq, width,frequency_list)
   print("asked spike for frquencies")
   show_marker_list(frequency_list)

def show_marker_list(m_freq_list):
    print("marker list:")
    my_message = ""
    a = 1
    for item in m_freq_list:
        #itemidx = global_df.index[global_df[item]]
        for index, row in global_df.iterrows():
            if item in row.values:
                print(f"Row at index {index} contains the value {item}")
                temp_str = str(a) + ".  " + global_df.loc[index,'freqName'] + ":  " + str(global_df.loc[index,'freq']) + "\r" 
                print(f"A is:  {a} and temp string is:  {temp_str}")
                my_message += temp_str
                
                a = a + 1
                
    messagebox.showinfo("marker list",my_message)

def is_between(num, lower_bound, upper_bound):
    return lower_bound <= num <= upper_bound

def get_value():
    e_text=entry.get()
    f_text=freq.get()
    #print(e_text)
    width = 5
    SetSpike.set_Spike(e_text,f_text,width)

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")])
    if file_path:
        #selected_file_label.config(text=f"Selected File: {file_path}")
        display_csv(file_path)

def display_csv(filename):
    #urllib.request.urlopen("http://http://192.168.2.3/?spike")
    
    global global_df
    global global_table
    global_df = pd.read_csv(filename)
    
    global_df.insert(2,'order','')
    global_df.insert(3, 'row_color','')
    dftable = tk.Toplevel()
    dftable.title("Soundbase coord")
    dftable.geometry("325x800")
    #print(global_df)
    frame = tk.Frame(dftable)
    wwBbutton = tk.Button(root, text="WWB")
    wwBbutton.grid(row=0, column=0)

    frame.pack(fill='both', expand=True)

    global_table = MyTable(frame, dataframe=global_df, showtoolbar=False, showstatusbar=False)
    #table.show()
    global_table.model.df = global_df# Assign the modified DataFrame to the global_table model
    global_table.visibleColumns = ['freq', 'freqName']
   
    global_table.show()
    
    global_table.redraw()
        

 
    dftable.mainloop()
    #window.mainloop()


def export_order_info():
    global global_df
    global_df['order'] = global_df['order'].apply(str)
    export_file_path= filedialog.asksaveasfile(defaultextension=".csv")
    columns_to_export = ['freqName', 'order']
    global_df[columns_to_export].to_csv(export_file_path,index=False)

    for index, row in MyTable:
        #style = row.get('style')
        print(dir(row))


def import_order_info():
    global global_df
    global_df['order'] = global_df['order'].apply(str)
    layout_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")])
    layout_df =  pd.read_csv(layout_path)
    layout_df['order'] = layout_df['order'].apply(str)
    #print(layout_df)
    for index, row in layout_df.iterrows():
        #print(f"Row freqName is:  {row['freqName']}")
        #print(f"Order is:  {row[1]}")
        global_df.loc[global_df['freqName']==row['freqName'], 'order']= row['order']
    MyTable.updatemystuff()

    #print(global_df)
def pcwwb():
    link = "http://192.168.2.3/?wwb"
    f = urlopen(link)

def pcspike():
    link = "http://192.168.2.3/?spike"
    f = urlopen(link)

def trace_one_cl():
    e_text=entry.get()
    if var.get():
        
        SetSpike.trace_visible(e_text,"1","ON")
    else:
        SetSpike.trace_visible(e_text,"1","OFF")

def trace_two_cl():
    e_text=entry.get()
    if var2.get():
        
        SetSpike.trace_visible(e_text,"2","ON")
    else:
        SetSpike.trace_visible(e_text,"2","OFF")

def trace_three_cl():
    e_text=entry.get()
    if var3.get():
        
        SetSpike.trace_visible(e_text,"3","ON")
    else:
        SetSpike.trace_visible(e_text,"3","OFF")
        
def chk_freqs():
    e_text=entry.get()
    for index, row in global_df.iterrows():
        #print(f"{index}:  {row['freqName']}, Frequency:  {row['freq']}" )
        width = 5
        newfreq = row['freq']
        freq = str(newfreq)
        SetSpike.set_Spike(e_text,freq,width) 
        messagebox.showinfo(f"Frequency information", "Displayed frequency is:  "+ str(row['freq']) + " for " + str(row['freqName']))
        
def import_wwb():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Show Files", "*.shw"), ("All files", "*.*")])
    if file_path:
        #selected_file_label.config(text=f"Selected File: {file_path}")
        print(file_path)
        tree = ET.parse(file_path)
        root = tree.getroot()

        print(f"Root tag: {root.tag}")



        for item in root.findall('inventory/device'):
            item_id = item.get('id')
            item_text = item.text
            
            for child in item:
                if child.tag =='series':
                    if child.text != 'None':
                        print("Device series:  "  + str(child.text))
                if child.tag =='band':
                    if child.text != 'None':
                        print("Device Band:  "  + str(child.text))
                
                if child.tag =='channel':
                    name_f_color=""
                    html_color=""
                    for children in child:
                       
                        
                        if children.tag == "channel_name":
                            print("Name:  " + str(children.text))
                            
                            name_f_color = children.text
                        if children.tag == "color":
                            print("Color:  " + str(children.text))
                            
                            new_color = android_color_to_html_hex(int(children.text))
                            print("new color = " + str(new_color))
                            html_color = new_color
                            
                    
                    for index, row in global_df.iterrows():
                        if name_f_color == row['freqName']:
                           
                            
                            global_df.loc[index, 'row_color']=html_color
                            
                            print(html_color)
                            
                            print(isValidHexaCode(html_color))
                            
                            
                            try:
                                global_table.setRowColors(rows=int(index), clr = html_color, cols='all')
                            except Exception as e:
                                print(f"An unexpected error occurred: {e}")
                           
                    
                
                
def isValidHexaCode(str):

    if (str[0] != '#'):
        return False

    if (not(len(str) == 4 or len(str) == 7)):
        return False

    for i in range(1, len(str)):
        if (not((str[i] >= '0' and str[i] <= '9') or (str[i] >= 'a' and str[i] <= 'f') or (str[i] >= 'A' or str[i] <= 'F'))):
            return False

    return True

                
                
def android_color_to_html_hex(android_color_int):
  """Converts an Android color integer to an HTML hex color code (#RRGGBB or #AARRGGBB)."""

  alpha = (android_color_int >> 24) & 0xFF
  red = (android_color_int >> 16) & 0xFF
  green = (android_color_int >> 8) & 0xFF
  blue = android_color_int & 0xFF

  # Format components as two hexadecimal digits
  alpha_hex = hex(alpha)[2:].zfill(2)
  red_hex = hex(red)[2:].zfill(2)
  green_hex = hex(green)[2:].zfill(2)
  blue_hex = hex(blue)[2:].zfill(2)

  # Return #RRGGBB format if alpha is 255 (opaque), otherwise #AARRGGBB
  if alpha == 255:
    return f"#{red_hex}{green_hex}{blue_hex}"
  else:
    return f"#{alpha_hex}{red_hex}{green_hex}{blue_hex}"
    
    
def hex_to_color_name(hex_code):
    try:
        # Attempt to convert hex to name using CSS3 color names
        color_name = webcolors.hex_to_name(hex_code, spec=webcolors.CSS3)
        return color_name
    except ValueError:
        # Handle cases where an exact match is not found
        return "No exact match found"

    

        



if __name__ == '__main__':
    
    
   

    root = tk.Tk()
    root.title("PB&J")
    root.geometry("300x175")
    entry= tk.Entry(root,font=('Century 12'),width=20)
    entry.insert(0, "192.168.2.3")
    entry.grid(row=0, column=1,padx=5, pady=5)
    freq = tk.Entry(root,font=('Century 12'),width=20)
    freq.grid(row=1, column=1,padx=5, pady=5)
    label = tk.Label(root, text="IP Address:  ").grid(row=0, column=0, padx=3, pady=2)
    button1 = tk.Button(root, text="5 Mhz Wide", command= get_value).grid(row=1, column=0, padx=3, pady=2)
    var = tk.IntVar()
    var2= tk.IntVar()
    var3= tk.IntVar()
    trace_one = tk.Checkbutton(root, text="Trace 1", variable=var, onvalue=1, offvalue=0, command=trace_one_cl)
    trace_one.grid(row=2,column=0)
    trace_two = tk.Checkbutton(root, text="Trace 2", variable=var2, onvalue=1, offvalue=0, command=trace_two_cl)
    trace_two.grid(row=3,column=0)
    trace_three = tk.Checkbutton(root, text="Trace 3", variable =var3, onvalue=1, offvalue=0, command=trace_three_cl)
    trace_three.grid(row=4,column=0)
    menubar = tk.Menu(root)

    # Create a File menu
    filemenu = tk.Menu(menubar, tearoff=0)
    #filemenu.add_command(label="New", command=do_nothing)
    filemenu.add_command(label="Open Soundbase File", command= open_file_dialog)
    filemenu.add_command(label="Export Layout info", command= export_order_info)
    filemenu.add_command(label="Import Layout info", command= import_order_info)
    filemenu.add_command(label="Import WWB info", command= import_wwb)
    #filemenu.add_command(label="Save", command=do_nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    window_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Window", menu=window_menu)
    window_menu.add_command(label="Show PC WWB",command=pcwwb)
    window_menu.add_command(label="Show PC Spike",command=pcspike)
    window_menu.add_command(label="Double Check Frequencies",command=chk_freqs)
    root.config(menu=menubar)



    root.mainloop()
