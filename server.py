import socket
from threading import Thread
import json
import time


clients = []  # ارایه برای نگهداری کلاینت ها
cnt = 0  # برای شمارش تعداد کالینت ها


def recving(csoc):  # تابع برای گرفتن داده از قابل جیسون
    try:
        b = csoc.recv(1024)
        return json.loads(b.decode('utf-8'))
    except socket.error as e:
        print(e)


def sending(csoc, msg):  # تابع برای ارسال پیام در قالب جیسون
    try:
        csoc.sendall(json.dumps(msg).encode("utf-8"))
    except socket.error as e:
        print(e)


# تابع برای ارسال پیام به تمام کلاینت‌ها
def send_to_all_clients(msg):
    for csoc in clients:
        sending(csoc, msg)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("127.0.0.1", 8000))
soc.listen(2)
print('listening....')
####################################################################################################
#############################################################################
#                                                                           #
#             تابع برای ذخیره داده های بازی ها در یک فایل متنی          #
#                                                                           #
#############################################################################


def save_to_file(text):
    with open("game_history.txt", "a") as file:
        file.write(text + "\n")

#############################################################################
#                                                                           #
#                 ساخت کلاس برای ساخت ابجکت جادو گران                     #
#                                                                           #
#############################################################################


class Wizard:
    def __init__(self, name, health, magic, magic_attack, physical_attack, defense, magic_charge):
        self.name = name  # اسم جادوگر
        self.health = health  # سلامتی جادوگر
        self.magic = magic  # میزان جادو جادوگر
        # حداکثر میزان جادو باری اینکه در هنگام شارژ شدن جادو ، بیشتر از مقدار اولیه نشود
        self.max_magic = magic
        self.magic_attack = magic_attack  # میزان قدرت حمله جادو
        self.physical_attack = physical_attack  # میزان قدرت حمله فیزیکی
        self.defense = defense  # میزان قدرت دفاع کردن
        self.magic_charge = magic_charge  # نرخ شارژ جادو برای هر راند جدید بازی
        self.move = None  # نوع حرکت جادوگر

    def fill_magic(self):  # تابع برای شارژ کردن جادو به میزان نرخ شارژ جادو
        self.magic += self.magic_charge
        if self.magic > self.max_magic:  # اگر جادو از میزان ماکسیمم جادو بیشتر بود ، برابر با ماکسیم قرار میگیره
            self.magic = self.max_magic

    def set_move(self, move):  # تابع برای گرفتن حرکت بازی کن و قرار دادن ان با متغییر حرکت جادوگر
        self.move = move

    # تابع  برای نبرد جادو گر که ورودی ابجکت جادوگر مقابل مییگره برای دسترسی به مقادیر حریف
    def attack(self, opponent):
        if self.move == "magic":  # اگه حرکت ما از نوع جادو بود
            if opponent.move == "defense":  # و حریف دفاع کرده بود
                damage = self.magic_attack  # قدرت جادوم در یک متغیر میریزم
                enemy_defense = opponent.defense  # و قدرت دفاع حریف در متغیر دیگر
                if damage - enemy_defense >= 0:  # اگر قدرت حمله ما پس از کسر با قدرت دفاع دشمن بزرگتر مساوی 0 بود
                    # سامتی دشمن از باقی مانده قدرت حمله کم میکینم
                    opponent.health -= (damage - enemy_defense)
                # و به میزان قدرت حلمه از میزان جادوی خودت کم میکنیم
                self.magic -= self.magic_attack
            else:  # در غیر این صورت گه دشمن دفاع نکرده بود
                damage = self.magic_attack  # قدرت جادوم در یک متغیر میریزم
                opponent.health -= damage  # و سلامتی دشمن به اندازه قدرت حمله کم میکنیم
                # و در اخر از میزان جادو به اندازه قدرت جادو کم میکنیم
                self.magic -= self.magic_attack
        elif self.move == "physical":  # اگه حمله ما از نوع فیزیکی بود
            if opponent.move == "defense":  # و حریف دفاع کرده بود
                damage = self.physical_attack  # قدرت فیزیکی در یک متغیر میریزم
                enemy_defense = opponent.defense  # و قدرت دفاع حریف در متغیر دیگر
                if damage - enemy_defense >= 0:  # اگر قدرت حمله ما پس از کسر با قدرت دفاع دشمن بزرگتر مساوی 0 بود
                    # سامتی دشمن از باقی مانده قدرت حمله کم میکینم
                    opponent.health -= (damage - enemy_defense)
            else:  # در غیر این صورت گه دشمن دفاع نکرده بود
                damage = self.physical_attack  # قدرت فیزیکی در یک متغیر میریزم
                opponent.health -= damage  # و سلامتی دشمن به اندازه قدرت حمله کم میکنیم
        # else:
        #     print("Invalid move!")
        #     save_to_file("Invalid move!")
        #     return
        #
        #                          در غیر این صورت اگه ما دفاع انتخواب کرده بودیم ، منتظر انتخواب حرکت دشمن میمونیم
        #

    def is_alive(self):  # تابع برای برسی انیکه کارکتر هنوز زنده هست یا نع
        return self.health > 0


#############################################################################
#                                                                           #
#         ساخت دیکشنری اولیه برای ساخت ارسال داده به کلاینت ها           #
#                                                                           #
#############################################################################
msg = {
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

#############################################################################
#                                                                           #
#               تابع برای ساخت ابجکت کاراتر های بازی بر                  #
#                اساس انتخواب سه گزینه 1 تا 3                             #
#               که کاراکتر ها به صورت دستی تعریف شده است                 #
#                                                                           #
#############################################################################


def select_character(character_choice):
    if character_choice == "1":
        character = Wizard("The Elves Wizard", 100, 100, 30, 20, 25, 7)
    elif character_choice == "2":
        character = Wizard("The Undead Wizard", 100, 100, 25, 35, 30, 5)
    elif character_choice == "3":
        character = Wizard("The Human Wizard", 100, 100, 20, 40, 30, 3)
    else:
        raise ValueError(
            "Invalid character choice. Please enter a valid character number.")

    return character  # بر گشت ابحکت کارکتر ساخته شده


#############################################################################
#                                                                           #
#          گزینه های حرکت بازی کن ها به عنوان یک دیکشنری                 #
#                                                                           #
#############################################################################
options = {
    "1": "magic",
    "2": "physical",
    "3": "defense"
}

#############################################################################
#                                                                           #
#    ساخت تابع بازی و وردی تابع از نوع کلاینت ها برای دو بازی کن هست     #
#                                                                           #
#############################################################################


def play_game(client1, client2):
    global msg  # قرار دادن دیکشنری به صورت گلوبال برای تغیرر مقدار اعضای دیکشنری در طول بازی

    # بعد از ورود کلینت دوم مقدار جدید برای عوض کردن صفحه بازی کن ها در
    msg['page'] = 'new'
    #                                                        دیکشنری قرار میگیرد که در کلاینت ها پس از دریاقت توسط دستور شرطی بررسی شده و صفحه جدید میسازد
    send_to_all_clients(msg)  # ازسال پیام به تمام کلاینته ها
    print("--- New Game ---")
    save_to_file("--- New Game ---")  # ذخیره شروع بازی در فایل متنی
    print("Enter Player 1's name: ")
    # دریافت داده های کاینت اول برای انتخواب کارکتر و تععین اسم خود
    player1_name_choice = recving(client1)
    # گرفتن اسم بازی کن اول از قایل دریافتی و قرار دادن در متغیر
    player1_name = player1_name_choice['name']
    # گرقتن انتخواب کارتر بازی کن اول و قرار دادن در متغیر
    player1_choice = player1_name_choice['choice']
    save_to_file("Enter Player 1's name: ")  # ذخیره در فایل
    save_to_file('---------')  # ذخیره در فایل
    save_to_file(player1_name)  # ذخیره در فایل
    save_to_file('---------')  # ذخیره در فایل
    # ساخت ابجکت کاراکتر بازی کن اول با قرار دادن مقدار انتخواب که بین  0 تا 1 هست در تابع سازنده کاراکتر ها
    player1_character = select_character(player1_choice)

    print("Enter Player 2's name: ")
    # دریافت داده های کاینت دوم برای انتخواب کارکتر و تععین اسم خود
    player2_name_choice = recving(client2)
    # گرفتن اسم بازی کن دوم از قایل دریافتی و قرار دادن در متغیر
    player2_name = player2_name_choice['name']
    # گرقتن انتخواب کارتر بازی کن دوم و قرار دادن در متغیر
    player2_choice = player2_name_choice['choice']
    save_to_file("Enter Player 2's name: ")  # ذخیره در فایل
    save_to_file('---------')  # ذخیره در فایل
    save_to_file(player2_name)  # ذخیره در فایل
    save_to_file('---------')  # ذخیره در فایل
    # ساخت ابجکت کاراکتر بازی دوم اول با قرار دادن مقدار انتخواب که بین  0 تا 1 هست در تابع سازنده کاراکتر ها
    player2_character = select_character(player2_choice)

    round_num = 1  # متغیر برای شمارش راند بازی ها که از 1 شروع میشود
    #
    #
    #                                 این قسمت مقادیر بدست امده شمامل نام بازی کن ها و کاراتر ها و شماره راند
    #                                      یکبار برای کلاینت ها برای جلوگیری از مشکل قبل از حلقه نبرد بازی میفرستیم
    msg["page"] = 'new'  # صفحه نبرد بازی قرار میدیم
    msg['rund'] = round_num  # شماره راند بازی
    msg["player1"] = player1_name  # اسم بازی کن اول
    # میزان سلامتی کارکتر بازی کن اول
    msg["player1_helth"] = player1_character.health
    msg["player1_mana"] = player1_character.magic  # میزن جادو کارکتر اول
    msg["player1_wizard"] = player1_character.name  # اسم کارکتر اول
    msg["player2"] = player2_name  # اسم بازی کن دوم
    # میزنا سلامتی کارکتر بازی کن دوم
    msg["player2_helth"] = player2_character.health
    msg["player2_mana"] = player2_character.magic  # میزان جادو کارتر دوم
    msg["player2_wizard"] = player2_character.name  # اسم کاراتر بازی کن دوم
    send_to_all_clients(msg)  # ارسال به همه کلاینت ها


#########################################################################################
#                                                                                      #
#           شروع حلقه بازی در تابع بازی ، که تا وقت هر دو بازیکن زنده هستن        #
#    ادامه دارد تا وقتی که یکی از بازی کن ها یا هردو بسوزند و حلقه شکسته میشود   #
#                                                                                     #
#######################################################################################
    while player1_character.is_alive() and player2_character.is_alive():
        #
        #    قرار دادن مقادیر اولیه هر راند بازی
        #    و تعیر صحفه بازی برای عوض شدن صفحه بازی کن ها
        #
        msg["page"] = 'battel'
        msg['rund'] = round_num
        msg["player1"] = player1_name
        msg["player1_helth"] = player1_character.health
        msg["player1_mana"] = player1_character.magic
        msg["player1_wizard"] = player1_character.name
        msg["player2"] = player2_name
        msg["player2_helth"] = player2_character.health
        msg["player2_mana"] = player2_character.magic
        msg["player2_wizard"] = player2_character.name

        send_to_all_clients(msg)  # ارسال برای همه کلاینت ها

        print(f"\n--- Round {round_num} ---")
        save_to_file(f"\n--- Round {round_num} ---")  # ذخیره در فایل
        print(
            f"{player1_name}: Health - {player1_character.health}, Magic - {player1_character.magic}")
        save_to_file(
            f"{player1_name}: Health - {player1_character.health}, Magic - {player1_character.magic}")  # ذخیره در فایل
        print(
            f"{player2_name}: Health - {player2_character.health}, Magic - {player2_character.magic}")
        save_to_file(
            f"{player2_name}: Health - {player2_character.health}, Magic - {player2_character.magic}")  # ذخیره در فایل

        # Player 1's turn
        print(f"\n{player1_name}, choose your move:")
        save_to_file(f"\n{player1_name}, choose your move:")  # ذخیره در فایل
        while True:# انتظار تا زمانی که بازی کن اول حرکت خود انتخواب کند
            choice_move = recving(client1) # دریافت حرکت کلاینت اول یعنی بازی کن اول
            move = choice_move['move']# قرار دادن میقدار دریافتی در یک متغیر 
            print(
                "1. Magic Attack\n2. Physical Attack\n3. Defense\nEnter the move number: ")
            save_to_file(
                "1. Magic Attack\n2. Physical Attack\n3. Defense\nEnter the move number: ")  # ذخیره در فایل
            save_to_file(move)  # ذخیره در فایل
            if move == "1" and player1_character.magic < player1_character.magic_attack: # اگر حرکت بازی کن حمله با جادو بود و میزان جادو کافی نیود حرکت نادیده میگیره تا حرکت مناسب انتخواب بشود
                print("Not enough magic. Choose another move.")
                # ذخیره در فایل
                save_to_file("Not enough magic. Choose another move.")
                save_to_file(move)  # ذخیره در فایل
            else:
                player1_character.set_move(options.get(move))# قرار دادن حرکت بازی کن و ست کردن با استفاده از  ، اول در دیکشنری اپشن تا مقدار به کلمه به دست بیاد و سپس ارسال به ابجکت کاراکتر توسط متد ذخیره حرکت
                break

        # Player 2's turn
        print(f"\n{player2_name}, choose your move:")
        save_to_file(f"\n{player2_name}, choose your move:")  # ذخیره در فایل
        while True:  # انتظار تا زمانی که بازی کن دوم حرکت خود انتخواب کند
            choice_move = recving(client2)# دریافت حرکت کلاینت دوم یعنی بازی کن دوم
            move = choice_move['move']  # قرار دادن مقدار دریافتی در یک متغیر
            print(
                "1. Magic Attack\n2. Physical Attack\n3. Defense\nEnter the move number: ")
            save_to_file(
                "1. Magic Attack\n2. Physical Attack\n3. Defense\nEnter the move number: ")  # ذخیره در فایل
            save_to_file(move)  # ذخیره در فایل
            if move == "1" and player2_character.magic < player2_character.magic_attack: # اگر حرکت بازی کن حمله با جادو بود و میزان جادو کافی نیود حرکت نادیده میگیره تا حرکت مناسب انتخواب بشود
                print("Not enough magic. Choose another move.")
                # ذخیره در فایل
                save_to_file("Not enough magic. Choose another move.")
                save_to_file(move)  # ذخیره در فایل
            else:
                player2_character.set_move(options.get(move))# قرار دادن حرکت بازی کن و ست کردن با استفاده از  ، اول در دیکشنری اپشن تا مقدار به کلمه به دست بیاد و سپس ارسال به ابجکت کاراکتر توسط متد ذخیره حرکت
                break

        # Battle
        time.sleep(0.5) # انتظار 500 میلی ثانیه در برنامه برای جلوگیر از خطا
        player1_character.attack(player2_character) # محاصبه نتیجه حرکت بازی کنان با ازتفاده از متد حمله در کلاس جادوگران
        player2_character.attack(player1_character)# محاصبه نتیجه حرکت بازی کنان با ازتفاده از متد حمله در کلاس جادوگران
        time.sleep(0.5)  # انتظار 500 میلی ثانیه در برنامه برای جلوگیر از خطا
        #
        #
        #                 تغیر صفحه به صفحه نتیه راند بازی
        #                 و قرار دادن مقادیر جدید بعد از نتیجه بدست امده از متد حمله
        #
        #
        msg["page"] = 'ressult'
        msg['rund'] = round_num
        msg["player1"] = player1_name
        msg["player1_helth"] = player1_character.health
        msg["player1_mana"] = player1_character.magic
        msg["player1_wizard"] = player1_character.name
        msg["player1_move"] = player1_character.move
        msg["player2"] = player2_name
        msg["player2_helth"] = player2_character.health
        msg["player2_mana"] = player2_character.magic
        msg["player2_wizard"] = player2_character.name
        msg["player2_move"] = player2_character.move
        send_to_all_clients(msg) #  ارسال به همه کلاینت ها

        print(f"\n--- Round {round_num} Result ---")
        save_to_file(f"\n--- Round {round_num} Result ---")  # ذخیره در فایل
        print(
            f"{player1_name}: Health - {player1_character.health}, Magic - {player1_character.magic}")
        save_to_file(
            f"{player1_name}: Health - {player1_character.health}, Magic - {player1_character.magic}")  # ذخیره در فایل
        print(f"Move: {player1_character.move}")
        save_to_file(f"Move: {player1_character.move}")  # ذخیره در فایل
        print()
        save_to_file("")  # ذخیره در فایل
        print(
            f"{player2_name}: Health - {player2_character.health}, Magic - {player2_character.magic}")
        save_to_file(
            f"{player2_name}: Health - {player2_character.health}, Magic - {player2_character.magic}")  # ذخیره در فایل
        print(f"Move: {player2_character.move}")
        save_to_file(f"Move: {player2_character.move}")  # ذخیره در فایل

        round_num += 1 #          افزایش متغیر نگهدارنده مقدار راند بازی به ا ندازه 1 واحد  
        player1_character.fill_magic() #      صدا زدن متد شارژ کارکتر ها برای افزایش میزان جادو قبل از راند بعدی
        player2_character.fill_magic()#      صدا زدن متد شارژ کارکتر ها برای افزایش میزان جادو قبل از راند بعدی
        time.sleep(5)#        استراحت بازی کنان قبل از راند جدید به میزان 5 ثانیه

    print("\n--- Game Over ---")
    save_to_file("\n--- Game Over ---")  # ذخیره در فایل


    if player1_character.is_alive() and not player2_character.is_alive(): # بررسی اینکه بازی کن اول زنده هست و بازی کن دوم سوخته که نیتجه برابر با پیروزی بازی کن اول هست
        msg['player1_wins!'] = "wins!"  # قرار دادن بازی کن اول به عنوان برنده
        msg['player2_wins!'] = "loser!"  # قرار دادن بازی کن دوم به عنوان بازنده
        send_to_all_clients(msg) # ارسال به همه کلاینت ها
        print(f"{player1_name} wins!")
        save_to_file(f"{player1_name} wins!")  # ذخیره در فایل
    elif player2_character.is_alive() and not player1_character.is_alive(): # بررسی اینکه بازی کن دوم زنده هست و بازی کن اول سوخته که نیتجه برابر با پیروزی بازی کن دوم هست
        msg['player2_wins!'] = "wins!"   # قرار دادن بازی کن دوم به عنوان برنده
        msg['player1_wins!'] = "loser!"  # قرار دادن بازی کن اول به عنوان بازنده
        send_to_all_clients(msg)
        print(f"{player2_name} wins!")
        save_to_file(f"{player2_name} wins!")  # ذخیره در فایل
    else:#                                                اگه هر دو بازی کن بسوزن نیجه بشه شرح زیر هست
        msg['player2_wins!'] = "It's a draw!!"#  مقدار نتیجه برای بازی کنان برابر مساوی هست
        msg['player1_wins!'] = "It's a draw!!"#  مقدار نتیجه برای بازی کنان برابر مساوی هست
        send_to_all_clients(msg) # ارسال به همه کلاینت ها
        print("It's a draw!")
        save_to_file("It's a draw!")  # ذخیره در فایل
    client1.close()# بعد از اتمام بازی سرور برای کلاینت ها بسته مشود
    client2.close()# بعد از اتمام بازی سرور برای کلاینت ها بسته مشود


#####################################################################################################
while True: # حلقه بی نهایت برای ذیرش کلاینت ها
    csoc, addr = soc.accept() # قبول کردن کلاینت ها
    clients.append(csoc) # اضافه کردن کلاینت جدید به لیست کلاینت ها
    clients[cnt].sendall(bytes('Hello from server', "utf-8")) # ارسال پیام خوشامد گویی به کلاینت ه 
    if len(clients) >= 2: # اگر تعداد کاینت ها دو نقر شد 
        Thread(target=play_game, args=(clients[0], clients[1])).start() # قرار دادن بازی در یک رشته و ارسال کلاینت ها به عنوان ارگومانت به تابع بازی

    cnt += 1 # برایش شمارش کلاینت ها 
