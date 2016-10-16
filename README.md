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
- Run final configuration of `.zsh` by adding individual lines to individual
  users' `.zshrc` files.

## Variables by task

### `zsh.yml`: Zsh setup

This task sets zsh as the default shell for a list of users. Note that it does
*not* install zsh, and will fail if zsh does not exist on the system. It uses
the (configurable) variables in the following table.

| Variable name  | Default value | Description |
|----------------|---------------|-------------|
| `zsh_path`     | `/bin/zsh`    | The expected path for `zsh` |
| `zsh_users`    | `[]`          | An array of users expected to use (oh my) zsh. Each item should include `user`, `group`, and `settings` (see `defaults/main.yml` for details). |

### `oh-my-zsh-install.yml`: Oh My Zsh installation

This task clones the Oh My Zsh repository into the user directory of each
specified user and sets the appropriate permissions on the directory. The
(configurable) variables in the following table are used in the actual Oh My
Zsh installation (see also the `zsh.yml` variables, above).

| Variable name | Default value | Description |
|---------------|---------------|-------------|
| `oh_my_zsh_git_repository`   | `git@github.com:robbyrussell/oh-my-zsh.git ` | Complete `git clone` url to Oh My Zsh repository. |
| `oh_my_zsh_install_directory` | `.oh-my-zsh` | Name of the directory to clone Oh My Zsh repository to. Assumes it will be installed in individual users' home directories. |
| `zsh_users_home_path_prefix` | `/Users`                                     | path (from `/`) to the parent directory containing users on the system (should be identical to `$HOME`, and should not include a trailing slash). Default value works for MacOS. |

### `oh-my-zsh-zshrc.yml`: Oh My Zsh configuration

This task creates a `.zshrc` file per-user containing global values for various
Oh My Zsh options based on [the `.zshrc` template in the oh-my-zsh repository](https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/templates/zshrc.zsh-template). Note that it
will back up any existing `.zshrc` file. The variables in the following table
are used in this task.

| Variable name | Default value | Description |
|---------------|---------------|-------------|
| `oh_my_zsh_zshrc_create` | `true` | Whether or not perform this task at all. |
| `oh_my_zsh_zshrc_template` | `templates/zshrc.zsh-template.j2` | The location of the template to use. |

### `zsh-zshrc.yml`: Final Zsh configuration

This task adds individual lines to the `.zshrc` file. This is useful for adding
individual Zsh settings on a per-user basis. It uses no variables not defined
elsewhere.
