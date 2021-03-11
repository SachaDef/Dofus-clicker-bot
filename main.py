from tkinter import *
from pynput import mouse as m
from pynput import keyboard as k
from MainBot.main_gui import *
from MainBot.main_bot import *


def move():

    def on_press(key):
        if AHK().active_window == AHK().find_window(title=b"Dofus"):
            print("Yes")
            if key == k.Key.left:
                dofus_bot.move_left()
            elif key == k.Key.right:
                dofus_bot.move_right()
            elif key == k.Key.up:
                dofus_bot.move_up()
            elif key == k.Key.down:
                dofus_bot.move_down()
            elif key == k.Key.delete:
                dofus_bot.reset()
        if key == k.Key.home:
            bot_update_gui1 = DofusBotInterface(init=True)
            bot_update_gui1.mainloop()
            if bot_update_gui1.data:
                x_pos = int(bot_update_gui1.data[0])
                y_pos = int(bot_update_gui1.data[1])
                dofus_bot.set_pos((x_pos, y_pos))
            dofus_bot.travel_stop()
        elif key == k.Key.end:
            dofus_bot.travel_start()
            bot_update_gui2 = DofusBotInterface(init=False)
            bot_update_gui2.mainloop()
            if bot_update_gui2.data:
                x_dest = int(bot_update_gui2.data[0])
                y_dest = int(bot_update_gui2.data[1])
                dofus_bot.set_dest((x_dest, y_dest))
                dofus_bot.automate_travel()
                AutoCloseMessageBox("Dofus TravelBot", "Trajet fini", 1)
            dofus_bot.travel_stop()
        elif key == k.Key.f1:
            AutoCloseMessageBox("Dofus TravelBot", f"X = {dofus_bot.x_pos}    Y = {dofus_bot.y_pos}", 1)
        elif key == k.Key.f2:
            if not dofus_bot.map_creation_running:
                AutoCloseMessageBox("Dofus MapMakingBot", "Enregistrement des clics", 1)
                dofus_bot.map_creation_start()
            else:
                if dofus_bot.append_map_clicks():
                    AutoCloseMessageBox('Dofus MapMakingBot', 'Coordonnées de clic ajoutées', 1)
                else:
                    AutoCloseMessageBox('Dofus MapMakingBot', 'Coordonnées de clic supprimées', 1)
                dofus_bot.map_creation_stop()
        if key == k.Key.f3:
            confirm_exit = ConfirmBox()
            confirm_exit.mainloop()
            if confirm_exit.value:
                dofus_bot.exit()
                klistener.stop()
                mlistener.stop()

    def on_click(x, y, button, pressed):
        if dofus_bot.map_creation_running:
            if pressed:
                dofus_bot.mouse_coords.append((x, y))

    bot_init_gui = DofusBotInterface(init=True)
    bot_init_gui.mainloop()
    if bot_init_gui.data:
        dofus_bot = DofusBot(x_pos=int(bot_init_gui.data[0]), y_pos=int(bot_init_gui.data[1]))

    with k.Listener(on_press=on_press) as klistener:
        with m.Listener(on_click=on_click) as mlistener:
            mlistener.join()
        klistener.join()


move()
