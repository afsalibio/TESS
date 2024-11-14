import jellyfish
import pandas as pd

def phonetic_similarity_percentage(target_word, word_list, method='metaphone'):
    # Get the phonetic code of the target word
    if method == 'soundex':
        target_code = jellyfish.soundex(target_word)
    elif method == 'metaphone':
        target_code = jellyfish.metaphone(target_word)
    else:
        raise ValueError("Method should be either 'soundex' or 'metaphone'")
    
    # Array to store similarity percentages
    similarity_percentages = []

    for word in word_list:
        # Get the phonetic code of each word
        if method == 'soundex':
            word_code = jellyfish.soundex(word)
        elif method == 'metaphone':
            word_code = jellyfish.metaphone(word)

        # Calculate Levenshtein distance between phonetic codes
        distance = jellyfish.levenshtein_distance(target_code, word_code)
        
        # Convert distance to similarity percentage
        max_len = max(len(target_code), len(word_code))
        similarity_percentage = ((max_len - distance) / max_len) * 100
        similarity_percentages.append(similarity_percentage)

    return similarity_percentages

def save_to_excel(finalVosk, finalWV, target, wordsVosk, wordsWV, raw_Vosk, raw_WV, eval_Vosk, eval_WV):
    data = {
        'Word' : target,
        'Vosk_Results': wordsVosk,
        'Vosk Unprocessed Results': raw_Vosk,
        'Vosk Processed Results': finalVosk,
        'Vosk Evaluation': eval_Vosk,
        'Wav2Vec Results': wordsWV,
        'WV Unprocessed Results': raw_WV,
        'WV Processed Results': finalWV,
        'WV Evaluation': eval_WV
    }
    df = pd.DataFrame(data)
    df.to_excel(r"D:\Documents0\Alexa Files\PythonProject\TessResearch\Program\New folder\Frustrated2.xlsx", index=False)
    print("Excel sheet created successfully as phonetic_similarity_results.xlsx.")

def no_post(target, words):
    result = []
    for word in words:
        if target.lower() in word.lower():
            result.append("PASS")
        else:
            result.append("FAIL")

    if 'PASS' in result:
        return 'PASS'
    else:
        return 'FAIL'

def with_post(final):
    grades = []
    for grade in final:
        if grade >= 70.0:
            grades.append("PASS")
        else:
            grades.append("FAIL")
    
    return grades

# Example usage
target = ['start','start','start','stop','stop','stop','skip','skip','skip','see','see','see','look','look','look','mother','mother','mother','little','little','little','here','here','here','can','can','can','want','want','want','come','come','come','one','one','one','baby','baby','baby','three','three','three','run','run','run','jump','jump','jump','down','down','down','is','is','is','up','up','up','make','make','make','ball','ball','ball','help','help','help','play','play','play','with','with','with','friends','friends','friends','came','came','came','horse','horse','horse','ride','ride','ride','under','under','under','was','was','was','what','what','what','bump','bump','bump','live','live','live','very','very','very','puppy','puppy','puppy','dark','dark','dark','first','first','first','wish','wish','wish','basket','basket','basket','food','food','food','road','road','road','hill','hill','hill','along','along','along','game','game','game','hide','hide','hide','grass','grass','grass','across','across','across','around','around','around','breakfast','breakfast','breakfast','field','field','field','large','large','large','better','better','better','suddenly','suddenly','suddenly','happen','happen','happen','farmer','farmer','farmer','river','river','river','lunch','lunch','lunch','sheep','sheep','sheep','hope','hope','hope','forest','forest','forest','stars','stars','stars','heavy','heavy','heavy','station','station','station','safe','safe','safe','against','against','against','smash','smash','smash','reward','reward','reward','evening','evening','evening','stream','stream','stream','empty','empty','empty','stone','stone','stone','grove','grove','grove','desire','desire','desire','ocean','ocean','ocean','bench','bench','bench','damp','damp','damp','timid','timid','timid','perform','perform','perform','destroy','destroy','destroy','delicious','delicious','delicious','hunger','hunger','hunger','excuse','excuse','excuse','understood','understood','understood','harness']
wordsVosk = [['start'],['start'],['', 'start', 'start', 'start'],['stop'],['stop'],['stop'],['scape'],['scape'],['the', 'scape', 'scape', 'scape', '', ''],['see'],['see'],['see'],['nope'],['nope'],['nope'],['mod'],['mod there'],['mother'],['lit'],['lit then'],['nathan'],['hey', 'here'],['here'],['here'],['the', 'can', 'i can', '', ''],['hi'],['gone'],['what'],['one'],['one'],['com'],['com'],['com'],['one'],['one'],['one'],['maybe'],['baby'],['the', 'baby', 'baby'],['did he'],['three'],['three'],['run'],['run'],['the', 'run', 'run', 'run', '', ''],['jump'],['gump'],['the', 'jump', 'jump', '', ''],['done'],['down'],['the', 'dow', 'one down', '', ''],['he'],['east'],['ease'],['up'],['up'],['the', 'up', 'up'],['make'],['make'],['the', 'make', '', '', '', 'make', 'mate', '', ''],['boy'],['boy'],['boy'],['hey'],['head'],['headed'],['play'],['play'],['play'],['one', ''],['what'],['what', 'wait'],['the', 'france'],['friends'],['friends'],['come'],['come'],['hmmmm'],['', 'hmmmm', 'whoa', 'source who', 'horse', ''],['horse'],['horse'],['right', 'ahead'],['read'],['read'],['under'],['under'],['the', 'under', '', 'the', '', 'under', 'under', '', ''],['was'],['was'],['was', ''],['wow', 'one'],['ap', ''],['what'],['dumb'],['the'],['dump'],['live'],['live'],['the', 'live', '', 'live', 'live', '', ''],['the'],['very'],['very'],['the', 'but puppy'],['bobby'],['puppy'],['dark'],['dark'],['dark'],['the', 'fish', 'nice fish', 'she', ''],['fish'],['fish'],[''],['who is she'],['the', 'please', 'wish', '', ''],['my', 'skip'],['by skip'],['musket'],['food'],['food'],['food'],['', 'rod'],['rod'],['rod'],['he'],['he and'],['the', 'hill', 'hen', '', ''],['i know'],['i know'],['i know'],['game'],['game'],['game'],['hi'],['hi'],['hi'],['the', 'yes'],['good ass'],['good ass'],['', 'gross'],['how gross'],['a cruel', 'this'],['ira', 'one'],['around'],['around'],['the', 'but', '', ''],['the'],['the', '', 'the', 'the'],['the'],['feel'],['fig', ''],['lol', 'nije'],['nudge'],['large'],['the', 'but be my theory', '', 'but did he'],['but did he'],['by betty'],['so', 'the sub daily', '', ''],['the'],['', 'the', 'the', 'the'],['', 'have been'],['happen'],['happen'],['the', 'but fire mer', ''],['farmer'],['farmer'],['hey', 'leaves', 'fever', ''],['reaver'],['reaver'],['lol', 'large lunch'],['lunch'],['lunch'],['the', 'sheep'],['sheep'],['sheep'],['whoa'],['hope'],['whoa'],['', 'forests', 'yes'],['four'],['four'],['the', 'starts'],['starts'],['start', ''],['hey'],['heavy'],['the', 'heavy', 'the heavy', '', ''],['the', 'stop', 'it'],['stashing'],['station'],['safe'],['safe'],['safe'],['', 'dad', "it's against", ''],['again'],['again'],['sm', 'smiles'],['sm', 'mas'],['samoyedes'],['you', 'or'],['hm reward'],['reward'],['everett'],['every man'],['every mean'],['the', 'steady stream'],['stray', 'im'],['stream'],['april', 'me', ''],['and blippy'],['and blippy'],['', 'stone'],['stone'],['stone'],['girl'],['goof'],['groove'],['', 'bs', '', '', '', ''],[""],['the'],['', 'oxygen', ''],['oxen'],['oxygen'],['ben', 'nj'],['bench'],['bench'],['dump'],['dumb'],['', 'dump', 'dump'],['the', 'they made'],['they made'],['be mate'],['the', 'but for them'],['bad for them'],['perform'],['the'],['destroy'],['the', 'destroy', 'oi destroy', 'oi', '', ''],['', 'dean', "she's delicious", ''],['delicious'],['delicious'],['hunger'],['hunger'],['hunger'],['ix'],['excuse'],['excuse'],['i', 'and their son', "there's those"],['and there'],['understood'],['the', 'hon harm', 'harness', '']]
wordsWV = [['STATE'],['STATE'],['ILL', 'START', 'START', 'START', '', ''],['STOB'],['STOP'],['STOP'],['ESCAPED'],['ESCAPE'],['', 'ESCAPE', 'SCAPED', 'SCAPED', '', ''],['SEE'],['SEE'],['SEE'],['ILO'],['HOL'],['HE LOOKED'],['MADEUR'],['MADER'],['MY DER'],['LLI BELE'],['DILITALE', ''],['LIPILE'],['HERE', ''],['HERE'],['HERE'],['', 'KAN', 'KAN', '', ''],['KAN', ''],['GAN'],['WHAT'],['ON'],['WONP'],['COME'],['COME'],['COME'],['ONE'],['ONE'],['ONE'],['MAYBE'],['BABE'],['', 'BABY', 'BABY', '', ''],['PE'],['THREE'],['PIDE'],['RUN'],['RUN'],['', 'RUN', 'RUN', 'RUN', '', ''],['GUMP'],['GUMP'],['', 'DUMP', 'DUMP', '', ''],['DOWN'],['DOWN'],['', 'DOWN', 'DOWN', '', ''],['EAST'],['ES'],['IS'],['A'],['AH'],['', 'AB', 'AB', '', ''],['MAKE'],['MAKE'],['', 'MAKE', '', '', '', 'MAK', 'MAK', '', ''],['MORDY'],['BOY'],['MY'],['HEAD'],['HEAD'],['HEADED'],['BLA', ''],['BLE'],['LULL'],['ANT', ''],['WHAT'],['FOAT WAY', ''],['FREND', 'SO'],['FRANCE'],['FRANCE'],['COME'],['HOME'],['COME'],['', 'COME', 'HORSE', 'HORSE', '', ''],['HORCE'],['HORSE'],['READ', ''],['READ'],['HE'],['UNDER'],['UNDER'],['', 'UNDER', '', '', '', 'UNDER', 'UNDER', '', ''],['BLUS'],['WHAS'],['WAS', ''],['WANT', ''],['', '', ''],['WHAT'],['DUMB', ''],['DUMP'],['HE LUMP'],['LIVE'],['LIVE'],['', 'LIVE', '', 'LIVES', 'LIVES', '', ''],['VERY', ''],['VERY'],['VERY'],['', 'BUBBY'],['BOPI'],['BOBBY'],['DYK'],['DARK'],['DARK'],['', 'FIEST', 'FIEST', '', ''],['FIT'],['FEST'],['WI', ''],['VOICE'],['', 'LEASE', 'LEASE', '', ''],['MUST GET', ''],['BUSKIP'],['MUSKET'],['FOOD'],['GOOD'],['GOD'],['HROD', ''],['HROD'],['HERAD'],['HENCSE'],['HE AN'],['', 'HELL', 'HELL', '', ''],['ILONG', ''],['I LONG'],['I LONG'],['GAIN'],['GAIN'],['GAME'],['HI'],['HI'],['HI'],['GRAS', ''],['GRAS'],['YE GERES'],['', ''],['ACRUSS'],['ACRUS', ''],['IRONE', ''],['I ROUND'],['I ROUN'],['', 'A', '', ''],[''],['', '', '', '', '', ''],['SEE'],['FEAL'],['FEARED', ''],['LAR LA', 'IGE'],['NUDGE'],['HELICE'],['BY', 'EE MATREE', 'M', 'ITI', ''],['BUT DIDDY'],['BATITI'],['SUBD', 'SUBDAILY', 'S', ''],[''],['', '', 'S', 'S'],['HAVE BEEN', ''],['HA BEN'],['HAVE BEEN'],['FE', 'FAR MAYRE', ''],['FIMER'],['FIRMER'],['ANS', '', 'IVER', ''],['LIVER'],['IVER'],['LARGE', 'LUNCH'],['LUNCH'],['LUNCH'],['SHE', ''],['HIP'],['SHIP'],['HO'],[''],['OH'],['', 'SPHORIS', ''],['FORES'],['FORIS', ''],['START', ''],['STARTS'],['STARTS', ''],['HEAVY'],['HEAVY'],['', 'HEAVY', 'HEAVY', '', ''],['STOP', 'STATHU', '', ''],['STASHON'],['STASION'],['SAFE', 'S'],['SAFE'],['SAFE'],['AGAN', 'S', 'AGAINS', ''],['AGAINST'],['AGAINST'],['SMILE', 'S'],['SMILE', ''],['CHIMOS'],['HE LERD', ''],['REEWARD'],['HETTY WAD'],['EVERY DEAN'],['EVERY MING', 'EVERY'],['EVERY NING'],['STA', 'EAM STEAM'],['STAIM', ''],['STREAM'],['EBRY', '', ''],['EMPLITY', ''],['M PLIB'],['S', 'OWN'],['STONE'],['STONE'],['GO'],['GOD'],['GO'],['', 'BS', 'SERS', '', '', ''],[""],[''],['UC', 'INE', ''],['AUXXEN'],['OUXIENN'],['BENCH', ''],['BUNCH'],['BANC'],['DUMB'],['DUM'],['', 'DUMP', 'DUMP', '', ''],['', 'DEAR ME'],['DEMAD'],['HE MADE'],['BERE', 'FORM'],['BEFOIM', ''],['BYPM'],['DESTROY'],['DESTROY'],['', 'DESTROY', 'DESTROY', '', '', ''],['', 'DI', "SHE'S DELICIUS", ''],['DEMICIUS'],['DELITRS'],['HUNGER'],['HUNGER'],['HUNGER'],['EXCUSE', ''],['EXCUSE'],['EXCUSE'],['ANDE', "EVE AND THERE'S THE", ''],['AND THERE STOOD', ''],['UNTHERSTOOD'],['', 'AN HARMN HARNESS', '', '']]
finalVosk =[]
finalWV = []
raw_Vosk = []
raw_WV = []

for i in range(len(target)):
    raw_Vosk.append(no_post(target[i], wordsVosk[i]))
    raw_WV.append(no_post(target[i], wordsWV[i]))

for i in range(len(target)):
    results = phonetic_similarity_percentage(target[i], wordsVosk[i], method='metaphone')
    finalVosk.append(max(results))

for i in range(len(target)):
    results = phonetic_similarity_percentage(target[i], wordsWV[i], method='metaphone')
    finalWV.append(max(results))

eval_Vosk = with_post(finalVosk)
eval_WV = with_post(finalWV)

save_to_excel(finalVosk, finalWV, target, wordsVosk, wordsWV, raw_Vosk, raw_WV, eval_Vosk, eval_WV)
#print("Phonetic similarity percentages:", final)
