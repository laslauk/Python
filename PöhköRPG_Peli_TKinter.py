# Johdatus ohjelmointiin kurssin vapaa projektityö.

# 9.12.2016
# RPG Peli - Graafisen käyttöliittymän projektityö

# ****DOKUMENTAATIO*****

# PELI JA PELINKULKU:
# Kyseessä on "vuoropohjainen" taisteluroolipeli (action RPG), jossa tarkoituksea on selvitä mahdollisimman
# monta tasoa (level) vihollisia. Pelaajalla on käytösseen tavaroita (item) ja taikoja (magic/spells)

# Tavanomaisien roolipelien mukaisesti pelaajan hahmolla on atribuutteina:
#   > Health: Iskupisteet, joiden loputtua pelaaja häviää pelin.
#   > Mana: Taikavoimapisteet, jotka kuluvat kun pelaaja käyttää taikoja (spells).
#   > XP level: Kokemustaso, joka korottaa hahmon muita ominaisuuksiin ja joka kasvaa vihollisia voittamalla
#   > Attack dmg: Pelaajan kyky tehdä vahinkoa viholliseen ja vihollisen iskupisteisiin.

# Pelinäkymä:
#   > Vasen: Pelaajan hahmon tiedot, eli kaikki hänen atribuuttinsa: Health, mana, xp jne.
#   > Keskellä (ylä): Näkyvät kaikki kyseisen tason (levelin) viholliset ja niiden tiedot.
#   > Keskellä (keski): Pelaajan "actionbar", jonka kautta pelaaja ohjaa hahmoaan ja toimintojaan.
#   > Keskellä (ala): alhaalla on tapahtumalogi/konsoli, jolla ilmoitetaan pelaajalle pelin kulkuun liittyvää tietoa

#   > Oikealla: Oikealla voi olla joko lista pelaajan tavaroista tai taijoista
#               [Item] -nappia painamalla näkyy pelaajalle lista hänen tavaroistaan
#               [Magic] - nappia painamalla ikkuna vaihtuu
#               pelaajan näyttämään pelaajan käytössä olevat taijat


# Peli alkaa, kun pelaaja syöttää hahmolleen nimen ja painaa Start Game.
# Pelin alussa on pelaajan vuoro. Kun pelaaja hyökkää viholliseen [Attack]
# tai käyttää  taikalistasta [Magic] taijan, pelaajan vuoro siirtyy vastustajille.

# Vastustajan vuorolla kaikki hengissä olevat vastustajat hyökkäävät pelaajaan, jolloin pelaajan
# iskupisteistä (health) lähtee pois kaikkien vihollisten Dmg -tekstin ilmoittamien lukujen summa.
# Kun vastustajat ovat hyökänneet, siirtyy vuoro takaisin pelaajalle.

# Esimerkki: hengissä on 4 vihollista, joilla on kaikilla [Dmg: 1].
# Vihollisten vuoron loputtua pelaaja ottaa vahinkoa, eli menettää yhteensä 4 iskupistettä (health - 4).
# Jos pelaaja menettää kaikki iskupisteensä, peli loppuu.
# Jos pelaaja on päihittänyt kaikki kyseisen tason vastustajat, alkaa seuraava taso (level), jossa on uudet vastustajat.
# Tällä hetkellä vastustajat nousevat voimakkaammiksi ja niiden määrä kasvaa sattumanvaraisesti pelattavien tasojen noustessa.


# HYÖKKÄÄMINEN:
# Pelaaja voi hyökätä viholliseen painamalla ensin [Attack] -nappulaa ja sitten klikkaamalla keski-ikkunassa
# näkyvää vastustajan nimi-nappulaa eli vastustajan ikonia. Pelaaja voi peruuttaa hyökkäyksen painamalla uudestaan
# [Attack] -nappulaa, jolloin pelaaja ei menetä vuoroaan. Pelaajan hyökättyä vastustajaan, vuoro siirtyy vastustajille.

# Pelaaja voi käyttää taikoja, avaamalla ensin [Magic] -nappulasta listan ja valitsemallaan haluamansa taijan.
# Taika näkyy vihreänä, mikäli pelaajalla on tarpeeksi manaa ja punaisena, mikäli mana ei riitä kyseiseen taikaan.
# Taijan käytettyä pelaajan vuoro siirtyy vastustajille.

# Pelaaja voi käyttää samaantapaan tavaroita (item), klikkaamalla [Item] -nappulaa. Tavaroiden käyttö ei kuluta pelaajan vuoroa.

# Vuoronvaihto: 1. kun pelaaja käyttää attack
#               2. kun pelaaja käyttää magic

# HUOMIOITAVAA, Tässä versiossa tasojen vaihto ja taikojen käyttö on hieman epäselvää, koska
# pelaajalle ei anneta tarpeeksi visuaalista palautetta näiden tapahduttua. Esimerkiksi
# firestorm spelli saattaa tuhota kaikki viholliset, mutta kenttä vaihtuu liian nopeasti, että
# pelaaja ei ole varma tapahtuiko mitään.

#LYHYT VERSIO:
# Pelaaminen: 1. Paina [Attack], 2. Paina keskellä olevaa vihollisen nappulaa, 3. Item / magic avaa tavara- ja taikaluettelon.
# Viholliset hyökkäävät pelaajan vuoron loputtua ja tekevät damagea yhteensä kaikkien vihollisten dmg:n verran.





from tkinter import *
import random




class Game:

    def __init__(self):

        self.__game_gui = Tk()
        self.__game_gui.title("Pointless RPG")
        self.__current_level = 0
        self.__turn_counter = 0
        self.__turn = {
            "Player Turn" : 0,
            "Enemy Turn" : 1
        }
        self.__player_actionbars = []
        self.__currentTurn = 0

        # TODO: Parempi systeemi statsien hakuun
        # [0] name,[1] mana,[2] base_dmg,[3]
        # health,[4] spellbook, [5] xp, [6] xplvl
        self.__player_stats = []

        # Lists for elements in th game
        self.__enemy_icons = []
        self.__enemy_health_labels = []
        self.__enemy_damage_labels = []
        self.__level_enemies = []
        self.__player = Player(10,"DefaultName",10,10)
        self.__player_attacking = False

        # game views
        self.__StartView = Frame(self.__game_gui,bg="gray14")
        self.__CombatView = Frame(self.__game_gui,bg="gray24")
        self.__GameOverView = Frame(self.__game_gui,bg="gray14")

        # Create frames for each gameview
        for frame in (self.__StartView,self.__CombatView,self.__GameOverView):
            frame.grid(row=0,column=0,sticky='news')

        self.init_start_page()
        self.init_combat_view()
        self.rungame()

    def do_action(self,action):
        """
        Hoitaa actionbareista tulevat funktiopyynnöt.
        :param action: stringi suoritettavasta pelaajan toimenpiteestä

        """
        if action == "attack":
            if self.__currentTurn == self.__turn["Player Turn"]:
                if not self.__player_attacking:
                    self.__attackButton.configure(bg="yellow", text="Choose target...")
                    self.__player_attacking = True
                    print("Player is attacking")

                    for actionbar in self.__player_actionbars:
                        actionbar['state'] = DISABLED

                else:
                    self.__attackButton.configure(bg="blue", text="Attack")
                    self.__player_attacking = False
                    print("Player cancels attack")
                    for actionbar in self.__player_actionbars:
                        actionbar['state'] = NORMAL

        elif action == "skip":
            self.__console.insert(END,"Turn " + str(self.__turn_counter) + ":" + "Skipped turn! \n")
            self.__currentTurn = self.__turn["Enemy Turn"]
            self.__turn_counter += 1
            self.manage_turns()

        elif action == "magic":
            self.show_spellbook()

        elif action == "item":
            self.show_inventory()

    def use_item(self,item):
        """
        Hoitaa inventoryn itemeiden käytön.
        Kutsuu pelaajan use_inventory_item -funktiota, jossa itemin käyttöön
        liittyvät toimenpiteet suoritetaan. Hoitaa kirjoituksen pelin konsoliin.
        :param item: käytettävän tavaran nimi stringinä.
        """

        # info about used item to be outputted to the gameconsole
        item_info = self.__player.use_inventory_item(item)
        self.__console.insert(END,"Turn " + str(self.__turn_counter) + ": Used item: " + item + "\n")
        self.__console.insert(END,item_info + "\n")
        self.update_labels()

    def show_spellbook(self):
        """
        Rakentaa spellbookin perusteella listan kaikista spelleistä
        right_bar_frameen oikealle.
        Hoitaa pelaajan manan riittoisuuden ja disabloi taijat, joihin pelaajalla
        ei ole tarpeeksi manaa.
        """

        spellbook = self.__player_stats[4]
        self.clear_inventory_view()

        # Create spellbook menu
        # Structure: CombatView > right_bar_frame > canvas, scroll > subrame,spellFrame
        self.__right_bar_canvas = Canvas(self.__right_bar_frame, bg="gray24",width=140)
        self.__right_bar_subFrame = Frame(self.__right_bar_canvas,bg="black")
        self.__scroll = Scrollbar(self.__right_bar_frame,command=self.__right_bar_canvas.yview,bg="red")
        self.__right_bar_canvas.configure(yscrollcommand=self.__scroll.set)
        self.__right_bar_canvas.configure(scrollregion=(0, 0, 100, 120*len(spellbook)))
        self.__scroll.grid(row=1,column=1,sticky="news")
        self.__right_bar_canvas.bind('<MouseWheel>', self.mouse_wheel)
        self.__right_bar_canvas.grid(row=1,column=0)
        self.__right_bar_subFrame.grid(column=0,row=0)
        self.__right_bar_canvas.create_window((20, 4),
                                              window=self.__right_bar_subFrame,
                                              anchor="nw",
                                              tags="self.__right_bar_subFrame")

        paddingMultiplier = 0
        for spell in sorted(spellbook):
            print("Spellbook: " + spell + ": " + str(self.__player_stats[4][spell]))
            mana_cost = str(self.__player_stats[4][spell])
            self.__spell_frame = Frame(self.__right_bar_canvas,bg="gray14")
            self.__spell_frame.grid(row=paddingMultiplier)
            spell_icon = Button(self.__spell_frame, padx=5,pady=5, command=lambda name=spell: self.cast_spell(name))

            # Generate spell tooltips at labels
            label_text = "Placeholder spell for scrolling."
            if spell == "Firestorm":
                label_text = "Deals damage to all enemies. "
            elif spell == "Heal":
                label_text = "Restores health for player."
            elif spell =="Random bolt":
                label_text = "Goofy bolt of something that hits random target."

            spell_label = Label(self.__spell_frame,text=label_text,wraplength=100,pady=5,padx=5,fg="gray75",bg="gray20")
            spell_label.grid(row=1)

            if self.__player.get_mana() < spellbook[spell]:
                spell_icon.configure(bg="red",fg="white",state=DISABLED)

            else:
                spell_icon.configure(bg="forest green",fg="light cyan",state=NORMAL)

            spell_icon['text'] = spell +"\n "+ "manacost: " + mana_cost
            spell_icon.config(font=("Helvetica",8))
            spell_icon.grid(row=0,sticky=E+W,pady=5)

            self.__right_bar_canvas.create_window(15,105*paddingMultiplier,
                                                  window=self.__spell_frame,
                                                  anchor="nw")

            # Bind mousewheel to spell_icon and label to allow scrolling
            spell_icon.bind('<MouseWheel>', self.mouse_wheel)
            spell_label.bind('<MouseWheel>', self.mouse_wheel)
            paddingMultiplier +=1

    def cast_spell(self,spell_name):
        """
        Hoitaa spellien mekaniikat ja vaikutukset peliin.
        Spellien käyttämät arvot saadaan pelaaja-classilta use_spell -funktiolta, joka palauttaa kaksi arvoa:
        1. True tai False pelaajan manan riittävyyden mukaan.
        2. Jokin kokonaisluku, liittyen spellin toiminnallisuuteen
        :param spell_name: spellin nimi stringinä
        :return:
        """
        #TODO: turhan monta kertaa tarkistetaan onko manaa, Fix this
        # Check if player has the spell_name in spellbook
        if spell_name in self.__player.get_spellbook():

            if spell_name == "Firestorm":
                hasMana, spell_damage = self.__player.use_spell(spell_name)

                if hasMana:
                    self.__console.insert(END,"Turn " + str(self.__turn_counter) + ": " + self.__player.get_name() + " used firestorm! \n")

                    for enemy in self.__level_enemies:
                        enemy.damage(spell_damage)
                        self.__console.insert(END,"**Firestorm damaged: " +
                                              str(enemy.get_name()) + " for "
                                              +  str(spell_damage) + "\n")

                        indx = self.__level_enemies.index(enemy)
                        self.check_for_dead_enemies(indx)

                        # TODO: Some effects for spells

            elif spell_name == "Heal":
                hasMana,heal_amount = self.__player.use_spell(spell_name)
                self.__console.insert(END,"Turn " + str(self.__turn_counter) + ": "
                                      + " you healed yourself for "
                                      + str(heal_amount) + " hp! \n")
                self.update_labels()


            elif spell_name == "Random bolt":
                hasMana, spell_damage = self.__player.use_spell(spell_name)

                if hasMana:
                    # Get target that is alive
                    while True:
                        enemy = random.choice(self.__level_enemies)
                        if not enemy.is_dead():
                            break

                    target = self.__level_enemies.index(enemy)
                    enemy.damage(spell_damage)
                    self.check_for_dead_enemies(target)
                    self.__console.insert(END, "Turn " + str(
                        self.__turn_counter) + ": " + self.__player.get_name()
                                          + " used Random bolt! \n")

                    self.__console.insert(END, "**Random bolt damaged: " + str(
                        enemy.get_name()) + " for " + str(spell_damage) + "\n")
                    print("Random bolt target:" + str(target) + "/" + enemy.get_name())

            # Spell has no functionality yet
            else:
                print("No implementation found for spell:" + spell_name)

        #TODO: Single target spell
        #TODO: Click spell ja lukitsee kaikki muut
        #TODO: Vlitaan vihollinen ja tehdään asioita sille
        #TODO: STATUS EFFECTS

        else:
            print("Player has no mana")
            self.__middle_bar_frame.config(bg="gray14")

        self.__turn_counter += 1
        self.__currentTurn = self.__turn["Enemy Turn"]
        self.manage_turns()

    def mouse_wheel(self,event):
        """
        hiiren rullan toiminnallisuus kun käytetään linux/windows
        :param event: hiiren rullausevent, ylös tai alas
        """
        if event.num == 5 or event.delta == -120:
            self.__right_bar_canvas.yview('scroll', 1, 'units')
        if event.num == 4 or event.delta == 120:
            self.__right_bar_canvas.yview('scroll', -1, 'units')

    def clear_inventory_view(self):
        """
        Poistetaan oikeanpuoleinen inventory/spellbook näkymästä
        kaikki widgetit
        """
        for item in self.__right_bar_frame.grid_slaves():
            item.destroy()

    def show_inventory(self):
        """
        Rakentaa pelaajan omistamista itemeistä listan oikealle
        right_bar_frame:een.
        """
        #TODO: Scrollautuus kuten spelleille

        inventory = self.__player.get_inventory()
        for item in inventory:
            print(item)

        # Clear old inventory
        self.clear_inventory_view()

        # Create icon for each item
        for item in inventory:
            item_icon = Button(self.__right_bar_frame,bg="red",padx=5,pady=5,
                               command=lambda x=item:self.use_item(x))

            if item == "Mana Potion":
                item_icon.configure(text=item,bg="dodger blue",fg="ivory")
                item_icon.grid()

            elif item == "Healing Potion":
                item_icon.configure(text=item,bg="OrangeRed2",fg="gray3")
                item_icon.grid()

    # Handles enemy attacks on their turn
    # Checks after enemy attacks if player is dead, then game over screen if true
    def manage_turns(self):
        """
        Hoitaa vuorojen vaihdot ja vihollisten hyökkäämisen, kun pelaaja on lopettanut
        oman vuoronsa. Jos pelaaja kuolee vastustajien vuoron hyökkäykseen, lopettaa pelin.
        """

        self.update_player_stats()
        self.update_labels()

        self.__attackButton.configure(bg="blue", text="Attack")
        self.__player_attacking = False

        # Enemy turn to attack, change back to player turn
        if self.__currentTurn == self.__turn["Enemy Turn"]:
            all_are_dead = True

            for enemy in self.__level_enemies:
                # Enemies that are alive attacks

                if not enemy.is_dead():
                    all_are_dead = False
                    enemys_damage = enemy.get_damage()
                    self.__player.damage(enemys_damage)
                    self.__console.insert(END,"Turn "+ str(self.__turn_counter)+": "
                                          + enemy.get_name() + " attacked player for "
                                          + str(enemys_damage) + " dmg! \n")


            # Check if all enemies are dead, True: change level
            if all_are_dead:
                self.__console.insert(END,"Level {0} cleared!".format(self.__current_level))
                self.change_level(self.__current_level + 1)

            self.update_labels()
            print("Player health1:  " + str(self.__player.get_health()))

        self.__currentTurn = 0
        self.__turn_counter += 1

        if self.__player.is_dead():
            self.game_over_screen()

    # updates enemy labels in the level
    def update_enemy_labels(self):
        """
        Päivittää vihollisten kaikki niiden statsit
        """

        print("Päivitetään vihujen labelit")
        print("Iconit " + str(len(self.__enemy_icons)))
        print(self.__enemy_icons)
        print("Health " + str(len(self.__enemy_health_labels)))
        print("damage labers " + str(len(self.__enemy_damage_labels)))

        for enemy_icon in self.__enemy_icons:
            indx = self.__enemy_icons.index(enemy_icon)
            enemy = self.__level_enemies[indx]
            if enemy_icon.winfo_exists():
                self.__enemy_damage_labels[indx].configure(text="Dmg:" + str(enemy.get_damage()))
                self.__enemy_health_labels[indx].configure(text="Health: " + str(enemy.get_health()))

    def update_player_stats(self):
        """
        Päivitetään pelaajan statsmuuttujan tiedot
        """
        ##TODO: Parempi systeemi
        self.__player_stats = self.__player.get_stats()

    def update_labels(self):
        """
        Päivitetään kaikki pelinäkymässä olevat tekstien/labeliden ilmoittamat
        tiedot, vihollisten ja omien. Lisäksi poistetaan oikealla olevat mahdollinen
        inventory/spellbook näkymä.
        """

        print("Päivitetään labelit")
        self.__mana_label['text'] = "Mana: " + str(self.__player.get_mana())
        self.__health_label['text'] = "Health: " + str(self.__player.get_health())
        self.__name_label['text'] = self.__player.get_name()
        self.__plr_damage_label['text'] = "Attack dmg: " + str(self.__player_stats[2])
        self.__xp_level_label['text'] = "XP Level: " + str(self.__player.get_xp_level())
        self.clear_inventory_view()
        self.update_enemy_labels()

    def change_level(self,level):
        """
        Hoitaa levelien vaihtoon liittyvät asiat.
        Palauttaa pelaajalle hieman hp/mana.

        :param level: leveli, jolle halutaan siirtyä
        """
        self.__current_level = level
        self.__name_label = self.__player.get_name()
        self.__player.restore_hp(5)
        self.__player.restore_mana(1)
        print("changing level")
        self.__turn_counter = 0
        self.__currentTurn = 0
        self.init_combat_view()
        self.init_enemies(self.__current_level)
        self.__console.insert(END,"Level: {0} \n".format(self.__current_level))
        self.__console.insert(END,"HP: {0} left \n".
                              format(self.__player.get_health()))
        self.__attackButton.configure(bg="blue", text="Attack")
        self.__player_attacking = False

    # Kutsutaan kun tehdään vihollisiin jotakin
    def attack(self,target):
        """
        Funktio hoitaa attack -napilla suoritetut hyökkäykset
        :param target: kohdevihollisen indeksi
        """

        if self.__currentTurn == self.__turn["Player Turn"]:
            print("attacking target:" + str(target))

            if self.__player_attacking:
                enemy = self.__level_enemies[target]

                # Player attacked, unlock actionbars
                for actionbar in self.__player_actionbars:
                    actionbar['state'] = NORMAL

                # Attack target is alive
                if not enemy.is_dead():

                    print("player attacked" + str(self.__level_enemies[target].get_name()))
                    playerDamage = self.__player_stats[2]
                    enemy.damage(playerDamage)
                    print(enemy.get_health())
                    self.__console.insert(END,"Turn " +  str(self.__turn_counter) + ": "+ self.__player.get_name().capitalize()
                                          + " attacked " + enemy.get_name() +  " for " + str(playerDamage) + "dmg.\n")
                    health_label = self.__enemy_health_labels[target]
                    health_label['text'] = "Health: " + str(enemy.get_health())

                    # Pieni viive jotta nähdään mihin hyökättiin
                    health_label.after(500)

                else:
                    self.__console.insert\
                        (END,enemy.get_name() + " is already dead! "
                                                "Can't attack dead enemies! \n")

                self.check_for_dead_enemies(target)
                self.__currentTurn = 1
                self.__turn_counter += 1
                self.manage_turns()
        else:
            print("ei pelaajan vuoro")

    def check_for_dead_enemies(self,indx):
        """
        Tarkastetaan, onko kyseisellä indeksillä oleva vihollinen elossa.
        Jos ei ole, muutetaan kyseisen vihollisen ikonit osoittamaan,
        että se on kuollut.
        :param indx: tarkasteltavan vihollisen indeksi
        :return:
        """

        if self.__level_enemies[indx].is_dead():
            if self.__player.earn_experience(1):
                self.__console.insert(END,"YOU GAINED A NEW XP LEVEL: " +
                                      str(self.__player.get_xp_level()) + "\n")

            self.__enemy_icons[indx].configure(bg="black", state=DISABLED)
            self.__enemy_damage_labels[indx].configure(bg="black",fg="black")
            self.__enemy_health_labels[indx].configure(bg="black",fg="black")

    def init_enemies(self,currentLevel):
        """
        Luo kentälle kasan uusia vihollisia. Vaikeustaso, eli vihollisten laatu
        ja määrä määräytyy currentLevel -parametrin mukaan. Suuremmalla arvolla
        vastustajat ovat pahempia.
        Hoitaa edellisen kentän vihollisten tietojen poistamisen listoista.
        :param currentLevel: nykyisen levelin numero
        :return:
        """

        # Destroy all possible remenants of enemie's widgets
        for oldEnemy in self.__enemy_icons:
            oldEnemy.destroy()
        for enemyLabel in self.__enemy_health_labels:
            enemyLabel.destroy()
        for enemyLabel in self.__enemy_damage_labels:
            enemyLabel.destroy()

        # Overwrite old list content
        self.__level_enemies = []
        self.__enemy_health_labels = []
        self.__enemy_damage_labels = []
        self.__enemy_icons = []

        # Calculate difficulty of the new enemies
        if self.__current_level < 4:
            eAmount = random.randint(1,3)
        elif self.__current_level > 4:
            eAmount = random.randint(3, 6)
        else:
            eAmount = random.randint(4, 7)

        # Generate new enemies
        for x in range(0,eAmount):
            eHealth = random.randint(2,4+self.__current_level)
            eDamage = random.randint(1,2+int(self.__current_level/4))

            if self.__current_level > 2 and x == random.randint(1,eAmount):
                self.__level_enemies.append(Enemy(eHealth+10, "Knight", eDamage+2,"knight"))
            else:
                self.__level_enemies.append(Enemy(eHealth, "Soldier", eDamage,"soldier"))
        indx = 0
        rowCounter = 0  # needed for enemy placement to the grid
        columnCounter = 0  # needed for enemy placement to the grid

        for enemy in self.__level_enemies:
            if columnCounter >= 6:
                rowCounter += 1
                columnCounter = 0

            self.__enemy_frame = Frame(self.__middle_bar_frame,padx=5,pady=5,bg="gray14")
            self.__enemy_frame.grid(row=rowCounter,column=columnCounter)
            enemyIcon = Button(self.__enemy_frame,bg="gold3",fg="black",pady=10,
                               padx=10,command=lambda target=indx:self.attack(target))

            # Change color for different enemy types
            if enemy.get_type() == "knight":
                enemyIcon.configure(bg="red4")

            enemyIcon['text'] = enemy.get_name()+ " " + str(indx)
            enemyIcon.pack()

            self.__enemy_icons.append((enemyIcon))
            enemy_health_label = Label(self.__enemy_frame,bg="green",fg="white",pady=2,padx=2,font=("Helvetica",10))
            enemy_health_label['text'] = "Health: " + str(enemy.get_health())
            enemy_health_label.pack()
            self.__enemy_health_labels.append(enemy_health_label)
            enemy_damage_label = Label(self.__enemy_frame,bg="OrangeRed3",fg="black",pady=2,padx=2,font=("Helvetica",10))
            enemy_damage_label['text'] = "Dmg: " + str(enemy.get_damage())
            enemy_damage_label.pack()
            self.__enemy_damage_labels.append(enemy_damage_label)

            indx += 1
            columnCounter += 1
            print("vihu count on level:", len(self.__level_enemies))

    def raise_frame(self,frame):
        """
        Nostaa halutun framen päälimmäiseksi.
        Käytetään vaihtamaan eri pelinäkymiä, kuten startView ja combatView
        :param frame: haluttu frame
        :return:
        """
        frame.tkraise()

    def init_combat_view(self):
        """
        Hoidetaan taistelunäkymänluontiin tarvittavien
        elementtienluontifunktioiden kutsuminen
        :return:
        """
        self.create_left_bar()
        self.create_middle_bar()
        self.create_right_bar()
        self.create_bottom_bar()
        self.create_action_bar()
        self.__level_label['text'] = "Level: " + str(self.__current_level)

    def init_start_page(self):
        """
        Hoitaa aloitusnäkymän rakentamisen.
        """
        self.raise_frame(self.__StartView)
        self.__startFrame = Frame(self.__StartView,bg="gray14")
        self.__startFrame.grid(padx=150)
        nameEntry = StringVar()

        Label(self.__startFrame,padx=5,pady=5 ,text="ENTER YOUR CHARACTER'S NAME",
              bg="gray14",font=("Helvetica",16)).grid(pady=(100,0))

        Label(self.__startFrame, padx=5,pady=10,
              text="Name cannot be empty",bg="gray14",font=("Helvetica",16)).grid()

        name_field = Entry(self.__startFrame,textvariable=nameEntry)
        name_field.grid()
        Button(self.__startFrame, text="Start Game",bg="gray14",
               font=("Helvetica",16), command=lambda:self.start_game(nameEntry.get())).grid()

        self.__errorLabel = Label(self.__startFrame,bg="gray14",font=("Helvetica",16))
        self.__errorLabel.grid()

        for item in self.__startFrame.grid_slaves():
            item.config(fg="gray75")

        name_field.config(fg="gray14")


    def game_over_screen(self):
        """
        Rakentaa game over näkymän
        """
        self.raise_frame(self.__GameOverView)
        Label(self.__GameOverView,text="GAME OVER",font=("Helvetica",20)).grid()
        quitButton = Button(self.__GameOverView,text= "QUIT GAME" ,width=20,height=20, command=self.__game_gui.quit)
        quitButton.grid()

    def go_to_next_level(self):
        """
        Vaihtaa kentän seuraavaan
        """
        gotolevel = self.__current_level +1
        self.change_level(gotolevel)

    # Create player Character and start combat view
    def start_game(self,player_name):
        """
        Hoitaa pelin aloitukseen liittyvät toimenpiteet.
        :param player_name: pelaajahahmon nimi stringinä
        """
        try:
            if not player_name.strip() == "" and str(player_name.strip()):
                self.raise_frame(self.__CombatView)
                self.change_level(1)

                # Set Player character values
                self.__player = Player(50, player_name.capitalize(), 5, 10)
                self.__name_label['text']= self.__player.get_name()
                self.__player_stats = self.__player.get_stats()
                self.__player.init_default_inventory()
                self.__player.init_default_spellbook()

                self.__console.insert(END, "NEW GAME STARTED \n")
                self.__console.insert(END,"How to play: 1. Attack enemies by clicking [Attack] button and then click on enemy! \n")
                self.__console.insert(END,"Use items and magic from [item] and [magic] buttons. \n")
                self.__console.insert(END,"Using items will not use a turn. \n But using spells from [Magic] will use your turn\n")
                self.__console.insert(END,"All enemies will attack you on their turn, so you take damage equal of sum of their damage! \n" )
                self.__console.insert(END,"You will lose when your health reaches zero! *******\n" )
                self.update_labels()
            else:
               self.__errorLabel.config(text="Name is not valid!")
        except ValueError:
            pass

    def rungame(self):
        """
        Käynnistää tkinterin mainloopin
        """
        self.__game_gui.mainloop()

    def create_left_bar(self):
        self.__left_bar_frame = Frame(self.__CombatView,height=300,width=120,bg="gray14")
        self.__left_bar_frame.grid(column=0,row=0,padx=0,pady=5)
        self.__character_panel = Frame(self.__left_bar_frame,bg="gray14",padx=8)
        self.__character_panel.grid()

        # PLAYER NAME
        self.__name_label = Label(self.__character_panel,bg="gray14",fg="moccasin", font=("Helvetica", 20),wraplength=200)
        self.__name_label.grid(row=0,column=0,sticky=W,pady=10)

        # PLAYER HEALTH
        self.__health_label = Label(self.__character_panel,fg="red2",bg="gray14",text="Health: ", font=("Helvetica", 16))
        self.__health_label.grid(row=2,column=0,sticky=W)

        # PLAYER DAMAGE
        self.__plr_damage_label = Label(self.__character_panel,fg="gray75",bg="gray14",text="Damage: ", font=("Helvetica",16))
        self.__plr_damage_label.grid(row=4,column=0,sticky=W)

        # PLAYER MANA
        self.__mana_label = Label(self.__character_panel,bg="gray14", fg="aquamarine", text="Mana: ", font=("Helvetica", 16))
        self.__mana_label.grid(row=3, column=0,sticky=W)

        # PLAYER LEVEL
        self.__xp_level_label = Label(self.__character_panel,bg="gray14",fg="orange2",text="lvl: ", font=("Helvetica",16))
        self.__xp_level_label.grid(row=8,column=0,sticky=W)

        # CURRENT LEVEL
        self.__level_label = Label(self.__character_panel, fg="light grey",
                                   bg="gray14",
                                   font=("Helvetica", 12))
        self.__level_label.grid(row=9, column=0, sticky=W, pady=15)

    def create_middle_bar(self):
        self.__middle_bar_frame = Frame(self.__CombatView,height=300,width=500,bg="gray14")
        self.__middle_bar_frame.grid(column=1,row=0,padx=5,pady=5)

    def create_right_bar(self):
        self.__right_bar_frame = Frame(self.__CombatView, height=300, width=120,
                                 bg="gray24")
        self.__right_bar_frame.grid(column=2, row=0, padx=5, pady=5)

    def create_bottom_bar(self):
        self.__bottom_bar_frame = Frame(self.__CombatView,height=100,bg="blue",width=500)
        self.__bottom_bar_frame.grid(row=2,columnspan=1,column=1)
        self.__bottom_bar_frame.grid_columnconfigure(0,weight=1)

        self.__console = Text(self.__bottom_bar_frame,width=72)
        self.__console.bind("<Key>", lambda e: "break")
        self.__console.grid(row=0)

    def create_action_bar(self):
        self.__action_bar_Frame = Frame(self.__CombatView,height=20,bg="dim gray")
        self.__action_bar_Frame.grid(row=1,column=1,columnspan=1,sticky=W+E)

        # Create player buttons
        self.__attackButton = Button(self.__action_bar_Frame, text="Attack",
                                     bg="blue",fg="gray75",command=lambda: self.do_action("attack"),padx=5,pady=5)
        self.__attackButton.grid(column=1,row=0)
        self.__itemsButton = Button(self.__action_bar_Frame, text="Item",
                                     bg="blue",fg="gray75",
                                     command=lambda: self.do_action("item"))
        self.__itemsButton.grid(column=2,row=0)
        self.__magicButton = Button(self.__action_bar_Frame, text="Magic",
                                    bg="blue",fg="gray75",
                                    command=lambda: self.do_action("magic"))
        self.__magicButton.grid(column=3,row=0)
        self.__skipButton = Button(self.__action_bar_Frame, text="Skip turn",
                                    bg="Gray",
                                    command=lambda: self.do_action("skip"))
        self.__skipButton.grid(column=6,row=0)
        self.__player_actionbars.append(self.__itemsButton)
        self.__player_actionbars.append(self.__magicButton)
        self.__player_actionbars.append(self.__skipButton)

        for actionbar in self.__player_actionbars:
            actionbar.config(padx=5,pady=5)


class Enemy:

    def __init__(self,health,name,damage,type):
        self.__type = type
        self.__name = name
        self.__damage = damage
        self.__health = health
       # self.__status_effects = [] TODO: status implementation

    def get_damage(self):
        return self.__damage

    def get_health(self):
        return self.__health

    def damage(self, amount):
        self.__health -= amount

        if self.__health <= 0:
            self.__isDead = True

    def get_name(self):
        return self.__name

    def is_dead(self):

        if self.__health <= 0:
            return True
        else:
            return False

    def get_type(self):
        return self.__type


class Player:

    def __init__(self,health,name,base_damage,mana):
        print("Player", name, "created")
        self.__mana = mana
        self.__name = name
        self.__base_damage = base_damage
        self.__health = health
        self.__MAX_HEALTH = health
        self.__MAX_MANA = mana
        self.__isDead = False
        self.__inventory = []
        self.__experience = 0
        self.__xp_level = 1
        self.__spell_power = 0
        self.__spellbook = {}

    def has_mana(self,spell_name):
        if self.__mana >= self.__spellbook[spell_name]:
            return True
        else:
            return False

    def use_spell(self,spell_name):

        if spell_name in self.__spellbook:

            if spell_name == "Heal":
                if self.has_mana(spell_name):
                    heal_amount = random.randint(15,25) + self.__spell_power
                    self.__mana -= self.__spellbook[spell_name]
                    self.restore_hp(heal_amount)
                    return True, heal_amount

            elif spell_name == "Firestorm":
                if self.has_mana(spell_name):
                    damage = 4 + int(self.__spell_power/2)
                    self.__mana -= self.__spellbook[spell_name]
                    return True, damage

            elif spell_name == "Random bolt":
                if self.has_mana(spell_name):
                    damage = random.randint(5,10)+self.__spell_power
                    self.__mana -= self.__spellbook[spell_name]
                    return True, damage
        else:
            return False

    def restore_hp(self,amount):
        if (self.__health+amount >= self.__MAX_HEALTH):
            self.__health = self.__MAX_HEALTH

        else:
            self.__health += amount
        print("Restored hp:" + str(amount))


    def restore_mana(self,amount):
        if (self.__mana + amount >= self.__MAX_MANA):
            self.__mana = self.__MAX_MANA

        else:
            self.__mana += amount
        print("Restored mana:" + str(amount))


    def add_inventory_item(self,item):
        self.__inventory.append(item)


    # Return info string what happened
    def use_inventory_item(self,item_name):
        if item_name in self.__inventory:
            self.__inventory.remove(item_name)
            print(item_name + " removed from inventory")

            if item_name == "Healing Potion":

                # Healing potion heals now for random 15-35
                healAmount = random.randint(15,35)
                self.restore_hp(healAmount)
                return "Healing Potion restored " + str(healAmount) +" hp!"

            if item_name == "Mana Potion":
                # Healing potion heals now for random 15-35
                manareg = random.randint(5,15)
                self.restore_mana(manareg)
                return "Mana Potion restored " + str(manareg) + " mana!"

            return True
        else:
            return False


    def init_default_inventory(self):
        self.__inventory.append("Healing Potion")
        self.__inventory.append("Healing Potion")
        self.__inventory.append("Healing Potion")
        self.__inventory.append("Mana Potion")
        self.__inventory.append("Mana Potion")

    def init_default_spellbook(self):
        # name : manacost
        self.__spellbook["Heal"] = 4
        self.__spellbook["Firestorm"] = 5
        self.__spellbook["Random bolt"] = 3
        self.__spellbook["_DummySpell 2"] = 51
        self.__spellbook["_DummySpell 3"] = 2
        self.__spellbook["_DummySpell 4"] = 4
        self.__spellbook["_DummySpell 5"] = 0


    def earn_experience(self,amount):
        self.__experience += amount
        return self.check_xp_level()


    # checks if player has enough xp for new level
    # Handles stats increases

    def check_xp_level(self):

        if self.__experience > 5*self.__xp_level:
            self.__xp_level += 1
            print("LEVELI ON:" + str(self.__xp_level))

            self.__MAX_HEALTH += 5
            self.__health += 5

            self.__MAX_MANA += 1
            self.__mana += 1
            self.__spell_power += 1

            if self.__xp_level % 2 == 0:
                self.__base_damage += 1
            return True

            print("LEVEL GAINED:" + str(self.__xp_level))








    def get_inventory(self):
        return self.__inventory


    def get_stats(self):
        stats = []
        stats.append(self.__name)
        stats.append(self.__mana)
        stats.append(self.__base_damage)
        stats.append(self.__health)
        stats.append(self.__spellbook)
        stats.append(self.__experience)
        stats.append(self.__xp_level)
        return stats

    def get_mana(self):
        return self.__mana

    def get_health(self):
        return self.__health

    def damage(self, amount):
        self.__health -= amount

        if self.__health <= 0:
            self.__isDead = True


    def get_name(self):
        return self.__name

    def is_dead(self):
        return self.__isDead

    def get_xp_level(self):
        return self.__xp_level

    def get_spellbook(self):
        return self.__spellbook





def main():




    game = Game()



main()