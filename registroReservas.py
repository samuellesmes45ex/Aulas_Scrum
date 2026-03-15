def reservar_aula():
    print("REGISTRO DE RESERVAS")

    Aula=input("AULA:")

    if not Aula.isdigit():
        print("Error. Ingrese el número de aula.")
        return
   


    while True:
        Fecha=input("FECHA (DD/MM/AAAA):").strip()


        if len(Fecha) != 10:
                
            print("Formato incorrecto. Debe ser DD/MM/AAAA (ej: 15/02/2026)")
            continue
                
        if Fecha[2] != "/" or Fecha[5] != "/":
            print("""Debe usar "/" para separar (DD/MM/AAAA). """)
            continue
            
        partes = Fecha.split("/")
                
        if len(partes) != 3:
            print("Formato incorrecto.")
            continue
                
        dia = partes[0]
        mes = partes[1]
        anio = partes[2]
                
        if not dia.isdigit() or not mes.isdigit() or not anio.isdigit():
            print("Día, mes y año deben ser números.")
            continue  
        break
    

    while True:
        
        while True:
            HoraInicio=input("HORA DE INCIO (13:00):")


            if len(HoraInicio) != 5:
                    
                print("Formato incorrecto. Debe ser HH:MM (ej: 08:00)")
                continue
                    
            if HoraInicio[2] != ":":
                print("""Debe usar (:) para separar (HH:MM).""")
                continue
                
            partes = HoraInicio.split(":")
                    
            if len(partes) != 2:
                print("Formato incorrecto.")
                continue
                    
            Hora_ini = partes[0]
            Minutos = partes[1]
                    
            if not Hora_ini.isdigit() or not Minutos.isdigit():
                    print("Las horas y minutos deben ser dígitos.")  
                    continue 
            break    

        while True:
            HoraFin=input("HORA FINALIZACIÓN:")
            
            if len(HoraFin) != 5:
                    
                print("Formato incorrecto. Debe ser HH:MM (ej: 08:00)")
                continue
                    
            if HoraFin[2] != ":":
                print("""Debe usar (:) para separar (HH:MM).""")
                continue
                
            partes = HoraFin.split(":")
                    
            if len(partes) != 2:
                print("Formato incorrecto.")
                continue
                    
            Hora_fin = partes[0]
            Minutos = partes[1]
                    
            if not Hora_fin.isdigit()  or not Minutos.isdigit():
                    print("Las horas y minutos deben ser dígitos.")   
            break

        if Hora_ini > Hora_fin:
            print ("la fecha hora inicial no puede ser menor que la hora final...")
            continue
        break


    while True:
        Responsable=input("RESPONSABLE:")
        if Responsable.isdigit():
            print("Error. Ingrese nombre del responsable.")
            continue
        break
    

    Descripción=input("DESCRIPCIÓN (opcional):")

reservar_aula()