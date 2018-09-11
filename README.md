# Installation

```
git clone https://github.com/Sajam/toggl-cli.git
chmod +x toggl-cli.py
sudo ln -s $(pwd)/toggl-cli.py /usr/local/bin/tcli
```

Create credentials file in `~/.tcli/config`, example:

```
[Account]
user=test@example.com
password=mysecret
```

# Usage

```
$ tcli

1 Blog: Design
2 Blog: Backend
3 Forun: Backend
4 Forum: Frontend

Which task to start? 2

Blog: Backend started.
```

```
$ tcli stop

Stopped.
```