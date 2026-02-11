# wot-project-2024-2025-SensorDataLayer

## Descrizione del servizio

Il servizio sensordatalayer fa parte del progetto Pothole detection in particolare si occupa di:

- Tracciare i sensori in arrivo 
- RRicevere le segnalazioni degli utenti
- Identificare lo stato di salute della strada tramite random forest
- Inviare tramite protocollo mqtt le informazioni sullo stato della strada,con coordinate geografiche e la via in cui è stata inviata la segnalazione

Tecnologie utilizzate

- Python: linguaggio di programmazione impiegato per lo sviluppo del backend.
- Flask: framework utilizzato per la realizzazione dei microservizi.
- SQLite: database relazionale scelto per la memorizzazione dei dati relativi ai sensori.
- Docker: strumento per la containerizzazione dei microservizi.
- Docker Compose: strumento per la gestione e orchestrazione dei container.
