HISTFILE="$ZDOTDIR/.histfile"
HISTSIZE=1500
SAVEHIST=1000
setopt autocd
bindkey -e

## Completion

autoload -U +X compinit && compinit
autoload -U bashcompinit
bashcompinit
eval "$(register-python-argcomplete pipx)"

zstyle ':completion:*' menu select

## History Settings
export HISTORY_IGNORE="(pwd|exit|sudo reboot|history)"
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS

## Compinit Settings
zstyle :compinstall filename "$ZDOTDIR/.zshrc"
autoload -Uz compinit
compinit

## Kitty Settings
if [ "$TERM" = "xterm-kitty" ]; then
	source "$ZDOTDIR/kittyrc"
fi

## ALIASES

# Changing "ls" to "exa"
alias ls='exa -al --color=always --group-directories-first --icons' # my preferred listing
alias la='exa -a --color=always --group-directories-first --icons'  # all files and dirs
alias ll='exa -l --color=always --group-directories-first --icons'  # long format
alias lt='exa -aT --color=always --group-directories-first --icons' # tree listing

# get fastest mirrors
alias mirror="sudo reflector -f 30 -l 30 --number 10 --verbose --save /etc/pacman.d/mirrorlist"
alias mirrord="sudo reflector --latest 50 --number 20 --sort delay --save /etc/pacman.d/mirrorlist"
alias mirrors="sudo reflector --latest 50 --number 20 --sort score --save /etc/pacman.d/mirrorlist"
alias mirrora="sudo reflector --latest 50 --number 20 --sort age --save /etc/pacman.d/mirrorlist"

# Colorize grep output (good for log files)
alias grep='grep --color=auto'

# confirm before overwriting something
alias cp="cp -i"
alias mv='mv -i'

# get error messages from journalctl
alias jctl="journalctl -p 3 -xb"

# gpg encryption
# verify signature for isos
alias gpg-check="gpg2 --keyserver-options auto-key-retrieve --verify"
# receive the key of a developer
alias gpg-retrieve="gpg2 --keyserver-options auto-key-retrieve --receive-keys"

# Reloading .zshrc
alias srczsh="source $ZDOTDIR/.zshrc"

# Use dotfiles git repo
alias dotfiles="/usr/bin/git --git-dir="$HOME/.dotfiles" --work-tree=$HOME"

# Pastebin command
alias 0x0st="curl -F 'file=@-' 0x0.st"

# Plugins
fpath=($ZDOTDIR/.zfunc /usr/share/zsh/site-functions/ $fpath)
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
source /usr/share/zsh/plugins/pnpm-shell-completion/pnpm-shell-completion.zsh

eval "$(zoxide init zsh)"
eval "$(fnm env --use-on-cd)"
eval "$(starship init zsh)"

# Keys:
bindkey "$terminfo[kdch1]" delete-char
bindkey "$terminfo[khome]" beginning-of-line
bindkey "$terminfo[kend]" end-of-line
bindkey "$terminfo[kcuu1]" history-substring-search-up
bindkey "$terminfo[kcud1]" history-substring-search-down
bindkey "^[[H" beginning-of-line
bindkey "^[[F" end-of-line
bindkey "^[[A" history-substring-search-up
bindkey "^[[B" history-substring-search-down

