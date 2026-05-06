     1|# Live selfcheck verification notes
     2|
     3|## Verified in Hermes
     4|
     5|- Required tools checked with `command -v`:
     6|  - `curl`
     7|  - `ffmpeg`
     8|  - `magick`
     9|  - `convert`
    10|  - `ping`
    11|  - `nslookup`
    12|  - `whois`
    13|  - `nmap`
    14|  - `pandoc`
    15|- Actual message delivery was verified by sending test messages to:
    16|  - WhatsApp home channel: `85291628523@s.whatsapp.net`
    17|  - Telegram home channel: `604594539`
    18|
    19|## Operational rule
    20|
    21|If a required tool is missing during selfcheck, alert Telegram immediately after the script run. If WhatsApp or Telegram delivery fails, repair the channel first and then resend the selfcheck message.
    22|