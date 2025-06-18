import pandas as pd
import glob
import os
import re



def separate_sensor_data(input_folder, accel_pattern,output_folder="output"):
    """
        Separa automaticamente dati accelerometro e giroscopio per NanoEdgeAI

        Args:
            input_folder: cartella contenente i CSV
            output_folder: cartella di output
            accel_pattern: regex pattern di accel
        """

    # Crea cartella output se non esiste
    #os.makedirs(output_folder, exist_ok=True)

    # Pattern per identificare colonne accelerometro e giroscopio
    #accel_patterns = [
     #   r'acc.*[xyz]', r'accel.*[xyz]', r'a[xyz]',
      #  r'accelerometer.*[xyz]', r'acc_[xyz]'
    #]


    gyro_patterns = [
        r'gyro.*[xyz]', r'gyroscope.*[xyz]', r'g[xyz]',
        r'angular.*[xyz]', r'gyro_[xyz]', r'omega.*[xyz]'
    ]

    # Lista per tracciare i file processati
    processed_files = []

    # Processa tutti i CSV nella cartella
    for file_path in glob.glob(f"{input_folder}/*.csv"):
        try:
            print(f"Processando: {os.path.basename(file_path)}")

            df = pd.read_csv(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]

            # Identifica colonne accelerometro
            accel_cols = find_sensor_columns(df.columns, accel_pattern)

            # Identifica colonne giroscopio
            gyro_cols = find_sensor_columns(df.columns, gyro_patterns)

            # Crea CSV accelerometro
            if len(accel_cols) >= 3:
                accel_df = create_nanoedge_csv(df, accel_cols[:3])
                accel_path = os.path.join(output_folder, f"{base_name}_accelerometer.csv")
                accel_df.to_csv(accel_path, index=False, header=False)
                print(f"  ✓ Accelerometro: {len(accel_df)} righe -> {accel_path}")
            else:
                print(f"  ⚠ Accelerometro: trovate solo {len(accel_cols)} colonne")

            # Crea CSV giroscopio
            if len(gyro_cols) >= 3:
                gyro_df = create_nanoedge_csv(df, gyro_cols[:3])
                gyro_path = os.path.join(output_folder, f"{base_name}_gyroscope.csv")
                gyro_df.to_csv(gyro_path, index=False, header=False)
                print(f"  ✓ Giroscopio: {len(gyro_df)} righe -> {gyro_path}")
            else:
                print(f"  ⚠ Giroscopio: trovate solo {len(gyro_cols)} colonne")

            processed_files.append(file_path)

        except Exception as e:
            print(f"  ❌ Errore con {file_path}: {str(e)}")

    print(f"\n🎉 Processati {len(processed_files)} file!")
    return processed_files


def find_sensor_columns(columns, patterns):
    """Trova colonne che matchano i pattern del sensore"""
    matched_cols = []

    for pattern in patterns:
        matches = [col for col in columns if re.search(pattern, col, re.IGNORECASE)]
        if matches:
            # Ordina per X, Y, Z se possibile
            matches.sort(key=lambda x: ('x' in x.lower(), 'y' in x.lower(), 'z' in x.lower()))
            matched_cols.extend(matches)
            break  # Usa il primo pattern che trova match

    # Rimuovi duplicati mantenendo l'ordine
    return list(dict.fromkeys(matched_cols))


def create_nanoedge_csv(df, columns):
    """
    Crea CSV nel formato richiesto da NanoEdgeAI
    - Solo i tre assi (X, Y, Z)
    - Senza header
    - Valori numerici puliti
    """

    # Seleziona le colonne e pulisci i dati
    sensor_df = df[columns].copy()

    # Rimuovi righe con valori mancanti
    sensor_df = sensor_df.dropna()

    # Assicurati che siano tutti numerici
    for col in sensor_df.columns:
        sensor_df[col] = pd.to_numeric(sensor_df[col], errors='coerce')

    # Rimuovi eventuali righe con NaN dopo conversione
    sensor_df = sensor_df.dropna()

    # Rinomina colonne per chiarezza (opzionale)
    sensor_df.columns = ['X', 'Y', 'Z']

    return sensor_df


def preview_dataset_structure(input_folder):
    """Anteprima della struttura dei dataset per debug"""

    print("📊 ANTEPRIMA STRUTTURA DATASET")
    print("=" * 50)

    for file_path in glob.glob(f"{input_folder}/*.csv")[:3]:  # Solo primi 3 file
        try:
            df = pd.read_csv(file_path)
            print(f"\n📁 {os.path.basename(file_path)}")
            print(f"   Righe: {len(df)}")
            print(f"   Colonne: {list(df.columns)}")
            print(f"   Primi valori:")
            print(df.head(2).to_string(index=False))
        except Exception as e:
            print(f"   ❌ Errore: {e}")



def run():
    # Cartella con i tuoi dataset
    input_folder = "/home/alessioc/Documenti/Università/magistrale/IOT/25-CalogiuriDellannaScarciglia-7-StatoStradaST/dataset/"
    output_folder = "nanoedge_datasets"
    accel_pattern = [
        r'acc.*[xyz]_*_*', r'acc.*[xyz]',
        r'accel.*[xyz]', r'a[xyz]',
        r'accelerometer.*[xyz]', r'acc_[xyz]'
    ]

    # Anteprima struttura (opzionale)
    # preview_dataset_structure(input_folder)

    # Separa i sensori
    separate_sensor_data(input_folder, accel_pattern, output_folder)


def preprocess_for_anomaly_detection(df, sensor_type):
    # Standardizzazione/normalizzazione
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df),
                             columns=df.columns,
                             index=df.index)

    # Aggiungi features derivate utili per anomaly detection
    if len(df.columns) >= 3:  # x,y,z
        df_scaled['magnitude'] = (df_scaled.iloc[:, :3] ** 2).sum(axis=1) ** 0.5

    return df_scaled