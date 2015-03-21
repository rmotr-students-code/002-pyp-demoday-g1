from SteamScout import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
    
    # site url: https://002-pyp-demoday-g1-chanchar.c9.io
    
    # server error: Port being used ... yada yada
    # terminal: "lsof -i :8080" looks for a process that using port 8080.
    #           "kill {process number}", it's usually the first one listing using the second number in the listing. 
    # Rerun the serve to see if it works. 