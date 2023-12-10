import csv
import os 
import http.client
import json

#### Se genera el token ######

### Se crea la conexión http ###
conn = http.client.HTTPConnection("100.127.4.48", 8008)
payload = 'username=crqventanas&password=%23crqventanas%23'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
conn.request("POST", "/api/jwt/login", payload, headers)
res = conn.getresponse()
data = res.read()
token=data.decode("utf-8")

#### Proceso para los cambios que estan en proceso ####

### Dirección para los procesados ###
dir_proc='C:/Users/CONSULTOR/Desktop/linux/InhibirAlarmas/Procesados'
contenido=os.listdir(dir_proc)

cambios=[]
print(cambios)
for file in contenido:
    if os.path.isfile(os.path.join(dir_proc,file)) and file.endswith('.csv'):
        cambios.append(file)
print(cambios)
for i in cambios:
    with open(f'{dir_proc}/{i}', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=',')
        for fila in lector_csv:
            cambio=fila[0]
            sitio=fila[1]
            fecha_ini=fila[2]
            fecha_fin=fila[3]
            
            print(fila[0], type(file[0]))

            payload = ''
            headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
            }
            conn.request("GET", "/api/arsys/v1/entry/Site-EP/?q='536870925'=%22{}%22&fields=values(1)".format(sitio), payload, headers)
            res = conn.getresponse()
            data = res.read()
            json_data=json.loads(data.decode("utf-8"))
            id_sitio=json_data["entries"][0]['values']['Entry ID-EP']
            print(id_sitio)

            ## Agregar la información de los CRQs en el formulario de Site EP ##

            payload = json.dumps({
            "values": {
                "ID CRQ": f"{cambio}",
                "Fecha programada de inicio":f"{fecha_ini}",
                "Fecha programada de fin":f"{fecha_fin}"
            }
            })
            headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
            }
            conn.request("PUT", f"/api/arsys/v1/entry/Site-EP/{id_sitio}", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

#### Proceso para los cambios que estan en finalización ####

### Dirección para los finalizados ###

dir_fin='C:/Users/CONSULTOR/Desktop/linux/InhibirAlarmas/Finalizados'
contenido=os.listdir(dir_fin)

cambios2=[]
print(cambios)
for file in contenido:
    if os.path.isfile(os.path.join(dir_fin,file)) and file.endswith('.csv'):
        cambios2.append(file)
print(cambios2)
for j in cambios2:
    with open(f'{dir_fin}/{j}', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=',')
        for fila in lector_csv:
            cambio=fila[0]
            sitio=fila[1]
            fecha_ini=fila[2]
            fecha_fin=fila[3]
            
            print(fila[0], type(file[0]))

            payload = ''
            headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
            }
            conn.request("GET", "/api/arsys/v1/entry/Site-EP/?q='536870925'=%22{}%22&fields=values(1)".format(sitio), payload, headers)
            res = conn.getresponse()
            data = res.read()
            json_data=json.loads(data.decode("utf-8"))
            id_sitio=json_data["entries"][0]['values']['Entry ID-EP']
            print(id_sitio)

            ## Agregar la información de los CRQs en el formulario de Site EP ##

            payload = json.dumps({
            "values": {
                "ID CRQ": "-",
                "Fecha programada de inicio":"-",
                "Fecha programada de fin":"-"
            }
            })
            headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
            }
            conn.request("PUT", f"/api/arsys/v1/entry/Site-EP/{id_sitio}", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
