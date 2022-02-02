import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from Pokemon import Pokemon
from Team import Team


# PATH = "/Users/saraabdul/PycharmProjects/LearningfunNov5/chromedriver"
# user_data_directory = '~/Library/Application Support/Google/Chrome'


def choose_os():
    if os.name == 'posix':
        PATH = "/usr/local/bin/chromedriver"
        user_data = '/home/gondola/.config/google-chrome/Default/'
        return user_data, PATH


user_data_directory = choose_os()[0]
PATH = choose_os()[1]
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_directory}")
chrome_options.page_load_strategy = 'normal'
coach_list = ['Joe', 'HB', 'BanetteBandit', 'Mo', 'Raj', 'Lukas', 'TODD', 'Ben', 'Jared', 'Marty', 'Josh', 'ANDRE',
              'Harry', 'Ariel', 'GIRI', 'Quentin', 'Tom', 'Jim', 'Natesh', 'tester_account']
team_list = ['Raraku19', 'UnknownPingu', 'BanetteBandit', 'mocranks', 'Trishul105', 'SharpeedoInASpeedo', 'TODD',
             'Hypno Gengar Man', 'Mccoy124', 'Mchay071', 'Pine112', 'AndreC', 'elkulees', 'pb2+indahood', 'GIRI',
             'laser671', 'SupremeLeaderThom', 'jchemma', 'CrimsonFlames', 'jannies banny']
good_links = []
# with webdriver.Chrome() as driver:
driver = webdriver.Chrome(PATH, options=chrome_options)
time.sleep(1)


def find_mon_in_txt(string):
    poke_string = string
    a_file = open("pokemon7.txt", "r")
    lines = a_file.readlines()
    lines2 = []
    for line in lines:
        line = line.strip('\n')
        lines2.append(line)
    a_file.close()
    for line in lines2:
        if line in poke_string:
            return line
    return poke_string


def strip_mon(string):
    string = string.lower()
    string = string.replace('(par)', '')
    string = string.replace('(tox)', '')
    string2 = string.split()
    if len(string2) == 1:
        return string2[0]

    for item in string2[::-1]:
        m = item.replace("(", "").replace(")", "")
        if m == 'fainted' or m == 'active':
            continue
        if any(map(str.isdigit, item)):
            continue
        n = find_mon_in_txt(m)
        return n


def add_cookies():
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


def send_message(string):
    driver.find_element(By.CSS_SELECTOR, '.battle-log-add > form:nth-child(1) > textarea:nth-child(3)').send_keys(
        string, Keys.RETURN)


def login():
    username = 'Omega Theta Alpha'
    password = 'Updates123'
    driver.get('https://play.pokemonshowdown.com')
    time.sleep(1)
    # driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/button[1]').click()
    # time.sleep(1)
    # driver.find_element(By.CLASS_NAME, "ps-popup")
    # driver.find_element(By.CSS_SELECTOR, '.textbox.autofocus').sendkeys(username, Keys.RETURN)

    time.sleep(1)
    time.sleep(20)
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def find_game():
    wait = WebDriverWait(driver, 1)
    driver.get("https://play.pokemonshowdown.com/")
    time.sleep(1)
    add_cookies()
    time.sleep(1)
    # watch_button = driver.find_element(By.XPATH, '//*[@id="room-"]/div/div[1]/div[2]/div[3]/p[1]/button')
    watch_button = driver.find_element(By.CSS_SELECTOR,
                                       '#room- > div > div.leftmenu > div.mainmenu > div:nth-child(3) > p:nth-child(1) > button')
    watch_button.click()
    room_list = WebDriverWait(driver, 20).until(presence_of_element_located((By.CLASS_NAME, "roomlist")))
    battle_list = room_list.find_element(By.XPATH, '//*[@id="room-battles"]/div/div/div')

    time.sleep(2)
    searchbox = driver.find_element(By.CSS_SELECTOR, '#room-battles > div > div > form > input')
    searchbox.click()
    searchbox.send_keys("Hypno Gengar Man", Keys.RETURN)
    time.sleep(2)
    boxes = battle_list.find_elements(By.XPATH, 'div')

    for box in boxes:
        rating = box.find_element(By.CLASS_NAME, 'ilink')
        # testo1 = rating.get_property('attributes')[0]
        # print(testo1)
        player_1 = box.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/a/em[2]')
        text = rating.get_attribute('textContent')
        print("Loading . . .")
        for team in team_list:
            if team in text:
                print(f"Now joining {team}'s game.")
                gottem = rating.get_attribute('href')
                rating.click()
                time.sleep(5)
                good_links.append(gottem)
                join_game(gottem)


def join_game(link):
    driver.get(link)
    time.sleep(2)

    # room_list = WebDriverWait(driver, 20).until(presence_of_element_located((By.CLASS_NAME, "roomlist")))

    team_near = Team()
    team_far = Team()

    def set_teams():
        trainer_near = WebDriverWait(driver, 20).until(
            presence_of_element_located((By.CSS_SELECTOR, '.trainer.trainer-near')))
        trainer_far = WebDriverWait(driver, 20).until(
            presence_of_element_located((By.CSS_SELECTOR, '.trainer.trainer-far')))

        time.sleep(1)
        mon1 = trainer_far.find_elements(By.CLASS_NAME, 'has-tooltip')
        mon2 = trainer_near.find_elements(By.CLASS_NAME, 'has-tooltip')
        player_far_mon_list = []
        player_near_mon_list = []
        trainer_near = trainer_near.text
        trainer_far = trainer_far.text
        for mon in mon1:
            mon_name = mon.get_attribute('aria-label')
            mon_name = strip_mon(mon_name)
            # mon_name = find_mon_in_txt(mon_name)
            player_far_mon_list.append(mon_name)

        p1_pokemon_list = []
        for i in range(len(player_far_mon_list)):
            p1_pokemon_list.append(Pokemon())
            p1_pokemon_list[i].set_name(player_far_mon_list[i])
            p1_pokemon_list[i].set_owner(trainer_far)

        for mon in mon2:
            mon_name = mon.get_attribute('aria-label')
            mon_name = strip_mon(mon_name)
            # mon_name = find_mon_in_txt(mon_name)
            player_near_mon_list.append(mon_name)
        p2_pokemon_list = []
        for i in range(len(player_near_mon_list)):
            p2_pokemon_list.append(Pokemon())
            p2_pokemon_list[i].set_name(player_near_mon_list[i])
            p2_pokemon_list[i].set_owner(trainer_near)

        # object stuff below, parser stuff above
        team_near.trainer_name = trainer_near
        team_near.alive_list = p2_pokemon_list
        team_near.all_mons = p2_pokemon_list
        print(f'Trainer Near is named : {team_near.get_name()}')
        team_near.print_alive()
        team_far.trainer_name = trainer_far
        team_far.alive_list = p1_pokemon_list
        team_far.all_mons = p1_pokemon_list
        print(f'Trainer Far is named : {team_far.get_name()}')
        team_far.print_alive()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    set_teams()
    time.sleep(2)

    textbox_holder1 = driver.find_element(By.CLASS_NAME, 'battle-log-add')

    box_holder1 = driver.find_element(By.CLASS_NAME, 'battle-log')
    pre_battle = True
    pre_battle2 = True
    while pre_battle:
        box_holder1 = driver.find_element(By.CLASS_NAME, 'battle-log')
        box_holder2 = box_holder1.find_element(By.CLASS_NAME, 'message-log')
        box_holder3 = box_holder2.find_elements(By.CLASS_NAME, 'battle-history')
        # below is old find activemon, saving it for no reason
        for box in box_holder3:
            if box.text.startswith('Go! '):
                box_text = box.text
                box_text = box_text.lower()
                p2_startermon = box.text.split("Go! ", 1)
                p2_startermon = strip_mon(p2_startermon[1])
                p2_startermon = p2_startermon.replace("!", "")
                p2_startermon = p2_startermon.lower()
                for mon in team_near.all_mons:
                    if mon.get_name() == p2_startermon and pre_battle2 == True:
                        mon.set_is_active()
                        pre_battle2 = False
                        player_near_activemon = p2_startermon
                        # print(f"CHECKING IF {mon.get_name()} IS ACTIVE")
                        print(f'Team near active : {mon.get_is_active()}')
                        p2_startermon = box_text.split('go! ', 1)
                        p2_startermon = p2_startermon[1].split(f' ({mon.get_name()})!', 1)
                        p2_startermon[0] = p2_startermon[0].strip('!')
                        team_near.get_active().set_nickname(p2_startermon[0])
                        # print(f'nickname is {p2_startermon[0]}')
                        print(team_near.get_active().get_nickname())

                    else:
                        pass

            if "sent out" in box.text and pre_battle == True:
                p1_startermon = box.text.split("sent out ", 1)
                p1_startermon = strip_mon(p1_startermon[1])
                p1_startermon = p1_startermon.replace("!", "")
                p1_startermon = p1_startermon.lower()
                box_text = box.text
                box_text = box_text.lower()
                for mon in team_far.all_mons:
                    if mon.get_name() == p1_startermon:
                        mon.set_is_active()
                        # print(f"CHECKING IF {mon.get_name()} IS ACTIVE")
                        print(f'Team Far active : {mon.get_is_active()}')
                        pre_battle = False
                        p2_startermon = box_text.split("sent out ", 1)
                        p2_startermon = p2_startermon[1].split(f' ({mon.get_name()})!', 1)
                        p2_startermon[0] = p2_startermon[0].strip('!')
                        team_far.get_active().set_nickname(p2_startermon[0])
                        # print(f'nickname is {p2_startermon[0]}')
                        print(team_far.get_active().get_nickname())

                    else:
                        mon.set_is_inactive()

                pre_battle = False
        pre_battle = False
        time.sleep(4)
    time.sleep(3)
    print("The battle has begun!")
    current_turn = 1
    turn_dictionary = {}
    line_count = 0
    during_battle = True
    chat_iterator = 0

    # These functions read the battle while it is happening. All new functions will be put here, and have parse in the name.
    def parse_active_mon(string1):
        line = string1
        if line.startswith('Go! '):
            line = line.lower()
            line = line[:-1]
            p2_startermon = line.split("go! ", 1)
            p2_startermon = strip_mon(p2_startermon[1])
            p2_startermon = p2_startermon.replace("!", "")
            p2_startermon = p2_startermon.lower()
            for mon in team_near.all_mons:
                if mon.get_name() == p2_startermon:
                    mon.set_is_active()
                    p2_startermon = line.split('go! ', 1)
                    p2_startermon = p2_startermon[1].split(f' ({mon.get_name()})!', 1)

                    team_near.get_active().set_nickname(p2_startermon[0])
                else:
                    mon.set_is_inactive()
        if "sent out" in line:
            line = line.lower()
            line = line[:-1]
            p1_startermon = line.split("sent out ", 1)
            p1_startermon = strip_mon(p1_startermon[1])
            p1_startermon = p1_startermon.replace("!", "")
            p1_startermon = p1_startermon.lower()
            for mon in team_far.all_mons:
                if mon.get_name() == p1_startermon:
                    mon.set_is_active()
                    p1_startermon = line.split("sent out ", 1)
                    p1_startermon = p1_startermon[1].split(f' ({mon.get_name()})!', 1)
                    p1_startermon = p1_startermon[0].strip('!')
                    p1_startermon = p1_startermon.replace(f'({mon.get_name})', '')
                    team_far.get_active().set_nickname(p1_startermon)

                else:
                    mon.set_is_inactive()
        # try:
        #     print(f'Player fars active mon (no nick) is {team_far.get_active().get_name()}')
        #     print(f'Player fars active mon is {team_far.get_active().get_nickname()}')
        #     print(f'Player Nears active mon (no nick) is {team_near.get_active().get_name()}')
        #     print(f'Player Nears active mon is {team_near.get_active().get_nickname()}')
        # except AttributeError:
        #     pass

    def parse_mega(string2):  # this also checks the status of rocks.
        line = string2
        line = line.lower()
        # this is malware
        if 'has mega evolved into mega ' in line:
            for mon in team_far.all_mons:
                if mon.get_name() in line:
                    mon.set_name(mon.get_name() + '-mega')
                    # print(f'FOUND A MEGA : {mon.get_name()}')
            for mon in team_near.all_mons:
                if mon.get_name() in line:
                    mon.set_name(mon.get_name() + '-mega')
                    # print(f'FOUND A MEGA : {mon.get_name()}')
        # adding and removing rocks to the team object
        if 'pointed stones float in the air around the opposing team!' in line:
            team_near.set_rocks()
            try:
                team_near.get_active().set_live_rocks()
            except AttributeError:
                time.sleep(1)
                team_near.get_active().set_live_rocks()
        if 'pointed stones float in the air around your team!' in line:
            team_far.set_rocks()

            try:
                team_far.get_active().set_live_rocks()
            except AttributeError:
                time.sleep(1)
                team_far.get_active().set_live_rocks()
        if 'pointed stones disappeared from around the opposing team!' in line:
            team_far.remove_rocks()
        if 'pointed stones disappeared from around the opposing team!' in line:
            print('rocks gone (far)')
            team_far.remove_rocks()
        if 'pointed stones disappeared from around your team' in line:
            print('rocks gone (near)')
            team_near.remove_rocks()
        # adding moves to the pokemon object
        if f' used ' in line:
            try:
                far_used = f'the opposing {team_far.get_active().get_nickname()} used '
                near_used = f'{team_near.get_active().get_nickname()} used '
            except AttributeError:
                far_used = f'the opposing {team_far.get_active().get_name()} used '
                near_used = f'{team_near.get_active().get_name()} used '

            if far_used in line:
                move = line.replace(far_used, '')
                move = move.replace('!', '')
                team_far.get_active().add_move(move)
                print(f'{team_far.get_active().get_nickname()}{team_far.get_active().get_moves()}')

            if near_used in line:
                move = line.replace(near_used, '')
                move = move.replace('!', '')
                team_near.get_active().add_move(move)
                print(f'{team_near.get_active().get_nickname()}{team_near.get_active().get_moves()}')



    def parse_dictionary_real(dictionary, turn):
        line = dictionary.get(turn)
        for item in line:
            print(item)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            far_used = f'{team_far.get_active().get_name()} used '
            near_used = f'{team_far.get_active().get_nickname()} used '
            if far_used in item:
                print(item.replace(far_used, ''))
            if near_used in item:
                print(item.replace(near_used, ''))

    while during_battle:
        next_turn = current_turn + 1
        box_holder1 = driver.find_element(By.CLASS_NAME, 'battle-log')
        box_holder2 = box_holder1.find_element(By.CLASS_NAME, 'message-log')
        box_holder3 = box_holder2.find_elements(By.CLASS_NAME, 'battle-history')
        chatbox_holder1 = driver.find_elements(By.CLASS_NAME, 'chat')
        for i in range(chat_iterator, len(chatbox_holder1)):
            if '@Omega do points' in chatbox_holder1[i].text:
                send_message(
                    f"{team_far.get_name()} has {team_far.analyze_points()} points VERSUS {team_near.get_name()}'s {team_near.analyze_points()} points.")
            elif '@Omega do rocks' in chatbox_holder1[i].text:
                if team_near.rock_turns > team_far.rock_turns and team_near.rock_turns > 0:
                    send_message(
                        f"{team_near.get_name()} has **Stones Supremacy** with {team_near.rock_turns} turns of rocks verus {team_far.get_name()}'s {team_far.rock_turns} turns.")
                if team_far.rock_turns > team_near.rock_turns and team_far.rock_turns > 0:
                    send_message(
                        f"{team_far.get_name()} has **Stones Supremacy** with {team_far.rock_turns} turns of rocks verus {team_near.get_name()}'s {team_near.rock_turns} turns.")
                if team_near.rock_turns == team_far.rock_turns and team_far.rock_turns > 0:
                    send_message(f"{team_far.get_name()} and {team_near.get_name()} have **Pebble Parity**!")
                elif team_near.rock_turns == team_far.rock_turns:
                    send_message(f"{team_far.get_name()} and {team_near.get_name()} have **Pebble Parity**!")

            chat_iterator = chat_iterator + 1
        # Below chunk is the logic that scrapes the fight. It won't get the last turn because it doesn't get turns until it knows that the next turn is available. Pass endgame method to do that.
        for box in box_holder3:
            if f"Turn {next_turn}" in box.text or f'{team_far.get_name()} won the battle!' in box.text or f'{team_near.get_name()} won the battle!' in box.text:
                for skip, box in enumerate(box_holder3):
                    if skip < line_count:
                        continue
                    if f"Turn {current_turn}" in box.text:
                        temp_turn_holder = []
                        for i in range(line_count, len(box_holder3)):
                            # if ' used Fake Out!' in box_holder3[i].text:
                            #    send_message('FREE')
                            if box_holder3[i].text == f"Turn {next_turn}":
                                break

                            temp_turn_holder.append(box_holder3[i].text)

                            test_line = box_holder3[i].text
                            # all the line checks will go here, 1 by one. TRhe most efficient way to do python.
                            parse_active_mon(test_line)
                            parse_mega(test_line)
                            if f'{team_far.get_name()} won the battle!' in test_line or f'{team_near.get_name()} won the battle!' in test_line:
                                during_battle = False
                                print(turn_dictionary)
                            line_count += 1
                        print(turn_dictionary.get(current_turn))
                        try:
                            print(f'It is Turn {current_turn}; Player Far is : {team_far.get_active().get_nickname()} Player Near is : {team_near.get_active().get_nickname()}')
                        except AttributeError:
                            print('couldnt find active mon')
                        current_turn += 1
                        turn_dictionary[current_turn] = temp_turn_holder
                        if team_far.has_rocks:
                            team_far.rock_turns += 1
                        if team_near.has_rocks:
                            team_near.rock_turns += 1

                        break
            # below block candidate for deletion
            if box.text == f'{team_far.get_name()} won the battle!' or box.text == f'{team_near.get_name()} won the battle!':
                if len(turn_dictionary) >= current_turn - 1:
                    during_battle = False
                    send_message(
                        "The battle has finished!")
                    last_turn = []
                    for i in range(line_count, len(box_holder3)):
                        last_turn.append(box_holder3[i].text)
                    turn_dictionary[current_turn] = last_turn

    post_battle = True
    print(f'team far has {team_far.analyze_points()} points, team near has {team_near.analyze_points()} points.')
    print('Team Near Most Used Moves : ')
    for mon in team_near.all_mons:
        try:
            print(mon.most_used_move())
        except ValueError:
            print(f'{mon.get_name()} was unable to attack today :(')
    print('Team Far Most Used Moves : ')
    for mon in team_far.all_mons:
        try:
            print(mon.most_used_move())
        except ValueError:
            print(f'{mon.get_name()} was unable to attack today :(')

    while post_battle:
        chatbox_holder1 = driver.find_elements(By.CLASS_NAME, 'chat')
        for i in range(chat_iterator, len(chatbox_holder1)):
            if '@Omega do points' in chatbox_holder1[i].text:
                send_message(
                    f"{team_far.get_name()} has {team_far.analyze_points()} points VERSUS {team_near.get_name()}'s {team_near.analyze_points()} points.")
            elif '@Omega do rocks' in chatbox_holder1[i].text:
                print('We hear u')
                if team_near.rock_turns > team_far.rock_turns and team_near.rock_turns > 0:
                    send_message(
                        f"{team_near.get_name()} has **Stones Supremacy** with {team_near.rock_turns} turns of rocks verus {team_far.get_name()}'s {team_far.rock_turns} turns.")
                if team_near.rock_turns > team_near.rock_turns and team_far.rock_turns > 0:
                    send_message(
                        f"{team_far.get_name()} has **Stones Supremacy** with {team_far.rock_turns} turns of rocks verus {team_near.get_name()}'s {team_near.rock_turns} turns.")
                if team_near.rock_turns == team_far.rock_turns and team_far.rock_turns > 0:
                    send_message(f"{team_far.get_name()} and {team_near.get_name()} have **Pebble Parity**!")
                elif team_near.rock_turns == team_far.rock_turns:
                    send_message(f"{team_far.get_name()} and {team_near.get_name()} have **Pebble Parity**!")
            elif '@Omega print match' in chatbox_holder1[i].text:
                print(turn_dictionary)

            chat_iterator += 1
        print('GOTTOEND')
        time.sleep(3)
        pass


def parse_oubl_tier_list():
    driver.get('https://draft-league.nl/public/pages/leaguetier.php?league=48')
    time.sleep(3)
    main_body = WebDriverWait(driver, 20).until(
        presence_of_element_located((By.XPATH, '/html/body/div/div[2]/main/div/div[3]/div/div/div[2]/table')))
    for i in range(1, 87):
        print(f"LINE NUMBER {i}")
        iterate1 = main_body.find_element(By.XPATH,
                                          f'/html/body/div/div[2]/main/div/div[3]/div/div/div[2]/table/tbody/tr{[i]}')
        print(iterate1.text)
        # I just used this function to get data from the web site into an excel doc, its not really relevant anymore.

# find_game() # THIS IS THE FUNCTION WE USUALLY USE TO TEST. NO LONGER.
join_game('https://play.pokemonshowdown.com/battle-gen8ou-1502849714')


# run this only once to save proper cookies for acc log in, will automate when I run out of exciting things to do
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))