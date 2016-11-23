# -*- coding: cp1251 -*-
from Tkinter import *
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class MyApp:
    def __init__(self, parent ):

                self.button_width = 6
                btn_padx = "1m"
                btn_pady = "1m"

                frm_padx = "1m"
                frm_pady = "1m"
                frm_ipadx = "1m"
                frm_ipady = "1m"

                self.lmbd = 1.0
                self.qty = 100

                self.myParent = parent

                self.drawResults = StringVar()
                self.probabilityes = StringVar()
                # topmost frame
                self.myContainer1 = Frame( self.myParent )
                self.myContainer1.pack()
                                
                # description frame:
                self.dscr_frame = LabelFrame( self.myContainer1, relief=RIDGE, width=300, height=150, borderwidth=5, \
                                        bg = "purple", labelanchor = "nw", text = u"Описание" )
                self.dscr_frame.pack(side=TOP, fill=BOTH, expand=YES )

                # parametres frame
                self.params_frame = LabelFrame( self.myContainer1, relief=RIDGE, width=300, height=250, borderwidth=5, \
                                        bg = "magenta", labelanchor="nw", text=u"Параметры" )
                self.params_frame.pack( side=TOP, fill=BOTH, expand=YES )

                #results frame
                self.results_frm = LabelFrame( self.myContainer1, relief = RIDGE, borderwidth = 5, height = 50,\
                                           labelanchor = "nw", text = u"Результаты", pady=4, padx=4)
                self.results_frm.pack( side=TOP, fill=BOTH, expand=YES )
                
                # bottom frame 
                self.btm_frame = Frame( self.myContainer1 )
                self.btm_frame.pack( side=TOP, fill=BOTH, expand=YES )
                
                # 2nd results frame 
                self.res2_frm = Frame( self.btm_frame, relief = RIDGE, borderwidth = 5, height = 50,\
                                background = "tan" )
                self.res2_frm.pack( side=LEFT, fill=BOTH, expand=YES )
                
                # buttons frame
                self.btn_frame = Frame( self.btm_frame )
                self.btn_frame.pack( side=RIGHT, ipadx = frm_ipadx, ipady = frm_ipady, \
                                padx = frm_padx, pady = frm_pady)

                description = u"Случайная величина \u03b7 \u2013 время \
обслуживания покупателей в кассе магазина.\n\
Пусть \u03b7 распределена показательно с параметром \u03bb.\n\
Гипотеза - выборка имеет экспоненциальное распределение"
                self.l_dscr = Label( self.dscr_frame, text= description )
                self.l_dscr.pack() # greek lambda unicode U+03bb

                # widgets for PARAMETERS frame
                self.l_lambd = Label( self.params_frame, text=u"\u03bb := " )
                self.l_lambd.grid(row=0, column=0, sticky="e" )

                self.e_lambd = Entry( self.params_frame, width = 10 )
                self.e_lambd.grid(row=0, column=1 ) #, columnspan=3)
                self.e_lambd.insert(0, "1.0" )

                self.l_qty = Label( self.params_frame, text=u"Число испытаний: " )
                self.l_qty.grid(row=1, column=0 )

                self.e_qty = Entry( self.params_frame, width = 10 )
                self.e_qty.grid(row=1, column=1) #, columnspan=3)
                self.e_qty.insert(0, "5000" )

                self.l_interval = Label( self.params_frame, text=u"Число столбов\nдля гистограммы" )
                self.l_interval.grid(row=0,column=2, ipadx=8)

                self.e_interval = Entry( self.params_frame, width=10 )
                self.e_interval.grid( row=1,column=2 )
                self.e_interval.insert(0, "20" )

                ##self.l_intr2 =Label( self.params_frame, text=u"Ширина интервала\n для проверки гипотезы" )
                ##self.l_intr2.grid( row=0, column = 3 )

                ##self.e_intr2 = Entry( self.params_frame, width=10 )
                ##self.e_intr2.grid( row=1, column=3 )
                ##self.e_intr2.insert('end', '5.0')

                self.l_hyp_param = Label( self.params_frame, text=u"Параметр значимости\nгипотезы" )
                self.l_hyp_param.grid(row=0, column=4, sticky=E )

                self.e_hyp_param = Entry( self.params_frame, width = 10 )
                self.e_hyp_param.grid( row=1, column = 4 )
                self.e_hyp_param.insert('end', '0.8')            

                # button for BUTTONS frame
                self.btn_launch = Button( self.btn_frame, command = self.btnLaunchClick )
                self.btn_launch.configure( text=u"Запуск", width = self.button_width, padx = btn_padx, pady = btn_pady )
                self.btn_launch.focus_force()
                self.btn_launch.grid( row=0, column=0, padx = 8 )#, rowspan=2, sticky=W)
                self.btn_launch.bind("<Return>", self.btnLaunchClick_a )
                
                # widgets for results frame
                ## list box for 1st part
                self.l_results = Label( self.results_frm, text=u"Значения случайной\nвеличины \u03b7" )
                self.l_results.grid( row=0, column=2, columnspan=2 )
                self.yScroll  =  Scrollbar ( self.results_frm, orient=VERTICAL )
                self.yScroll.grid ( row=1, column=3, sticky=N+S )

                ##self.xScroll  =  Scrollbar ( self.results_frm, orient=HORIZONTAL )
                ##self.xScroll.grid ( row=2, column=2, sticky=E+W )

                self.lb_draw = Listbox( self.results_frm, exportselection=0, 
                                selectmode=SINGLE, ##xscrollcommand=self.xScroll.set,
                                yscrollcommand=self.yScroll.set, height=8, width=18 )  #, activestyle="dotbox" 
                self.lb_draw.grid( row=1, column=2, sticky=N+E+W+S )

                self.lb_draw["listvariable"] = self.drawResults

                ##self.xScroll["command"]  =  self.lb_draw.xview
                self.yScroll["command"]  =  self.lb_draw.yview
                ## widgets for 2nd part
                self.l_charss = Label( self.results_frm, text=u"Теор. мат. ожидание\n\
Выборочн. мат. ожидание\nМодуль их разности\n Теор. дисперсия\nВыборочн. дисперсия\n\
Модуль их разности\nВыборочн. медиана\nРазмах выборки" )
                self.l_charss.grid( row=1, column=0 )

                self.lb_charss = Listbox( self.results_frm, exportselection=0, 
                                selectmode=SINGLE, width=15, height=8 )  #, activestyle="dotbox" 
                self.lb_charss.grid( row=1, column=1, ipadx=8 ) #, sticky=N+E+W+S )

                # Widgets for 2nd part
                # table of bins
                self.tblScroll  =  Scrollbar( self.res2_frm, orient=VERTICAL, command=self.OnTblScroll )
                self.tblScroll.grid ( row=1, column=3, sticky=N+S )
                 
                self.l_tab1 = Label( self.res2_frm, text='Zj')
                self.l_tab1.grid( row=0, column=0 )
                self.lb_table1 = Listbox( self.res2_frm, exportselection=0, 
                                selectmode=SINGLE, height=8, width=18, yscrollcommand=self.tblScroll.set )  #, activestyle="dotbox"
                self.lb_table1.bind( "<MouseWheel>", self.OnMouseWheel )
                self.lb_table1.grid( row=1, column=0, ipadx=8, sticky=E ) #, sticky=N+E+W+S )

                self.l_tab2 = Label( self.res2_frm, text=u"Теор. пл-ть\nраспределения")
                self.l_tab2.grid( row=0, column=1 )                
                self.lb_table2 = Listbox( self.res2_frm, exportselection=0, 
                                selectmode=SINGLE, height=8, width=18, yscrollcommand=self.tblScroll.set  )  #, activestyle="dotbox"
                self.lb_table2.bind( "<MouseWheel>", self.OnMouseWheel )
                self.lb_table2.grid( row=1, column=1, ipadx=8) #, sticky=N+E+W+S )

                self.l_tab3 = Label( self.res2_frm, text=u"Высота столба\nгистограммы")
                self.l_tab3.grid( row=0, column=2 )
                self.lb_table3 = Listbox( self.res2_frm, exportselection=0, 
                                selectmode=SINGLE, height=8, width=18, yscrollcommand=self.tblScroll.set  )  #, activestyle="dotbox"
                self.lb_table3.bind( "<MouseWheel>", self.OnMouseWheel )                
                self.lb_table3.grid( row=1, column=2, ipadx=8 ) #, sticky=N+E+W+S )

                self.l_result = Label( self.res2_frm )
                self.l_result.grid( row=5, column=0, ipadx=8, columnspan=4)

                ## widgets for 3rd part
                
                self.hypScroll  =  Scrollbar( self.results_frm, orient=VERTICAL)#, command=self.OnTblScroll )
                self.hypScroll.grid( row=1, column=6, sticky=N+S )

                self.l_hyp = Label( self.results_frm, text=u"Теоретические\nвероятности" )
                self.l_hyp.grid( row=0, column=5)
                
                self.lb_hyp = Listbox( self.results_frm, exportselection = 0,
                                       selectmode=SINGLE, height=8, width=18,
                                       yscroll=self.hypScroll.set )
                self.lb_hyp.grid( row=1, column=5 )
                self.lb_hyp['listvariable'] = self.probabilityes
                self.hypScroll['command'] = self.lb_hyp.yview
                
                
                #for i in range(100):
                #    self.lb_table1.insert("end","item %s" % i)
                #    self.lb_table2.insert("end","item %s" % i)
                #    self.lb_table3.insert("end","item %s" % i) 
                
                ##self.tblScroll["command"]  =  self.lb_draw.yview
                
                
    def btnLaunchClick( self ): 
                if self.btn_launch["background"] == "green":
                        self.btn_launch["background"] = "yellow"
                else:
                        self.btn_launch["background"] = "green"

                self.qty = int( self.e_qty.get() )
                self.lmbd = float( self.e_lambd.get() )
                self.unfrm = np.random.uniform( 0.0, 1.0, self.qty )

                #print(self.unfrm )
                self.unfrm = np.log(self.unfrm)
                self.unfrm = np.multiply( self.unfrm, -1/self.lmbd ) 
                
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ## caution!!! reuse of variable !!!
                self.qty = int(self.e_interval.get())
                # the histogram of the data
                n, bins, patches = ax.hist(self.unfrm, self.qty, normed=1, facecolor='green')

                # hist uses np.histogram under the hood to create 'n' and 'bins'.
                # np.histogram returns the bin edges, so there will be 50 probability
                # density values in n, 51 bin edges in bins and 50 patches.  To get
                # everything lined up, we'll compute the bin centers
                ##bincenters = 0.5*(bins[1:]+bins[:-1])
                # add a 'best fit' line for the normal PDF
                ##y = mlab.normpdf( bincenters, mu, sigma)
                
                self.absciss = np.arange(0, np.amax(self.unfrm), np.amax(self.unfrm)/1000)
                self.ordinate = np.multiply( self.lmbd, np.exp( np.multiply( self.absciss, -self.lmbd )))
                l = ax.plot(self.absciss, self.ordinate, 'r-', linewidth=1)
                
                #r = ax.plot( bins, np.ones_like(bins), 'go' )
                #q = ax.plot( n, n, 'b^')#np.zeros_like(n), 'b^')

                self.unfrm.sort()
                #print( self.unfrm )

                self.expDrawString = ""
                ##self.expDrawList = [str(i) for i in self.unfrm]
                for i in self.unfrm:
                    self.expDrawString += str(i)
                    self.expDrawString += " "

                #print self.expDrawString

                self.drawResults.set(self.expDrawString)

                # заполнение данных для 2й части работы
                # Числовые характеристики
                mean = np.mean(self.unfrm)
                variance = np.var(self.unfrm)

                self.lb_charss.delete(0, 'end')
                self.lb_charss.insert('end', 1/self.lmbd )
                self.lb_charss.insert('end', mean )
                self.lb_charss.insert('end', abs(1/self.lmbd - mean) )
                self.lb_charss.insert('end', 1/(self.lmbd*self.lmbd) )
                self.lb_charss.insert('end', variance )
                self.lb_charss.insert('end', abs(1/(self.lmbd*self.lmbd) - variance) )
                self.lb_charss.insert('end', np.median(self.unfrm) )
                self.lb_charss.insert('end', np.ptp(self.unfrm) )

                # Таблица
                beans = np.add( bins, (bins[1]-bins[0])*0.5 )
                beans = beans[0:-1]
                
                k=0
                self.lb_table1.delete(0,'end')
                self.lb_table2.delete(0,'end')
                self.lb_table3.delete(0,'end')
                self.distfunc = np.multiply( self.lmbd, np.exp( np.multiply( beans, -self.lmbd )))
                for i in beans :
                    self.lb_table1.insert('end', i )
                    self.lb_table2.insert('end', self.distfunc[k] )
                    self.lb_table3.insert('end', n[k] )
                    k += 1
                ## подсчёт невязки
                self.distfunc = np.abs(self.distfunc - n)
                maxmod = np.amax(self.distfunc)
                
                #self.l_result['text'] = u"Невязка: " + str( maxmod ) см. ниже

                pj = lambda j: np.exp(-bins[j]*self.lmbd)-np.exp(-bins[j+1]*self.lmbd)
                probs = [ pj(j) for j in xrange(self.qty)]
                self.expDrawString = ""
                for i in probs:
                    self.expDrawString += str(i)
                    self.expDrawString += " "

                self.probabilityes.set(self.expDrawString )
                    
                #print len(probs), len(n)
                #print bins[0:3], '\n', probs, '\n', n, (bins[1]-bins[0]) * n[0], (bins[1]-bins[0]) *n[1]
                statistic = np.sum(np.divide(np.square(n-probs), probs ))
                #print statistic
                                      
                ##statistic = 
                # calculating an integral of normal PDF ( n, sqrt(2*n))
                # here n is self.qty
                # fetching n
                self.qty = int( self.e_qty.get() ) - 1
                # integration bounds are based on 3 sigma rule
                start = self.qty - 3*np.sqrt(2*self.qty)
                #end = self.qty + 3*np.sqrt(2 *self.qty)
                print start, statistic
                if statistic > start :
                    end = self.qty + 3*np.sqrt(2*self.qty)
                    if statistic < end : end = statistic
                    self.absciss = np.arange(start, end, 0.01 )
                    # integration itself
                    PDF = np.divide(np.exp( np.divide( np.square(self.absciss - self.qty), -4*self.qty ) ), 2*np.sqrt(np.pi*self.qty))
                    
                    criteria = 1 - np.trapz( PDF, dx = 0.01 )
                    if criteria > float(self.e_hyp_param.get()):
                        self.l_result['text'] = u"Невязка: " + str( maxmod ) + u' Значение ф-ии распределения: ' + str( criteria )\
                                                + u'\nГипотеза не отвергнута'
                    else: self.l_result['text'] = u"Невязка: " + str( maxmod ) + u' Значение ф-ии распределения: ' + str( criteria )\
                                                + u'\nГипотеза отвергнута'
                    print criteria

                else: self.l_result['text'] = u"Невязка: " + str( maxmod ) + u' Значение ф-ии распределения: 1'\
                                                + u'\nГипотеза не отвергнута'
                
                
                ax.set_xlabel('x')
                ax.set_ylabel(u"Distribution function")
                #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
                ax.grid(True)

                plt.show()
                plt.close()
               
##        def btn2Click( self ): #, event ):
##                self.myParent.destroy()
    def OnTblScroll(self, *args):
        self.lb_table1.yview(*args)
        self.lb_table2.yview(*args)
        self.lb_table3.yview(*args)

    def OnMouseWheel(self, event):
         self.lb_table1.yview("scroll", event.delta,"units")
         self.lb_table2.yview("scroll", event.delta,"units")
         self.lb_table3.yview("scroll", event.delta,"units")
         # this prevents default bindings from firing, which
         # would end up scrolling the widget twice
         return "break"

    def btnLaunchClick_a( self, event ):
                #print "hello!"
                self.btnLaunchClick()

root = Tk()
myapp = MyApp(root)
root.resizable( False, False )
root.title( "PT lab")
root.mainloop()
