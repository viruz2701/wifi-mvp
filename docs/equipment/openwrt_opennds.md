# Настройка OpenWrt с OpenNDS для работы с WiFi Auth Platform

## Установка пакетов
```bash
opkg update
opkg install opennds


Отредактируйте файл /etc/config/opennds:

text
config opennds
        option enabled 1
        option fashost 'your-server.com'   # адрес вашего сервера
        option fasport 443                  # порт (80 или 443)
        option faspath '/api/v1/portal/opennds'  # путь к FAS
        option dhcpstart 100
        option dhcpend 200
        option network 'lan'
Замените your-server.com на реальный адрес вашего сервера.

Перезапуск сервиса
bash
/etc/init.d/opennds restart
Проверка
Подключитесь к Wi-Fi и убедитесь, что вы перенаправляетесь на страницу авторизации.