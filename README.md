# Attack25
![ScreenShot](https://github.com/kuboyoo/Attack25/blob/master/img/ss.gif)

## Requirements
- Python3
- pygame (for BGM)

## Notification
- This program has 2 mode (1. Default mode, 2. Transition mode)
- Default mode is non-transition mode (line. 243 - 258 is commented out in "main.py").
- If you change to Transition mode, cancel line. 243 - 258 's comment.

## Usage
1. Default mode
    1. `python3 main.py`
    2. Press key "esc" => save panels information ./datas/chanp_panels*.txt & finish program
    3. `mkdir photos_for_film_quiz`
    4. Put photos there
    5. `python3 film_quiz.py`

2. Transition mode
This mode needs rooter, main PC and 4 sub PCs.
    1. On rooter, setting each IP Address (e.g. rooter: `192.168.0.1`, main PC: `192.168.0.2`, sub PC: `192.168.0.3` - `192.168.0.6`)
    2. On sub terminal, `python3 sub.py`
    3. On main terminal, `python3 main.py`
    4. Later just like 1.iii - 1.v

## Key Bind
|key|mode|
|:--|:--|
|'r'|red team mode|
|'g'|green team mode|
|'w'|white team mode|
|'b'|blue team mode|
|'a'|attack chance mode|
|'q'|all sub PC's color painting reset|
|'c'|suggest function cancel|
|','|back 1 turn|
|'.'|reset panels|

About BGM

|key|mode|
|:--|:--|
|'m'|mistake BGM play|
|'s'|success BGM play|
|'S'|all BGM stop|
|'t'|thinking time BGM play|

## Reference
- [Wikipedia](https://en.wikipedia.org/wiki/Panel_Quiz_Attack_25)
- [ポケットサウンド/効果音素材](https://pocket-se.info/)
