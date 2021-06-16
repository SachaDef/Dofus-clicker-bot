# from pynput import mouse as m
from pynput import keyboard as k
from main_bot.main_gui import DofusBotInterface
from main_bot.main_bot import *
from utilities.message_boxes import AutoCloseMessageBox, ConfirmBox


def main():

    def on_press(key):
        if dofus_bot.character_name in GetWindowText(GetForegroundWindow()):
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
            bot_update_gui1 = DofusBotInterface(mode="update")
            bot_update_gui1.mainloop()
            if bot_update_gui1.data:
                x_pos = int(bot_update_gui1.data[0])
                y_pos = int(bot_update_gui1.data[1])
                dofus_bot.set_pos((x_pos, y_pos))
            dofus_bot.travel_stop()
        elif key == k.Key.end:
            dofus_bot.travel_start()
            bot_update_gui2 = DofusBotInterface()
            bot_update_gui2.mainloop()
            if bot_update_gui2.data:
                x_dest = int(bot_update_gui2.data[0])
                y_dest = int(bot_update_gui2.data[1])
                dofus_bot.set_dest((x_dest, y_dest))
                dofus_bot.automate_travel()
                # AutoCloseMessageBox(dofus_bot.character_name, "Trajet fini", 1)
            # dofus_bot.travel_stop()
        elif key == k.Key.f1:
            AutoCloseMessageBox(dofus_bot.character_name, f"X = {dofus_bot.x_pos}    Y = {dofus_bot.y_pos}", 1)
        elif key == k.Key.f2:
            if not dofus_bot.creating:
                AutoCloseMessageBox(dofus_bot.character_name, "Enregistrement des clics", 1)
                dofus_bot.creation_start()
            else:
                if dofus_bot.append_map_clicks():
                    AutoCloseMessageBox(dofus_bot.character_name, 'Coordonnées de clic ajoutées', 1)
                else:
                    AutoCloseMessageBox(dofus_bot.character_name, 'Coordonnées de clic supprimées', 1)
                dofus_bot.creation_stop()
        elif key == k.Key.f3:
            if dofus_bot.creating or dofus_bot.traveling:
                dofus_bot.cancel_flag = True
                dofus_bot.reset()
                dofus_bot.cancel_flag = False
                dofus_bot.travel_stop()
                dofus_bot.creation_stop()
                AutoCloseMessageBox(dofus_bot.character_name, 'Action interrompue', 1)
        elif key == k.Key.f4:
            confirm_exit = ConfirmBox(dofus_bot.character_name)
            confirm_exit.mainloop()
            if confirm_exit.value:
                AutoCloseMessageBox(dofus_bot.character_name, "A la prochaine fois !", 1.5)
                dofus_bot.exit()
                klistener.stop()
                # mlistener.stop()

    # def on_click(x, y, _, pressed):
    #     if dofus_bot.creating:
    #         if pressed:
    #             dofus_bot.click_coords.append((x, y))

    bot_init_gui = DofusBotInterface(mode="init")
    bot_init_gui.mainloop()
    if bot_init_gui.data:
        dofus_bot = DofusBot(char_name=bot_init_gui.data[0] ,x_pos=int(bot_init_gui.data[1]), y_pos=int(bot_init_gui.data[2]))
    else:
        # dofus_bot = DofusBot(char_name=bot_init_gui.data[0], x_pos=0, y_pos=0)
        exit()

    with k.Listener(on_press=on_press) as klistener:
        # with m.Listener(on_click=on_click) as mlistener:
        #     mlistener.join()
        klistener.join()

if __name__ == '__main__':
    main()
