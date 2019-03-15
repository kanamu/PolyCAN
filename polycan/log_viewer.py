from polycan.menu import *
from polycan.log_handler import *
class LogDisplay:
    def __init__(self, log_name, log, resolution, known):
        self.__log = log
        self.__log_name = log_name
        self.__log_iter = log.index
        self.__log_rev_iter = log.index.reverse()
        self.__known = known
        self.__min_line = 0
        self.__cur_line = 0
        self.__max_line = resolution if len(log) > resolution else len(log)
        self.__resolution = resolution
        self.__expand = False
        self.__active = False
        self.__detailed = False
        self.__modify = False
        self.__modify_choice = 0
        self.__pgn_info = None
        self.__data_breakdown = None
    @property
    def log(self):
        return self.__log
    @property
    def log_name(self):
        return self.__log_name
    @property
    def known(self):
        return self.__known
    @property
    def min_line(self):
        return self.__min_line
    @property
    def cur_line(self):
        return self.__cur_line
    @property
    def max_line(self):
        return self.__max_line
    @property
    def resolution(self):
        return self.__resolution
    @property
    def pgn_info(self):
        return self.__pgn_info
    @property
    def data_breakdown(self):
        return self.__data_breakdown
    @property
    def expand(self):
        return self.__expand
    @property
    def active(self):
        return self.__active
    @property
    def detailed(self):
        return self.__detailed
    @property
    def modify(self):
        return self.__modify
    @log.setter
    def log(self, l):
        self.__log = l
    @log_name.setter
    def log_name(self, name):
        self.__log_name = name
    @known.setter
    def known(self, d):
        self.__known = d
    @min_line.setter
    def min_line(self, x):
        self.__min_line = x
    @cur_line.setter
    def cur_line(self, x):
        self.__cur_line = x
    @max_line.setter
    def max_line(self, x):
        self.__max_line= x
    @resolution.setter
    def resolution(self, x):
        self.__resolution = x
    @expand.setter
    def expand(self, b):
        self.__expand = b
    @active.setter
    def active(self, b):
        self.__active = b
    @detailed.setter
    def detailed(self, b):
        self.__detailed = b
    @modify.setter
    def modify(self, b):
        self.__modify = b
    @pgn_info.setter
    def pgn_info(self, df):
        self.__pgn_info = df
    @data_breakdown.setter
    def data_breakdown(self, df):
        self.__data_breakdown = df
    def show(self):
        print(self.log_name)
        if self.expand == True:
            if self.active == True: 
                if self.detailed == True:
                    df1 = self.log[self.min_line:self.cur_line+1]
                    print(df1)
                    print(self.pgn_info)
                    print(self.data_breakdown)
                    df2 = pd.DataFrame(self.log[self.cur_line+1:self.max_line],
                        columns=[' ','    ','   ','        ',
                            '      ','           ','    ','           '])
                    if not df2.empty:
                        print(df2)
                else: 
                    df = self.log[self.min_line:self.max_line]
                    df.at[self.cur_line, ' '] = '>'
                    print(df)
            else:
                print(self.log[self.min_line:self.max_line])
    def up(self):
        if self.detailed == True:
            pass
        elif self.cur_line == self.min_line:
            if self.min_line == 0:
                if len(self.log) <= self.resolution:
                    self.cur_line = self.max_line-1
                else:
                    self.max_line = len(self.log)
                    self.min_line = self.max_line - self.resolution
                    self.cur_line = self.max_line - 1
            else:
                self.min_line -= 1
                self.max_line -= 1
                self.cur_line -= 1
        else:
            self.cur_line -= 1 

    def down(self):
        if self.detailed == True:
            pass
        elif self.cur_line == self.max_line-1:
            if self.max_line == len(self.log):
                self.min_line = 0
                self.cur_line = 0
                self.max_line = self.resolution if len(self.log) > self.resolution else len(self.log)
            else:
                self.min_line += 1
                self.cur_line += 1
                self.max_line += 1
        else:
            self.cur_line += 1
                         
    def left(self):
        if self.detailed == True:
            pass
        elif len(self.log) <= self.resolution:
            pass
        elif self.min_line - self.resolution >= 0:
            self.min_line -= self.resolution
            self.cur_line -= self.resolution
            self.max_line -= self.resolution
        else:
            diff = self.cur_line - self.min_line
            self.max_line = len(self.log)
            self.min_line = len(self.log) - self.resolution 
            self.cur_line = self.min_line+diff
    def right(self):
        if self.detailed == True:
            pass
        elif len(self.log) <= self.resolution:
            pass
        elif self.max_line + self.resolution > len(self.log):
            diff = self.cur_line - self.min_line
            self.min_line = 0
            self.max_line = self.resolution
            self.cur_line = diff
        else:
            self.max_line += self.resolution
            self.min_line += self.resolution
            self.cur_line += self.resolution
    def enter(self):
        if self.detailed == True:
            pass
        elif self.expand == False:
            self.expand = True
        elif self.active == False:
            self.active = True
        else:
            pgn = self.log.at[self.cur_line, 'pgn']
            if pgn in self.known:
                pgn_obj = known[pgn]
                self.pgn_info = pd.DataFrame(columns={'\t': '\t', 
                    'Data Length':pgn_obj.data_length,
                    'EDP': pgn_obj.edp, 'DP':pgn_obj.dp,
                    'PDU Format': pgn_obj.pdu_format, 
                    'PDU Specific' : pgn_obj.pdu_specific,
                    'Priority': pgn_obj.default_priority})
                pdata = param_values(data,pgn_object.data_length, pgn_pbject.parameters)
                self.data_breakdown = pd.DataFrame(pdata)
                self.detailed_index = self.cur_index
                self.detailed = True
    def collapse(self):
        if self.detailed == True:
            self.detailed = False
        elif self.active == True:
            self.active = False
        else:
            self.expand = False 
class LogViewer:
    def __init__(self, log_dict = {}, known = {}, max_display=2, resolution=20):
        self.__log_dict = log_dict
        self.__known = known
        self.__log_displays = []
        self.__max_display = max_display
        self.__resolution = resolution
    @property
    def log_dict(self):
        return self.__log_dict
    @property
    def known(self):
        return self.__known
    @property
    def log_displays(self):
        return self.__log_displays
    @property
    def resolution(self):
        return self.__resolution
    @property
    def max_display(self):
        return self.__max_display
    @log_dict.setter
    def set_log_dict(self, log_dict):
        self.__log_dict = log_dict
    @resolution.setter
    def set_resolution(self, r):
        self.__resolution = r
    @max_display.setter
    def set_max_display(self, n):
        self.__max_display = n

    def add_log(self, log, name):
        if name in self.__logdict:
            pass
        else:
            self.__log_dict[name] = {'cur_page':1, 'max_page':len(log)//resolution, 'log':log}
    def log_menu(self):
        for k,v in self.log_dict.items():
            log = v.copy(deep=True)
            log.insert(0,' ', ' ')
            ld = LogDisplay(k, log, self.resolution, self.known)
            self.log_displays.append(ld)

        log_select = 0
        log_select_max = len(self.log_displays)-1
        while(1):
            clear_screen()
            for i in range(0, log_select_max+1):
                if i == log_select:
                    print("* ", end='')
                    self.log_displays[i].show()
                else:
                    print("  ", end='')
                    self.log_displays[i].show()
            keyreader = kr.KeyReader()
            inp, outp, err = select.select([sys.stdin], [], [])
            entry = keyreader.getch()
            del keyreader     
            if entry == down:
                if self.log_displays[log_select].active == True:
                    self.log_displays[log_select].down()
                elif (log_select < log_select_max):
                    log_select += 1
                else:
                    log_select = 0 
            elif entry == up:
                if self.log_displays[log_select].active == True:
                    self.log_displays[log_select].up()
                elif (log_select > 0): 
                    log_select -= 1
                else:
                    log_select = log_select_max
            elif entry == left:
                if self.log_displays[log_select].active == True:
                    self.log_displays[log_select].left()
            elif entry == right:
                if self.log_displays[log_select].active == True:
                    self.log_displays[log_select].right()
            elif entry == enter:
                self.log_displays[log_select].enter()
            elif entry == collapse:
                if self.log_displays[log_select].expand == True:
                    self.log_displays[log_select].collapse()
            elif entry == delete:
                if self.log_displays[log_select].active == True:
                    pass
                else:
                    del self.log_dict[self.log_displays[log_select].log_name()]
                    del self.log_displays[log_select]
                    if self.log_displays == []:
                        return
                    elif log_select == log_select_max:
                        log_select -= 1
                    log_select_max -= 1    
            elif entry == modify:
                if self.log_displays[log_select].active == False:
                    newlog = log_menu(self.log_displays[log_select].log, self.known)
                    self.log_displays[log_select] = LogDisplay(
                        self.log_displays[log_select].log_name,
                        newlog, self.resolution, self.known)
                    
            elif entry == quit:
                return

    def set_current_log(self, name):
        if name not in self.__logdict:
            pass
        else:
            self.__cur_log = '' 
    def display_log(self, name):
        if name not in self.__logdict:
            pass
