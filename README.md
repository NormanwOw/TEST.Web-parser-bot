# Web Parser Bot

[@test_web_scrapper_bot](https://t.me/test_web_scrapper_bot)

Telegram bot for site scrapping


## Install
To get started with this BOT you should to edit constant `BOT_TOKEN` in `deploy/.env`.
1. `BOT_TOKEN` you can get from the [@BotFather](https://t.me/BotFather) in the Telegram application.  
More information about this you can find [here](https://core.telegram.org/bots/tutorial)
2. `$ cd deploy && docker compose up -d --build`

## About
File structure: HEADERS - **title** | **url** | **xpath** | **next_page_xpath**  
* **title** - Query description
* **url** - First page site URL
* **xpath** - Path to element with price
* **next_page_xpath** *(nullable)* - Path to element with next page url 

## Test

You can test it with the file [example.xlsx](example.xlsx)
