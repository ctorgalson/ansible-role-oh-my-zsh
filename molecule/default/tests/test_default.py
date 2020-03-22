import os

import testinfra.utils.ansible_runner

import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package", [
    "zsh",
])
def test_packages(host, package):
    p = host.package(package)

    assert p.is_installed


@pytest.mark.parametrize("name", [
    "lorem",
    "ipsum",
])
def test_user_shell(host, name):
    u = host.user(name)

    assert 'zsh' in u.shell


@pytest.mark.parametrize("name", [
    "lorem",
    "ipsum",
])
def test_oh_my_zsh_install(host, name):
    d = host.file("/home/{0}/.oh-my-zsh".format(name))

    assert d.exists and d.is_directory


@pytest.mark.parametrize("name", [
    "lorem",
])
def test_zshrc_create(host, name):
    f = host.file("/home/{0}/.zshrc".format(name))

    assert f.exists and f.is_file
    assert "export ZSH=/home/{0}/.oh-my-zsh".format(name) in f.content_string
    assert "plugins=(autojump git)" in f.content_string


@pytest.mark.parametrize("user,setting", [
    ("lorem", "PLATFORMSH_CLI_TOKEN=10987654321"),
    ("ipsum", "ls -AF"),
])
def test_zshrc_settings(host, user, setting):
    f = host.file("/home/{0}/.zshrc".format(user))

    assert setting in f.content_string
