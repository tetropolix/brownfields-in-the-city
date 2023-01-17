Server start:
    Execute following bash script from backend dir **./start-server.sh**
    
    Options: 
        -h {host} Bind socket to this host.
        -p {port} Bind socket to this port.
        -e {env_file_path} Specify file path relative to src dir for .env file for configuration, if ommited configuration will be searched in actual environment
        -r pass true if server should react to code changes (default is false)

    Example: ./start-server.sh -h 0.0.0.0 -p 8000 -e .env_file -r true