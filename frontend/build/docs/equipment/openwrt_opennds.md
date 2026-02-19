
### 2. Обновлённый `docs/equipment/openwrt_opennds.md`

```markdown
# Настройка OpenWrt с OpenNDS для работы с WiFi Auth Platform

OpenNDS (Open Network Demarcation Service) – это современная и гибкая система Captive Portal, которая пришла на смену NoDogSplash и CoovaChilli. Она поддерживает внешние серверы авторизации (FAS), что позволяет использовать страницы портала, размещённые на нашей платформе.

## Содержание
- [Установка OpenNDS](#установка-opennds)
- [Базовая настройка OpenNDS](#базовая-настройка-opennds)
- [Настройка внешнего FAS (платформы)](#настройка-внешнего-fas-платформы)
- [Дополнительные параметры](#дополнительные-параметры)
- [Проверка работы](#проверка-работы)
- [Интеграция с RADIUS (опционально)](#интеграция-с-radius-опционально)
- [WireGuard для защищённого управления](#wireguard-для-защищённого-управления)
- [Устранение неполадок](#устранение-неполадок)

## Установка OpenNDS
Подключитесь к OpenWrt по SSH и выполните:

```bash
opkg update
opkg install opennds
Пакет будет установлен вместе с зависимостями (включая luci-app-opennds для управления через веб-интерфейс, если нужно).

Базовая настройка OpenNDS
Конфигурационный файл /etc/config/opennds
После установки файл выглядит примерно так:

text
config opennds
        option enabled 0
        option network 'lan'
        option dhcpstart 100
        option dhcpend 200
Для включения и базовой работы достаточно изменить enabled на 1 и указать интерфейс, на котором будет работать портал (обычно lan или отдельный bridge для гостей). Например:

text
config opennds
        option enabled 1
        option network 'lan'
        option dhcpstart 100
        option dhcpend 200
Важно: Интерфейс lan должен иметь включённый DHCP-сервер, чтобы клиенты получали IP-адреса.

Запуск сервиса
bash
/etc/init.d/opennds enable
/etc/init.d/opennds start
После этого при подключении к Wi-Fi клиенты будут перехватываться и видеть стандартную страницу OpenNDS.

Настройка внешнего FAS (платформы)
Чтобы перенаправить пользователей на страницы авторизации, размещённые на нашей платформе, необходимо указать параметры fashost, fasport и faspath.

Отредактируйте /etc/config/opennds:

text
config opennds
        option enabled 1
        option fashost 'your-server.com'      # домен или IP вашего сервера
        option fasport 443                     # порт (80 для HTTP, 443 для HTTPS)
        option faspath '/api/v1/portal/opennds' # путь к эндпоинту OpenNDS на бэкенде
        option dhcpstart 100
        option dhcpend 200
        option network 'lan'
Пояснения:

fashost – должен быть доступен с клиентских устройств (публичный IP или домен). Если сервер за NAT, используйте WireGuard (см. ниже).

fasport – 443 для HTTPS, 80 для HTTP. Убедитесь, что на сервере настроен SSL, если используете 443.

faspath – этот путь должен соответствовать маршруту в бэкенде (см. opennds.py).

После изменения конфигурации перезапустите OpenNDS:

bash
/etc/init.d/opennds restart
Теперь при подключении к Wi-Fi клиенты будут перенаправляться на страницу платформы (например, https://your-server.com/api/v1/portal/opennds?clientip=...&gatewayname=...&tok=...).

Дополнительные параметры
Таймауты и лимиты
Вы можете настроить время сессии, лимиты трафика и другие параметры. Например:

text
option sessiontimeout 3600      # секунды
option idletimeout 600
option uploadrate 1024          # скорость в кбит/с
option downloadrate 2048
Список разрешённых доменов (Walled Garden)
Чтобы некоторые сайты были доступны до авторизации (например, страница портала), добавьте их в список:

text
option walled_garden_fqdn 'your-server.com,accounts.google.com'
Проверка работы
Убедитесь, что OpenNDS запущен: ps | grep opennds.

Подключитесь к гостевой Wi-Fi сети.

Откройте браузер – вы должны быть перенаправлены на страницу авторизации платформы.

Введите номер телефона, получите SMS, подтвердите код.

После успеха вы должны попасть на приветственную страницу и получить доступ в интернет.

В платформе проверьте появление сессии.

Интеграция с RADIUS (опционально)
Если вы хотите использовать RADIUS для учёта трафика и управления сессиями (например, чтобы видеть в платформе активные сессии и трафик), можно настроить OpenNDS на отправку RADIUS-пакетов.

Установите пакет freeradius или используйте встроенную поддержку RADIUS в OpenNDS (требуется дополнительная компиляция). Проще всего настроить отправку аккаунтинга через radclient с помощью скриптов. Однако в текущей версии платформы для OpenNDS достаточно работы через FAS – RADIUS не обязателен, так как все данные о сессиях платформа получает через события от FAS и RADIUS-аккаунтинг от самого устройства (если настроен). Рекомендуется всё же настроить RADIUS-клиент на OpenWrt для отправки accounting-пакетов.

Настройка RADIUS-клиента (радиуса) на OpenWrt
Установите freeradius3 или radsecproxy, но проще использовать пакет radclient для отправки пакетов из скриптов.

В конфигурации OpenNDS можно добавить скрипты событий, которые будут вызывать radclient. Например, в файле /etc/config/opennds:

text
option userscript '/etc/opennds/script.sh'
А в скрипте обрабатывать события и отправлять accounting.

Примечание: Детальная настройка RADIUS выходит за рамки данного руководства. Для большинства сценариев достаточно работы через FAS.

WireGuard для защищённого управления
Если ваша платформа находится за NAT или вы хотите обеспечить шифрованный канал для обмена данными между OpenWrt и сервером, можно использовать WireGuard.

Настройка WireGuard на OpenWrt
Установите пакет WireGuard:

bash
opkg update
opkg install wireguard-tools luci-proto-wireguard
Создайте интерфейс WireGuard в /etc/config/network (пример):

text
config interface 'wg0'
    option proto 'wireguard'
    option private_key 'YOUR_PRIVATE_KEY'
    list addresses '10.0.0.2/24'

config wireguard_wg0
    option public_key 'SERVER_PUBLIC_KEY'
    option endpoint_host 'your-server.com'
    option endpoint_port '51820'
    list allowed_ips '10.0.0.0/24'
Приватный ключ можно сгенерировать командой wg genkey.

Перезапустите сеть:

bash
/etc/init.d/network restart
Проверьте статус:

bash
wg show
Теперь в настройках OpenNDS укажите fashost равным WireGuard IP сервера (например, 10.0.0.1). Убедитесь, что клиенты могут достучаться до этого IP (возможно, потребуется настроить маршруты или SNAT).

Устранение неполадок
Проблема	Возможная причина	Решение
Клиенты не перенаправляются на портал	OpenNDS не запущен или неправильный интерфейс	Проверьте статус: /etc/init.d/opennds status. Убедитесь, что network указан верно.
Ошибка «Could not resolve host» при обращении к FAS	Проблемы с DNS на клиентском устройстве	Убедитесь, что DHCP выдаёт корректные DNS-серверы. Добавьте option dns '8.8.8.8' в настройки DHCP.
Страница портала загружается, но код не приходит	Проблемы с SMS-провайдером	Проверьте настройки SMS-провайдеров в платформе. Временно включите логирование и посмотрите ответы.
Туннель WireGuard не поднимается	Неправильные ключи или firewall	Проверьте, что на сервере открыт порт 51820/UDP. Сверьте публичные ключи.
Полезные скрипты
Автоматическая настройка OpenNDS
Сохраните как setup_opennds.sh и выполните на OpenWrt:

bash
#!/bin/sh

FAS_HOST="your-server.com"
FAS_PORT="443"
FAS_PATH="/api/v1/portal/opennds"

# Установка пакета
opkg update
opkg install opennds

# Конфигурация
cat > /etc/config/opennds <<EOF
config opennds
        option enabled 1
        option fashost '$FAS_HOST'
        option fasport $FAS_PORT
        option faspath '$FAS_PATH'
        option dhcpstart 100
        option dhcpend 200
        option network 'lan'
EOF

# Запуск
/etc/init.d/opennds enable
/etc/init.d/opennds restart

echo "OpenNDS настроен. Проверьте статус: /etc/init.d/opennds status"
Просмотр активных клиентов
bash
cat /tmp/opennds/ndsctl.sock | ndsctl status
Принудительное завершение сессии клиента
bash
ndsctl logout <mac-address>
Эти инструкции покрывают основные сценарии. При возникновении сложностей обращайтесь к логам OpenNDS (logread -e opennds) и логам платформы.


 Настройка OpenWrt с OpenNDS и внешним FAS
OpenNDS (Open Network Demarcation Service) – современная замена CoovaChilli, поддерживающая внешние FAS-серверы. В нашем случае FAS – это сама платформа (эндпоинт /api/v1/portal/opennds).

2.1. Установка OpenNDS
Подключитесь к OpenWrt по SSH и выполните:

bash
opkg update
opkg install opennds
2.2. Настройка конфигурации OpenNDS
Отредактируйте файл /etc/config/opennds:

bash
vi /etc/config/opennds
Приведите его к следующему виду (замените your-server.com на домен или IP вашего сервера):

text
config opennds
        option enabled 1
        option fashost 'your-server.com'
        option fasport 443
        option faspath '/api/v1/portal/opennds'
        option dhcpstart 100
        option dhcpend 200
        option network 'lan'
Пояснения:

fashost – адрес вашего сервера (можно использовать IP, но лучше домен с HTTPS).

fasport – порт (80 для HTTP, 443 для HTTPS). Рекомендуется использовать HTTPS, если настроен SSL.

faspath – путь к эндпоинту FAS на бэкенде (должен совпадать с маршрутом в opennds.py).

network – имя интерфейса, на котором будет работать OpenNDS (обычно lan для гостевой сети).

Если гостевая сеть находится на отдельном интерфейсе (например, guest), укажите его.

2.3. Перезапуск сервиса
bash
/etc/init.d/opennds restart
2.4. Настройка WireGuard для управления (опционально)
Если устройство не имеет публичного IP, можно использовать WireGuard аналогично MikroTik.

Установка WireGuard:

bash
opkg update
opkg install wireguard-tools luci-proto-wireguard
Создание конфигурации:

Создайте файл /etc/wireguard/wg0.conf:

text
[Interface]
PrivateKey = ВАШ_ПРИВАТНЫЙ_КЛЮЧ
Address = 10.0.0.3/24
DNS = 8.8.8.8

[Peer]
PublicKey = ПУБЛИЧНЫЙ_КЛЮЧ_СЕРВЕРА
Endpoint = ваш-сервер.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
Затем активируйте интерфейс:

bash
wg-quick up wg0
/etc/init.d/network restart
Для автоматического запуска при загрузке добавьте в /etc/rc.local:

bash
wg-quick up wg0
2.5. Проверка работы OpenNDS
Подключитесь к гостевой Wi-Fi сети.

Откройте браузер – вы должны быть перенаправлены на страницу авторизации платформы (URL вида https://ваш-сервер/api/v1/portal/opennds?clientip=...&gatewayname=...&tok=...).

Введите номер телефона, получите SMS, введите код – доступ должен открыться.

Если страница не загружается, проверьте:

Доступность сервера из гостевой сети (ping, DNS).

Правильность параметров fashost и faspath.

Логи OpenNDS: logread -e opennds.