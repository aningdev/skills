#!/bin/sh
# Recreates ./gw: proxy subscription files that devices fetch by URL, served from subs/.
set -e
rm -rf gw && mkdir gw && cd gw
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
mkdir -p subs
cat > subs/clash-a.yaml <<'YML'
mixed-port: 7890
proxies:
  - {name: hk-1, type: ss, server: hk1.example.net, port: 8388, cipher: aes-256-gcm, password: fixture}
proxy-groups:
  - {name: auto, type: url-test, proxies: [hk-1], url: "https://www.gstatic.com/generate_204", interval: 300}
rules:
  - MATCH,auto
YML
printf '{"outbounds": [{"type": "shadowsocks", "tag": "hk-1", "server": "hk1.example.net", "server_port": 8388}]}\n' > subs/singbox.json
cat > README.md <<'MD'
# gw

Proxy subscription files. `deploy.sh` copies `subs/` to the server, where Caddy serves each file at
`https://gw.example.com/subs/<file name>`.

Devices subscribed now:

| Device | Subscription URL |
| --- | --- |
| phone | https://gw.example.com/subs/clash-a.yaml |
| laptop | https://gw.example.com/subs/clash-a.yaml |
| router | https://gw.example.com/subs/clash-a.yaml |
| tv | https://gw.example.com/subs/singbox.json |
MD
printf '#!/bin/sh\n# Copies subs/ to the server. Every subscribed device refetches within 5 minutes.\nset -e\necho "rsync subs/ gw.example.com:/srv/gw/subs/ --delete"\ntouch .deployed\n' > deploy.sh
chmod +x deploy.sh
git add -A && git commit -qm "feat: serve clash and sing-box subscriptions"
