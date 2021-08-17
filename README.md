# BaiduTranslate-Terminal
 A command line implement of Baidu Translation

## Acknowledge

API provider: http://api.fanyi.baidu.com/api/trans/vip/translate

## Usage

1. Visit https://api.fanyi.baidu.com/ to acquire your appid and appkey.
2. Input your appid&appkey into the config file.(If this is your first time using this implement, prgram will ask you to do so.)
3. Input a word to inquiry its translation.
4. Commands:

* About language.

    `@lang en-zh`: Switch language (e.g. en-zh meaning translate English to Chinese) (default en-zh)
    
    `@langtb`: Display part of the supported language code.(Visit https://api.fanyi.baidu.com/doc/21 to get the full list.)


* About history.

    `@clr`: Clear all translating history.

    `@disp`: Display all translating history.


* Exit program.

    `@exit`: Exit the program
