# Monitoring cron job — surveillance quotidienne du VPS

Ce job Hermes s'exécute quotidiennement avec le profile `nico_monitoring`.

## Création du cron job

```bash
hermes cron create "0 8 * * *" \
    --name monitoring-daily \
    --profile monitoring \
    --prompt "Tu es le Monitoring Agent. Fais un rapport complet du VPS : CPU, RAM, disque, Docker, Nginx, SSL, sauvegardes. Alerter si un seuil est dépassé." \
    --deliver origin
```

## Script pré-collection (optionnel)

Avec `no_agent=True`, le job peut exécuter un script qui collecte les métriques brutes :

```bash
mkdir -p ~/scripts/monitoring
cat > ~/scripts/monitoring/collect.sh <<'EOF'
#!/bin/bash
echo "=== SYSTEM ==="
free -h
df -h /
echo "=== DOCKER ==="
docker ps --format "table {{.Names}}\t{{.Status}}"
echo "=== NGINX ==="
systemctl is-active nginx || true
echo "=== SSL ==="
for domain in example.com www.example.com; do
    echo -n "$domain: "
    echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -dates | grep notAfter || echo "ERREUR"
done
echo "=== BACKUP ==="
# Adapter selon l'outil de backup (restic snapshots / rclone / rsync)
ls -lt /backups | head -5 || echo "pas de dossier /backups"
EOF
chmod +x ~/scripts/monitoring/collect.sh
```

Puis relier le script au cron :

```bash
hermes cron edit monitoring-daily
# ajouter script: ~/scripts/monitoring/collect.sh
```

## Seuils par défaut

Voir le skill `nico_monitoring` dans `profiles/monitoring/SKILL.md`.

## Exemple de rapport attendu

```markdown
## Rapport monitoring — 2026-08-02 08:00

### Système
- CPU : 12 %
- RAM : 4.2 / 8 GB (52 %)
- Disque : 45 / 100 GB (45 %)

### Docker
- 5/5 conteneurs actifs
- 0 en erreur

### Nginx
- Actif
- 2 erreurs 5xx sur 24h

### SSL
- example.com : expire dans 45 jours ✅

### Sauvegardes
- Dernière : 2026-08-01 03:00 ✅

### Alertes
- Aucune
```
