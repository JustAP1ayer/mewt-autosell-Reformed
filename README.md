# Mewt-AutoResell-Reformed

> What is it?
- It gathers all the UGC Limiteds you have and sells all the one that are out of its holding period according to your settings.

## Credits 
- [Mewt](https://discord.gg/mewt)
- [Redblue]([https://discord.gg/javaw](https://www.roblox.com/users/116781531/profile))

## Requirements
- [Python](https://www.python.org/downloads/)
- [requests](https://pypi.org/project/requests/)
- [colorama](https://pypi.org/project/colorama/)
- [rgbprint](https://pypi.org/project/rgbprint/)

## Discwaimew
If you do pwany ony usinyg this, anyd if somethinyg goes wwonyg anyd you woose wobux. You wiww nyot be wefunyded as you awe usinyg this by youw owny choice.~ ~v~

## Installation
Grab the latest version from [here]([https://github.com/workframes/mewtxjava-autosell/releases](https://github.com/JustAP1ayer/mewt-autosell-Reformed/tree/main))
If you are running this on `Mac OS` run it using `main.py`, if you are running it on `Windows` you can run it with either `start.bat` or `main.py`

## Settings Documentaion
- `COOKIE`
    * The `.ROBLOXSECURITY` of the acount you want to sell items on.
- `KEEP_SERIALS`
    * The serials you keep, this will not put up any resales if its equal or lower to the value
- `KEEP_COPIES`
    * The copies you keep, this will not put up any resales if its equal or lower to the value
- `CUSTOM_VALUES`
    * These are the custom prices that will be used to for the sell method `CUSTOM` While using this only the items included in custom values will be resold. Example:
        * ```json
            "CUSTOM_VALUES": {
                "13345169760": 40
            }
            ```
- `BLACKLIST` 
    * If a item is in this list, it will not put it up for resale.
- `WEBHOOK`
    * If you have this enabled it will send notfications when a item sells.
    - `ENABLED`
        * `true` to enabled the feature
        * `false` to disable the feature
    - `URL`
        * If you have enabled you must have a discord webhook.
## Example Settings
```json
{
    "KEEP_SERIALS": 5,
    "KEEP_COPIES": 1,
    "BLACKLIST": [
        13636293210
    ],
    "WEBHOOK": {
        "ENABLED": true,
        "URL": "https://discord.com/api/webhooks/abc/abc"
    }
}
```
