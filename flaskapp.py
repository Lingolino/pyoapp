from sqlalchemy import Column, Integer, String, ForeignKey, Text, inspect
from flask import Flask, render_template,request,jsonify
from datetime import datetime
from urllib.parse import urlencode
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base 
import MySQLdb
import mysql.connector
import logic
from logic import Controller, apiGateway, DatabaseManager


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


def get_infos():
    start_time=1704859587
    queue_code=420
    match_type="ranked"
    count=70
    start=0
    max_requests_per_minute = 50
    requests_count = 0


    played_games_by_player = []
    winrate_by_player = []
    players_rank_stats = []
    players_most_played_champ_stats = []
    all_games = []
    dbManager = DatabaseManager()
    dbManager.delete_table()

    for index,puuid in enumerate(players_puuid):      
        logics = Controller(puuid,max_requests_per_minute,requests_count)
        logics.add_player()
        logics.update_player()
        requests_count =logics.add_games(start_time,queue_code,match_type,count,start)


        game_count, winrate, win_count = logics.get_winrate()
        if game_count[-1] >= 70:
            played_games_by_player.append(70)
        else:
            played_games_by_player.append(game_count[-1])
        

        winrate_by_player.append(winrate)


        rank_stats,most_played_champ_stats = logics.get_player_stats()
        rank_stats.append(winrate[-1])
        rank_stats.append(played_games_by_player[-1])
        rank_stats.append(win_count)
        players_rank_stats.append(rank_stats)
        
        players_most_played_champ_stats.append(most_played_champ_stats) 
    # print(played_games_by_player)
    # print(winrate_by_player)
    # print(players_most_played_champ_stats)
    # print(players_rank_stats)

    return played_games_by_player, winrate_by_player, players_most_played_champ_stats, players_rank_stats

    


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def start_page():
    if request.method== 'POST':
        None

    SpielerUnsortiert = player_names 
    played_games_by_player, winrates, players_champ_stats, players_rank_stats = get_infos() 
    


    # Daten für Fortschrittsbalken sortieren, Spieler mit den meisten Spielen
    
    GamesSortiert = sorted(played_games_by_player, key=lambda x: int(x), reverse=True)
    SpielerSortiertGames = [player_names[i] for i in sorted(range(len(played_games_by_player)), key=lambda x: int(played_games_by_player[x]),reverse=True)]
    SpielerAnzahl = range(len(player_names))


   
    # Daten für Color Step/ Rangliste sortieren, Spieler mit der höchsten Winrate

    aktuelleWinrates = [item[-1]for item in winrates]
    WinratesSortiert = sorted(aktuelleWinrates, key=lambda y: float(y), reverse=True)
    SpielerSortiertWinrate = [player_names[i] for i in sorted(range(len(aktuelleWinrates)), key=lambda y: float(aktuelleWinrates[y]),reverse=True)]
    GamesSortiertWinrate = [played_games_by_player[i] for i in sorted(range(len(aktuelleWinrates)), key=lambda y: float(aktuelleWinrates[y]),reverse=True)]
    
    WinrateDict =[WinratesSortiert,SpielerSortiertWinrate,GamesSortiertWinrate]


    # Daten für Liniendiagramm vorbereiten

    SpielerProzent=[]
    for i in GamesSortiert:
        Prozent=i/70*100
        SpielerProzent.append(Prozent)
    Games =list(range(1,71))


    # Daten für Rekorde vorbereiten

    Record_Kills = [[2074, 4495, 3860, 4021, 4495], ['Pfaffy', 'pYo Titanic', 'Oriannna Grande', 'Kha Chicks', 'pYo Titanic'], ['Tristana', 'Yone', 'Smolder', 'Hwei', 'Darius'], [25, 23, 21, 21, 20], [8, 5, 11, 5, 12], [11, 8, 8, 12, 24], [240, 207, 374, 251, 241], ['EUW1_6860292961', 'EUW1_6801831973', 'EUW1_6817280994', 'EUW1_6842061599', 'EUW1_6843316938']]
    Record_Deaths = [[28, 4495, 3860, 28, 28], ['VolBeat1', 'pYo Titanic', 'Oriannna Grande', 'VolBeat1', 'VolBeat1'], ['Karthus', 'Yone', 'Smolder', 'Thresh', 'Shyvana'], [8, 3, 3, 2, 9], [16, 15, 15, 14, 14], [14, 5, 7, 16, 7], [118, 201, 274, 27, 25], ['EUW1_6797799998', 'EUW1_6842522049', 'EUW1_6815688418', 'EUW1_6816395710', 'EUW1_6774022465']]
    Record_Assists = [[3855, 3855, 3855, 3855, 3855], ['Osko1', 'Osko1', 'Osko1', 'Osko1', 'Osko1'], ['Maokai', 'Thresh', 'Soraka', 'Thresh', 'Lulu'], [3, 2, 2, 1, 2], [11, 10, 6, 5, 4], [38, 37, 32, 31, 31], [61, 40, 36, 42, 39], ['EUW1_6843805349', 'EUW1_6857716172', 'EUW1_6820629598', 'EUW1_6860655634', 'EUW1_6765331303']]
    Record_Minions = [[3860, 4068, 3378, 4495, 4904], ['Oriannna Grande', 'Faho541', 'Jermain96', 'pYo Titanic', 'DoubIe Ling'], ['Smolder', 'Trundle', 'Teemo', 'Irelia', 'Smolder'], [21, 10, 4, 7, 7], [11, 6, 1, 13, 3], [8, 6, 5, 2, 3], [374, 323, 319, 314, 308], ['EUW1_6817280994', 'EUW1_6771949520', 'EUW1_6765330019', 'EUW1_6770237425', 'EUW1_6806278906']]




    
    

    return render_template('index.html',WinrateDict= WinrateDict, RecordKills=Record_Kills, 
                           RecordDeaths= Record_Deaths, RecordMinions=Record_Minions, RecordAssists = Record_Assists, 
                           SpielerRang = players_rank_stats, mostPlayedChampion = players_champ_stats, SpielerWinrate = winrates, 
                           Games =Games, SpielerAnzahl = SpielerAnzahl,SpielerProzent =SpielerProzent,
                           GamesSortiert = GamesSortiert, SpielerSortiertGames = SpielerSortiertGames,
                           WinratesSortiert = WinratesSortiert,
                           SpielerSortiertWinrate = WinratesSortiert,
                           SpielerUnsortiert = SpielerUnsortiert)


@app.route('/get_match_details', methods=['GET'])
def get_match_details():
    match_id = request.args.get('id')
    print(match_id)
    player_api = apiGateway()
    match = player_api.get_match_details(match_id)
    if not match:
        print("error match details not found")
        

    else:
        match_details = []
        for i in range(10):
            names = match['info']['participants'][i]['summonerName']
            icons = match['info']['participants'][i]['profileIcon']
            champs = match['info']['participants'][i]['championName']
            kills = match['info']['participants'][i]['kills']
            deaths = match['info']['participants'][i]['deaths']
            assists = match['info']['participants'][i]['assists']
            minions = match['info']['participants'][i]['totalMinionsKilled']
            gold = match['info']['participants'][i]['goldEarned']
            wards = match['info']['participants'][i]['wardsPlaced'] 
            dmg = match['info']['participants'][i]['totalDamageDealt']
            if match['info']['participants'][i]['win'] == True:
                win = "VICTORY"
            else:
                win = "DEFEAT"
            

            participants = [names,icons,champs,kills,deaths,assists,minions,dmg,gold,wards,win]
            match_details.append(participants)
        print(match_details)
        return jsonify(match_details)
    
    



    # if match_id =="EUW1_6797799998":
        
    #     return jsonify(match_details)
    # else:
    #     return jsonify({"error": "Produkt nicht gefunden"})

if __name__ =="__main__":
    app.run(debug=True)


# Winrate 
# kills
#death
# death
# minions
#vision score
#wards placed
# spiele an einem Tag 

# champion, name, icon kda, minions, items wäre krasss summuners lvl viktory oder defeat
