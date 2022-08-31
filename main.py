from pynput import keyboard as k, mouse as m
import globals as gl
import bot as b
import gui as g
from win32gui import GetWindowText, GetForegroundWindow

def main():
    def process_queue():
        if not gl.popQ.running:
            return
        if not gl.popQ.empty():
            msg = gl.popQ.MyGet()
            if msg == "home":
                bot_update_gui1 = g.DofusBotInterface(mode="update")
                bot_update_gui1.mainloop()
                if bot_update_gui1.data:
                    x_pos = int(bot_update_gui1.data[0])
                    y_pos = int(bot_update_gui1.data[1])
                    dofus_bot.set_pos((x_pos, y_pos))
                
            elif msg == "end":
                bot_update_gui2 = g.DofusBotInterface()
                bot_update_gui2.mainloop()
                if bot_update_gui2.data:
                    x_dest = int(bot_update_gui2.data[0])
                    y_dest = int(bot_update_gui2.data[1])
                    dofus_bot.set_dest((x_dest, y_dest))
                    dofus_bot.automate_travel()
            
            elif msg == "pos":
                g.AutoCloseMessageBox(dofus_bot.character_name, f"X = {dofus_bot.x_pos}    Y = {dofus_bot.y_pos}", 1)

            elif msg == "rec":
                g.AutoCloseMessageBox(dofus_bot.character_name, "Enregistrement des clics", 1)
                dofus_bot.creation_start()
            
            elif msg == "stopRec":
                dofus_bot.creation_stop()                
                confirm_append = g.ConfirmBox(dofus_bot.character_name)
                confirm_append.mainloop()
                if confirm_append.value:
                    with open(dofus_bot.maps_file, 'a') as f:
                        to_append = str((dofus_bot.x_pos, dofus_bot.y_pos)) + ":" + dofus_bot.click_coords + "\n"
                        f.write(to_append)
                    g.AutoCloseMessageBox(dofus_bot.character_name, 'Coordonnées de clic ajoutées', 1)
                else:
                    g.AutoCloseMessageBox(dofus_bot.character_name, 'Coordonnées de clic supprimées', 1)
                dofus_bot.click_coords = ""

            elif msg == "interrup":
                g.AutoCloseMessageBox(dofus_bot.character_name, 'Action interrompue', 1)
            
            elif msg == "askQuit":
                confirm_exit = g.ConfirmBox(dofus_bot.character_name)
                confirm_exit.mainloop()
                if confirm_exit.value:
                    g.AutoCloseMessageBox(dofus_bot.character_name, "A la prochaine fois !", 1.5)
                    gl.popQ.running = False
                    dofus_bot.exit()
                    klistener.stop()
            
            elif msg == "endTr":
                g.AutoCloseMessageBox(dofus_bot.character_name, "Trajet fini", 1)

            elif msg == "noMap":
                g.AutoCloseMessageBox(dofus_bot.character_name, "Map non répertoriée", 1)

            gl.popQ.open = True


    def on_press(key):
        if dofus_bot.character_name.lower() in GetWindowText(GetForegroundWindow()).lower():
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
            dofus_bot.travel_stop()
            gl.popQ.MyPut("home")
            gl.popQ.open = False
        elif key == k.Key.end:
            dofus_bot.travel_start()
            gl.popQ.MyPut("end")
            gl.popQ.open = False
        elif key == k.Key.f1:
            gl.popQ.MyPut("pos")
            gl.popQ.open = False
        elif key == k.Key.f2:
            if not dofus_bot.creating:
                gl.popQ.MyPut("rec")
                gl.popQ.open = False
            else:
                gl.popQ.MyPut("stopRec")
                gl.popQ.open = False
        elif key == k.Key.f3:
            dofus_bot.farming_start()
        elif key == k.Key.f4:
            if dofus_bot.creating or dofus_bot.traveling or dofus_bot.farming:
                dofus_bot.cancel_flag = True
                dofus_bot.reset()
                dofus_bot.cancel_flag = False
                dofus_bot.travel_stop()
                dofus_bot.creation_stop()
                dofus_bot.farming_stop()
                gl.popQ.MyPut("interrup")
                gl.popQ.open = False
        elif key == k.Key.f5:
            gl.popQ.MyPut("askQuit")
            gl.popQ.open = False
        elif key==k.Key.f6:
            gl.popQ.MyPut("cmd")
            gl.popQ.open = False


    bot_init_gui = g.DofusBotInterface(mode="init")
    bot_init_gui.mainloop()
    if bot_init_gui.data:
        dofus_bot = b.DofusBot(char_name=bot_init_gui.data[0] ,x_pos=int(bot_init_gui.data[1]), y_pos=int(bot_init_gui.data[2]))
    else:
        exit()

    with k.Listener(on_press=on_press) as klistener:
        while gl.popQ.running:
            process_queue()
        klistener.join()
        exit()


if __name__ == '__main__':
    main()
