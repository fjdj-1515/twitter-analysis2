# twitter-analysis2

## Installation

```
pipenv install
cp .env.sample .env
$EDITOR .env
```

## Usage

以下のようなスクリプトで実行することを想定している。

```
#!/bin/sh

while true
do
/home/fjdj/.local/bin/pipenv run python notice-user-tweet.py ${userid} 2>> /home/fjdj/twitter-analysis2/err.log > /dev/null;sleep 5; 
done
```