import os


animals_base_dir = 'X:/Neuro-Leventhal/data/mouseSkilledReaching/'

all_csv_fullpath = []
krista_scored_fullpath = []

all_csv_files = []
krista_scored_files = []
duplicate_with_krista = []
ugrad_scored_files = []



et_files = [entry for entry in os.listdir(animals_base_dir) if entry.startswith('et')]


for etdir in et_files:

    eartag = etdir.strip('et')

    if not etdir.startswith('et'):
        continue

    et_dir = animals_base_dir + etdir
    if not os.path.isdir(et_dir):
        continue

    et_training_dir = et_dir + '/Training/'
    if not os.path.isdir(et_training_dir):
        continue

    for item in os.listdir(et_training_dir):
        trainingday_dir = et_training_dir + item
        if not os.path.isdir(trainingday_dir):
            continue

        scored_csv = [file for file in os.listdir(trainingday_dir) if 'Scored' in file]
        available_csv = [file for file in os.listdir(trainingday_dir) if ('Scored' not in file and file.endswith('.csv'))]
        for file in available_csv:
            all_csv_fullpath.append(trainingday_dir + '/' + file)
            all_csv_files.append(file)
        for file in scored_csv:
            krista_scored_fullpath.append(trainingday_dir + '/' + file)
            krista_scored_files.append(file.strip('_Scored.csv'))

    et_blinded_dir = et_dir + '/BlindedScoring/'
    if os.path.isdir(et_blinded_dir):
        blindedScoring = True

        blinded_files = [file.split('_')[:-1] for file in os.listdir(et_blinded_dir)]
        for file in os.listdir(et_blinded_dir):
            if file in krista_scored_files:
                duplicate_with_krista.append(file)
                continue
            else:
                blind_file = file.split('_')
                blind_file = '_'.join(blind_file[:-1])
                if blind_file in krista_scored_files:
                    duplicate_with_krista.append(blind_file)
                    continue
                else:
                    ugrad_scored_files.append(file)

# all_csv_files
# all_csv_fullpath
# krista_scored_fullpath
# krista_scored_files
# duplicate_with_krista
# ugrad_scored_files

for file in ugrad_scored_files:
    print(file)
    if file in all_csv_files:
        print('real file')
    else:
        print('check formatting')





