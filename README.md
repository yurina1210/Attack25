# Attack25
![ScreenShot](https://github.com/kuboyoo/Attack25/blob/master/img/ss.gif)

## Requirements
- Python3
- pygame (for BGM)

## Information
- If you need sound effects, make "bgms" directory and put audio files(mp3, mov, etc...) there.
- If you don't need socket function, comment out L.242 - L.254( with socket.socket ... print(repr(data)) ) in attack25.py.

## Usage
1. `python3 attack25.py`
2. press key "esc" => save panels information ./datas/chanp_panels*.txt & finish program
3. `mkdir photos_for_film_quiz`
4. put photos there
5. `python3 film_quiz.py`

## Key Bind
|key|mode|
|:--|:--|
|'r'|red team mode|
|'g'|green team mode|
|'w'|white team mode|
|'b'|blue team mode|
|'a'|attack chance mode|
|','|back 1 turn|
|'.'|reset panels|

if you don't need BGM, ignore below.

|key|mode|
|:--|:--|

|'m'|mistake BGM play|
|'s'|success BGM play|
|'S'|all BGM stop|
|'t'|thinking time BGM play|
|'A'|attack chance question pre BGM play|

## Reference
[Wikipedia](https://en.wikipedia.org/wiki/Panel_Quiz_Attack_25)
