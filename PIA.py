import sys
import re
import datetime
import sqlite3
from sqlite3 import Error
import openpyxl



try:
    with sqlite3.connect("BaseReserva.db") as conn:
        cursor1 = conn.cursor()
        cursor1.execute("CREATE TABLE IF NOT EXISTS Clientes (clave INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT NOT NULL); ")
        cursor1.execute("CREATE TABLE IF NOT EXISTS Salas (clave INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL ,capacidad INTEGER);")
        cursor1.execute("CREATE TABLE IF NOT EXISTS Reservaciones (folio INTEGER PRIMARY KEY AUTOINCREMENT,Cliente TEXT,Clave_Sala INTEGER,Nombre_Sala TEXT, Nombre_Evento TEXT,Turno TEXT ,Fecha timestamp);")        
        cursor1.execute("CREATE TABLE IF NOT  EXISTS Turnos (Turno TEXT PRIMARY KEY);")
        cursor1.execute("INSERT INTO Turnos (Turno) VALUES ('MATUTINO')")
        cursor1.execute("INSERT INTO Turnos (Turno) VALUES ('VESPERTINO')")
        cursor1.execute("INSERT INTO Turnos (Turno) VALUES ('NOCTURNO')")       
        print("Tabla creada")
except Error as error:
    print (error)
except:
    print(f"Se ha producido el error {sys.exc_info()[0]}")
finally:
    conn.close()

def generar_menu(selecciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        Iniciar_menu(selecciones)
        opcion = Llamar_opciones(selecciones)
        ejecutar_opcion(opcion, selecciones)
        print()

def Iniciar_menu(selecciones):
    print('Selecciona opcion: ')
    for clave in selecciones:
        print(f'{clave} {selecciones[clave][0]}')


def Llamar_opciones(selecciones):
    while (Selecciona := input('Opción: ')) not in selecciones:
        print('Opcion no es valida, vuelve a seleccionar una correcta')
    return Selecciona


def ejecutar_opcion(opcion, selecciones):
    selecciones[opcion][1]()

def Llamar_opciones(selecciones):
    while (Selecciona := input('Opción: ')) not in selecciones:
        print('Opcion no es valida, vuelve a seleccionar una correcta')
    return Selecciona



 
def menu_principal():
    selecciones={"1":("//.-Reservar                         //",Reserva),
              "2":("//.- Modificar Reserva               //",Modificar),
              "3":("//.- Consultar sala en fecha elegida //",Consulta_Fecha),
              "4":("//.- Elimnar una Reserva             //",Eliminar),
              "5":("//.- Reporte De Reserva de una fecha //",Reporte),
              "6":("//.- Reporte en Excel                //",Generar_Excel),
              "7":("//.- Registrar Sala                  //",Sala),
              "8":("//.- Inscripcion de Cliente          //",Cliente),
              "9":("//.- Cerrar programa                 //",Cerrar)
    }
    generar_menu(selecciones, '9')

#Aqui
def Modificar():
    while True:
        print("*" * 23)
        print("| EVENTOS DISPONIBLES |")
        print("*" * 23)
        try:
            with sqlite3.connect("BaseReserva.db") as conn:
                cursor1 = conn.cursor()
                cursor1.execute("SELECT * FROM Reservaciones ORDER BY Nombre_Evento")
                registros = cursor1.fetchall()
                if registros:
                    print("Clave\t     Nombre")
                    for folio,Cliente,CSala,Nombre_Sala,Nombre_Evento,Turno,Fecha in registros:
                        print(f"{folio}\t     {Nombre_Evento}\n")                    
                else:
                    print("No se encontraron registros en la respuesta")
        except Error as error:
            print (error)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            try:
                with sqlite3.connect("BaseReserva.db") as conn:
                    cursor1 = conn.cursor()
                    Seleccion_folio=int(input("Selecciona el folio de la sala (Solo se permiten numeros): ")) 
                    nuevo_nombre=input("Selecciona el nombre nuevo (Si deseas regresar al menu escribe salir): ")
                    if nuevo_nombre=="":
                        print("No se Puede omitir este campo")
                        continue
                    if nuevo_nombre.upper()=="SALIR":
                        break
                    valores={"nuevo_nombre":nuevo_nombre,"seleccion":Seleccion_folio}
                    cursor1.execute("UPDATE Reservaciones SET Nombre_Evento=(:nuevo_nombre) WHERE folio=(:seleccion)",valores)
                    
                    print("//* RESERVACION MODIFICADA CON EXITO *//")
                     
            except ValueError:
                print("No Puedes Seleccionar datos numericos en el folio\nIntentalo de nuevo")
            except Error as error:
                print (error)
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()
        break                       


def Reserva():
    while True:
        
        print("//* CLIENTES REGISTRADOS *//")
       
        try:
            with sqlite3.connect("BaseReserva.db") as conn:
                cursor1 = conn.cursor()                
                cursor1.execute("SELECT * FROM Clientes ORDER BY cliente")
                registros = cursor1.fetchall()
                if registros:
                    print("Clave\t     Cliente")
                    for Clave,Cliente in registros:
                        print(f"{Clave}\t     {Cliente}\n")                    
                else:
                    print("No se encontro registr")
        except Error as error:
            print (error)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            try:
                with sqlite3.connect("BaseReserva.db") as conn:
                    cursor1 = conn.cursor() 
                    
                    print("//* SALAS  REGISTRADAS *//")
                  
                    cursor1.execute("SELECT * FROM Salas ORDER BY nombre")
                    registros = cursor1.fetchall()
                    if registros:
                        print("Clave\t     Sala")
                        for Clave,Cliente,Capacidad in registros:
                            print(f"{Clave}\t     {Cliente}\n")                    
                    else:
                        print("No se encontro registro")
            except Error as error:
                print (error)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()
                try:
                    CCliente=int(input("Ingresa clave de usuario (SOLO NUMEROS):  "))
                    CSala=int(input("Ingresa clave de sala (SOLO NUMEROS):  "))
                except ValueError:
                    print("Seleccionaste datos incorrectos")
                    print("Intenta nuevamente\n")
                else:
                    try:
                        with sqlite3.connect("BaseReserva.db") as conn:
                            cursor1 = conn.cursor()
                            criterios_clientes={"clave_cliente":CCliente}
                            cursor1.execute("SELECT cliente FROM Clientes WHERE clave=(:clave_cliente)",criterios_clientes)
                            registros_clientes = cursor1.fetchall()
                            if registros_clientes:
                                for cliente in registros_clientes:
                                    
                                    print(f"//*BIENVENIDO {cliente}//*")
                                  
                    except Error as error:
                        print (error)
                    except Exception:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    finally:
                        conn.close()
                        try:
                            with sqlite3.connect("BaseReserva.db") as conn:
                                cursor1 = conn.cursor()
                                criterios_salas={"clave_sala":CSala}
                                cursor1.execute("SELECT nombre FROM Salas WHERE clave=(:clave_sala)",criterios_salas)
                                registros_sala = cursor1.fetchall()
                                if registros_sala:
                                    for sala in registros_sala:
                                        
                                        print(f"//*SE ASIGNO LA SALA: {sala}//*")
                                        
                        except Error as error:
                            print (error)
                        except Exception:
                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                        finally:
                            conn.close()
                            try:
                                Sala_Asignada=input("Selecciona el nombre de la sala la cual se te asigno: ")
                                if Sala_Asignada=="":
                                    print("La sala no puede quedar vacia, intenta de nuevo")
                                    continue
                                Nombre=input("Escribe el nombre del evento(Si deseas salir teclea 'Salir' ): " )
                                if Nombre=="":
                                    print("El nombre de la reserva no puede estar en blanco")
                                    continue
                                if Nombre.upper() =="SALIR":
                                    break
                                print("Turnos\n")
                                
                                print("(M).MATUTINO\n" +
                                      "(V).VESPERTINO\n"+
                                      "(N).NOCTURNO\n")
                                
                                Turnos=input("Selecciona el Turno M,V o N: \n")
                                
                                if Turnos=="":
                                    print("Este campo no puede quedar vacio")
                                    continue
                                
                                if(not Turnos in "MVNmvn"):
                                    print("Opcion incorrecta")
                                    continue
                                
                                M="MATUTINO"
                                V="VESPERTINO"
                                N="NOCTURNO"
                                
                                if Turnos.upper()=="M":
                                    Turno=M
                                    
                                elif Turnos.upper()=="V":
                                    Turno=V
                                    
                                elif Turnos.upper()=="N":
                                    Turno=N
                            except:
                                print(f"{sys.exc_info[0]}\nIntentalo de nuevo")
                            else:          
                                fecha_actual=fecha_actual = datetime.date.today()
                                dias_total= 2
                                nueva_fecha= fecha_actual + datetime.timedelta(days=+dias_total)
                                fecha_deseada = input("Dime una fecha (dd/mm/aaaa): \n")
                                if fecha_deseada=="":
                                    print("La Fecha no puede quedar vacia")
                                    continue
                                if(not re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$",fecha_deseada)):
                                    print("La fecha debe estar en formato (DD/MM/AAAA)(Ejemplo: 11/09/2022)\nIntenta nuevamente")
                                    continue
                                fecha = datetime.datetime.strptime(fecha_deseada, "%d/%m/%Y").date()
                                if fecha < nueva_fecha:
                                    print(f"ERROR")
                                    print(f"Se tiene que reservar con minimo dos dias de anticipacion")
                                    continue
                                try:
                                    with sqlite3.connect("BaseReserva.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                                        cursor1 = conn.cursor()
                                        cliente_str=str(cliente)
                                        nombre_sala_str=str(sala)
                                        valores={"cliente":cliente_str,"clave_sala":CSala,"nombre_sala":Sala_Asignada,"nombre_evento":Nombre,"turno":Turno,"fecha":fecha}
                                        cursor1.execute("INSERT INTO Reservaciones (Cliente,Clave_Sala,Nombre_Sala,Nombre_Evento,Turno,Fecha) VALUES(:cliente,:clave_sala,:nombre_sala,:nombre_evento,:turno,:fecha);" , valores)                                 
                                        
                                        print("//* RESERVACION REGISTRADA CON EXITO *//")
        
                                except Error as error:
                                    print (error)
                                except Exception:
                                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                                finally:
                                    conn.close()
        break






def Eliminar():
    while True:
        print("//EVENTOS REGISTRADOS//")
        try:
            with sqlite3.connect("BaseReserva.db") as conn:
                cursor1 = conn.cursor()
                cursor1.execute("SELECT * FROM Reservaciones ORDER BY Nombre_Evento")
                registros = cursor1.fetchall()
                if registros:
                    print("Clave\t     Nombre")
                    for folio,Cliente,Clave_Sala,Nombre_Sala,Nombre_Evento,Turno,Fecha in registros:
                        print(f"{folio}\t     {Nombre_Evento}\n")                    
                else:
                    print("No se encontraron registros")
        except Error as error:
            print (error)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            try:
                with sqlite3.connect("BaseReserva.db") as conn:
                    cursor1 = conn.cursor()
                    Seleccion_folio=int(input("Selecciona el folio de la sala (Solo numeros): "))
                    valores={"seleccion":Seleccion_folio}
                    cursor1.execute("DELETE FROM Reservaciones WHERE folio=(:seleccion)",valores)
                    print("//* RESERVACION  ELIMINADA CON EXITO *//")
     
            except ValueError:
                print("debes Seleccionar datos numericos\nIntentalo de nuevo")
            except Error as error:
                print (error)
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()
        break                       


def Consulta_Fecha():
    while True:
        try:
            Lista_de_clientes=[]
            Listado_posibles=[]
            
            fecha_deseada=input('Selecciona la fecha que desees: ')
            if fecha_deseada =="":
                print("La fecha no se puede omitir\nIntentalo de nuevo")
                continue
            elif(not re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$",fecha_deseada)):
                print("La fecha debe ser DD/MM/AAAA")
                continue
        
            fecha_convertida=datetime.datetime.strptime(fecha_deseada,"%d/%m/%Y").date()

        except:
            print(f"{sys.exc_info[0]}")
        else:
            try:
                with sqlite3.connect("BaseReserva.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    cursor1 = conn.cursor()
                    criterios = {"fecha":fecha_convertida}
                    cursor1.execute("SELECT Clave_Sala,Nombre_Sala,Turno FROM Reservaciones WHERE DATE(Fecha) = :fecha;", criterios)
                    registros = cursor1.fetchall()
                    for clave,nombre_sala,turno in registros:
                        Lista_de_clientes.append((clave,nombre_sala,turno[0][0]))

                    reservaciones_hechas= set(Lista_de_clientes)
                    
                    cursor1.execute("SELECT * FROM Salas ORDER BY clave")
                    registros_salas = cursor1.fetchall()
                    if registros_salas:
                        for clave,nombre,Capacidad in registros_salas:
                            cursor1.execute("SELECT * FROM Turnos")
                            registros_turnos = cursor1.fetchall()
                            if registros_turnos:
                                for turnos in registros_turnos:
                                    Listado_posibles.append((clave,nombre,turnos[0][0]))
                            
                    posible_combinacion=set(Listado_posibles)
                    
                    salas_disponibles=sorted(list(posible_combinacion - reservaciones_hechas))
                    
                    print(f"//*   DISPONIBILIDAD: {fecha_convertida}   //*")
                   
                        
                    print("Sala\t  Nombre\t  Turno\t")
                        
                    for sala in salas_disponibles:
                        print(f"{sala[0]}\t  {sala[1]}\t           {sala[2]}\t")
                    
            except sqlite3.Error as e:
                print (e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                if (conn):
                    conn.close()

        break



def Reporte():
    while True:
        try:
            print("REPORTE DE RESERVACION DE UNA FECHA")
            fecha_deseada=input("Selecciona la fecha de tu evento en el formato (dd/mm/aaaa): ")
            if fecha_deseada =="":
                print("La fecha no se puede omitir\nIntentalo de nuevo")
                continue
            elif(not re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$",fecha_deseada)):
                print("La fecha debe estar en formato DD/MM/AAAA")
                continue
            fecha_a_comparar=datetime.datetime.strptime(fecha_deseada,"%d/%m/%Y").date()
            
            print(f"//* REPORTE DE TU FECHA {fecha_a_comparar} //*")

        except :
            print(f"Se produjo el siguiente error {sys.exc_info[0]}\nIntentalo de nuevo")
        else:
            try:
                with sqlite3.connect("BaseReserva.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    cursor1 = conn.cursor()
                    criterios = {"fecha":fecha_a_comparar}
                    cursor1.execute("SELECT Clave_Sala,Cliente,Nombre_Evento,Turno From Reservaciones WHERE DATE(Fecha) =:fecha;",criterios)
                    registros = cursor1.fetchall()
                    for idsala, cliente,evento,turno in registros:
                        print("{:<10} {:<20} {:<30} {:<40}  ".format("Sala", "Cliente" ,"Evento","Turno"))
                        print("{:<10} {:<20} {:<30} {:<40}  ".format(idsala,cliente,evento,turno))
                        print("|                          FIN  DE REPORTE                           |")
            except sqlite3.Error as e:
                print (e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                if (conn):
                    conn.close()

        break








       

def Sala():
    while True:
        try:
            Nombre_Sala=input("Nombre de la sala (Si desear regresar al menu escribe salir): ")
            if Nombre_Sala=="":
                print("El nombre de la sala no puede omitirse")
                continue
            elif Nombre_Sala.upper()=="SALIR":
                break
            Capacidad=int(input("Selecciona la capacidad: "))
            if Capacidad < 1:
                print("La Capacidad de la sala debe de ser mayor a 0")
                continue            
        except TypeError:
            print(f"Sucedio un error\nIntentalo de nuevo {sys.exc_info[0]}")        
        except ValueError:
            print("No se debe omitir la capacidad")
            print("Solo se admite datos enteros")
        else:
            
            print("//*  SALA REGISTRADA CON EXITO  *//")
          
        try:
            with sqlite3.connect("BaseReserva.db") as conn:
                cursor1 = conn.cursor()
                valores = {"nombre":Nombre_Sala,"cupo":Capacidad}
                cursor1.execute("INSERT INTO Salas (nombre,capacidad) VALUES(:nombre,:cupo);" , valores) 
        except Error as error:
            print (error)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            break  




def Generar_Excel():
    while True:
        try:
            print("REPORTE DE RESERVACION DE UNA FECHA EXCEL")
            fecha_deseada=input("Selecciona la fecha de tu evento  en el formato (dd/mm/aaaa) ,(Si deseas salir escribe salir): ")
            if fecha_deseada =="":
                print("La fecha no se puede omitir\nIntentalo de nuevo")
                continue
            elif(not re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$",fecha_deseada)):
                print("La fecha debe estar en formato DD/MM/AAAA")
                continue
            fecha_a_comparar=datetime.datetime.strptime(fecha_deseada,"%d/%m/%Y").date()
        except:
            print(f"Se produjo el siguiente error {sys.exc_info[0]}\Intentalo de nuevo")
        else:
            try:
                with sqlite3.connect("BaseReserva.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    cursor1 = conn.cursor()
                    criterios = {"fecha":fecha_a_comparar}
                    cursor1.execute("SELECT Clave_Sala,Cliente,Nombre_Evento,Turno From Reservaciones WHERE DATE(Fecha) =:fecha;",criterios)
                    registros = cursor1.fetchall()
                    for idsala, cliente,evento,turno in registros:
                        Lista_Excel=[]
                        Lista_Excel.append((idsala,cliente,evento,turno))
                        wb = openpyxl.Workbook()
                        hoja = wb.active
                        hoja.append(('Sala', 'Cliente', 'Nombre', 'Turno'))
                        
                        for datos in Lista_Excel:
                            hoja.append(datos)
                        
                        wb.save('Reservaciones.xlsx')
                        
                        
                        print("//* EXCEL GENERADO CON EXITO *//")
                        
                                    
            except sqlite3.Error as e:
                print (e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                if (conn):
                    conn.close()
    
        break







def Cliente():
    while True:
        try:
            Nombre_Cliente=input("Selecciona tu nombre completo. (Si desear regresar al menu escribe salir): " )
            if Nombre_Cliente=="":
                print("No se debe de omitir")
                continue
            elif Nombre_Cliente.upper()=="SALIR":
                break
        except:
            print(f"Sucedio un error {sys.exc_info[0]} ")
        else:
         
            print("//*CLIENTE REGISTRADO CON EXITO//*")
                                                    
        try:
            with sqlite3.connect("BaseReserva.db") as conn:
                cursor1 = conn.cursor()
                valores = {"Cliente":Nombre_Cliente}
                cursor1.execute("INSERT INTO Clientes (cliente) VALUES(:Cliente)",valores) 
        except Error as erorr:
            print (erorr)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            break        





def Cerrar():
    print("Cerrando Programa")

                    
                        
if __name__ == '__main__':
    menu_principal()
