# Ansible Role Oh My ZSH

![Build status](https://travis-ci.com/ctorgalson/ansible-role-oh-my-zsh.svg?branch=master)

This is a basic Ansible role to enable and configure Oh My Zsh on Ubuntu or
MacOS. It should also work on many other \*nix variants. It performs the
following tasks:

- Install and minimally configure Zsh:
  - make sure it exists,
  - set it as the default shell for the user specified by the role.
- Install Oh My Zsh for each specified user (in `~/.oh-my-zsh` by default).
- Configure (Oh My) Zsh by optionally creating a `.zshrc` file for each
  specified user.
- Alternately, configure Zsh by adding a block of lines to individual
  users' `.zshrc` files.

## Role variables

| Variable name  | Default value | Description |
|----------------|---------------|-------------|
| `install_zsh` | `false` | Defines whether or not the role should attempt to install Zsh. |
| `zsh_user` | `[]` | The user to install/configure (Oh My) Zsh for. See below for its properties. |
| `zsh_user.name` | `-` | The name of the user. |
| `zsh_user.group` | `-` | The group of the user |
| `zsh_user.settings` | `-` | Extra settings (as a mult-line string) such as variable exports or aliases to add to the user's `.zshrc` file. Only used if `oh_my_zsh_zshrc_create` is `true`. |
| `oh_my_zsh_git_repository` | `https://github.com/robbyrussell/oh-my-zsh.git` | The git repo to clone Oh My Zsh from. |
| `oh_my_zsh_install_directory` | `.oh-my-zsh` | The name of the directory to clone Oh My Zsh into. |
| `oh_my_zsh_zshrc_create` | `true` | Whether or not to create `.zshrc`. If `true`, will create `.zshrc` from a template. |
| `oh_my_zsh_zshrc_template` | `templates/zshrc.zsh-template.j2` | The template used to create the user's `.zshrc` file when `oh_my_zsh_zshrc_create` is `true`. |
| `oh_my_zsh_zshrc_backup` | `true` | Whether or not to create backup the existing `.zshrc` files when the role changes it. |
| `oh_my_zsh_zshrc` | (see below) | List of variables used in `templates/zshrc.zsh-template.j2` or your custom template. |
| `oh_my_zsh_zshrc.zsh_theme` | `robbyrussell` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.case_sensitive` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.hyphen_insensitive` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.disable_auto_update` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.update_zsh_days` | `13` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.disable_ls_colors` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.disable_auto_title` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.enable_correction` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.completion_waiting_dots` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.disable_untracked_files_dirty` | `false` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.hist_stamps` | `mm/dd/yyyy` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.zsh_custom` | `$ZSH/custom` | See `templates/zshrc.zsh-template`. |
| `oh_my_zsh_zshrc.plugins` | `[]` | A list of Oh My Zsh plugins to enable. |

## Role task files

### `main.yml`: task coordination

This file includes files that peform specific subsets of tasks.

### `zsh.yml`: Zsh setup

This task installs and sets zsh as the default shell for a user.

#### Variables used

- `zsh_user`

### `oh-my-zsh-install.yml`: Oh My Zsh installation

This task clones the Oh My Zsh repository into the user directory of each
specified user and sets the appropriate permissions on the directory.

#### Variables used

- `zsh_user`
- `oh_my_zsh_install_directory`
- `oh_my_zsh_git_repository`
- `oh_my_zsh_install_path`

### `oh-my-zsh-zshrc.yml`: Oh My Zsh configuration

This task creates the user a `.zshrc` file containing global values for various
Oh My Zsh options based on [the `.zshrc` template in the oh-my-zsh repository](https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/templates/zshrc.zsh-template).
The task can be configured to back up any existing `.zshrc` file.

This task only runs when `oh_my_zsh_zshrc_create` is set to `true`.

#### Variables used

- `zsh_user`
- `oh_my_zsh_zshrc_template`
- `oh_my_zsh_zshrc_backup`

### `zsh-zshrc.yml`: final Zsh configuration

This task adds individual lines to the `.zshrc` file. This is useful for adding
Zsh settings on an already-existing `.zshrc` file without creating it
from scratch.

This task only runs when `oh_my_zsh_zshrc_create` is set to `false`.

#### Variables used

- `zsh_user`
- `oh_my_zsh_zshrc_backup`

## Sample playbook

    ---
    - name: Playbook
      hosts: all
      become: true

      vars:
        install_zsh: true
        users:
          - name: "lorem"
            group: "lorem"
            settings: ""
          - name: "ipsum"
            group: "ipsum"
            settings: |
              export PATH="/usr/local/sbin:$path"
              alias l="ls -AF"
      tasks:
        - name: Run ansible-role-oh-my-zsh.
          include_role:
            name: "ansible-role-oh-my-zsh"
          vars:
            zsh_user: "{{ item }}"
            # Only create `.zshrc` for user 'lorem'; item.settings will be
            # appended to `.zshrc` for the user 'ipsum'.
            oh_my_zsh_zshrc_create: "{{ (item.name == 'lorem') | ternary(true, false) }}"
          with_items: "{{ users }}"
