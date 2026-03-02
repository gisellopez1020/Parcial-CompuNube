# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :servidorWeb do |servidorWeb|
    servidorWeb.vm.box = "bento/ubuntu-22.04"
    servidorWeb.vm.network :private_network, ip: "192.168.80.3"
    servidorWeb.vm.provision "file", source: "frontend", destination: "/home/vagrant/frontend"
    servidorWeb.vm.provision "file", source: "microUsers", destination: "/home/vagrant/microUsers"
    servidorWeb.vm.provision "file", source: "microProducts", destination: "/home/vagrant/microProducts"
    servidorWeb.vm.provision "file", source: "microOrders", destination: "/home/vagrant/microOrders"
    servidorWeb.vm.provision "file", source: "init.sql", destination: "/home/vagrant/init.sql"
    servidorWeb.vm.provision "file", source: "docker-compose.yml", destination: "/home/vagrant/docker-compose.yml"
    servidorWeb.vm.provision "file", source: ".env.docker", destination: "/home/vagrant/.env.docker"
    servidorWeb.vm.provision "file", source: "requirements-common.txt", destination: "/home/vagrant/requirements-common.txt"
    servidorWeb.vm.provision "file", source: ".dockerignore", destination: "/home/vagrant/.dockerignore"
    servidorWeb.vm.provision "shell", path: "script.sh"
    servidorWeb.vm.hostname = "servidorWeb"
  end
end
