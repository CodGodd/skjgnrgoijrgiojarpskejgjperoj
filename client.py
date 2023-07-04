import socket
import json
from threading import Thread
import tkinter as tk
from tkinter import font

###############################################################################
#                                                                             #
#         ساخت دیکشنری برای ارسال دریافت و تبدیل فایل جیسون از سرور       #
#                                                                             #
###############################################################################
dataAll = {
    'page': 'wellcom',
    'rund': 0,
    'player1': '',
    'player2': '',
    'player1_wizard': '',
    'player2_wizard': '',
    'player1_helth': 0,
    'player2_helth': 0,
    'player1_mana': 0,
    'player2_mana': 0,
    'player1_move': '',
    'player2_move': '',
    'player1_wins!': '',
    'player2_wins!': ''
}

page = dataAll.get("page")
rund = dataAll.get('rund')
player1_name = dataAll.get('player1')
player2_name = dataAll.get('player2')
player1_wizard = dataAll.get('player1_wizard')
player2_wizard = dataAll.get('player2_wizard')
player1_helth = dataAll.get('player1_helth')
player2_helth = dataAll.get('player2_helth')
player1_mana = dataAll.get('player1_mana')
player2_mana = dataAll.get('player2_mana')
player1_move = dataAll.get('player1_move')
player2_move = dataAll.get('player2_move')
player1_wins = dataAll.get('player1_wins!')
player2_wins = dataAll.get('player2_wins!')

###############################################################################
#                                                                             #
#        تابع برای بروز رسانی صفحات بیج پس زا دریافت اطلاعت از سمت سرور    #
#                                                                             #
###############################################################################


def creat_page(page, rund, player1_name, player2_name, player1_wizard, player2_wizard, player1_helth, player2_helth, player1_mana, player2_mana, player1_move, player2_move, player1_wins, player2_wins):
    ###
    # صفحه خوشامد گویی
    ###
    if page == 'wellcom':
        print('wellcom')
        close_frame(wellcom, newgame, battle, ressult)
        wellcom.pack(side=tk.LEFT)
        wellcom.config()
    ###
    # صفحه انتخواب کارکتر و وارد کردن اسم
    ###
    elif page == 'new':
        print('new')
        close_frame(wellcom, newgame, battle, ressult)
        newgame.pack(side=tk.LEFT)
    ###
    # صفحه شروع نبرد
    ###
    elif page == "battel":
        print("battel")
        player1Helth = int((player1_helth * 40) / 100)
        if player1Helth <= 0:
            player1Helth = 1
        player1_helth_P.config(width=player1Helth)
        player1_helth_E.config(width=(40 - player1Helth))
        player1mana = int((player1_mana * 40) / 100)
        if player1mana <= 0:
            player1mana = 1
        player1_mana_P.config(width=player1mana)
        player1_mana_E.config(width=(40 - player1mana))
        #
        player2Helth = int((player2_helth * 40) / 100)
        if player2Helth <= 0:
            player2Helth = 1
        player2_helth_P.config(width=player2Helth)
        player2_helth_E.config(width=(40 - player2Helth))
        player2mana = int((player2_mana * 40) / 100)
        if player2mana <= 0:
            player2mana = 1
        player2_mana_P.config(width=player2mana)
        player2_mana_E.config(width=(40 - player2mana))
        player1_data.config(
            text=f'\nRound Game: {rund}\nPlayer 1 Name: {player1_name}\nPlayer 1 Wizard name: {player1_wizard}\nPlayer 1 Health: {player1_helth}\nPlayer 1 Mana: {player1_mana}')
        player2_data.config(
            text=f'\nRound Game: {rund}\nPlayer 2 Name: {player2_name}\nPlayer 2 Wizard name: {player2_wizard}\nPlayer 2 Health: {player2_helth}\nPlayer 2 Mana: {player2_mana}')
        close_frame(wellcom, newgame, battle, ressult)
        battle.pack(side=tk.LEFT)
    ###
    # صفحه نمایش نتیحه
    ###
    elif page == "ressult":
        print("ressult")
        player1Helth_ressult = int((player1_helth * 40) / 100)
        if player1Helth_ressult <= 0:
            player1Helth_ressult = 1
        player1_helth_P_ressult.config(width=player1Helth_ressult)
        player1_helth_E_ressult.config(width=(40 - player1Helth_ressult))
        player1mana_ressult = int((player1_mana * 40) / 100)
        if player1mana_ressult <= 0:
            player1mana_ressult = 1
        player1_mana_P_ressult.config(width=player1mana_ressult)
        player1_mana_E_ressult.config(width=(40 - player1mana_ressult))
        #
        player2Helth_ressult = int((player2_helth * 40) / 100)
        if player2Helth_ressult <= 0:
            player2Helth_ressult = 1
        player2_helth_P_ressult.config(width=player2Helth_ressult)
        player2_helth_E_ressult.config(width=(40 - player2Helth_ressult))
        player2mana_ressult = int((player2_mana * 40) / 100)
        if player2mana_ressult <= 0:
            player2mana_ressult = 1
        player2_mana_P_ressult.config(width=player2mana_ressult)
        player2_mana_E_ressult.config(width=(40 - player2mana_ressult))
        player1_data_ressult.config(
            text=f'\nRessult Of Round Game: {rund}\nPlayer 1 Name: {player1_name}\nPlayer 1 Wizard name: {player1_wizard}\nPlayer 1 Move : {player1_move}\nPlayer 1 Health: {player1_helth}\nPlayer 1 Mana: {player1_mana} \n  Player 1 is {player1_wins}')
        player2_data_ressult.config(
            text=f'\nRessult Of Round Game: {rund}\nPlayer 2 Name: {player2_name}\nPlayer 2 Wizard name: {player2_wizard}\nPlayer 2 Move : {player2_move}\nPlayer 2 Health: {player2_helth}\nPlayer 2 Mana: {player2_mana}\n  Player 2 is {player2_wins}')
        close_frame(wellcom, newgame, battle, ressult)
        ressult.pack(side=tk.LEFT)


###############################################################################
#                                                                             #
#                   تابع برای بستن فریم ها قبل                              #
#                                                                             #
###############################################################################
# تابع برای بستن فریم ها قبلی
def close_frame(wellcom, newgame, battle, ressult):
    wellcom.pack_forget()
    newgame.pack_forget()
    battle.pack_forget()
    ressult.pack_forget()


###############################################################################
#                                                                             #
#                tkinter   ایجاد صفحات با کتابخانه                          #
#                                                                             #
###############################################################################
# ایجاد یک نمونه از کلاس Tk
root = tk.Tk()
# تنظیم ابعاد صفحه
root.geometry("600x500")

###############################################################################
#                                                                             #
#               صفحه خوش آمدگویی و انتظار برای کلاینت دوم                   #
#                                                                             #
###############################################################################

# صفحه خوش آمدگویی و انتظار برای کلاینت دوم
wellcom = tk.Frame(root, width=600, height=500, bg="gray")

# اضافه کردن متن به فریم wellcom با فونت متوسط
welcome_label = tk.Label(
    wellcom, text="خوش آمدید به سرور \n انتظار برای کلاینت دوم", font=font.Font(size=12, weight="bold"))
welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

###############################################################################
#                                                                             #
#             ایجاد فریم انتخواب کاراکتر و تعیین اسم بازی کن              #
#                                                                             #
###############################################################################

# ایجاد فریم انتخواب کاراکتر و تعیین اسم بازی کن
newgame = tk.Frame(root, width=600, height=500, bg="gray")

# فریم ردیف بالای پنجره باری گزینه های انتخوابی و کادر ورودی و دکمه تایید
up = tk.Frame(newgame, width=600, height=100, bg="gray")
Uframe = tk.Frame(up)

# ایجاد ورودی نام
label_name = tk.Label(Uframe, text="نام:")
entry = tk.Entry(Uframe)

# ایجاد گزینه‌ها
var = tk.StringVar()
var.set(None)  # مقدار اولیه خالی
label_option = tk.Label(Uframe, text="گزینه:")
radio1 = tk.Radiobutton(Uframe, text="Elves", variable=var, value="1")
radio2 = tk.Radiobutton(Uframe, text="Undead", variable=var, value="2")
radio3 = tk.Radiobutton(Uframe, text="Human", variable=var, value="3")
#
#


# تابع ارسال نام و گزینه انتخوابی به سرور ، که درصورتی که نام و گزینه وارد شده باشه عمل میکند در غیر این صورت هیچ
def submit():
    # گرقتن نام در متغیر
    y = entry.get()
    # گرقتن گزینه انتخوابی در متغیر
    x = var.get()

    if len(y) > 0 and len(x) > 0 and x != "None":
        msg = {
            'name': y,
            'choice': x
        }
        # ارسال گزینه ها با استفاده از تابع ارسال به سرور
        sending(soc, msg)


# ایجاد دکمه ارسال
button = tk.Button(Uframe, text="ارسال", command=submit)

####################################################################
# فریم ردیف پایینی  برای نمایش اطاعات  کاراکتر ها یعنی همون سه جادوگر
down = tk.Frame(newgame, width=600, height=400, bg="gray")

# قریم سمت چپ
Dleft = tk.Frame(down, bg="gray")
# فریم ستمت وسط
Dcenter = tk.Frame(down, bg="gray")
# فریم سمت راست
Dright = tk.Frame(down, bg="gray")
# اضافه کردن متن به هر فریم
label1 = tk.Label(Dleft, text="1. The Elves Wizard\n   Magic Attack: 30\n   Physical Hit: 20\n   Defense: 25\n   Magic Charge: 7", height=200,
                  width=27, fg="black", bg="gray")
label2 = tk.Label(Dcenter, text="2. The Undead Wizard\n   Magic Attack: 25\n   Physical Hit: 35\n   Defense: 30\n   Magic Charge: 5", height=200,
                  width=27, fg="black", bg="gray")
label3 = tk.Label(Dright, text="3. The Human Wizard\n   Magic Attack: 20\n   Physical Hit: 40\n   Defense: 30\n   Magic Charge: 3", height=200,
                  width=27, fg="black", bg="gray")
#############################################################################
#                                                                           #
#                        ساخت  فریم ها صفحه انتخواب کاراتر و اسم         #
#                                                                           #
#############################################################################
up.pack(side=tk.TOP, fill=tk.X)
Uframe.pack(side=tk.TOP, pady=10)
label_name.pack(side=tk.LEFT)
entry.pack(side=tk.LEFT)
label_option.pack(side=tk.LEFT)
radio1.pack(side=tk.LEFT)
radio2.pack(side=tk.LEFT)
radio3.pack(side=tk.LEFT)
button.pack()
down.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
Dleft.pack(side=tk.LEFT, padx=0, pady=0)
Dcenter.pack(side=tk.LEFT, padx=0, pady=0)
Dright.pack(side=tk.LEFT, padx=0, pady=0)
label1.pack()
label2.pack()
label3.pack()
################################################################################################################
#
#
###############################################################################
#                                                                             #
#                      ایجاد فریم نبرد                                       #
#                                                                             #
###############################################################################
# ایجاد فریم نبرد
battle = tk.Frame(root, width=600, height=500, bg="gray")
#    ردیف نمایش اطلاعات دو بازی کن
row1 = tk.Frame(battle, width=600, height=450, bg="green")
###############################################################
# ساخت ستون نمایش اطاعات بازی کن اول سمت چپ رودف اول
player1 = tk.Frame(row1, width=300, height=450)
###############################################################
#
###############################################################

#  ساخت ردیف اویل برای نمایش  میزان سلامتی بازی کن اول

player1_row1 = tk.Frame(player1, height=50)
#  بروز رسانی سامتی بازی کن اول و تبدیل به بازه 0 تا 40 ، برای بهم نریختن نمایش نوار سلامتی
player1Helth = int((player1_helth * 40) / 100)
# اگه سلامتی کمتر از 1 بود برای بهم نریخت نوار سلامتی مقدار برابر با 1 قرار میدیم
if player1Helth <= 0:
    player1Helth = 1
# نوار سلامتی و متن سلامتی به عرض  متغیر بالا ذر بازه 0 تا 40
player1_helth_P = tk.Label(player1_row1, text="helth",
                           width=player1Helth, bg="red")
# ساخت نوار خاکساری باری پر کردن عرض ردیف نوار سلامتی که حاصل از تفاوت سالمتی با عدد 40 هست برای بهم نریخت ردیف سالمتی
player1_helth_E = tk.Label(player1_row1,
                           width=(40 - player1Helth), bg="gray")
#  یک فضای سیاه رنگ در انتهای ردیف سلامتی برای جدا کردن با بازی کن دیگر
spass1 = tk.Label(player1_row1, width=3, bg='black')

################################################################

# ساخت دریف دوم باری نمایش نوار میزان جادو با متن

player1_row2 = tk.Frame(player1, height=50)

#  بروز رسانی جادو بازی کن اول و تبدیل به بازه 0 تا 40 ، برای بهم نریختن نمایش نوار جادو
player1mana = int((player1_mana * 40) / 100)
# اگه جادو کمتر از 1 بود برای بهم نریخت نوار جادو مقدار برابر با 1 قرار میدیم
if player1mana <= 0:
    player1mana = 1
# نوار جادو و متن مانا به عرض  متغیر بالا ذر بازه 0 تا 40
player1_mana_P = tk.Label(player1_row2, text="mana",
                          width=player1mana, bg="blue")

# ساخت نوار خاکساری باری پر کردن عرض ردیف نوار جادو که حاصل از تفاوت سالمتی با عدد 40 هست برای بهم نریخت ردیف جادو
player1_mana_E = tk.Label(player1_row2,
                          width=(40 - player1mana), bg="gray")

#  یک فضای سیاه رنگ در انتهای ردیف مانا برای جدا کردن با بازی کن دیگر
spass2 = tk.Label(player1_row2, width=3, bg='black')
############################################################################################
# ساخت ردیف سوم برای نمایش اطاعات بازی کن اول
player1_row3 = tk.Frame(player1, height=50)
player1_data = tk.Label(
    player1_row3, text=f'\nRound Game: {rund}\nPlayer 1 Name: {player1_name}\nPlayer 1 Wizard name: {player1_wizard}\nPlayer 1 Health: {player1_helth}\nPlayer 1 Mana: {player1_mana}', width=42, height=27)
#############################################################################################
#
#
# ساخت ستون نمایش اطاعات بازی کن دوم سمت راست رودف اول
player2 = tk.Frame(row1, width=300, height=450)

####################################################
#  ساخت ردیف اویل برای نمایش  میزان سلامتی بازی کن دوم
player2_row1 = tk.Frame(player2,  height=50)
#  بروز رسانی سامتی بازی کن دوم و تبدیل به بازه 0 تا 40 ، برای بهم نریختن نمایش نوار سلامتی
player2Helth = int((player2_helth * 40) / 100)
# اگه سلامتی کمتر از 1 بود برای بهم نریخت نوار سلامتی مقدار برابر با 1 قرار میدیم
if player2Helth <= 0:
    player2Helth = 1
# نوار سلامتی و متن سلامتی به عرض  متغیر بالا ذر بازه 0 تا 40
player2_helth_P = tk.Label(player2_row1, text="helth",
                           width=player2Helth, bg="red")
# ساخت نوار خاکساری باری پر کردن عرض ردیف نوار سلامتی که حاصل از تفاوت سالمتی با عدد 40 هست برای بهم نریخت ردیف سالمتی
player2_helth_E = tk.Label(player2_row1,
                           width=(40 - player2Helth), bg="gray")
#  یک فضای سیاه رنگ در ابتدای ردیف سلامتی برای جدا کردن با بازی کن دیگر
spass3 = tk.Label(player2_row1, width=3, bg='black')
############################################################################################
# ساخت دریف دوم باری نمایش نوار میزان جادو با متن
player2_row2 = tk.Frame(player2, width=42, height=50)

#  بروز رسانی جادو بازی کن اول و تبدیل به بازه 0 تا 40 ، برای بهم نریختن نمایش نوار جادو
player2mana = int((player2_mana * 40) / 100)
# اگه سلامتی کمتر از 1 بود برای بهم نریخت نوار سلامتی مقدار برابر با 1 قرار میدیم
if player2mana <= 0:
    player2mana = 1
# نوار سلامتی و متن سلامتی به عرض  متغیر بالا ذر بازه 0 تا 40
player2_mana_P = tk.Label(player2_row2, text="mana",
                          width=player2mana, bg="blue")
# ساخت نوار خاکساری برای پر کردن عرض ردیف نوار جادو که حاصل از تفاوت سالمتی با عدد 40 هست برای بهم نریخت ردیف جادو
player2_mana_E = tk.Label(player2_row2,
                          width=(40 - player2mana), bg="gray")
#  یک فضای سیاه رنگ در ابتدای ردیف مانا برای جدا کردن با بازی کن دیگر
spass4 = tk.Label(player2_row2, width=3, bg='black')
############################################################################################
# ساخت ردیف سوم برای نمایش اطاعات بازی کن اول
player2_row3 = tk.Frame(player2, height=50)
player2_data = tk.Label(
    player2_row3, text=f'\nRound Game: {rund}\nPlayer 2 Name: {player2_name}\nPlayer 2 Wizard name: {player2_wizard}\nPlayer 2 Health: {player2_helth}\nPlayer 2 Mana: {player2_mana}', width=42, height=27)
################################################################################################
# ردیف سوم با ارتفاع 50 برای ساخت گزینه های نبرد و دکمه تایید انتخواب
row2 = tk.Frame(battle, width=600, height=50, )
# ایجاد گزینه‌ها
var2 = tk.StringVar()
var2.set(None)  # مقدار اولیه خالی
radio1 = tk.Radiobutton(row2, text="Magic Attack", variable=var2, value="1")
radio1.pack(side=tk.LEFT, padx=(130, 10,))
radio2 = tk.Radiobutton(row2, text="Physical Attack", variable=var2, value="2")
radio2.pack(side=tk.LEFT, padx=(0, 10))
radio3 = tk.Radiobutton(row2, text="Defense", variable=var2, value="3")
radio3.pack(side=tk.LEFT, padx=(0, 10))


# تابع برای گرفتن مقدار انتخوابی و ارسال به سرور
def sub():
    move = var2.get()
    # بررسی اینکه گزینه‌ای انتخاب شده است یا خیر
    if len(move) > 0 and move != "None":
        sending(soc, {'move': move})


# ایجاد دکمه
button = tk.Button(row2, text="تایید", command=sub)
#############################################################################
#                                                                           #
#                        ساخت  فریم ها صفحه نبرد کاراتر                   #
#                                                                           #
#############################################################################
button.pack(side=tk.LEFT, padx=(10, 130))
row1.pack(side='top')
row2.pack(side='bottom')
######################################
player1.pack(side=tk.LEFT)
player2.pack(side=tk.RIGHT)
###################################
player1_row1.pack(side=tk.TOP)
player2_row1.pack(side=tk.TOP)
player1_helth_P.pack(side=tk.LEFT)
player1_helth_E.pack(side=tk.LEFT)
spass1.pack(side=tk.RIGHT)
spass3.pack(side=tk.LEFT)
player2_helth_P.pack(side=tk.RIGHT)
player2_helth_E.pack(side=tk.LEFT)
#################################
player1_row3.pack(side=tk.BOTTOM)
player2_row3.pack(side=tk.BOTTOM)
##################################
player1_row2.pack(side=tk.BOTTOM)
player2_row2.pack(side=tk.BOTTOM)
player1_mana_P.pack(side=tk.LEFT)
player1_mana_E.pack(side=tk.LEFT)
spass2.pack(side=tk.RIGHT)
spass4.pack(side=tk.LEFT)
player2_mana_P.pack(side=tk.RIGHT)
player2_mana_E.pack(side=tk.LEFT)
######################################
player1_data.pack(side=tk.LEFT)
player2_data.pack(side=tk.LEFT)

#####################################################################################
#
###############################################################################
#                                                                             #
#                      ایجاد فریم نتیجه نبرد                                #
#                                                                             #
###############################################################################

# ایجاد فریم نتیجه
ressult = tk.Frame(root, width=600, height=500, bg="gray")
# ایجاد یک فریم برای نمایش نیجه دو بازی کن
row1_ressult = tk.Frame(ressult, width=600, height=450, bg="green")
#######################################################################################
#                                                                                     #
#       مشابه فریم صفحه نبرد با نام تغیر های متفاوت برای ساخت صفحه نتیجه بازی    #
#                                                                                     #
#######################################################################################
#
#                              نتیجه بازی کن اول  برای سلامتی
#
player1_ressult = tk.Frame(row1_ressult, width=300, height=450)

player1_row1_ressult = tk.Frame(player1_ressult, height=50)
player1Helth_ressult = int((player1_helth * 40) / 100)
if player1Helth_ressult <= 0:
    player1Helth_ressult = 1

player1_helth_P_ressult = tk.Label(player1_row1_ressult, text="helth",
                                   width=player1Helth_ressult, bg="red")
player1_helth_E_ressult = tk.Label(player1_row1_ressult,
                                   width=(40 - player1Helth_ressult), bg="gray")
spass1_ressult = tk.Label(player1_row1_ressult, width=2, bg='black')
#
#                              نتیجه بازی کن اول  برای جادو
#
player1_row2_ressult = tk.Frame(player1_ressult, height=50)
player1mana_ressult = int((player1_mana * 40) / 100)
if player1mana_ressult <= 0:
    player1mana_ressult = 1

player1_mana_P_ressult = tk.Label(player1_row2_ressult, text="mana",
                                  width=player1mana_ressult, bg="blue")
player1_mana_E_ressult = tk.Label(player1_row2_ressult,
                                  width=(40 - player1mana_ressult), bg="gray")
spass2_ressult = tk.Label(player1_row2_ressult, width=2, bg='black')
#
#                        اطاعات نتیجه بازی کن اول
#
player1_row3_ressult = tk.Frame(player1_ressult, height=50)
player1_data_ressult = tk.Label(
    player1_row3_ressult, text=f'\nRessult Of Round Game: {rund}\nPlayer 1 Name: {player1_name}\nPlayer 1 Wizard name: {player1_wizard}\nPlayer 1 Move : {player1_move}\nPlayer 1 Health: {player1_helth}\nPlayer 1 Mana: {player1_mana} \n  Player 1 {player1_wins}', width=42, height=27)
###############################################################
#
#                              نتیجه بازی کن دوم  برای سلامتی
#
player2_ressult = tk.Frame(row1_ressult, width=300, height=450)

player2_row1_ressult = tk.Frame(player2_ressult,  height=50)
player2Helth_ressult = int((player2_helth * 40) / 100)
if player2Helth_ressult <= 0:
    player2Helth_ressult = 1
player2_helth_P_ressult = tk.Label(player2_row1_ressult, text="helth",
                                   width=player2Helth_ressult, bg="red")
player2_helth_E_ressult = tk.Label(player2_row1_ressult,
                                   width=(40 - player2Helth_ressult), bg="gray")
spass3_ressult = tk.Label(player2_row1_ressult, width=2, bg='black')
#
#                              نتیجه بازی کن دوم  برای جادو
#
player2_row2_ressult = tk.Frame(player2_ressult, width=42, height=50)
player2mana_ressult = int((player2_mana * 40) / 100)
if player2mana_ressult <= 0:
    player2mana_ressult = 1
player2_mana_P_ressult = tk.Label(player2_row2_ressult, text="mana",
                                  width=player2mana_ressult, bg="blue")
player2_mana_E_ressult = tk.Label(player2_row2_ressult,
                                  width=(40 - player2mana_ressult), bg="gray")
spass4_ressult = tk.Label(player2_row2_ressult, width=2, bg='black')
#
#                        اطاعات نتیجه بازی کن اول
#
player2_row3_ressult = tk.Frame(player2_ressult, height=50)
player2_data_ressult = tk.Label(
    player2_row3_ressult, text=f'\nRessult Of Round Game: {rund}\nPlayer 2 Name: {player2_name}\nPlayer 2 Wizard name: {player2_wizard}\nPlayer 2 Move : {player2_move}\nPlayer 2 Health: {player2_helth}\nPlayer 2 Mana: {player2_mana}\n  Player 2 {player2_wins}', width=42, height=27)
########################################################################################################################
#############################################################################
#                                                                           #
#                 ساخت  فریم ها صفحه نتیجه نبرد کاراتر                   #
#                                                                           #
#############################################################################
row1_ressult.pack(side='top')
######################################
player1_ressult.pack(side=tk.LEFT)
player2_ressult.pack(side=tk.RIGHT)
###################################
player1_row1_ressult.pack(side=tk.TOP)
player2_row1_ressult.pack(side=tk.TOP)
player1_helth_P_ressult.pack(side=tk.LEFT)
player1_helth_E_ressult.pack(side=tk.LEFT)
spass1_ressult.pack(side=tk.RIGHT)
spass3_ressult.pack(side=tk.LEFT)
player2_helth_P_ressult.pack(side=tk.RIGHT)
player2_helth_E_ressult.pack(side=tk.LEFT)
#################################
player1_row3_ressult.pack(side=tk.BOTTOM)
player2_row3_ressult.pack(side=tk.BOTTOM)
##################################
player1_row2_ressult.pack(side=tk.BOTTOM)
player2_row2_ressult.pack(side=tk.BOTTOM)
player1_mana_P_ressult.pack(side=tk.LEFT)
player1_mana_E_ressult.pack(side=tk.LEFT)
spass2_ressult.pack(side=tk.RIGHT)
spass4_ressult.pack(side=tk.LEFT)
player2_mana_P_ressult.pack(side=tk.RIGHT)
player2_mana_E_ressult.pack(side=tk.LEFT)
######################################
player1_data_ressult.pack(side=tk.LEFT)
player2_data_ressult.pack(side=tk.LEFT)
#####################################################################################
#
#
#######################################################################################


# ساخت اولیه صفحه بازی در هنگام اجرای برنامه
creat_page(page, rund, player1_name, player2_name, player1_wizard, player2_wizard, player1_helth,
           player2_helth, player1_mana, player2_mana, player1_move, player2_move, player1_wins, player2_wins)
#################################################################

#############################################################################
#                                                                           #
#                تابع دریافت اطاعات از سرور به شکل                       #
#                             JSON                                          #
#############################################################################


def recving(csoc):
    # گلوبال قرار دادن متغییر های دیکشنری برای بروز رسانی توسط تابع
    global dataAll, page, rund, player1_name, player2_name, player1_wizard, player2_wizard, player1_helth, player2_helth, player1_mana, player2_mana, player1_move, player2_move, player1_wins, player2_wins
    #
    # ریخت صفحه فعلی در متغیر جدید بری بررسی اینکه صفحه جدید از سرور تغییر کرده یا نه
    lastPage = page
    while csoc:

        try:
            b = csoc.recv(1024)  # گرفتن داده ها از سرور
            dataAll = json.loads(b.decode('utf-8'))  # تبدیل تاده
            # بروز رسانی متغیر ها
            page = dataAll["page"]
            rund = dataAll['rund']
            player1_name = dataAll['player1']
            player2_name = dataAll['player2']
            player1_wizard = dataAll['player1_wizard']
            player2_wizard = dataAll['player2_wizard']
            player1_helth = dataAll['player1_helth']
            player2_helth = dataAll['player2_helth']
            player1_mana = dataAll['player1_mana']
            player2_mana = dataAll['player2_mana']
            player1_move = dataAll['player1_move']
            player2_move = dataAll['player2_move']
            player1_wins = dataAll['player1_wins!']
            player2_wins = dataAll['player2_wins!']
            #
            #              شرط برای اینکه اگه صفحه جدید که از سرور رسیده با صفحه  فعلی یکی نیست ، تابع ساخت صغحه ها برای بروز سانی صفحه صدا زده شه
            if page != lastPage:
                creat_page(page, rund, player1_name, player2_name, player1_wizard, player2_wizard, player1_helth,
                           player2_helth, player1_mana, player2_mana, player1_move, player2_move, player1_wins, player2_wins)

        except socket.error:
            break

#     تابع برای ارسال اطلاعات به شکل جی سان JSON


def sending(socket, data):
    message = json.dumps(data).encode('utf-8')
    socket.sendall(message)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(("127.0.0.1", 8000))
b = soc.recv(1024)
print(b.decode("utf-8"))


#            گوش دادن به  اطاعات دریافتی از سرور  و بروز رسانی مداوم
Thread(target=recving, args=(soc,)).start()
#####################################################################
#   tkinter  شروع حلقه کتاب خانه
root.mainloop()
