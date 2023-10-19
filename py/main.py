from gui import build_gui
from events import bind_events

def run_program():
    '''Build GUI, bind actions to events, and run application loop'''
    root, cnvs, hlp_txt, radio_mode, bttns = build_gui()
    bind_events(cnvs, hlp_txt, radio_mode, **bttns)
    root.mainloop()

run_program()