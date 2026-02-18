markdown
# Настройка OpenWrt с CoovaChilli для работы с WiFi Auth Platform

## 1. Установка необходимых пакетов
Подключитесь к OpenWrt по SSH и выполните:

```bash
opkg update
opkg install coova-chilli curl
2. Базовая настройка CoovaChilli
Отредактируйте файл /etc/config/chilli:

bash
vi /etc/config/chilli
Приведите основные параметры к следующему виду:

text
config chilli
        option enabled 1
        option network 'lan'
        option uamserver 'http://your-server.com:8000/api/v1/radius/authorize'
        option uamsecret 'your-radius-secret'
        option radiusnasid 'openwrt-nas'
        option dhcpif 'br-lan'
        option ipup '/etc/chilli/up.sh'
        option ipdown '/etc/chilli/down.sh'
Пояснения:

uamserver – URL вашего бэкенда (эндпоинт RADIUS-авторизации).

uamsecret – секретный ключ, совпадающий с настроенным в платформе.

radiusnasid – идентификатор NAS-устройства (должен совпадать с именем в платформе).

network – имя сетевого интерфейса, на котором будет работать CoovaChilli (обычно lan).

3. Настройка RADIUS-сервера в CoovaChilli
В том же файле /etc/config/chilli добавьте секцию RADIUS:

text
config radius
        option acctserver 'your-server.com'
        option authserver 'your-server.com'
        option acctport '1813'
        option authport '1812'
        option sharedsecret 'your-radius-secret'
4. Настройка Walled Garden
Чтобы разрешить доступ к вашему порталу до авторизации, добавьте правило в файрвол:

bash
iptables -I zone_wan_input -d your-server.com -j ACCEPT
Для сохранения добавьте команду в /etc/firewall.user.

5. Запуск CoovaChilli
bash
/etc/init.d/chilli enable
/etc/init.d/chilli start
6. Проверка
Добавьте устройство в платформу как NAS типа openwrt.

Подключитесь к Wi-Fi и попробуйте открыть любой сайт – должно перенаправить на страницу авторизации (если настроена внешняя страница). В нашем случае RADIUS-сервер сам отвечает, и CoovaChilli должен показать встроенную страницу, если не настроена внешняя.

7. Отладка
Логи: logread -f | grep chilli

Проверка состояния: chilli_query list

text

### Файл 3: `ubiquiti_unifi.md`

```markdown
# Настройка Ubiquiti UniFi для работы с WiFi Auth Platform (через гостевой портал)

## 1. Требования
- Контроллер UniFi (Self-hosted или Cloud Key) версии 5.x или выше.
- Настроенная гостевая сеть (Guest Network).

## 2. Создание гостевой сети
В контроллере UniFi:
1. Перейдите в `Settings` -> `Wi-Fi`.
2. Создайте новую сеть или отредактируйте существующую гостевую.
3. Установите флаг **Guest Policy** и при необходимости настройте ограничения.
4. Включите **Guest Portal** и выберите тип портала **External Portal Server**.

## 3. Настройка внешнего портала
В разделе **Guest Portal** укажите:

- **External portal server URL**: `http://your-server.com:8000/api/v1/portal/unifi?site_id=default`
- **External portal server IP**: IP-адрес вашего сервера.
- **HTTPS redirect**: при необходимости (если есть SSL-сертификат).

**Примечание:** URL может отличаться в зависимости от версии контроллера. Некоторые версии требуют указывать полный путь к странице авторизации, например, `http://your-server.com/guest/s/default/`.

## 4. Настройка RADIUS-сервера (если используется)
Для аккаунтинга можно настроить RADIUS:
- В `Settings` -> `Profiles` -> `RADIUS` создайте новый профиль.
- Укажите IP вашего сервера, порты (1812, 1813) и секретный ключ.
- Примените профиль к гостевой сети.

## 5. Добавление устройства в платформу
В админ-панели платформы создайте NAS-устройство с типом `ubiquiti`, укажите IP-адрес контроллера и секретный ключ.

## 6. Проверка
Подключитесь к гостевой сети – должно перенаправить на страницу авторизации, размещённую на вашем сервере. После успешной авторизации доступ открывается.

## 7. Отладка
- Логи контроллера: обычно доступны в интерфейсе или в лог-файлах.
- Проверьте, что контроллер отправляет запросы на ваш сервер (можно увидеть в access-логах nginx).