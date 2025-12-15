# Installation Guide - My Personal Map

Guida completa all'installazione di My Personal Map per tutti i sistemi operativi.

---

## Indice

- [Requisiti di Sistema](#requisiti-di-sistema)
- [Installazione MySQL](#installazione-mysql)
- [Installazione Applicazione](#installazione-applicazione)
- [Primo Avvio](#primo-avvio)
- [Troubleshooting](#troubleshooting)

---

## Requisiti di Sistema

### Tutti i Sistemi

**Software Richiesto**:
- MySQL 8.0+ (raccomandato) **O** SQLite (fallback con limitazioni)
- 4GB RAM minimo
- 500MB spazio disco disponibile

**Opzionale**:
- Python 3.11+ (solo per sviluppo)

---

## Installazione MySQL

MySQL è necessario per sfruttare tutte le funzionalità dell'applicazione, in particolare il supporto per query spaziali avanzate.

### Windows

#### Opzione 1: MySQL Installer (Raccomandato)

1. **Download**:
   - Vai a https://dev.mysql.com/downloads/installer/
   - Scarica "mysql-installer-community" (versione più recente)

2. **Installazione**:
   - Esegui l'installer
   - Scegli "Developer Default" o "Server Only"
   - Segui il wizard:
     - MySQL Server 8.0+
     - Imposta password di root (RICORDALA!)
     - Lascia le impostazioni di rete predefinite (porta 3306)

3. **Verifica Installazione**:
   ```cmd
   mysql --version
   ```

4. **Avvia Servizio**:
   - Il servizio MySQL si avvia automaticamente
   - Verifica: Services → MySQL80

#### Opzione 2: Chocolatey (Advanced)

```powershell
choco install mysql
```

---

### macOS

#### Opzione 1: Homebrew (Raccomandato)

```bash
# Installa Homebrew se non presente
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installa MySQL
brew install mysql

# Avvia MySQL
brew services start mysql

# Configura sicurezza (imposta password root)
mysql_secure_installation
```

Segui il wizard di `mysql_secure_installation`:
- Imposta password di root
- Rimuovi utenti anonimi: **Yes**
- Disabilita login root remoto: **Yes**
- Rimuovi database di test: **Yes**
- Ricarica privilegi: **Yes**

#### Opzione 2: Download DMG

1. Vai a https://dev.mysql.com/downloads/mysql/
2. Scarica il DMG per macOS
3. Installa come applicazione standard
4. Avvia dal System Preferences → MySQL

#### Verifica Installazione

```bash
mysql --version
```

---

### Linux

#### Ubuntu / Debian

```bash
# Aggiorna package list
sudo apt update

# Installa MySQL Server
sudo apt install mysql-server

# Avvia servizio
sudo systemctl start mysql

# Abilita avvio automatico
sudo systemctl enable mysql

# Configura sicurezza
sudo mysql_secure_installation
```

#### Fedora / RHEL / CentOS

```bash
# Installa MySQL Server
sudo dnf install mysql-server

# Avvia servizio
sudo systemctl start mysqld

# Abilita avvio automatico
sudo systemctl enable mysqld

# Trova password temporanea di root
sudo grep 'temporary password' /var/log/mysqld.log

# Configura sicurezza
sudo mysql_secure_installation
```

#### Arch Linux

```bash
# Installa MySQL (MariaDB)
sudo pacman -S mysql

# Inizializza database
sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# Avvia servizio
sudo systemctl start mysqld

# Configura sicurezza
sudo mysql_secure_installation
```

#### Verifica Installazione

```bash
# Verifica versione
mysql --version

# Verifica servizio
sudo systemctl status mysql  # Ubuntu/Debian
sudo systemctl status mysqld  # Fedora/RHEL
```

---

## Installazione Applicazione

### Windows

1. **Download**:
   - Vai alla pagina Releases su GitHub
   - Scarica `MyPersonalMap-Windows-x64.zip`

2. **Estrazione**:
   - Clicca destro sul file ZIP → "Estrai tutto..."
   - Scegli destinazione (es: `C:\Program Files\MyPersonalMap\`)

3. **Primo Avvio**:
   - Entra nella cartella estratta
   - Doppio click su `MyPersonalMap.exe`

4. **Note Sicurezza**:
   - Se Windows Defender blocca l'app:
     - Clicca "Maggiori informazioni"
     - Clicca "Esegui comunque"
   - Questo è normale per app non firmate

---

### macOS

1. **Download**:
   - Vai alla pagina Releases su GitHub
   - Scarica `MyPersonalMap-macOS.dmg`

2. **Installazione**:
   - Doppio click sul DMG
   - Trascina `MyPersonalMap.app` nella cartella Applications

3. **Primo Avvio**:
   - Apri Applications
   - Doppio click su `MyPersonalMap`
   - **SE** appare "App danneggiata":
     ```bash
     # Opzione 1: GUI
     System Settings → Privacy & Security → "Open Anyway"

     # Opzione 2: Terminal
     xattr -cr /Applications/MyPersonalMap.app
     ```

4. **Gatekeeper**:
   - Al primo avvio, macOS chiederà conferma
   - Clicca "Apri" nel dialog di sicurezza

---

### Linux

#### AppImage (Raccomandato)

1. **Download**:
   ```bash
   # Scarica dalla pagina Releases
   wget https://github.com/yourusername/mypersonalmap/releases/download/v1.0.0/MyPersonalMap-Linux-x86_64.AppImage
   ```

2. **Rendi Eseguibile**:
   ```bash
   chmod +x MyPersonalMap-Linux-x86_64.AppImage
   ```

3. **Esegui**:
   ```bash
   ./MyPersonalMap-Linux-x86_64.AppImage
   ```

4. **Opzionale - Desktop Integration**:
   ```bash
   # Sposta in directory binari locali
   mkdir -p ~/.local/bin
   mv MyPersonalMap-Linux-x86_64.AppImage ~/.local/bin/mypersonalmap

   # Crea desktop entry
   cat > ~/.local/share/applications/mypersonalmap.desktop <<EOF
   [Desktop Entry]
   Type=Application
   Name=My Personal Map
   Exec=$HOME/.local/bin/mypersonalmap
   Icon=mypersonalmap
   Categories=Office;Geography;
   EOF
   ```

#### Tar.gz (Alternativa)

1. **Download ed Estrazione**:
   ```bash
   wget https://github.com/yourusername/mypersonalmap/releases/download/v1.0.0/MyPersonalMap-Linux-x86_64.tar.gz
   tar -xzf MyPersonalMap-Linux-x86_64.tar.gz
   cd MyPersonalMap
   ```

2. **Esegui**:
   ```bash
   ./MyPersonalMap
   ```

---

## Primo Avvio

### Wizard di Setup Database

Al primo avvio, l'applicazione mostrerà un wizard di configurazione:

#### Se MySQL è Installato

1. **Rilevamento Automatico**:
   - L'app rileverà MySQL automaticamente
   - Ti chiederà la password di root

2. **Creazione Database**:
   - Inserisci password root MySQL
   - Imposta nome database (default: `mypersonalmap`)
   - Imposta utente database (default: `mypersonalmap_user`)
   - Imposta password utente database

3. **Conferma**:
   - Il wizard creerà automaticamente:
     - Database MySQL
     - Utente con privilegi
     - Tabelle e schema

#### Se MySQL NON è Installato

Il wizard ti offrirà due opzioni:

1. **Guida Installazione MySQL**:
   - Link e istruzioni per installare MySQL
   - Dopo l'installazione, riavvia l'app

2. **Usa SQLite (Fallback)**:
   - Database file-based integrato
   - ⚠️ Limitazioni:
     - Supporto limitato query spaziali
     - Performance ridotte su grandi dataset
   - Adatto per test o piccoli dataset

---

## Configurazione Manuale (Opzionale)

Se preferisci configurare manualmente il database:

### 1. Crea Database e Utente

```sql
-- Connettiti come root
mysql -u root -p

-- Crea database
CREATE DATABASE mypersonalmap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crea utente
CREATE USER 'mypersonalmap_user'@'localhost' IDENTIFIED BY 'your_strong_password';

-- Concedi privilegi
GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'localhost';
FLUSH PRIVILEGES;

-- Esci
EXIT;
```

### 2. File di Configurazione

**Percorsi file `.env`**:
- Windows: `%LOCALAPPDATA%\MyPersonalMap\.env`
- macOS: `~/Library/Application Support/MyPersonalMap/.env`
- Linux: `~/.local/share/MyPersonalMap/.env`

**Modifica `.env`**:
```env
DATABASE_USER=mypersonalmap_user
DATABASE_PASSWORD=your_strong_password
DATABASE_URL=localhost
DATABASE_NAME=mypersonalmap
DATABASE_PORT=3306
```

---

## Troubleshooting

### MySQL non Trovato

**Problema**: "MySQL not found" anche se installato

**Soluzioni**:

1. **Verifica Servizio Attivo**:
   ```bash
   # Windows
   services.msc → Cerca "MySQL80"

   # macOS
   brew services list | grep mysql

   # Linux
   sudo systemctl status mysql
   ```

2. **Verifica Porta**:
   ```bash
   # Verifica che porta 3306 sia in ascolto
   netstat -an | grep 3306
   ```

3. **Riavvia Servizio**:
   ```bash
   # Windows
   net stop MySQL80
   net start MySQL80

   # macOS
   brew services restart mysql

   # Linux
   sudo systemctl restart mysql
   ```

---

### Permission Denied (Linux)

**Problema**: `Permission denied` quando esegui AppImage

**Soluzione**:
```bash
chmod +x MyPersonalMap-*.AppImage
```

---

### App "Danneggiata" (macOS)

**Problema**: "MyPersonalMap.app is damaged and can't be opened"

**Soluzione**:
```bash
xattr -cr /Applications/MyPersonalMap.app
```

---

### Port 8000 Già in Uso

**Problema**: "Port 8000 is already in use"

**Soluzione**:

1. **Trova Processo**:
   ```bash
   # Windows
   netstat -ano | findstr :8000

   # macOS/Linux
   lsof -i :8000
   ```

2. **Termina Processo**:
   ```bash
   # Windows
   taskkill /PID <PID> /F

   # macOS/Linux
   kill -9 <PID>
   ```

---

### Errori di Connessione Database

**Problema**: "Can't connect to MySQL server"

**Verifiche**:

1. **Password Corretta**:
   ```bash
   mysql -u root -p
   # Inserisci password
   ```

2. **Firewall**:
   - Assicurati che porta 3306 non sia bloccata

3. **Bind Address**:
   - Verifica in `/etc/mysql/mysql.conf.d/mysqld.cnf`:
     ```ini
     bind-address = 127.0.0.1
     ```

---

### Errori di Performance

**Problema**: Applicazione lenta

**Soluzioni**:

1. **Usa MySQL invece di SQLite**
2. **Aumenta RAM disponibile**
3. **Chiudi altre applicazioni**

---

## Supporto

Per ulteriore assistenza:

- **GitHub Issues**: https://github.com/yourusername/mypersonalmap/issues
- **Documentation**: `/doc` directory nel repository

---

## Aggiornamenti

Per aggiornare l'applicazione:

1. Scarica la nuova versione dalla pagina Releases
2. Chiudi l'applicazione corrente
3. Sostituisci i file con la nuova versione
4. Il database verrà aggiornato automaticamente al primo avvio

**Importante**: Fai sempre un backup del database prima di aggiornare!

```bash
# Backup database
mysqldump -u mypersonalmap_user -p mypersonalmap > backup_$(date +%Y%m%d).sql
```

---

**Buon utilizzo di My Personal Map! 🗺️**
