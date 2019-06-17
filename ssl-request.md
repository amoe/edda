TO request  SSL certs you can use the config file attached that can also specify aliases.

The technical name for aliases in SSL is Subject Alternative Names.

    openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr -config csr-config.ini
