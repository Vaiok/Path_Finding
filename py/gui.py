import tkinter as tk
from tkinter import ttk

def build_root():
    '''Build non-resizable root window to 90% screen width and height'''
    root = tk.Tk()
    root.title('Path Finding')
    scr_w = round(root.winfo_screenwidth() * 0.9)
    scr_h = round(root.winfo_screenheight() * 0.8)
    off_w = round(root.winfo_screenwidth() * 0.05)
    off_h = round(root.winfo_screenheight() * 0.05)
    root.geometry(f'{scr_w}x{scr_h}+{off_w}+{off_h}')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(False, False)
    return root, scr_w - off_w / 2, off_h / 2.5

def build_frame(root, border_size):
    '''Build main frame that fills root, columns 2, 3, 4 and row 1 expand'''
    frame = tk.Frame(root, background='black',
                     padx=border_size, pady=border_size)
    frame.grid(sticky='nsew')
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    return frame

def build_help_txt(frame, text_width):
    '''Build help text with instructions for using program'''
    help_txt = ttk.Label(frame, background='white', foreground='black',
                         wraplength=text_width, font='TkDefaultFont 12')
    help_txt.grid(column=0, row=0, columnspan=4, sticky='nsew')
    help_txt['text'] = '''\
  This is the help text with instructions for how to use this program.\
  It can be toggled on and off with the 'Help' button.\
  The 'Clear Graph' button will clear all nodes and edges, resetting the graph.\
  The 'Find Path' button searches for a path from the start to the goal.\
  If there is no node marked as start or goal, 'Find Path' will do nothing.\
  Under 'Canvas Click Mode' are 5 radio buttons.\
  These buttons change how clicking on the canvas affects it.\
  'Create Nodes' adds a blue node to the canvas if you click on it.\
  This node represents a location.\
  New nodes that would overlap existing nodes are not created.\
  'Create Edges' adds a red edge between two nodes if you click on them both.\
  This edge represents a path between 2 locations.\
  Nodes can't have edges to themselves or multiple edges with the same node.\
  'Delete Items' deletes nodes and edges if you click on them.\
  Deleting a node automatically deletes all edges connected to it.\
  'Select Start' marks a node as the start of a path.\
  'Select Goal' marks a node as the goal of a path.\
  No more than one start node and one goal node are allowed at a time.\
  All mouse clicks are with the main button(left), other buttons do nothing.\
    '''
    return help_txt

def build_radio_area(frame):
    '''Build label and radio buttons into frame with variable for buttons'''
    radio_frame = tk.Frame(frame, background='lightgray')
    radio_frame.grid(column=0, row=1)
    click_mode_lbl = ttk.Label(radio_frame, text='Canvas Click Mode',
                               anchor='center', background='lightgray',
                               font='TkDefaultFont 16')
    click_mode = tk.StringVar()
    create_nodes = tk.Radiobutton(radio_frame, text='Create Nodes',
                                  value='nodes', variable=click_mode,
                                  background='lightgray')
    create_edges = tk.Radiobutton(radio_frame, text='Create Edges',
                                  value='edges',variable=click_mode,
                                  background='lightgray')
    delete_items = tk.Radiobutton(radio_frame, text='Delete Items',
                                  value='delete', variable=click_mode,
                                  background='lightgray')
    select_start = tk.Radiobutton(radio_frame, text='Select Start',
                                  value='start',variable=click_mode,
                                  background='lightgray')
    select_goal = tk.Radiobutton(radio_frame, text='Select Goal',
                                 value='goal', variable=click_mode,
                                 background='lightgray')
    click_mode_lbl.grid(column=0, row=0, columnspan=5, sticky='ew')
    create_nodes.grid(column=0, row=1)
    create_edges.grid(column=1, row=1)
    delete_items.grid(column=2, row=1)
    select_start.grid(column=3, row=1)
    select_goal.grid(column=4, row=1)
    return click_mode

def build_buttons(frame):
    '''Build, place, and return buttons'''
    clear_graph = ttk.Button(frame, text='Clear Graph', padding=10)
    find_path = ttk.Button(frame, text='Find Path', padding=10)
    help_bttn = ttk.Button(frame, text='Help', padding=10)
    clear_graph.grid(column=1, row=1)
    find_path.grid(column=2, row=1)
    help_bttn.grid(column=3, row=1)
    return {
        'clr_grph': clear_graph, 'fnd_pth': find_path, 'hlp_bttn': help_bttn
    }

def build_gui():
    '''Build canvas, help text, radio area, and buttons in frame in root'''
    root, text_width, border_size = build_root()
    frame = build_frame(root, border_size)
    cnvs = tk.Canvas(frame, background='white',
                     borderwidth=border_size, relief='groove')
    cnvs.grid(column=0, row=0, columnspan=4, sticky='nsew')
    help_txt = build_help_txt(frame, text_width)
    click_mode = build_radio_area(frame)
    buttons = build_buttons(frame)
    return (root, cnvs, help_txt, click_mode, buttons)