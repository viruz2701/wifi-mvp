# Настройка MikroTik (RouterOS) для работы с WiFi Auth Platform

## Содержание
- [Предварительные требования](#предварительные-требования)
- [Регистрация устройства в платформе](#регистрация-стройства-в-платформе)
- [Базовая настройка Hotspot](#базовая-настройка-hotspot)
- [Настройка RADIUS-клиента](#настройка-radius-клиента)
- [Настройка WireGuard для защищённого управления](#настройка-wireguard-для-защищённого-управления)
- [Проверка подключения](#проверка-подключения)
- [Устранение неполадок](#устранение-неполадок)
- [Полезные скрипты](#полезные-скрипты)

## Предварительные требования
- RouterOS версии 6.49 или выше (рекомендуется 7.x)
- Настроенный интерфейс для гостевой сети (например, bridge с DHCP-сервером)
- Доступ к устройству через SSH, WinBox или WebFig
- Зарегистрированное NAS-устройство в панели управления платформы (см. ниже)

## Регистрация устройства в платформе
1. Войдите в административную панель под учётной записью с правами суперпользователя.
2. Перейдите в раздел **NAS-устройства** → **Добавить**.
3. Заполните поля:
   - **Площадка** – выберите площадку, к которой относится устройство.
   - **Название** – например, «MikroTik в холле».
   - **Тип** – выберите `MikroTik`.
   - **IP-адрес** – публичный IP или WireGuard IP устройства (если планируется туннель).
   - **RADIUS secret** – придумайте сложный ключ (например, сгенерируйте случайную строку).
   - **API username / password** – укажите учётные данные для доступа к API (обычно admin и пароль).
   - **WireGuard** – если устройство находится за NAT, включите **«Сгенерировать ключи автоматически»**. Система создаст пару ключей и покажет IP для туннеля.
4. Сохраните устройство. Запишите сгенерированные параметры WireGuard (если использовали) – они понадобятся при настройке туннеля на роутере.

## Базовая настройка Hotspot

### Через командную строку (SSH)
Подключитесь к маршрутизатору по SSH. Выполните следующие команды (замените `RADIUS_SERVER_IP` и `SECRET` на свои значения):

```bash
# Создание bridge для гостевой сети
/interface bridge add name=bridge_guest

# Назначение IP-адреса
/ip address add address=192.168.100.1/24 interface=bridge_guest

# Настройка DHCP
/ip pool add name=pool_guest ranges=192.168.100.2-192.168.100.254
/ip dhcp-server add name=dhcp_guest interface=bridge_guest address-pool=pool_guest
/ip dhcp-server network add address=192.168.100.0/24 gateway=192.168.100.1 dns-server=8.8.8.8

# Включение Hotspot
/ip hotspot add name=hotspot1 interface=bridge_guest
/ip hotspot profile set [find] use-radius=yes

# Добавление RADIUS-сервера
/radius add address=RADIUS_SERVER_IP secret=SECRET service=hotspot
/radius incoming set accept=yes
Примечание: RADIUS_SERVER_IP должен быть доступен с роутера. Если платформа находится за NAT, используйте WireGuard IP (см. следующий раздел).

Через WinBox
Перейдите в меню IP → Hotspot → Hotspot Setup и следуйте мастеру, выбрав интерфейс bridge_guest.

После создания сервера откройте его настройки, перейдите на вкладку RADIUS и включите Use RADIUS.

В меню RADIUS добавьте сервер:

Address – IP платформы.

Secret – секретный ключ.

Service – выберите hotspot.

Включите Accounting (если нужен учёт трафика).

На вкладке Incoming установите галочку Accept для приёма запросов от сервера (опционально).

Настройка RADIUS-клиента
Убедитесь, что в настройках RADIUS указаны правильные порты (по умолчанию 1812 для авторизации, 1813 для аккаунтинга). В большинстве случаев этого достаточно.

Настройка WireGuard для защищённого управления
Если роутер находится за NAT или не имеет статического публичного IP, рекомендуется использовать WireGuard-туннель для связи с платформой.

Получение параметров от платформы
При регистрации устройства с опцией «Сгенерировать ключи автоматически» платформа создаст:

Приватный ключ (скачивается в виде файла)

Публичный ключ (уже сохранён в настройках NAS)

IP-адрес туннеля (например, 10.0.0.2/24)

Адрес сервера (endpoint) – публичный адрес платформы с портом WireGuard (обычно 51820)

Настройка WireGuard на MikroTik
Создайте интерфейс WireGuard:

text
/interface wireguard add name=wg1 private-key="<скопируйте приватный ключ из файла>"
Назначьте IP-адрес интерфейсу (тот, который выдала платформа):

text
/ip address add address=10.0.0.2/24 interface=wg1
Добавьте пир (сервер платформы):

text
/interface wireguard peers add interface=wg1 public-key="<публичный ключ сервера>" endpoint-address=<IP_сервера> endpoint-port=51820 allowed-address=10.0.0.0/24
Публичный ключ сервера можно получить в настройках платформы (раздел Настройки → WireGuard).

Включите интерфейс:

text
/interface wireguard enable wg1
Проверьте состояние туннеля:

text
/interface wireguard peers print
Теперь для связи с платформой используйте IP туннеля (например, 10.0.0.1) вместо публичного адреса в настройках RADIUS и API.

Настройка маршрутов (опционально)
Если необходимо, чтобы весь трафик управления шёл через туннель, добавьте маршрут:

text
/ip route add dst-address=<сеть платформы> gateway=10.0.0.1
Проверка подключения
В панели управления платформы убедитесь, что устройство отображается как online (статус обновляется раз в минуту).

Подключитесь к гостевой Wi-Fi сети любым устройством.

Откройте браузер – вы должны быть перенаправлены на страницу авторизации (внешний портал или встроенная страница).

Введите номер телефона, получите SMS с кодом и подтвердите его.

После успешной авторизации доступ в интернет должен открыться.

В платформе проверьте появление новой сессии в разделе Сессии или Пользователи Wi-Fi.

Устранение неполадок
Проблема	Возможная причина	Решение
Устройство offline	Недоступен порт RADIUS (1812) или API (8728)	Проверьте доступность с сервера: nc -zv <IP> 8728. Убедитесь, что firewall не блокирует трафик.
Пользователь не перенаправляется на портал	Неправильные настройки DHCP или DNS	Проверьте, что на интерфейсе bridge_guest включён DHCP и клиенты получают адреса.
RADIUS-запросы не доходят	Неправильный secret или IP сервера	Сверьте secret в настройках RADIUS на роутере и в платформе. Проверьте, что IP сервера указан верно (особенно при использовании WireGuard).
Туннель WireGuard не поднимается	Неверные ключи или endpoint	Проверьте правильность ввода публичного ключа сервера и приватного ключа. Убедитесь, что на сервере открыт порт 51820/UDP.
Полезные скрипты
Автоматическая настройка Hotspot и RADIUS
Сохраните скрипт setup_mikrotik.rsc и выполните его через import или в терминале:

text
:global radiusServer "10.0.0.1"
:global radiusSecret "mySecretKey"

/interface bridge add name=bridge_guest
/ip address add address=192.168.100.1/24 interface=bridge_guest
/ip pool add name=pool_guest ranges=192.168.100.2-192.168.100.254
/ip dhcp-server add name=dhcp_guest interface=bridge_guest address-pool=pool_guest
/ip dhcp-server network add address=192.168.100.0/24 gateway=192.168.100.1 dns-server=8.8.8.8
/ip hotspot add name=hotspot1 interface=bridge_guest
/ip hotspot profile set [find] use-radius=yes
/radius add address=$radiusServer secret=$radiusSecret service=hotspot
/radius incoming set accept=yes
Мониторинг состояния WireGuard
text
:foreach peer in=[/interface wireguard peers find] do={
    :local intf [/interface wireguard peers get $peer interface]
    :local pubkey [/interface wireguard peers get $peer public-key]
    :local endpoint [/interface wireguard peers get $peer endpoint-address]
    :local status [/interface wireguard peers get $peer allowed-address]
    :put "$intf : $pubkey -> $endpoint : $status"
}




1. Настройка MikroTik (RouterOS) с RADIUS и Hotspot, включая WireGuard для управления
1.1. Общая схема
Гостевая сеть – отдельный bridge с DHCP и Hotspot.

RADIUS-авторизация – все запросы авторизации и учёта направляются на сервер платформы.

WireGuard-туннель (опционально) – используется для защищённого управления, если устройство не имеет публичного IP или находится за NAT.

1.2. Настройка WireGuard на MikroTik (если необходимо)
Предварительно в панели администратора при регистрации NAS-устройства включите опцию «Сгенерировать ключи автоматически». После сохранения вы получите:

Приватный ключ (можно скачать)

Публичный ключ (уже сохранён в платформе)

IP-адрес WireGuard (например, 10.0.0.2/24)

Публичный ключ сервера и endpoint (будут доступны в разделе Настройки → WireGuard)

Теперь настройте WireGuard на MikroTik.

Через командную строку (SSH):

bash
# Создать интерфейс wg0 с вашим приватным ключом
/interface wireguard add name=wg0 private-key="ВАШ_ПРИВАТНЫЙ_КЛЮЧ"

# Назначить IP-адрес
/ip address add address=10.0.0.2/24 interface=wg0

# Добавить пир (сервер платформы)
/interface wireguard peers add interface=wg0 \
  public-key="ПУБЛИЧНЫЙ_КЛЮЧ_СЕРВЕРА" \
  endpoint-address="АДРЕС_СЕРВЕРА" endpoint-port=51820 \
  allowed-address=10.0.0.0/24
Проверьте связь: ping 10.0.0.1 (это IP сервера в туннеле).

1.3. Настройка Hotspot с RADIUS
Шаг 1. Создание bridge для гостевой сети

bash
/interface bridge add name=bridge_guest
/ip address add address=192.168.100.1/24 interface=bridge_guest
Шаг 2. Настройка DHCP-сервера

bash
/ip pool add name=pool_guest ranges=192.168.100.2-192.168.100.254
/ip dhcp-server add name=dhcp_guest interface=bridge_guest address-pool=pool_guest
/ip dhcp-server network add address=192.168.100.0/24 \
  gateway=192.168.100.1 dns-server=8.8.8.8
Шаг 3. Включение Hotspot

bash
/ip hotspot add name=hotspot1 interface=bridge_guest
/ip hotspot profile set [find] use-radius=yes
Шаг 4. Добавление RADIUS-сервера

Если используется WireGuard, укажите IP сервера из туннеля (10.0.0.1). Если устройство имеет прямой доступ к серверу, укажите его публичный IP.

bash
/radius add address=10.0.0.1 secret=ВАШ_RADIUS_SECRET service=hotspot
/radius incoming set accept=yes
Шаг 5. Проверка

Убедитесь, что в панели администратора устройство отображается как online.

Подключитесь к гостевой Wi-Fi сети, откройте браузер – должна появиться страница авторизации (встроенная или внешняя, в зависимости от настроек портала).

1.4. Автоматический скрипт для MikroTik
Сохраните как setup_mikrotik_full.sh:

bash
#!/bin/bash
# Полная настройка MikroTik: WireGuard + Hotspot + RADIUS

if [ $# -lt 5 ]; then
    echo "Использование: $0 <IP_роутера> <RADIUS_секрет> <WG_приватный_ключ> <WG_публичный_ключ_сервера> <WG_сервер_endpoint>"
    exit 1
fi

ROUTER_IP=$1
RADIUS_SECRET=$2
WG_PRIV=$3
WG_SERVER_PUB=$4
WG_ENDPOINT=$5

ssh admin@$ROUTER_IP <<EOF
# WireGuard
/interface wireguard add name=wg0 private-key="$WG_PRIV"
/ip address add address=10.0.0.2/24 interface=wg0
/interface wireguard peers add interface=wg0 public-key="$WG_SERVER_PUB" endpoint-address=${WG_ENDPOINT%:*} endpoint-port=${WG_ENDPOINT##*:} allowed-address=10.0.0.0/24

# Hotspot
/interface bridge add name=bridge_guest
/ip address add address=192.168.100.1/24 interface=bridge_guest
/ip pool add name=pool_guest ranges=192.168.100.2-192.168.100.254
/ip dhcp-server add name=dhcp_guest interface=bridge_guest address-pool=pool_guest
/ip dhcp-server network add address=192.168.100.0/24 gateway=192.168.100.1 dns-server=8.8.8.8
/ip hotspot add name=hotspot1 interface=bridge_guest
/ip hotspot profile set [find] use-radius=yes
/radius add address=10.0.0.1 secret=$RADIUS_SECRET service=hotspot
/radius incoming set accept=yes
EOF

echo "Настройка завершена."