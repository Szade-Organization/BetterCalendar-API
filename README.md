Aplikacja po wykonaniu pull requesta:  
1. Uruchamia workflow test.yml, który:  
2. Konfiguruje środowisko  
3. Uruchamia testy  
4. Jeżeli napotka na problem w trakcie wykonywania testów to:  
5. Loguje się do azure devboard  
6. Zgłasza buga wraz z informacjami o problemie  
  
Dodatkowo przygotowałem workflow create-azure-container.yml, który:  
1. Po wykonaniu pusha do gałęzi master:
2. Uruchamia workflow testów  
3. Jeżeli testy zostaną wykonane pomyślnie:  
4. Buduje nowy obraz dockera  
5. Publikuje obraz docker do ghcr.io  
6. Webapp w azure pobiera nowy obraz dockera i uruchamia go.
