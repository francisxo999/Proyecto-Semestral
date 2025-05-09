mascota=[]
cliente=[]
flag = True
print("\n***Vettsafe***\n")
while flag:
    try:
        opcion = int(input("\n1.-Ingresar Datos del animal.\n2.Mostrar las mascotas registradas-.\n3.-Salir de la vettsafe\nIngrese la opcion: "))
    except ValueError:
        print("\nHas ingresado un caracter, debes ingresar un numero.\n")
    else:
        if opcion == 1:
            while True:
                nombre_animal=input("\nIngrese el nombre de la mascota: ")
                mascota.append(nombre_animal)
                especie_animal=input("\nIngrese de que especie es el animal: ")
                mascota.append(especie_animal)
                raza_animal=input("\nIngrese la raza del animal: ")
                mascota.append(raza_animal)
                edad_animal=int(input("\nIngrese la edad del animal: "))
                mascota.append(edad_animal)
                print("Los datos del animal ha quedado registrado correctamente\n")
                break
        elif opcion == 2:
            print(mascota)
        elif opcion == 3:
            print("Saliendo de la vettsafe, espere un momento.")
            break
        else:
            print("\nDebes escoger una de las opciones mostradas en pantalla.\n")
