import tkinter as tk
from tkinter import ttk ,scrolledtext ,messagebox
import threading
from datetime import datetime
import time
from src .core import state ,config ,game_actions
from src .core .automation import CV2_AVAILABLE
class HarvestBotGUI :
    def __init__ (self ,root ):
        self .root =root
        self .root .title ("🌱 Волшебный садовый бот")
        self .root .geometry ("1200x750")
        self .root .resizable (True ,True )
        if not CV2_AVAILABLE :
            messagebox .showerror (
            "Отсутствует зависимость",
            "OpenCV (cv2) недоступен!\n\n"
            "Обнаружение изображений не будет работать.\n"
            "Пожалуйста, установите: pip install opencv-python"
            )
        self .setup_style ()
        main_container =tk .Frame (self .root ,bg =self .colors ['bg_dark'])
        main_container .pack (fill =tk .BOTH ,expand =True ,padx =10 ,pady =10 )
        left_panel =tk .Frame (main_container ,bg =self .colors ['bg_dark'])
        left_panel .pack (side =tk .LEFT ,fill =tk .BOTH ,expand =False ,padx =(10 ,5 ))
        right_panel =tk .Frame (main_container ,bg =self .colors ['bg_dark'])
        right_panel .pack (side =tk .RIGHT ,fill =tk .BOTH ,expand =True ,padx =(5 ,10 ))
        self .create_header (left_panel )
        self .create_control_panel (left_panel )
        self .create_stats_panel (left_panel )
        self .create_config_panel (left_panel )
        self .create_log_panel (right_panel )
        self .create_footer ()
        self .update_ui ()
    def setup_style (self ):
        style =ttk .Style ()
        style .theme_use ('clam')
        self .colors ={
        'bg_dark':"#1e1e2e",'bg_medium':"#2a2a3e",'bg_light':"#363650",
        'accent':"#89b4fa",'success':"#a6e3a1",'warning':"#fab387",
        'error':"#f38ba8",'text':"#cdd6f4"
        }
        style .configure ("TFrame",background =self .colors ['bg_dark'])
        style .configure ("Header.TLabel",background =self .colors ['bg_dark'],foreground =self .colors ['accent'],font =("Следуйте пользовательскому интерфейсу",20 ,"bold"))
        style .configure ("Title.TLabel",background =self .colors ['bg_medium'],foreground =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",11 ,"bold"))
        style .configure ("TLabel",background =self .colors ['bg_dark'],foreground =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",9 ))
        self .root .configure (bg =self .colors ['bg_dark'])
    def create_header (self ,parent ):
        header_frame =tk .Frame (parent ,bg =self .colors ['bg_dark'],height =60 )
        header_frame .pack (fill =tk .X ,pady =(10 ,10 ))
        ttk .Label (header_frame ,text ="🌱 Волшебный садовый бот для сбора урожая",style ="Header.TLabel").pack (side =tk .LEFT )
        ttk .Label (header_frame ,text ="Редактирование графического интерфейса",style ="TLabel").pack (side =tk .LEFT ,padx =(10 ,0 ))
    def create_control_panel (self ,parent ):
        control_frame =tk .Frame (parent ,bg =self .colors ['bg_dark'])
        control_frame .pack (fill =tk .X ,pady =10 )
        self .start_button =tk .Button (control_frame ,text ="▶ СТАРТ",command =self .start_bot ,bg =self .colors ['success'],fg ="black",font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),width =12 ,height =2 ,cursor ="hand2")
        self .start_button .pack (side =tk .LEFT ,padx =3 )
        self .stop_button =tk .Button (control_frame ,text ="⏹ СТОП",command =self .stop_bot ,bg =self .colors ['error'],fg ="black",font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),width =12 ,height =2 ,state =tk .DISABLED ,cursor ="hand2")
        self .stop_button .pack (side =tk .LEFT ,padx =3 )
        self .reset_button =tk .Button (control_frame ,text ="🔄 СБРОС",command =self .reset_stats ,bg =self .colors ['warning'],fg ="black",font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),width =12 ,height =2 ,cursor ="hand2")
        self .reset_button .pack (side =tk .LEFT ,padx =3 )
        status_frame =tk .Frame (parent ,bg =self .colors ['bg_dark'])
        status_frame .pack (fill =tk .X ,pady =5 )
        self .status_label =tk .Label (status_frame ,text ="● холостой ход",bg =self .colors ['bg_dark'],fg =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",12 ,"bold"))
        self .status_label .pack ()
    def create_stats_panel (self ,parent ):
        stats_frame =tk .LabelFrame (parent ,text ="📊 Статистика",bg =self .colors ['bg_medium'],fg =self .colors ['accent'],font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),padx =10 ,pady =10 )
        stats_frame .pack (fill =tk .X ,pady =10 )
        stats_grid =tk .Frame (stats_frame ,bg =self .colors ['bg_medium'])
        stats_grid .pack (fill =tk .X )
        self .stat_labels ={}
        stats_config =[
        ("Cycles","cycles",0 ,0 ),("Общий урожай","total_harvests",0 ,1 ),
        ("Всего продаж","total_sells",0 ,2 ),("Всего ходов","total_moves",1 ,0 ),
        ("Harvests/Hour","rate",1 ,1 ),("Runtime","runtime",1 ,2 ),
        ("Position","position",2 ,0 ),("Errors","errors",2 ,1 ),
        ("Status","detailed_status",2 ,2 ),
        ]
        for label_text ,key ,row ,col in stats_config :
            frame =tk .Frame (stats_grid ,bg =self .colors ['bg_light'],relief =tk .RAISED ,borderwidth =1 )
            frame .grid (row =row ,column =col ,padx =3 ,pady =3 ,sticky ="ew")
            tk .Label (frame ,text =label_text ,bg =self .colors ['bg_light'],fg =self .colors ['accent'],font =("Следуйте пользовательскому интерфейсу",8 ,"bold")).pack (pady =(3 ,0 ))
            value_label =tk .Label (frame ,text ="0",bg =self .colors ['bg_light'],fg =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",14 ,"bold"))
            value_label .pack (pady =(0 ,3 ))
            self .stat_labels [key ]=value_label
        for i in range (3 ):stats_grid .columnconfigure (i ,weight =1 )
    def create_config_panel (self ,parent ):
        config_frame =tk .LabelFrame (parent ,text ="⚙️ Конфигурация",bg =self .colors ['bg_medium'],fg =self .colors ['accent'],font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),padx =10 ,pady =10 )
        config_frame .pack (fill =tk .X ,pady =10 )
        self .config_vars ={}
        configs =[
        ("Размер сетки:","GRID_SIZE",1 ,20 ),("Количество урожая:","HARVEST_COUNT",1 ,10 ),
        ("Задержка перемещения (с):","MOVE_DELAY",0.05 ,1.0 ),("Задержка сбора урожая (с):","HARVEST_DELAY",0.05 ,1.0 ),
        ("Перезарядка цикла (с):","LOOP_COOLDOWN",0 ,10 ),
        ]
        for i ,(label_text ,config_key ,min_val ,max_val )in enumerate (configs ):
            tk .Label (config_frame ,text =label_text ,bg =self .colors ['bg_medium'],fg =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",9 )).grid (row =i //2 ,column =(i %2 )*2 ,padx =5 ,pady =5 ,sticky ="w")
            var =tk .DoubleVar (value =getattr (config .Config ,config_key ))
            self .config_vars [config_key ]=var
            tk .Spinbox (config_frame ,from_ =min_val ,to =max_val ,textvariable =var ,width =10 ,bg =self .colors ['bg_light'],fg =self .colors ['text'],buttonbackground =self .colors ['accent'],increment =0.05 if isinstance (min_val ,float )else 1 ).grid (row =i //2 ,column =(i %2 )*2 +1 ,padx =5 ,pady =5 ,sticky ="w")
        tk .Button (config_frame ,text ="💾 Сохранить конфигурацию",command =self .save_config ,bg =self .colors ['accent'],fg ="black",font =("Следуйте пользовательскому интерфейсу",9 ,"bold"),cursor ="hand2").grid (row =3 ,column =0 ,columnspan =2 ,pady =10 ,sticky ="ew",padx =5 )
    def create_log_panel (self ,parent ):
        log_frame =tk .LabelFrame (parent ,text ="📝 Журнал активности",bg =self .colors ['bg_medium'],fg =self .colors ['accent'],font =("Следуйте пользовательскому интерфейсу",11 ,"bold"),padx =10 ,pady =10 )
        log_frame .pack (fill =tk .BOTH ,expand =True )
        self .log_text =scrolledtext .ScrolledText (log_frame ,bg =self .colors ['bg_light'],fg =self .colors ['text'],font =("Consolas",9 ),wrap =tk .WORD ,state =tk .NORMAL )
        self .log_text .pack (fill =tk .BOTH ,expand =True )
        self .log_text .tag_config ("info",foreground =self .colors ['accent'])
        self .log_text .tag_config ("success",foreground =self .colors ['success'])
        self .log_text .tag_config ("warning",foreground =self .colors ['warning'])
        self .log_text .tag_config ("error",foreground =self .colors ['error'])
        self .log ("Бот инициализирован. Готов начать!","info")
        if CV2_AVAILABLE :self .log ("✓ OpenCV успешно загружен","success")
        else :self .log ("✗ OpenCV НЕДОСТУПЕН — обнаружение изображений отключено!","error")
    def log (self ,message ,tag ="info"):
        timestamp =datetime .now ().strftime ("%H:%M:%S")
        self .log_text .insert (tk .END ,f"[{timestamp }] {message }\n",tag )
        self .log_text .see (tk .END )
        self .root .update_idletasks ()
    def create_footer (self ):
        footer =tk .Frame (self .root ,bg =self .colors ['bg_dark'],height =30 )
        footer .pack (fill =tk .X ,padx =20 ,pady =(0 ,10 ))
        tk .Label (footer ,text ="Создатель: Джон Лемар Гонсалес",bg =self .colors ['bg_dark'],fg =self .colors ['text'],font =("Следуйте пользовательскому интерфейсу",8 )).pack (side =tk .LEFT )
    def get_elapsed_time (self ):
        if state .stats ['start_time']:
            elapsed =time .time ()-state .stats ['start_time']
            h ,r =divmod (elapsed ,3600 )
            m ,s =divmod (r ,60 )
            return f"{int (h ):02d}:{int (m ):02d}:{int (s ):02d}"
        return "00:00:00"
    def get_harvests_per_hour (self ):
        if state .stats ['start_time']:
            elapsed_hours =(time .time ()-state .stats ['start_time'])/3600
            if elapsed_hours >0 :
                return state .stats ['total_harvests']/elapsed_hours
        return 0
    def update_ui (self ):
        s =state .stats
        self .stat_labels ['cycles'].config (text =str (s ['cycles']))
        self .stat_labels ['total_harvests'].config (text =str (s ['total_harvests']))
        self .stat_labels ['total_sells'].config (text =str (s ['total_sells']))
        self .stat_labels ['total_moves'].config (text =str (s ['total_moves']))
        self .stat_labels ['errors'].config (text =str (s ['errors']))
        self .stat_labels ['runtime'].config (text =self .get_elapsed_time ())
        self .stat_labels ['position'].config (text =f"({state .current_position ['row']}, {state .current_position ['col']})")
        self .stat_labels ['rate'].config (text =f"{self .get_harvests_per_hour ():.1f}")
        if state .bot_running :
            self .stat_labels ['detailed_status'].config (text ="Running",fg =self .colors ['success'])
            self .status_label .config (text ="● БЕГ",fg =self .colors ['success'])
        else :
            self .stat_labels ['detailed_status'].config (text ="Idle",fg =self .colors ['warning'])
            self .status_label .config (text ="● холостой ход",fg =self .colors ['warning'])
        self .root .after (100 ,self .update_ui )
    def save_config (self ):
        for key ,var in self .config_vars .items ():
            value =var .get ()
            setattr (config .Config ,key ,int (value )if isinstance (value ,float )and value .is_integer ()else value )
        config .Config .save ()
        self .log ("Конфигурация сохранена!","success")
        messagebox .showinfo ("Success","Конфигурация успешно сохранена!")
    def reset_stats (self ):
        if messagebox .askyesno ("Сбросить статистику","Вы уверены, что хотите сбросить всю статистику?"):
            for key in ['total_harvests','total_sells','total_moves','errors','inventory_checks','cycles']:
                state .stats [key ]=0
            state .stats ['start_time']=None
            self .log ("Статистика сброшена!","warning")
    def start_bot (self ):
        if not CV2_AVAILABLE :
            messagebox .showerror ("Не могу начать","OpenCV недоступен. Пожалуйста, установите: pip install opencv-python")
            return
        state .bot_running =True
        state .stats ['start_time']=time .time ()
        self .start_button .config (state =tk .DISABLED )
        self .stop_button .config (state =tk .NORMAL )
        self .log ("Бот запустился! Переключиться в окно игры...","success")
        bot_thread =threading .Thread (target =self .run_bot_thread ,daemon =True )
        bot_thread .start ()
    def stop_bot (self ):
        state .bot_running =False
        self .start_button .config (state =tk .NORMAL )
        self .stop_button .config (state =tk .DISABLED )
        self .log ("Бот остановлен пользователем.","error")
    def run_bot_thread (self ):
        time .sleep (3 )
        self .log ("Начинаем цикл сбора урожая...","success")
        while state .bot_running :
            try :
                state .stats ['cycles']+=1
                self .log (f"━━━ Cycle #{state .stats ['cycles']} started ━━━","info")
                game_actions .harvest_loop (logger =self .log )
                if state .bot_running :
                    self .log (f"✓ Cycle #{state .stats ['cycles']} complete!","success")
                    if config .Config .LOOP_COOLDOWN >0 :
                        self .log (f"Waiting {config .Config .LOOP_COOLDOWN }s before next cycle...","info")
                    time .sleep (config .Config .LOOP_COOLDOWN )
            except Exception as e :
                self .log (f"An unexpected error occurred in bot thread: {e }","error")
                state .stats ['errors']+=1
                time .sleep (2 )