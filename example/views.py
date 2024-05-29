# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ships
import os

def home(request):
    #ticker_list = tuple(Ships.objects.values_list('id', flat = True))
    ticker_list = Ships.objects.values_list('ship_name', 'ship_class', 'ship_race', 'ship_price', 'ship_weapon', 'ship_turret', 'ship_hull', 'ship_cargo', 'ship_dock', 'ship_hangar', 'ship_dlc', 'ship_role', 'ship_shield', 'ship_speed', 'id')
    if len(ticker_list)>0:
        try:
            api = ticker_list
        except Exception as e:
            api = "Error"
        return render(request, 'home.html',{'api': api })
    else:
        return render(request, 'home.html',{'api': "" })

def about(request):
    return render(request, "about.html", {})

def calendar(request):
    import pandas as pd
    from django.contrib.auth.models import User
    from io import StringIO

    csv_raw = """ship_name;ship_class;ship_race;ship_price;ship_weapon;ship_turret;ship_hull;ship_cargo;ship_dock;ship_hangar;ship_dlc;ship_role;ship_shield;ship_speed
Albatross Sentinel; xl; argon;10948470;0;8;138000;50;2;50;0; builder;258962; 70.1
Albatross Vanguard; xl; argon;9123765;0;8;115000;50;2;50;0; builder;258962;80
Alligator (Gas); m; split;212670;0;2;4300;7600;0;0;1; miner;4375; 669.5
Alligator (Mineral); m; split;236300;2;2;4800;7000;0;0;1; miner;4375; 618.5
Ares; s; paranid;243540;4;0;4700;270;0;0;0; military;2235; 148.2
Asgard; xl; terran;26179920;3;22;275000;9000;4;40;2; military;543820; 70.7
Asp; s; split;255275;3;0;4600;170;0;0;1; military;703;304
Asp Raider; s; split;123940;3;0;1800;100;0;0;1; military;703; 319.8
Astrid; m; argon;2170000;2;6;4000;4300;0;0;3; ;5147; 317.6
Atlas E; xl; paranid;15457615;0;8;164000;34040;10;24;0; resupplier;233064; 110.2
Atlas Sentinel; xl; paranid;11568815;0;8;156000;34800;10;50;0; resupplier;233064; 114.1
Atlas Vanguard; xl; paranid;9640505;0;8;130000;29000;10;50;0; resupplier;233064; 130.4
Balaur; s; split;271350;4;0;5500;180;0;0;1; military;703; 335.5
Baldric; m; terran;734360;0;2;9000;10700;0;0;2; trader;5405; 100.1
Barbarossa; l; argon;7714025;0;14;114000;21000;1;2;3; trader;38844; 194.7
Barracuda; s; boron;245690;3;0;3700;330;0;0;4; military;2556; 123.9
Behemoth Sentinel; l; argon;5641250;2;10;111000;2760;4;40;0; military;116532;116
Behemoth Vanguard; l; argon;4713125;2;10;93000;2300;4;40;0; military;116532; 127.4
Boa; m; split;373740;0;2;7400;7500;0;0;1; trader;4375; 304.5
Bolo (Gas); m; terran;388740;0;2;5000;10000;0;0;2; miner;5405;247
Bolo (Mineral); m; terran;388740;1;2;5000;8800;0;0;2; miner;5405;247
Buffalo; l; split;2938525;0;9;37000;16000;1;40;1; trader;33018; 215.4
Buzzard Sentinel; s; teladi;190320;3;0;5000;360;0;0;0; military;1820; 134.6
Buzzard Vanguard; s; teladi;157850;3;0;4100;300;0;0;0; military;1820; 144.6
Callisto Sentinel; s; argon;98455;2;0;2500;1236;0;0;0; trader;827; 141.3
Callisto Vanguard; s; argon;80050;2;0;2100;1030;0;0;0; trader;827; 153.5
Cerberus Sentinel; m; argon;1145000;2;4;20000;2112;1;1;0; military;15441; 189.3
Cerberus Vanguard; m; argon;963665;2;4;17000;1760;1;1;0; military;15441; 218.7
Chimera; s; split;338625;5;0;6100;200;0;0;1; military;703; 337.5
Chthonios (Gas) Sentinel; l; paranid;1395770;0;6;28000;38400;2;40;0; miner;34960; 237.4
Chthonios (Gas) Vanguard; l; paranid;1154890;0;6;23000;32000;2;40;0; miner;34960; 259.9
Chthonios (Mineral) Sentinel; l; paranid;1395770;0;7;28000;38400;2;40;0; miner;34960; 237.4
Chthonios (Mineral) Vanguard; l; paranid;1154890;0;7;23000;32000;2;40;0; miner;34960; 259.9
Chthonios E (Gas); l; paranid;1591620;0;6;29000;35200;2;4;0; miner;34960;236
Chthonios E (Mineral); l; paranid;1591625;0;7;29000;34960;2;4;0; miner;34960;236
Cobra; m; split;2172540;3;4;32000;1290;1;1;1; military;8750; 472.6
Colossus Sentinel; xl; argon;12102675;0;17;259000;22800;12;50;0; military;388443; 104.6
Colossus Vanguard; xl; argon;10090050;0;17;216000;19000;12;50;0; military;388443; 116.7
Condor Sentinel; xl; teladi;13409595;0;13;287000;33600;9;50;0; military;284858; 103.7
Condor Vanguard; xl; teladi;11170550;0;13;239000;28000;9;50;0; military;284858; 116.2
Cormorant Vanguard; m; teladi;418830;1;2;10000;7900;0;0;0; trader;11324; 113.4
Courier (Mineral); s; argon;83265;1;0;1200;2600;0;0;0; miner;827; 265.3
Courier Sentinel; s; argon;185980;1;0;2600;2352;0;0;0; trader;827; 198.1
Courier Vanguard; s; argon;155760;1;0;2200;1960;0;0;0; trader;827;215
Crane (Gas) Sentinel; l; teladi;1804390;0;6;36000;52800;2;40;0; miner;128187; 131.9
Crane (Gas) Vanguard; l; teladi;1503310;0;6;30000;44000;2;40;0; miner;128187; 146.2
Crane (Mineral) Sentinel; l; teladi;1804390;0;9;36000;57600;2;40;0; miner;128187; 131.9
Crane (Mineral) Vanguard; l; teladi;1503310;0;9;30000;48000;2;40;0; miner;128187; 146.2
Defence Drone; s; gen;0;1;0;1200;0;0;0;0; ;827; 99.8
Demeter Sentinel; m; paranid;229050;0;1;7000;9480;0;0;0; trader;4632; 156.9
Demeter Vanguard; m; paranid;176650;0;1;5000;7900;0;0;0; trader;4632; 182.6
Discoverer Sentinel; s; argon;105930;2;0;1700;648;0;0;0; military;827; 225.7
Discoverer Vanguard; s; argon;87605;2;0;1400;540;0;0;0; military;827; 237.5
Dolphin; m; boron;255620;0;1;9000;9200;0;0;4; trader;10394; 117.8
Donia; l; argon;1564470;0;8;26000;34000;2;4;3; miner;38844;251
Dragon; m; split;1243415;6;2;17000;450;0;0;1; military;4375; 452.2
Dragon Raider; m; split;739265;6;2;8000;340;0;0;1; ;4375; 548.4
Drill (Mineral) Sentinel; m; argon;155915;1;2;5000;11760;0;0;0; miner;5147; 224.6
Drill (Mineral) Vanguard; m; argon;131965;1;2;4000;9800;0;0;0; miner;5147; 245.3
Eclipse Vanguard; s; argon;169745;4;0;4000;320;0;0;0; military;1654; 159.4
Elephant; xl; split;12022990;0;8;181000;50;2;50;1; builder;220116; 98.8
Elite Sentinel; s; argon;92990;1;0;2200;180;0;0;0; military;827; 166.2
Elite Vanguard; s; argon;76755;1;0;1800;150;0;0;0; military;827; 180.6
Erlking; xl; argon;14920415;1;22;500000;56000;0;6;3; ;129481; 191.1
Falcon Sentinel; s; teladi;195705;2;0;4600;408;0;0;0; military;1820; 177.2
Falcon Vanguard; s; teladi;164360;2;0;3900;340;0;0;0; military;1820; 186.8
Falx; m; terran;2813860;4;2;20000;1500;1;1;2; military;10810; 203.1
Forager; s; khaak;0;1;0;600;0;0;0;0; military;745;396
Frog; s; terran;299630;0;0;1700;4120;0;0;2; trader;869; 72.6
Gannascus; xl; argon;11470775;0;8;115000;50;2;50;3; builder;258962; 86.1
Gladius; s; terran;470800;4;0;4400;360;0;0;2; military;1738; 127.2
Gorgon Sentinel; m; paranid;1323040;2;4;23000;1956;1;1;0; military;13896; 258.8
Gorgon Vanguard; m; paranid;1098300;2;4;19000;1630;1;1;0; military;13896; 300.1
Grouper (Mineral); s; boron;83723;1;0;4000;2560;0;0;4; miner;852; 133.3
Guillemot Sentinel; s; teladi;166530;1;0;2700;1152;0;0;0; military;910; 208.9
Guillemot Vanguard; s; teladi;139525;1;0;2300;960;0;0;0; military;910; 234.8
Guppy; l; boron;6513220;0;16;117000;8000;0;8;4; military;160180; 207.6
Helios E; l; paranid;3470000;0;7;55000;25500;1;2;0; trader;34960; 111.7
Helios Sentinel; l; paranid;2410810;0;7;45000;25200;1;40;0; trader;34960; 127.1
Helios Vanguard; l; paranid;1995760;0;7;37000;21000;1;40;0; trader;34960; 142.1
Heracles Sentinel; xl; argon;10948470;0;8;138000;50;2;50;0; builder;258962; 75.7
Heracles Vanguard; xl; argon;9123765;0;8;115000;50;2;50;0; builder;258962; 86.1
Hermes Sentinel; m; paranid;229050;0;1;6000;8520;0;0;0; trader;4632; 171.4
Hermes Vanguard; m; paranid;176650;0;1;5000;7100;0;0;0; trader;4632; 198.8
Heron Sentinel; l; teladi;2908725;0;6;57000;46000;2;40;0; trader;128187; 69.4
Heron Vanguard; l; teladi;2436610;0;6;48000;36800;2;40;0; trader;128187; 78.4
Hive Guard; m; khaak;0;1;0;3000;0;0;0;0; military;4632; 400.8
Hokkaido (Gas); l; terran;2854250;0;8;24000;38000;2;40;2; miner;40786; 111.3
Hokkaido (Mineral); l; terran;2854250;0;9;24000;38000;2;40;2; miner;40786; 111.3
Honshu; xl; terran;26263870;0;14;157000;43000;10;50;2; resupplier;135955; 39.2
Hydra; m; boron;638546;4;3;7900;400;0;0;4; military;15591; 323.3
Hydra Regal; m; boron;676764;4;3;8100;400;0;0;4; military;15591; 336.1
I; xl; xenon;5059920;0;40;340000;0;0;0;0; military;615035; 86.7
Ides Sentinel; m; argon;208235;0;2;6000;8880;0;0;0; trader;5147; 129.2
Ides Vanguard; m; argon;173355;0;2;5000;7400;0;0;0; trader;5147; 149.7
Incarcatura Sentinel; l; argon;4999085;0;7;93000;54000;2;40;0; trader;77688; 45.8
Incarcatura Vanguard; l; argon;3096880;0;7;78000;45000;2;40;0; trader;77688; 52.7
Irukandji; s; boron;119702;1;0;2600;530;0;0;4; military;852; 396.9
Jaguar; s; split;146365;1;0;2000;380;0;0;1; military;703; 359.1
Jian; m; terran;2057600;1;6;13000;950;0;0;2; military;10810; 187.2
K; xl; xenon;2432440;0;13;165000;0;0;0;0; military;246014; 134.8
Kalis; s; terran;342750;2;0;3300;180;0;0;2; military;3476; 140.1
Katana; m; terran;1763540;4;2;11000;560;0;0;2; military;10810; 420.6
Kestrel Sentinel; s; teladi;110350;1;0;3100;912;0;0;0; military;910; 214.6
Kestrel Vanguard; s; teladi;91945;1;0;2500;760;0;0;0; military;910; 226.1
Kopis (Mineral); s; terran;171090;1;0;1000;5480;0;0;2; miner;869; 88.2
Kukri; s; terran;385380;3;0;3700;140;0;0;2; military;869; 148.3
Kuraokami; m; yaki;984025;5;2;10000;1100;0;0;2; military;10294;363
Kyd; s; argon;53080;2;0;3000;650;0;0;3; military;827; 200.5
Kyushu; xl; terran;21146490;0;8;153000;50;2;50;2; builder;271910;40
Lux; s; argon;175140;2;0;2600;500;0;0;3; military;827; 299.5
M; s; xenon;39840;2;0;2900;0;0;0;0; military;786; 242.1
Magnetar (Gas) Sentinel; l; argon;1589310;0;6;32000;50400;3;40;0; miner;77688; 134.6
Magnetar (Gas) Vanguard; l; argon;1307600;0;6;26000;42000;3;40;0; miner;77688; 148.3
Magnetar (Mineral) Sentinel; l; argon;1586095;0;7;32000;50400;3;40;0; miner;77688;135
Magnetar (Mineral) Vanguard; l; argon;1304385;0;7;26000;40000;3;40;0; miner;77688; 148.6
Magpie (Mineral); s; teladi;90820;1;0;1300;3500;0;0;0; miner;1820; 174.2
Magpie Sentinel; s; teladi;200045;1;0;2800;3870;0;0;0; trader;1820;127
Magpie Vanguard; s; teladi;168700;1;0;2400;3096;0;0;0; trader;1820; 138.7
Mako; s; boron;133165;2;0;3100;270;0;0;4; military;852; 233.6
Mamba; s; split;194430;2;0;3500;130;0;0;1; military;1406; 324.7
Mammoth Sentinel; xl; argon;10948470;0;8;138000;50;2;50;0; builder;258962; 75.7
Mammoth Vanguard; xl; argon;9123765;0;8;115000;50;2;50;0; builder;258962; 86.1
Manorina (Gas) Sentinel; m; teladi;143940;0;2;4500;12960;0;0;0; miner;11324; 206.5
Manorina (Gas) Vanguard; m; teladi;118865;0;2;3700;10800;0;0;0; miner;11324; 237.1
Manorina (Mineral) Sentinel; m; teladi;143940;1;2;4500;12000;0;0;0; miner;11324; 206.5
Manorina (Mineral) Vanguard; m; teladi;118865;1;2;3700;10000;0;0;0; miner;11324; 237.1
Manticore; m; argon;402755;0;3;8000;1360;0;0;0; tug;5147; 165.1
Medium Drop Drone; m; gen;46600;0;0;10000;0;0;0;0; ;0; 143.1
Medium Terraforming Drone; m; gen;46600;0;0;10000;0;0;0;0; ;0; 143.1
Mercury Sentinel; m; argon;208235;0;2;6000;9840;0;0;0; trader;5147; 118.4
Mercury Vanguard; m; argon;173355;0;2;5000;8200;0;0;0; trader;5147; 137.6
Minotaur Raider; m; argon;741015;2;2;13000;2370;0;0;0; military;10294;199
Minotaur Sentinel; m; argon;888430;2;4;14000;1056;0;0;0; military;10294; 160.1
Minotaur Vanguard; m; argon;750580;2;4;12000;880;0;0;0; military;10294; 184.1
Mokosi Sentinel; l; argon;3824825;0;7;64000;39600;1;40;0; trader;77688; 60.5
Mokosi Vanguard; l; argon;3182880;0;7;53000;33000;1;40;0; trader;77688; 68.6
Monitor; xl; split;17231160;0;12;160000;29000;10;50;1; resupplier;110058; 139.8
Moreya; s; yaki;269180;4;0;4000;510;0;0;2; military;827; 378.9
N; s; xenon;34530;2;0;2500;0;0;0;0; military;786;173
Nemesis Sentinel; m; paranid;746320;5;2;12000;672;0;0;0; military;9264; 254.8
Nemesis Vanguard; m; paranid;622295;5;2;10000;560;0;0;0; military;9264;291
Nimcha; s; terran;342750;1;0;3000;670;0;0;2; military;1738; 214.9
Nodan Sentinel; s; gen;95390;2;0;4600;840;0;0;0; ;827; 263.6
Nodan Vanguard; s; gen;77630;2;0;3900;700;0;0;0; ;827; 277.4
Nomad Sentinel; xl; argon;10313175;0;8;139000;34800;4;50;0; resupplier;258962; 75.3
Nomad Vanguard; xl; argon;8600515;0;8;116000;29000;4;50;0; resupplier;258962; 85.8
Nova Sentinel; s; argon;160100;2;0;3800;288;0;0;0; military;827; 197.4
Nova Vanguard; s; argon;131970;2;0;3100;240;0;0;0; military;827; 206.7
Odysseus E; l; paranid;5191150;2;16;128000;2600;3;6;0; military;69920; 188.1
Odysseus Sentinel; l; paranid;6042095;2;16;119000;2040;3;50;0; military;69920; 153.4
Odysseus Vanguard; l; paranid;5030940;2;16;99000;1700;3;50;0; military;69920; 169.2
Okinawa; l; terran;4472180;0;8;36000;42000;1;40;2; trader;81572; 49.9
Orca; xl; boron;17596810;0;12;174000;40000;0;20;4; resupplier;401298; 96.4
Osaka; l; terran;11833870;2;13;95000;2800;1;40;2; military;122358; 88.9
Osprey Sentinel; m; teladi;1263720;2;4;39000;2916;1;1;0; military;16986; 92.7
Osprey Vanguard; m; teladi;1044205;2;4;33000;2430;1;1;0; military;16986; 108.9
P; m; xenon;78620;2;2;10000;0;0;0;0; military;9780; 202.7
Pegasus Sentinel; s; paranid;97330;1;0;1600;528;0;0;0; military;745; 355.2
Pegasus Vanguard; s; paranid;80050;1;0;1300;440;0;0;0; military;745;376
Pelican Sentinel; l; teladi;3199035;0;6;63000;51000;2;40;0; trader;128187; 65.2
Pelican Vanguard; l; teladi;2652815;0;6;52000;40800;2;40;0; trader;128187; 73.9
Peregrine Sentinel; m; teladi;870425;2;4;14000;1020;0;0;0; military;16986; 194.2
Peregrine Vanguard; m; teladi;735710;2;4;12000;850;0;0;0; military;16986; 222.9
Perseus Sentinel; s; paranid;188150;2;0;4400;288;0;0;0; military;745;291
Perseus Vanguard; s; paranid;156805;2;0;3700;240;0;0;0; military;745; 306.5
Phoenix Sentinel; l; teladi;6307905;2;11;124000;4440;2;40;0; military;128187; 120.1
Phoenix Vanguard; l; teladi;5273360;2;11;104000;3700;2;40;0; military;128187; 132.7
Piranha; s; boron;102657;1;0;4000;790;0;0;4; military;852; 227.2
Plutus (Gas) Sentinel; m; paranid;162505;0;2;5000;11520;0;0;0; miner;4632; 288.5
Plutus (Gas) Vanguard; m; paranid;133010;0;2;4000;9600;0;0;0; miner;4632; 332.8
Plutus (Mineral) Sentinel; m; paranid;162505;1;2;5000;11520;0;0;0; miner;4632; 288.5
Plutus (Mineral) Vanguard; m; paranid;133010;1;2;4000;9000;0;0;0; miner;4632; 332.8
Porpoise (Gas); m; boron;164592;0;2;8000;8600;0;0;4; miner;10394; 279.1
Porpoise (Mineral); m; boron;172090;1;2;8000;7800;0;0;4; miner;10394; 279.1
Prometheus; m; paranid;292080;3;3;11000;4000;0;0;0; plunderer;9264; 301.5
Protector; s; khaak;0;2;0;800;0;0;0;0; military;745;396
Pulsar Vanguard; s; argon;113565;6;0;1900;150;0;0;0; military;827; 206.1
Python; xl; split;0;2;26;230000;1000;2;50;1; ;110058; 406.9
Quasar Vanguard; s; argon;100545;4;0;1700;190;0;0;0; military;827; 169.4
Queens Guard; m; khaak;0;2;0;4000;0;0;0;0; military;4632; 308.3
Raleigh (Condensate); s; argon;217900;1;0;2200;250;0;0;3; trader;827; 139.5
Raleigh (Container); s; argon;203995;1;0;2200;2080;0;0;3; trader;827; 148.6
Rapier; s; terran;213800;1;0;1400;440;0;0;2; military;869; 285.1
Raptor; xl; split;32605075;0;101;590000;19000;22;130;1; ;110058;124
Rattlesnake; l; split;12490790;4;18;211000;800;1;40;1; military;33018; 233.5
Raven; s; teladi;566090;2;0;6700;2580;0;0;0; raven;2730; 189.6
Ray; l; boron;6549396;1;14;114000;2000;0;4;4; military;160180; 173.7
Rorqual (Gas); l; boron;1381332;0;4;31000;42000;0;2;4; miner;120135; 255.3
Rorqual (Mineral); l; boron;1359733;0;6;31000;40000;0;2;4; miner;120135; 255.3
S; m; xenon;71350;1;1;6000;9500;0;0;0; miner;9780; 121.6
Selene Sentinel; l; paranid;2410810;0;7;40000;22800;1;40;0; ;34960; 135.7
Selene Vanguard; l; paranid;1995760;0;7;33000;19000;1;40;0; ;34960;151
Shark; xl; boron;21843004;0;16;383000;35000;0;72;4; military;668830; 166.7
Shih; s; argon;274485;4;0;4900;590;0;0;3; military;2481; 178.6
Shuyaku Sentinel; l; argon;5429245;0;9;101000;44400;2;40;0; trader;77688; 85.8
Shuyaku Vanguard; l; argon;4520540;0;9;84000;37000;2;40;0; trader;77688; 98.9
Small Drop Drone; s; gen;23300;0;0;2200;0;0;0;0; ;0;72
Small Terraforming Drone; s; gen;23300;0;0;2200;0;0;0;0; ;0;72
Sonra Sentinel; l; argon;4294770;0;9;80000;34800;2;40;0; trader;77688;103
Sonra Vanguard; l; argon;3587240;0;9;67000;29000;2;40;0; trader;77688; 117.9
Stork Sentinel; xl; teladi;9342630;0;9;126000;30000;9;50;0; resupplier;284858; 87.3
Stork Vanguard; xl; teladi;7784855;0;9;105000;25000;9;50;0; resupplier;284858; 99.4
Sturgeon; l; boron;4401675;0;14;40000;30000;1;2;4; trader;40045; 113.1
Sunder (Gas) Sentinel; m; argon;161380;0;2;5000;12480;0;0;0; miner;5147; 212.8
Sunder (Gas) Vanguard; m; argon;127545;0;2;4000;10400;0;0;0; miner;5147; 258.4
Syn; l; terran;14823980;3;12;119000;2600;1;40;2; military;122358; 73.5
T; s; xenon;25880;1;0;1200;0;0;0;0; military;786; 481.5
Takoba; s; terran;343160;2;0;3400;110;0;0;2; military;1738; 275.9
Tern Sentinel; m; teladi;308615;0;1;8000;13600;0;0;0; trader;11324; 82.2
Tern Vanguard; m; teladi;266020;0;1;7000;10880;0;0;0; trader;11324; 96.2
Terrapin; s; boron;198595;0;0;4000;2230;0;0;4; trader;852; 113.1
Tethys (Mineral); s; paranid;83265;2;0;1200;2100;0;0;0; miner;745; 290.7
Tethys Sentinel; s; paranid;183810;2;0;2600;1896;0;0;0; trader;745; 214.8
Tethys Vanguard; s; paranid;150295;2;0;2100;1580;0;0;0; trader;745; 233.8
Teuta; l; argon;4322065;0;5;66000;7700;2;4;3; compactor;38844; 79.5
Theseus Sentinel; s; paranid;211940;3;0;5000;324;0;0;0; military;745; 177.5
Theseus Vanguard; s; paranid;177380;3;0;4200;270;0;0;0; military;745; 188.5
Thresher; m; boron;626185;1;8;10900;850;0;0;4; military;10394;341
Tokyo; xl; terran;24318750;0;28;213000;22000;19;50;2; military;407865; 66.6
Tuatara; s; split;0;2;0;2300;1350;0;0;1; miner;703; 314.2
Tuatara (Mineral); s; split;128200;2;0;1200;1720;0;0;1; miner;703;401
Unknown Ship; xl; tfm;0;0;0;735000;0;0;0;0; ;0; 24.4
Veles Sentinel; l; argon;3694780;0;7;69000;43200;1;40;0; trader;77688; 57.7
Veles Vanguard; l; argon;3065695;0;7;57000;36000;1;40;0; trader;77688; 65.6
Viper; m; split;0;2;6;25000;740;0;0;1; ;4375; 444.4
Vulture Sentinel; m; teladi;308615;0;1;9000;15100;0;0;0; trader;11324; 74.9
Vulture Vanguard; m; teladi;266020;0;1;8000;12080;0;0;0; trader;11324; 87.9
Walrus; xl; boron;11954185;0;12;178000;50;2;4;4; builder;267532; 48.4
Wyvern (Gas); l; split;1610285;0;8;21000;22000;2;40;1; miner;33018; 416.8
Wyvern (Mineral); l; split;1610285;0;10;21000;20000;2;40;1; miner;33018; 416.8
Yasur; s; ven;255275;4;0;3300;370;0;0;5; ;827; 481.8
Yasur Mk1; s; ven;255275;4;0;3300;370;0;0;5; ;827; 481.8
Yasur Mk2; s; ven;255275;4;0;3300;370;0;0;5; ;827; 481.8
Yasur Mk3; s; ven;255275;4;0;3300;370;0;0;5; ;827; 481.8
Zeus E; xl; paranid;17540630;0;19;303000;22000;12;24;0; military;233064; 222.5
Zeus Sentinel; xl; paranid;15747905;0;19;337000;24000;12;50;0; military;233064; 145.1
Zeus Vanguard; xl; paranid;13127715;0;19;281000;20000;12;50;0; military;233064; 163.8"""

    
    from io import StringIO

    df = pd.read_csv(
        StringIO(csv_raw),
        skipinitialspace=True,
        index_col=0, sep=';'
    ) 

    
    
    
    
    return render(request, 'calendar.html' , {'file_path': df.head() })
