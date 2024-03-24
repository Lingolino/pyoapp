from flask import Flask, render_template,request,jsonify
from datetime import datetime
from urllib.parse import urlencode
import requests

class apiGateway():
    def __init__(self):
        
        self.api_key = "RGAPI-f17f540a-cba3-4053-b9d2-80d220c6d429"
        self.region="europe"
        self.regionCode="euw1"

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
    played_games_by_player = [59, 70, 65, 70, 69, 57, 70, 70, 46, 24]

    winrate_by_player = [[0.0, 0.0, 0.0, 25.0, 40.0, 50.0, 42.86, 37.5, 44.444, 50.0, 54.545, 50.0, 53.846, 50.0, 46.67, 50.0, 52.941, 55.556, 52.63, 50.0, 47.62, 45.45, 47.826, 45.83, 48.0, 46.15, 48.148, 50.0, 51.724, 53.333, 54.839, 53.12, 54.545, 55.882, 54.29, 52.78, 51.35, 50.0, 51.282, 50.0, 51.22, 52.381, 53.488, 54.545, 53.33, 52.17, 53.191, 52.08, 51.02, 52.0, 50.98, 50.0, 49.06, 48.15, 47.27, 46.43, 45.61, 46.552, 47.458], [0.0, 0.0, 33.333, 50.0, 60.0, 50.0, 42.86, 37.5, 33.33, 40.0, 36.36, 41.667, 38.46, 35.71, 40.0, 37.5, 41.176, 44.444, 42.11, 45.0, 42.86, 40.91, 43.478, 41.67, 40.0, 42.308, 40.74, 39.29, 37.93, 36.67, 35.48, 34.38, 33.33, 35.294, 37.143, 38.889, 37.84, 36.84, 35.9, 37.5, 39.024, 40.476, 41.86, 43.182, 44.444, 43.48, 44.681, 45.833, 44.9, 44.0, 45.098, 44.23, 43.4, 44.444, 43.64, 42.86, 42.11, 43.103, 44.068, 43.33, 44.262, 43.55, 42.86, 43.75, 43.08, 42.42, 43.284, 44.118, 44.928, 44.29], [100.0, 50.0, 66.667, 75.0, 60.0, 66.667, 71.429, 62.5, 66.667, 60.0, 54.55, 58.333, 53.85, 50.0, 53.333, 56.25, 58.824, 61.111, 57.89, 55.0, 52.38, 54.545, 52.17, 54.167, 52.0, 50.0, 51.852, 50.0, 51.724, 50.0, 51.613, 53.125, 51.52, 52.941, 54.286, 52.78, 51.35, 52.632, 53.846, 55.0, 56.098, 54.76, 53.49, 52.27, 51.11, 50.0, 48.94, 47.92, 48.98, 50.0, 49.02, 48.08, 49.057, 50.0, 49.09, 48.21, 47.37, 48.276, 47.46, 46.67, 47.541, 46.77, 46.03, 45.31, 44.62], [100.0, 100.0, 100.0, 100.0, 80.0, 83.333, 71.43, 75.0, 77.778, 70.0, 72.727, 75.0, 69.23, 71.429, 66.67, 68.75, 64.71, 61.11, 57.89, 60.0, 61.905, 63.636, 60.87, 62.5, 64.0, 65.385, 66.667, 64.29, 62.07, 63.333, 64.516, 62.5, 60.61, 61.765, 62.857, 63.889, 64.865, 63.16, 64.103, 65.0, 63.41, 61.9, 60.47, 59.09, 60.0, 58.7, 57.45, 56.25, 57.143, 58.0, 58.824, 59.615, 60.377, 59.26, 60.0, 60.714, 59.65, 60.345, 61.017, 61.667, 60.66, 59.68, 58.73, 59.375, 60.0, 59.09, 58.21, 57.35, 56.52, 57.143], [0.0, 50.0, 33.33, 50.0, 40.0, 33.33, 42.857, 37.5, 44.444, 50.0, 54.545, 50.0, 46.15, 42.86, 40.0, 43.75, 47.059, 50.0, 47.37, 50.0, 47.62, 45.45, 43.48, 41.67, 40.0, 38.46, 37.04, 35.71, 37.931, 40.0, 38.71, 40.625, 39.39, 38.24, 37.14, 38.889, 37.84, 36.84, 38.462, 40.0, 39.02, 38.1, 39.535, 40.909, 40.0, 39.13, 40.426, 41.667, 42.857, 42.0, 41.18, 40.38, 41.509, 42.593, 43.636, 44.643, 43.86, 44.828, 44.07, 45.0, 44.26, 43.55, 42.86, 42.19, 43.077, 43.939, 44.776, 45.588, 46.377], [100.0, 100.0, 66.67, 75.0, 60.0, 66.667, 57.14, 50.0, 55.556, 50.0, 45.45, 41.67, 46.154, 42.86, 46.667, 43.75, 41.18, 38.89, 42.105, 45.0, 42.86, 40.91, 43.478, 45.833, 44.0, 42.31, 40.74, 39.29, 37.93, 36.67, 38.71, 37.5, 39.394, 38.24, 40.0, 38.89, 40.541, 39.47, 38.46, 37.5, 39.024, 40.476, 39.53, 38.64, 40.0, 41.304, 40.43, 41.667, 42.857, 44.0, 45.098, 46.154, 45.28, 46.296, 45.45, 44.64, 43.86], [0.0, 0.0, 33.333, 25.0, 20.0, 16.67, 28.571, 25.0, 33.333, 30.0, 27.27, 25.0, 23.08, 21.43, 26.667, 31.25, 35.294, 33.33, 31.58, 30.0, 33.333, 31.82, 34.783, 37.5, 40.0, 38.46, 40.741, 39.29, 37.93, 36.67, 35.48, 37.5, 36.36, 38.235, 40.0, 41.667, 43.243, 44.737, 43.59, 45.0, 43.9, 45.238, 46.512, 45.45, 46.667, 45.65, 44.68, 43.75, 44.898, 46.0, 45.1, 44.23, 45.283, 46.296, 45.45, 46.429, 47.368, 46.55, 45.76, 45.0, 44.26, 45.161, 46.032, 45.31, 46.154, 46.97, 47.761, 47.06, 46.38, 45.71], [0.0, 0.0, 0.0, 0.0, 20.0, 33.333, 28.57, 25.0, 22.22, 30.0, 36.364, 33.33, 38.462, 42.857, 40.0, 37.5, 35.29, 38.889, 42.105, 45.0, 42.86, 40.91, 43.478, 41.67, 40.0, 38.46, 40.741, 39.29, 37.93, 40.0, 41.935, 43.75, 42.42, 41.18, 40.0, 41.667, 43.243, 44.737, 46.154, 47.5, 48.78, 50.0, 48.84, 47.73, 48.889, 50.0, 51.064, 50.0, 48.98, 48.0, 47.06, 48.077, 47.17, 48.148, 49.091, 48.21, 47.37, 48.276, 47.46, 48.333, 49.18, 48.39, 47.62, 48.438, 49.231, 50.0, 49.25, 50.0, 49.28, 50.0], [0.0, 50.0, 33.33, 25.0, 40.0, 33.33, 42.857, 37.5, 33.33, 40.0, 36.36, 33.33, 38.462, 35.71, 40.0, 43.75, 47.059, 44.44, 47.368, 45.0, 42.86, 45.455, 43.48, 45.833, 48.0, 50.0, 48.15, 50.0, 48.28, 46.67, 45.16, 43.75, 45.455, 47.059, 48.571, 50.0, 51.351, 52.632, 51.28, 52.5, 51.22, 52.381, 53.488, 52.27, 51.11, 50.0], [0.0, 0.0, 0.0, 0.0, 20.0, 16.67, 14.29, 12.5, 11.11, 20.0, 27.273, 33.333, 38.462, 42.857, 40.0, 43.75, 47.059, 50.0, 52.632, 50.0, 52.381, 50.0, 52.174, 50.0]]

    players_most_played_champ_stats = [[['Viktor', 36, 50.0, 6.78, 4.78, 5.92], ['TwistedFate', 4, 25.0, 4.75, 8.25, 6.75], ['Ahri', 3, 0.0, 5.0, 7.0, 7.67], ['Diana', 2, 100.0, 4.5, 8.0, 8.0], ['MissFortune', 2, 50.0, 3.5, 1.5, 4.5]], [['Nocturne', 14, 35.71, 6.07, 6.29, 7.29], ['Graves', 14, 71.43, 12.5, 4.36, 6.07], ['Karthus', 12, 66.67, 6.33, 9.0, 12.25], ['Brand', 10, 30.0, 4.2, 7.1, 4.7], ['Volibear', 10, 60.0, 6.4, 5.6, 9.8]], [['Tristana', 20, 40.0, 6.7, 6.25, 5.95], ['Jinx', 17, 35.29, 7.12, 6.06, 7.0], ['MissFortune', 15, 46.67, 9.2, 5.2, 5.8], ['Kaisa', 6, 50.0, 7.0, 5.0, 5.83], ['Caitlyn', 4, 75.0, 3.5, 5.75, 9.0]], [['Yone', 28, 57.14, 4.43, 4.68, 3.36], ['Nasus', 25, 56.0, 6.04, 5.0, 5.6], ['Trundle', 13, 76.92, 4.77, 4.38, 3.54], ['Nocturne', 9, 44.44, 6.33, 6.0, 7.44], ['Kayn', 7, 42.86, 7.57, 7.0, 8.43]], [['Darius', 12, 66.67, 9.08, 7.42, 7.5], ['Aatrox', 10, 50.0, 6.4, 5.4, 5.6], ['Senna', 5, 40.0, 4.8, 7.6, 11.8], ['Thresh', 5, 100.0, 3.2, 4.4, 19.0], ['Sion', 4, 50.0, 6.25, 12.25, 8.75]], [['Seraphine', 33, 48.48, 3.91, 5.3, 13.94], ['Teemo', 10, 60.0, 3.6, 3.8, 4.8], ['Maokai', 10, 30.0, 1.8, 5.9, 12.2], ['Garen', 2, 0.0, 5.5, 3.5, 4.5], ['Nasus', 1, 0.0, 1.0, 3.0, 1.0]], [['Thresh', 21, 61.9, 2.33, 5.76, 20.62], ['Ekko', 16, 68.75, 10.38, 6.06, 6.31], ['Lulu', 13, 53.85, 1.23, 4.23, 14.23], ['Karma', 11, 45.45, 4.36, 4.27, 10.91], ['Pyke', 10, 90.0, 10.2, 4.7, 10.2]], [['Smolder', 42, 52.38, 7.55, 6.48, 6.36], ['MissFortune', 4, 50.0, 4.25, 4.75, 4.0], ['Brand', 4, 50.0, 4.5, 5.75, 4.5], ['Jhin', 3, 0.0, 8.0, 7.0, 4.0], ['Senna', 3, 66.67, 5.67, 7.0, 13.0]], [['Urgot', 23, 56.52, 7.35, 7.04, 5.09], ['Rumble', 6, 50.0, 7.0, 8.17, 6.0], ['Sona', 5, 40.0, 2.2, 4.8, 12.2], ['Trundle', 4, 50.0, 3.75, 7.25, 2.5], ['Karma', 3, 66.67, 2.67, 4.33, 4.33]], [['Hwei', 13, 53.85, 7.08, 4.0, 7.23], ['Ahri', 6, 83.33, 5.83, 4.5, 8.67], ['Khazix', 1, 0.0, 5.0, 10.0, 7.0], ['Varus', 1, 0.0, 2.0, 5.0, 2.0], ['Syndra', 1, 0.0, 2.0, 5.0, 3.0]]]

    players_rank_stats = [['EMERALD', 'IV', 92, 47.458, 59, 28], ['EMERALD', 'III', 0, 44.29, 70, 31], ['PLATINUM', 'IV', 69, 44.62, 65, 29], ['PLATINUM', 'II', 51, 57.143, 70, 40], ['EMERALD', 'II', 74, 46.377, 69, 32], ['BRONZE', 'I', 47, 43.86, 57, 25], ['DIAMOND', 'IV', 11, 45.71, 70, 32], ['PLATINUM', 'III', 0, 50.0, 70, 35], ['GOLD', 'II', 63, 50.0, 46, 23], ['PLATINUM', 'I', 16, 50.0, 24, 12]]
    

    print(played_games_by_player)
    print(winrate_by_player)
    print(players_most_played_champ_stats)
    print(players_rank_stats)

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
