#result = ""

#for i in range(len(Notes_file_names)):
#	result+= '"' + Notes_file_names_names[i] + '"' + " : " + str(Notes_file_names[i]) + ",\n"
#result+="}"

Sharp_notes = [1, 3, 6, 8, 10]

Steps_strs = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

Intervals = [["Прима", "ч.1"], ["Секунда малая", "м.2", "Полутон"], ["Секунда большая", "Тон", "б.2"],
             ["Малая терция"], ["Большая терция"], ["Чистая кварта"], ["Увеличенная кварта"], ["Квинта"],
             ["Малая секста"], ["Большая секста"], ["Малая септима"], ["Большая септима"], ["Чистая октава"]]

Eng_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
Rus_notes = ['До', 'До#', 'Ре', 'Ре#', 'Ми', 'Фа', 'Фа#', 'Соль', 'Соль#', 'Ля', 'Ля#', 'Си']

Notes_files = {
"Фа2" : b'Samples/key01.wav',
"Фа#2" : b'Samples/key02.wav',
"Соль2" : b'Samples/key03.wav',
"Соль#2" : b'Samples/key04.wav',
"Ля2" : b'Samples/key05.wav',
"Ля#2" : b'Samples/key06.wav',
"Си2" : b'Samples/key07.wav',
"До3" : b'Samples/key08.wav',
"До#3" : b'Samples/key09.wav',
"Ре3" : b'Samples/key10.wav',
"Ре#3" : b'Samples/key11.wav',
"Ми3" : b'Samples/key12.wav',
"Фа3" : b'Samples/key13.wav',
"Фа#3" : b'Samples/key14.wav',
"Соль3" : b'Samples/key15.wav',
"Соль#3" : b'Samples/key16.wav',
"Ля3" : b'Samples/key17.wav',
"Ля#3" : b'Samples/key18.wav',
"Си3" : b'Samples/key19.wav',
"До4" : b'Samples/key20.wav',
"До#4" : b'Samples/key21.wav',
"Ре4" : b'Samples/key22.wav',
"Ре#4" : b'Samples/key23.wav',
"Ми4" : b'Samples/key24.wav'
}

Notes_hz = {
"До0" : 16.35,
"До#0" : 17.32,
"Ре0" : 18.35,
"Ре#0" : 19.45,
"Ми0" : 20.60,
"Фа0" : 21.83,
"Фа#0" : 23.12,
"Соль0" : 24.50,
"Соль#0" : 25.96,
"Ля0" : 27.50,
"Ля#0" : 29.14,
"Си0" : 30.87,
"До1" : 32.70,
"До#1" : 34.65,
"Ре1" : 36.71,
"Ре#1" : 38.89,
"Ми1" : 41.20,
"Фа1" : 43.65,
"Фа#1" : 46.25,
"Соль1" : 49.00,
"Соль#1" : 51.91,
"Ля1" : 55.00,
"Ля#1" : 58.27,
"Си1" : 61.74,
"До2" : 65.41,
"До#2" : 69.30,
"Ре2" : 73.42,
"Ре#2" : 77.78,
"Ми2" : 82.41,
"Фа2" : 87.31,
"Фа#2" : 92.50,
"Соль2" : 98.00,
"Соль#2" : 103.8,
"Ля2" : 110.0,
"Ля#2" : 116.5,
"Си2" : 123.5,
"До3" : 130.8,
"До#3" : 138.6,
"Ре3" : 146.8,
"Ре#3" : 155.6,
"Ми3" : 164.8,
"Фа3" : 174.6,
"Фа#3" : 185.0,
"Соль3" : 196.0,
"Соль#3" : 207.7,
"Ля3" : 220.0,
"Ля#3" : 233.1,
"Си3" : 246.9,
"До4" : 261.6,
"До#4" : 277.2,
"Ре4" : 293.7,
"Ре#4" : 311.1,
"Ми4" : 329.6,
"Фа4" : 349.2,
"Фа#4" : 370.0,
"Соль4" : 392.0,
"Соль#4" : 415.3,
"Ля4" : 440.0,
"Ля#4" : 466.2,
"Си4" : 493.9,
"До5" : 523.3,
"До#5" : 554.4,
"Ре5" : 587.3,
"Ре#5" : 622.3,
"Ми5" : 659.3,
"Фа5" : 698.5,
"Фа#5" : 740.0,
"Соль5" : 784.0,
"Соль#5" : 830.6,
"Ля5" : 880.0,
"Ля#5" : 932.3,
"Си5" : 987.8,
"До6" : 1047,
"До#6" : 1109,
"Ре6" : 1175,
"Ре#6" : 1245,
"Ми6" : 1319,
"Фа6" : 1397,
"Фа#6" : 1480,
"Соль6" : 1568,
"Соль#6" : 1661,
"Ля6" : 1760,
"Ля#6" : 1865,
"Си6" : 1976,
"До7" : 2093,
"До#7" : 2217,
"Ре7" : 2349,
"Ре#7" : 2489,
"Ми7" : 2637,
"Фа7" : 2794,
"Фа#7" : 2960,
"Соль7" : 3136,
"Соль#7" : 3322,
"Ля7" : 3520,
"Ля#7" : 3729,
"Си7" : 3951,
"До8" : 4186,
"До#8" : 4435,
"Ре8" : 4699,
"Ре#8" : 4978,
"Ми8" : 5274,
"Фа8" : 5588,
"Фа#8" : 5920,
"Соль8" : 6272,
"Соль#8" : 6645,
"Ля8" : 7040,
"Ля#8" : 7459,
"Си8" : 7902
}