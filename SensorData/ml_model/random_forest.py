import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.utils import resample
import matplotlib.pyplot as plt


class RandomForest:

    def classificatore(self):

        # Caricamento dati
        df = pd.read_csv("C:\\Users\\PC\\Desktop\\merged_dataset_semicolon.csv", delimiter=';')

        # Conversione dei valori
        numerical_cols = [
            'acc_x_dashboard', 'acc_y_dashboard', 'gyro_x_dashboard',
            'gyro_y_dashboard', 'gyro_z_dashboard', 'paved_road',
            'unpaved_road', 'good_road_right', 'bad_road_right'
        ]

        for col in numerical_cols:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.dropna(inplace=True)

        # Creazione target multiclass
        df['road_condition'] = df['bad_road_right'] * 2 + df['unpaved_road']

        # Classi finali: 0 (Good&Paved), 1 (Good&Unpaved), 2 (Bad&Paved), 3 (Bad&Unpaved)
        features = ['acc_x_dashboard', 'acc_y_dashboard', 'gyro_x_dashboard', 'gyro_y_dashboard', 'gyro_z_dashboard']
        df_comb = df[features + ['road_condition']]

        # Bilanciamento classi
        df_list = []
        for label in df_comb['road_condition'].unique():
            subset = df_comb[df_comb['road_condition'] == label]
            df_list.append(resample(subset, replace=True, n_samples=df_comb['road_condition'].value_counts().max(),
                                    random_state=42))
        df_balanced = pd.concat(df_list)

        X = df_balanced[features]
        y = df_balanced['road_condition']

        # Split e classificazione
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Valutazione
        y_pred = model.predict(X_test)
        labels = ["Good & Paved", "Good & Unpaved", "Bad & Paved", "Bad & Unpaved"]
        print(classification_report(y_test, y_pred, target_names=labels))

        ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=labels, xticks_rotation=45)
        plt.title("Classificazione Strada (4 classi)")
        plt.tight_layout()
        plt.show()