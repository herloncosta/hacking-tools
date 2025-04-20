
# 🔍 Python Port Scanner

Scanner de portas TCP com suporte a multithreading, captura de banners e exportação de resultados em JSON/CSV. Ideal para análises de segurança ofensiva, pentests e automações de reconhecimento.

---

## 🚀 Como usar

```bash
python3 scanner.py -t <alvo> [opções]
```

### Parâmetros obrigatórios

- `-t`, `--target` : IP ou hostname do alvo.

### Parâmetros opcionais

- `-p`, `--ports` : Range de portas (ex: `1-65535`). Padrão: `1-1024`
- `--threads` : Número de threads simultâneas. Padrão: `100`
- `--timeout` : Timeout de conexão em segundos. Padrão: `1.0`
- `--verbose` : Exibe progresso durante o scan.
- `--banners` : Ativa a coleta de banners dos serviços.
- `--output` : Exporta os resultados para arquivo `.json` ou `.csv`

---

## 🧪 Exemplo de uso

```bash
python3 scanner.py -t 192.168.1.1 -p 1-1000 --threads 50 --banners --output resultado.json
```

---

## 📝 Exemplo de saída

```text
[+] 22/tcp open - SSH-2.0-OpenSSH_8.2
[+] 80/tcp open - HTTP/1.1 200 OK
[✔] Portas abertas encontradas em 192.168.1.1:
    - 22/tcp open | SSH-2.0-OpenSSH_8.2
    - 80/tcp open | HTTP/1.1 200 OK

[💾] Resultados exportados para resultado.json
```

---

## 📂 Estrutura do JSON exportado

```json
[
    {
        "target": "192.168.1.1",
        "port": 22,
        "status": "open",
        "banner": "SSH-2.0-OpenSSH_8.2"
    }
]
```

---

## 🛡️ Requisitos

- Python 3.x
- Nenhuma dependência externa para funcionalidades básicas
- Para expansão com DNS/WHOIS: `dnspython`, `python-whois`

---

## 📣 Contribuição

Pull requests e sugestões são bem-vindas! Aproveite, evolua e compartilhe.

