from sqlalchemy import Column, Integer, String, ForeignKey, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base 
from datetime import datetime
from urllib.parse import urlencode
import requests
import json
import time
import calendar
from collections import Counter
import mysql.connector
import MySQLdb



player_names=["DoubIe Ling", "Volbeat1","Pfaffy","Faho541","pYo Titanic","Jermain96","Osko1","Oriannna Grande","Widefight","Kha Chicks"]
players_puuid=["S6FwiDgvHnvmjwwMkd0QwyJFL0j5A3MDYkyQdkj4RYKz8BRaaGucrT_CBq50b2Uo-xJEGdr2-TMjgw",
                "SKtbgaxUE3suMqvkqrzIzZKPar10W-95V3GNg-QdLdaZoett6o92hsUNh1ezbSicCJBtAqKk1Q__dQ",
                "dV7G-KIhrspygrvtfODC5Q8_hv93cPX7VFOS49VoYiD_XevUzayTAtWbhwhZOUqnsV0WCObL_lUkiA",
                "IlugQODSN_0EA7AhI2rw9ZAHy55hSAVtZ3vVQaIaRe2Fid2YPU7_2ZkFnlWi61ALeW8nnZ0nDSz6AQ",
                "7vPMrpX6K1LDy1AVC-B0Zm1WLvS5NQNHTLMUV6NwAq0n3B-srEcXCJlpstWK_ZSkmz5lDWfxXIxR4g",
                "NQdNibFbQFvK8XfQerYVEzO4SAPKVw6TVZAxLB_HMI4MNpVoHb9TgT4Xr9colsW7lWjcBaERYwjJbA",
                "Oh9OX3P_cJnXlolhhB4-LcUVTW9O9Bko9d1k58flnrWgpPqGWh-0_Dl1ccwMUZnMO5gMy2PYbXNpfQ",
                "V2M06G2ogO1CzolVGyNYJK8GVa2QIdz_Tahp5fXiiOuB2YCFguCLjywFDiMhX2P0HQ2-PCWHIAK8Jw",
                "EwKrLLx3OSW5TV0ciJU2-kOpjWZpHVuqeUCgoNUsGUI20rM9uga_GQzx5PyXpXMg82jjM4LTFgdFjg",
                "b0lEQQV-Nz6ORhdIPXkg-K4787kYlODOn2hYuvgmIcaj9ISA3ghDW8j0bpOQF578-w1giOjzkPgNYg"
                ]



# Verbindungsdaten für die DigitalOcean MySQL-Datenbank
# username = 'your_username'
# password = 'your_password'
# host = 'your_host'  # z.B. db-droplet-123456.db.ondigitalocean.com
# port = '3306'  # Standard MySQL-Port
# database = 'your_database_name'

username = "doadmin"
password = "AVNS_mKI9xsPKtGWOwXg5zyC"
host = "leaguedb-do-user-16020222-0.c.db.ondigitalocean.com"
port = 25060
database = "defaultdb"
sslmode = "REQUIRED"

# Verbindung zur Datenbank herstellen
#engine = create_engine(f'mysql://{username}:{password}@{host}:{port}/{database}?sslmode=REQUIRED')


# engine = create_engine('mysql://doadmin:AVNS_mKI9xsPKtGWOwXg5zyC@leaguedb-do-user-16020222-0.c.db.ondigitalocean.com:25060/defaultdb?ssl-mode=REQUIRED', echo=True)

Base = declarative_base()

class player_db(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    puuid = Column(String, unique=True)
    player_id = Column(String, unique=True)
    lvl = Column(Integer)
    icon = Column(Integer)
    solo_tier = Column(String)
    solo_rank = Column(String)
    solo_points = Column(Integer)
    matches = relationship('match_db', back_populates='player')



class match_db(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    player_puuid = Column(Integer, ForeignKey('players.puuid'))
    match_id = Column(String)
    champion_name = Column(String)
    champion_lvl = Column(Integer)   #raus
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    minions = Column(Integer)
    outcome = Column(String)
    date = Column(String)
    player = relationship('player_db', back_populates='matches')


class DatabaseManager:
    def __init__(self):
        username = "doadmin"
        password = "AVNS_mKI9xsPKtGWOwXg5zyC"
        host = "leaguedb-do-user-16020222-0.c.db.ondigitalocean.com"
        port = 25060
        database = "defaultdb"
       

            
        # SSL-Konfiguration für die Verbindung
        ssl_args = {'ssl': {'ca': 'ca-certificate.crt'}}

        # Verbindung zur Datenbank herstellen mit SSL-Konfiguration
        self.engine = create_engine(f'mysql://{username}:{password}@{host}:{port}/{database}', connect_args=ssl_args)
        #self.engine = create_engine(f'mysql://doadmin:AVNS_mKI9xsPKtGWOwXg5zyC@leaguedb-do-user-16020222-0.c.db.ondigitalocean.com:25060/defaultdb?ssl-mode=REQUIRED')
        #self.engine = create_engine('sqlite:///league.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        inspector = inspect(self.engine)
        if 'players' not in inspector.get_table_names():
            print("players wurder erstellt")
            player_db.__table__.create(self.engine)
            
        if 'matches' not in inspector.get_table_names():
            print("matches wurde erstellt")
            match_db.__table__.create(self.engine)
    

    def add_player(self,player_info,player_rank):
        
        
        #Daten für Datenbank vorbereiten
        
        player_puuid = player_info['puuid']
        player_id = player_info['id']
        player_lvl = player_info['summonerLevel']
        player_icon = player_info['profileIconId']
        player_name = player_info['name']
        
        
        if player_rank[0]['queueType'] == "RANKED_SOLO_5x5":
            index = 0
        else:
            index = 1  

        solo_tier = player_rank[index]['tier']
        solo_rank = player_rank[index]['rank']
        solo_points = player_rank[index]['leaguePoints']

        #Spieler in Datenbank hinzufügen
                  
        valid = self.get_player(player_puuid)
        if valid is None:
            player = player_db(name=player_name, puuid=player_puuid, 
                            solo_tier=solo_tier, solo_rank=solo_rank, solo_points=solo_points, 
                            lvl=player_lvl, icon=player_icon, player_id=player_id)
            self.session.add(player)
            self.session.commit()
            print("Spieler {} wurde hinzugefügt".format(player_name))
        else:
            print("Spieler {} bereits in DB".format(player_name))

        
    def get_player(self,puuid):

        #Spielerdaten aus Datenbank abrufen

        player = self.session.query(player_db).filter_by(puuid=puuid).first()
        self.session.close()

        #Spielerdaten in Dictionary umwandeln und zurückgeben

        if player:
            player_data = {
                "name" : player.name,
                "icon" : player.icon,
                "puuid" : player.puuid,
                "id" : player.player_id,
                "solo_tier" : player.solo_tier,
                "solo_rank" : player.solo_rank,
                "solo_points" : player.solo_points
            }
            return player_data
        else:
            return None
        


    def update_player(self,player_info,player_rank):
        
        #Daten für Datenbank vorbereiten
        player_puuid = player_info['puuid']
        player_id = player_info['id']
        player_lvl = player_info['summonerLevel']
        player_icon = player_info['profileIconId']
        player_name = player_info['name']

        if player_rank[0]['queueType'] == "RANKED_SOLO_5x5":
            index = 0
        else:
            index = 1

        solo_tier = player_rank[index]['tier']
        solo_rank = player_rank[index]['rank']
        solo_points = player_rank[index]['leaguePoints']


        #Spielerdaten aus Datenbank ziehen und Werte aktualisieren

        player = self.session.query(player_db).filter_by(puuid=player_puuid).first()
        player.lvl = player_lvl
        player.icon = player_icon
        player.solo_tier = solo_tier 
        player.solo_rank = solo_rank
        player.solo_points = solo_points

       
        #Spielerdaten in Datenbank aktualisieren
        
        if player:
            self.session.commit()
            print("Spieler {} wurde aktualisiert.".format(player_name))
        else:
            print("Spieler {} nicht gefunden.".format(player_name))
        self.session.close()

        
    def add_matches(self,puuid,match_id, match_details):

        
        player_index = match_details['metadata']['participants'].index(puuid)
        match_info = match_details['info']
        
        
        champion_name = match_info['participants'][player_index]['championName']
        champion_lvl = match_info['participants'][player_index]['champLevel']
        kills = match_info['participants'][player_index]['kills']
        deaths  = match_info['participants'][player_index]['deaths']
        assists = match_info['participants'][player_index]['assists']
        minions = match_info['participants'][player_index]['totalMinionsKilled']
        date_epoch = match_info['gameCreation']
        date = round(date_epoch/1000)
        info_outcome = match_info['participants'][player_index]['win']
        early_surrender = match_info["participants"][0]["gameEndedInEarlySurrender"]
            
        if early_surrender is not True:            
            if info_outcome is True:
                outcome = ("win")
            elif info_outcome is False:
                outcome = ("lose")
        else:
            outcome = ("remake")

        match = match_db(player_puuid = puuid, match_id = match_id,champion_name = champion_name,champion_lvl=champion_lvl, kills = kills, deaths = deaths,
                         assists = assists, minions = minions, outcome = outcome, date = date)
        self.session.add(match)
        self.session.commit()
        print("spiel hinzugefügt")


    def get_match_records(self,order):

        #Spieldaten sortiert in geforderter Order(kills,deaths,etc) aus Datenbank abrufen

        order = getattr(match_db, order)
        matches = self.session.query(match_db).order_by(-order).limit(5).all()
        self.session.close()
       
        #Spieldaten in Dictionary umwandeln und dicts in Liste speichern
        
        if matches:
            match_data = []
            for i in matches:
                data = {
                "match_id" : i.match_id,
                "champion" : i.champion_name,
                "kills" : i.kills,
                "deaths" : i.deaths,
                "assists" : i.assists,
                "minions" : i.minions,
                "puuid" : i.player_puuid,
                }
                match_data.append(data)
            

            return match_data
        else:
            breakpoint



    def get_matches(self,puuid,order):

        #Spieldaten sortiert in geforderter Order(hier dates) aus Datenbank abrufen
        
        order = getattr(match_db, order)
        matches = self.session.query(match_db).filter_by(player_puuid = puuid).order_by(order).all()
        self.session.close()

        #Spieldaten in Dictionary umwandeln und dicts in Liste speichern
        
        if matches:
            match_data = []
            for i in matches:
                data = {
                "match_id" : i.match_id,
                "outcome" : i.outcome,
                "champion" : i.champion_name,
                "kills" : i.kills,
                "deaths" : i.deaths,
                "assists" : i.assists,
                "minions" : i.minions,
                "date" : i.date
                }
                
                match_data.append(data)
            #print(match_data)
            return match_data
        else:
            match_data = []
            print("keine Spiel des Spielers gespeichert")
            return match_data

            


class apiGateway():
    def __init__(self):
        
        self.api_key = "RGAPI-eb379414-0ce3-44a9-83c2-5c7122f50788"
        self.region="europe"
        self.regionCode="euw1"

    def get_summoner_info(self,puuid):
        params = {
		    'api_key': self.api_key
            }
        api_url= f"https://{self.regionCode}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        
        try:
            response=requests.get(api_url, params=urlencode(params))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issue getting summoner data from API: {e}')
        return None 
    


    def get_rank(self,puuid):
        player_info=self.get_summoner_info(puuid)
        player_id = player_info['id']
        
        params = {
		    'api_key': self.api_key
            }
        api_url= f"https://{self.regionCode}.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_id}"
        try:
            response=requests.get(api_url, params=urlencode(params))          
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issue getting rang data from API: {e}')
        return None 


    def get_solo_games(self,puuid,start_time,end_time,queue_code,match_type,new_count,start):
        params = {
            'startTime': start_time,
            'endTime': end_time,
            'queue' : queue_code,
            'type' : match_type,
            'start': start,
            'count' : new_count,
            'api_key': self.api_key,
            }
        api_url =f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        
        try:
            response=requests.get(api_url, params=urlencode(params))
            response.raise_for_status()        
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issue getting solo match data from API: {e}')
            return None
    


    def get_match_details(self, match_id):            
        params = {
            'api_key': self.api_key,
            }
        api_url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}"

        try:
            response = requests.get(api_url, params=urlencode(params))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issue getting match details from match id from API: {e}')
            return None





class Controller():
    def __init__(self,puuid,max_requests_per_minute,requests_count):
        self.puuid = puuid
        self.max_requests_per_minute = max_requests_per_minute
        self.requests_count = requests_count

        self.db_manager = DatabaseManager()
        self.api = apiGateway()
        
        
        
    def safty(self):

        # Sicherheitsmechanismus, um die Anzahl der Anfragen pro Minute zu begrenzen

        print("request count: ",self.requests_count)
        if self.requests_count >= self.max_requests_per_minute:
            print("Maximale Anzahl von Anfragen erreicht. Wartezeit...")
            sleep = 60
            for i in range(sleep):
                sleep -=1
                print(sleep,"sleep")
                time.sleep(1)  
                self.requests_count = 0

    
        
    def add_player(self):

        #Spielerdaten von API abrufen

        
        player_info = self.api.get_summoner_info(self.puuid)
        player_rank =self.api.get_rank(self.puuid)
               
        self.requests_count +=2
        self.safty()
        
                
       
        self.db_manager.add_player(player_info,player_rank)

        return self.requests_count



    def update_player(self):  

        #Spielerdaten von API abrufen

        player_info = self.api.get_summoner_info(self.puuid)
        player_rank = self.api.get_rank(self.puuid)
     
        
        self.db_manager.update_player(player_info,player_rank)

        self.requests_count +=2
        self.safty()

        return self.requests_count



    def add_games(self,start_time,queue_code,match_type,count,start):

        #API request Paramter konfigurieren

        todays_time = datetime.now()
        end_time = calendar.timegm(todays_time.timetuple())
        
        all_games = []
        
        while True:
            print(end_time)
            player_matches = self.api.get_solo_games(self.puuid,start_time,end_time,queue_code,match_type,count,start)
            self.requests_count += 1
            self.safty()
            if not player_matches:
                break 
            all_games.extend(player_matches)
            last_match_details = self.api.get_match_details(all_games[-1]) 
            self.requests_count += 1
            self.safty()
            
            if not last_match_details:
                break
            player_index = last_match_details['metadata']['participants'].index(self.puuid)
            match_info = last_match_details['info']
            end_time_ms = match_info['gameCreation']
            end_time = round(end_time_ms/1000)

        #Sicherheitsmechanismus, ob Werte doppelt vorkommen.
            
        count_dic = {}
        for item in all_games:
            if item in count_dic:
                count_dic[item]+=1
            else:
                count_dic[item] = 1

        for item, count in count_dic.items():
            if count > 1:
                print(f"{item}: {count} mal")

        
        safed_data = self.db_manager.get_matches(self.puuid,"date")
        safed_matches  = [item['match_id'] for item in safed_data]


        for index,match_id in enumerate(all_games):       
            sleep = 60
            if match_id not in safed_matches:
                    match_details = self.api.get_match_details(match_id)
                    self.requests_count += 1
                    self.safty()
                    self.db_manager.add_matches(self.puuid,match_id, match_details)
            else:
                None       
       
        return self.requests_count
            




    def add_gamess(self,start_time,queue_code,match_type,count):

 
        
        safed_data = self.db_manager.get_matches(self.puuid,"date")
        safed_matches  = [item['match_id'] for item in safed_data]

        
        safed_outcomes = [item['outcome']for item in safed_data]
        finished_games = safed_outcomes.count("win")+ safed_outcomes.count('lose')
        


        if finished_games < 70:
            unfinished_games = safed_outcomes.count("remake")
            new_count = count + unfinished_games
            print(new_count)
            
            played_matches = self.api.get_solo_games(start_time,queue_code,match_type,new_count)
            print(len(played_matches))
            self.requests_count += 1
            self.safty()
            display_safed_matches = len(safed_matches) 
            
            for index,match_id in enumerate(played_matches):
                sleep = 60
                if match_id not in safed_matches:

                    match_details = self.api.get_match_details(match_id)
                    self.requests_count += 1
                    self.safty()
                    self.db_manager.add_matches(self.puuid,match_id, match_details)
                    display_safed_matches += 1
                    print(display_safed_matches," Spiele gespeichert, Spieler")
                else:
                    None


        elif finished_games == 70:
            print("genügend spiele gespeichert")
            return self.requests_count
        
        if finished_games > 70:
            print("zuviele Spiele gespeichert")
            return breakpoint


        # Controll Loop
        
        safed_data = self.db_manager.get_matches(self.puuid,"date")
        safed_outcomes = [item['outcome']for item in safed_data]
        finished_games = safed_outcomes.count("win")+ safed_outcomes.count('lose')

        if len(played_matches)>= 70:
            if finished_games < 70:

                self.add_games(start_time,queue_code,match_type,count)
                print("zu viele Remakes in den gespeicherten Spielen des Spierls")
                return self.requests_count
            else: 
                return self.requests_count
        else:
            print("nicht genügend Spiele gespielt")
            return self.requests_count


    def get_player_stats(self):
        

        player_data = self.db_manager.get_player(self.puuid)
        player_tier = player_data['solo_tier']
        player_division = player_data['solo_rank']
        player_lp = player_data['solo_points']

        rank_stats = [player_tier,player_division,player_lp]



        match_data = self.db_manager.get_matches(self.puuid,"date")
        
        played_champions = [item['champion'] for item in match_data]
        safed_outcome = [item['outcome'] for item in match_data]
        kills_list = [item['kills'] for item in match_data]
        deaths_list = [item['deaths'] for item in match_data]
        assists_list = [item['assists'] for item in match_data]


        counts = Counter(played_champions)
        # Sortiere die Elemente basierend auf ihrer Häufigkeit
        sorted_champions = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        # Extrahiere die eindeutigen Werte in der Reihenfolge der Häufigkeit
        most_played_champions = [item for item, _ in sorted_champions]
        #print(most_played_champions)
        most_played_champion_stats = []

        for i in range(0,5):
            champ_game_count = 0
            champ_win_count = 0
            champ_kills_list =[]
            champ_deaths_list = []
            champ_assist_list = []

            top_champion = most_played_champions[i]
            

            for i,played_champ in enumerate(played_champions):
                
                if top_champion == played_champ:
                   
                    champion_index = i
                    outcome = safed_outcome[i]
                   
                    if outcome != "remake":
                        champ_game_count +=1
                        champ_kills_list.append(kills_list[i])
                        champ_deaths_list.append(deaths_list[i])
                        champ_assist_list.append(assists_list[i])
                        if outcome == "win":
                            champ_win_count +=1
            
            champ_kills_median = round(sum(champ_kills_list) / len(champ_kills_list),2)
            champ_deaths_median = round(sum(champ_deaths_list) / len(champ_deaths_list),2)
            champ_assist_median = round(sum(champ_assist_list) / len(champ_assist_list),2)
            champ_winrate = round(champ_win_count/champ_game_count*100,2)

            champ_stats = [top_champion,champ_game_count,champ_winrate, champ_kills_median, champ_deaths_median, champ_assist_median]

            most_played_champion_stats.append(champ_stats)

        #print(most_played_champion_stats)
        return rank_stats,most_played_champion_stats
        



                
    def get_records(self,order):
       
        
        match_data = self.db_manager.get_match_records(order)

        match_id = [item['match_id'] for item in match_data]
        champion = [item['champion'] for item in match_data]
        
        kills = [item['kills'] for item in match_data]
        deaths = [item['deaths'] for item in match_data]
        minions = [item['minions'] for item in match_data]
        assists = [item['assists'] for item in match_data]
        player_puuid = [item['puuid'] for item in match_data]
        

        player_name = []
        player_icon = []

        for i in player_puuid:
            
            player_info = self.db_manager.get_player(i)
            name = player_info['name']
            icon = player_info['icon']
            player_name.append(name)
            player_icon.append(icon)
        
        



        record_list = [player_icon,player_name,champion,kills,deaths,assists,minions,match_id]
        
        return record_list

        



                    
    def get_winrate(self):
        
        match_data = self.db_manager.get_matches(self.puuid,"date")
        
        played_champions = [item['champion'] for item in match_data]
        safed_matches  = [item['match_id'] for item in match_data]
        safed_outcome = [item['outcome'] for item in match_data]
        
        match_counter = 0
        match_count = []
        winrate_per_count = []
        win_count = 0
        lose_count = 0
        remake_count = 0

        for index,id in enumerate(safed_matches):
            if match_counter<70:

                if safed_outcome[index]== "win":
                    match_counter += 1
                    win_count +=1
                    match_count.append(match_counter)
                    winrate= win_count/(match_counter) *100
                    winrate_per_count.append(round(winrate,3))

                elif safed_outcome[index] == "lose":
                    match_counter += 1
                    lose_count +=1
                    match_count.append(match_counter)
                    winrate= win_count/(match_counter) *100
                    winrate_per_count.append(round(winrate,2))
                else:
                    remake_count +=1

            else:
                None
        return match_count, winrate_per_count, win_count
                    
                

                        
                        



def delete_table():
    match_table  =match_db.__table__
    players_table = player_db.__table__
    # players_table.drop(engine)
    match_table.drop(engine)

#delete_table()
    #ad_player()
    # ad_games()
    # update_player()
    # get_winrate()
    #player_matches,player_winrate = get_winrate() 



def update_infos():
    start_time=1704859587
    queue_code=420
    match_type="ranked"
    count=70
    start=0
    max_requests_per_minute = 50
    requests_count = 0

    for index,puuid in enumerate(players_puuid):      
        Controller(puuid,max_requests_per_minute,requests_count)
        Controller.add_player()

update_infos()
        
