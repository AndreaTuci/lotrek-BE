## Installazione

	pip install -r requirements




## Utilizzo

```python
# La prima volta esegui le migrazioni
python manage.py migrate

# In una istanza del terminale avvia il bot
python telegramsend/bot.py

# In una seconda avvia il server
python manage.py runserver

```

##Endpoints:
/auth/signup  <-- Per la registrazione
/auth/signin  <-- Per l'autenticazione (prendi il token)
/telegram/send_message  <-- Invia messaggi al bot (inserisci il token nell'header)
