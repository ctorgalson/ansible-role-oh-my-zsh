# Ansible Role Oh My ZSH

This is a basic Ansible role to enable and configure oh-my-zsh on MacOS. It
should also work on many other \*nix variants. It performs the following tasks:

- Minimally configure ZSH:
  - make sure it exists,
  - make sure it's included in `/etc/shells`,
  - sets it as the default shell for the users specified by the role.
- Install Oh My ZSH for each specified user (in `~/.oh-my-zsh` by default).
- Configure (Oh My) ZSH by optionally creating a `.zshrc` file for each
  specified user.

## Variables

### ZSH configuration

These variables help specify the minimal configuration the role performs for
the ZSH shell.

- `zsh_path`: expected path for `zsh` to exist at.
- `zsh_users`: an array of users to install Oh My ZSH for. Each item should
  include `user` and `group`.
- `zsh_users_home_path_prefix`: path (from `/`) to the parent directory
  containing users on the system (should be identical to `$HOME`, and should
  not include a trailing slash).

## Oh My ZSH installation

These variables are used in the actual Oh My ZSH installation.

- `oh_my_zsh_git_repository`: complete `git clone` url to Oh My ZSH repo.
- `oh_my_zsh_install_directory`: directory name (relative to user home
  directory) for Oh My ZSH installation (should include neither leading nor
  trailing slashes).

## Oh My ZSH configuration

These variables are used in the configuration of Oh My ZSH--chiefly in setting
up a customized `.zshrc` file.

- `oh_my_zsh_zshrc_create`: Whether to create a `.zshrc` file at all.
- `oh_my_zsh_zshrc_tempalte`: Path to template to use for creating `.zshrc`
  file.
- `oh_my_zsh_zshrc`: This variable contains variables for most of the options
  that can be set in the `.zshrc` file. For more information, see:
  - [The Oh My ZSH `.zshrc` template](https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/templates/zshrc.zsh-template)
  - The role's own template: `templates/zshrc.zsh-template.js`
  - The default values for the role's template: `defaults/main.yml`
