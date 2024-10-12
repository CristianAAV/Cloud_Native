# Grupo 5 - Entrega 1
Para la entrega 1, se desarrollaron los servicios solicitados segun el siguiente detalle:

- [Gestión de usuarios](#gestión-de-usuarios)
- [Gestión de trayectos](#gestión-de-trayectos)
- [Gestión de publicaciones](#gestión-de-publicaciones)
- [Gestión de ofertas](#gestión-de-ofertas)
- [Scores](#scores)
- [RF003](#rf003)
- [RF004](#rf004)
- [RF005](#rf005)
- [RF006](#rf006)
- [Email Service](#email-management)
- [RF007](#rf007)

# Gestión de usuarios

Este servicio corresponde a la creación de usuarios y su validación por medio de tokens.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Otras Caracteristicas](#otras-caracteristicas)
6. [Autor](#autor)


## Estructura
Segun lo recomendado se construyeron las siguientes carpetas
- **src:** LA cual contiene el codigo y logica del servicio
  - **src/models:** Esta carpeta contiene la capa de persistencia, donde se definen el modelo de la entidad usuario.
  - **src/commands:** Contiene el codigo para cada caso de uso, por ejemplo "crear usuario", "generar token, etc"
  - **src/blueprints:** Esta carpeta alberga la capa de aplicación de nuestro microservicio, encargada de definir y desarrollar cada servicio API que exponemos.
  - **src/errors:** Para devolver errores HTTP en los blueprints
- **tests:** En la cual estan implementados los tests unitarios
- **Dockerfile:** Define cómo se debe construir la imagen de la aplicación.
- **docker-compose.yml:** Encargado de montar la base de datos y la aplicación.
- **.env:** Almacena variables de entorno como configuraciones y credenciales de manera segura

## Ejecución
En la raiz del servicio utilizar como plantilla el archivo "env.template" y crear uno denominado "env.development", con la siguiente informacion:
* DB_USER=admin
* DB_PASSWORD=adminpassword
* DB_HOST=cnt_db_users
* DB_PORT=5432
* DB_NAME=user_db

Seguidamente, ejecutar el siguiente comando:
```bash
docker-compose up --build
```
## Uso
Despues de iniciarse los contenedores, puede ejecutar los endpoints de acuerdo a la siguiente detale:
El servicio de gestión de usuarios permite crear usuarios y validar la identidad de un usuario por medio de tokens.

  - **Creación de usuarios**
    - **Método:** POST  
    - **Ruta:** /users
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:**
```json
{
  "username": "nombre de usuario",
  "password": "contraseña del usuario",
  "email": "correo electrónico del usuario",
  "dni": "identificación",
  "fullName": "nombre completo del usuario",
  "phoneNumber": "número de teléfono"
}
```
  - **Actualización de usuarios**
    - **Método:** PATCH
    - **Ruta:** /users/{id}
    - **Parámetros:** id: identificador del usuario
    - **Encabezados:** N/A
    - **Cuerpo:**
```json
{
  "status": nuevo estado del usuario,
  "dni": identificación,
  "fullName": nombre completo del usuario,
  "phoneNumber": número de teléfono
}
```
  - **Generación de token**
    - **Método:** POST
    - **Ruta:** /users/auth
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:**
```json
{
  "username": nombre de usuario,
  "password": contraseña del usuario
}
```
  - **Consultar información del usuario**
    - **Método:** GET
    - **Ruta:** /users/name
    - **Parámetros:** N/A
    - **Encabezados:** Authorization: Bearer token
    - **Cuerpo:** N/A
  - **Consulta de salud del servicio**
    - **Método:** GET
    - **Ruta:** /users/ping
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:** N/A
  - **Restablecer base de datos**
    - **Método:** POST
    - **Ruta:** /users/reset
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:** N/A

## Pruebas
- Ejecutar la BD de pruebas
```
docker run --name postgres-pruebas-local \
  -e POSTGRES_USER=user_management_user \
  -e POSTGRES_PASSWORD=user_management_pass \
  -e POSTGRES_DB=user_management_db \
  -p 5432:5432 \
  -d postgres:13
```
- Dirigirse a la carpeta  "user_management"
- Activar el entorno virtual, puede utilizar los siguientes comandos en linux:
  - python3 -m venv venv
  - source venv/bin/activate
- Instalar las dependencias:
  - pip install -r requirements.txt
- Ejecutar las pruebas:
  - pytest --cov-fail-under=70 --cov=src

## Otras Caracteristicas
- El servicio fue desarrollado en  Python con Flask
- Para la persistencia en base de datos, se utilizó Postgresql

## Autor
Emerson Chaparro Ampa
- correo: e.chaparroa@uniandes.edu.co

# Gestión de trayectos

El servicio de gestión de trayectos permite crear trayectos (rutas) para ser usados por las publicaciones. Este fue desarrollado en Golang con el framework Gin y el ORM gorm.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Otras caracteristicas](#Otras\_Características)
6. [Autor](#autor)

## Estructura

Describe la estructura de archivos de la carpeta, puedes usar una estructura de arbol para ello:
```
route_management
├── mocks # Carpeta con archivo con mocks de servicios para ser usados en las pruebas
│
├── model # Carpeta con modelos de gorm con sus respectivas funciones para transformar los datos a la base de datos
│
├── routes # Carpeta con archivos que tienen las funciones que las rutas que usa la aplicación
│   └── delete_routes.go # archivo con las rutas que sean de tipo DELETE
│   └── get_routes.go # archivo con las rutas que sean de tipo GET
│   └── post_routes.go # archivo con las rutas que sean de tipo POST
|
├── utils # Carpeta con utilidades compartidas por diferentes 
│   └── auth.go # archivo con la autenticación y sus respectivas interfaces e utilidades
│   └── utils.go # archivo con la utilidades usadas por varias rutas y partes de la aplicación
│
├── Dockerfile # Dockerfile base con la configuración para desplegar el servicio de manera segura
│
├── go.mod # archivo con las librerías usadas por la aplicación y la versión de golang
│
├── go.sum # archivo con las urls de las librerías y sus dependecias usadas por la aplicación
│
├── init.sql # sql usado para inicializar la base de datos
|
├── main_test.go # archivo con las pruebas de la aplicación a nivel de main.go
|
├── main.go # archivo con el entrypoint de la aplicación. genera la base de datos, el servidor y las rutas. 
|
├── test.sh # archivo para correr las pruebas en local o en los pipelines. 
|
└── README.md # usted está aquí
```
## Ejecución

Proporciona instrucciones claras y concisas sobre cómo instalar y ejecutar este proyecto. Si es necesario, incluye ejemplos de código o comandos.

```bash
go mod download
go build -o main .
./main
...
```

## Uso

Para consumir la API se necesita lo siguiente: 

### Variables de entorno

```bash
DB_USER=routes_management_user
DB_PASSWORD=routes_management_pass
DB_NAME=routes_management_db
DB_HOST=routes_db
DB_PORT=5432
CONFIG_PORT=3000
USERS_PATH="http://users:3000"
```

### Servicios

Tener una instancia del sevicio de users corriendo para poder obtener y validar los tokens. Si un token no es válido no se podrá usar el servicio de manera efectiva. 

El servicio de gestión de trayectos permite crear trayectos (rutas) para ser usados por las publicaciones.

#### 1. Creación de trayecto

Crea un trayecto con los datos brindados, solo un usuario autorizado puede realizar esta operación.

<table>
<tr>
<td> Método </td>
<td> POST </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td>

```Authorization: Bearer token```
</td>
</tr>
<tr>
<td> Cuerpo </td>
<td>

```json
{
  "flightId": código del vuelo,
  "sourceAirportCode": código del aeropuerto de origen,
  "sourceCountry": nombre del país de origen,
  "destinyAirportCode": código del aeropuerto de destino,
  "destinyCountry": nombre del país de destino,
  "bagCost": costo de envío de maleta,
  "plannedStartDate": fecha y hora de inicio del trayecto,
  "plannedEndDate": fecha y hora de finalización del trayecto
}
```
</td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 401 </td>
<td>El token no es válido o está vencido.</td>
<td> N/A </td>
</tr>
<tr>
<td> 403 </td>
<td>No hay token en la solicitud</td>
<td> N/A </td>
</tr>
<tr>
<td> 400 </td>
<td>En el caso que alguno de los campos no esté presente en la solicitud.</td>
<td> N/A </td>
</tr>
<tr>
<td> 412 </td>
<td>En el caso que el flightId ya existe.</td>
<td> N/A </td>
</tr>
<tr>
<td> 412 </td>
<td> En el caso que la fecha de inicio y fin del trayecto no sean válidas; fechas en el pasado o no consecutivas.</td>
<td> 

```json
{
    "msg": "Las fechas del trayecto no son válidas"
}
```
</td>
</tr>
<tr>
<td> 201 </td>
<td>En el caso que el trayecto se haya creado con éxito.</td>
<td>

```json
{
  "id": id del trayecto,
  "createdAt": fecha y hora de creación del trayecto en formato ISO
}
```
</td>
</tr>
</tbody>
</table>

#### 2. Ver y filtrar trayectos

Retorna todos los trayectos o aquellos que corresponden a los parámetros de búsqueda. Solo un usuario autorizado puede realizar esta operación.

<table>
<tr>
<td> Método </td>
<td> GET </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes?flight={flightId}</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> flightId: id del vuelo, este campo es opcional </td>
</tr>
<tr>
<td> Encabezados </td>
<td>

```Authorization: Bearer token```
</td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 401 </td>
<td>El token no es válido o está vencido.</td>
<td> N/A </td>
</tr>
<tr>
<td> 403 </td>
<td>No hay token en la solicitud</td>
<td> N/A </td>
</tr>
<tr>
<td> 400 </td>
<td>En el caso que alguno de los campos de búsqueda no tenga el formato esperado.</td>
<td> N/A </td>
</tr>
<tr>
<td> 200 </td>
<td>Listado de trayectos.</td>
<td>

```json
[
  {
    "id": id del trayecto
    "flightId": código del vuelo,
    "sourceAirportCode": código del aeropuerto de origen,
    "sourceCountry": nombre del país de origen,
    "destinyAirportCode": código del aeropuerto de destino,
    "destinyCountry": nombre del país de destino,
    "bagCost": costo de envío de maleta,
    "plannedStartDate": fecha y hora de inicio del trayecto,
    "plannedEndDate": fecha y hora de finalización del trayecto,
    "createdAt": fecha y hora de creación del trayecto en formato ISO
  }
]
```
</td>
</tr>
</tbody>
</table>


#### 3. Consultar un trayecto

Retorna un trayecto, solo un usuario autorizado puede realizar esta operación.

<table>
<tr>
<td> Método </td>
<td> GET </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes/{id}</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> id: identificador del trayecto </td>
</tr>
<tr>
<td> Encabezados </td>
<td>

```Authorization: Bearer token```
</td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 401 </td>
<td>El token no es válido o está vencido.</td>
<td> N/A </td>
</tr>
<tr>
<td> 403 </td>
<td>No hay token en la solicitud</td>
<td> N/A </td>
</tr>
<tr>
<td> 400 </td>
<td>El id no es un valor string con formato uuid.</td>
<td> N/A </td>
</tr>
</tr>
<tr>
<td> 404 </td>
<td>El trayecto con ese id no existe.</td>
<td> N/A </td>
</tr>
<tr>
<td> 200 </td>
<td>Trayecto que corresponde al identificador.</td>
<td>

```json
  {
    "id": id del trayecto
    "flightId": código del vuelo,
    "sourceAirportCode": código del aeropuerto de origen,
    "sourceCountry": nombre del país de origen,
    "destinyAirportCode": código del aeropuerto de destino,
    "destinyCountry": nombre del país de destino,
    "bagCost": costo de envío de maleta,
    "plannedStartDate": fecha y hora de inicio del trayecto,
    "plannedEndDate": fecha y hora de finalización del trayecto,
    "createdAt": fecha y hora de creación del trayecto en formato ISO
  }
```
</td>
</tr>
</tbody>
</table>


#### 4. Eliminar trayecto

Elimina el trayecto, solo un usuario autorizado puede realizar esta operación.

<table>
<tr>
<td> Método </td>
<td> DELETE </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes/{id}</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> id: identificador del trayecto </td>
</tr>
<tr>
<td> Encabezados </td>
<td>

```Authorization: Bearer token```
</td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 401 </td>
<td>El token no es válido o está vencido.</td>
<td> N/A </td>
</tr>
<tr>
<td> 403 </td>
<td>No hay token en la solicitud</td>
<td> N/A </td>
</tr>
<tr>
<td> 400 </td>
<td>El id no es un valor string con formato uuid.</td>
<td> N/A </td>
</tr>
</tr>
<tr>
<td> 404 </td>
<td>El trayecto con ese id no existe.</td>
<td> N/A </td>
</tr>
<tr>
<td> 200 </td>
<td>El trayecto fue eliminado.</td>
<td>

```json
  {
    "msg": "el trayecto fue eliminado"
  }
```
</td>
</tr>
</tbody>
</table>


#### 5. Consulta de salud del servicio

Usado para verificar el estado del servicio.

<table>
<tr>
<td> Método </td>
<td> GET </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes/ping</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td>N/A</td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 200 </td>
<td> Solo para confirmar que el servicio está arriba.</td>
<td>

```pong```
</td>
</tr>
</tbody>
</table>

#### 6. Restablecer base de datos

Usado para limpiar la base de datos del servicio.

<table>
<tr>
<td> Método </td>
<td> POST </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/routes/reset</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td>N/A</td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</table>

##### Respuestas

<table>
<tr>
<th> Código </th>
<th> Descripción </th>
<th> Cuerpo </th>
</tr>
<tbody>
<tr>
<td> 200 </td>
<td> Todos los datos fueron eliminados.</td>
<td>

```
{"msg": "Todos los datos fueron eliminados"}
```
</td>
</tr>
</tbody>
</table>

## Pruebas

Las pruebas se ejecutan corriendo el archivo `test.sh`.

Las pruebas se hicieron usando la librería [sqlMock para golang](https://pkg.go.dev/github.com/DATA-DOG/go-sqlmock@v1.5.2), para mockear los llamados a base datos, y se utilizó el patrón de inyección de dependencias para simular los llamados al autenticador (que deberían ser al servicio de users). El sentido de esto es para limitar la cantidad de pruebas que se hacen a código que no es el del servicio, sino las conexiones con terceros. La inyección de dependencias se hizo creando mocks en [este archivo](/route_management/mocks/mock_authenticator.go).

## Otras Características

Requerimientos

- Golang 1.23.0
- Docker
- Postgresql

## Autor

Andres Felipe Losada Luna


# Gestión de publicaciones

Este servicio corresponde a la creación de publicaciones de rutas, su consulta y su eliminación. 

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Otras Caracteristicas](#Otras\_Caracteristicas)
5. [Autor](#autor)


## Estructura
Segun lo recomendado se construyeron las siguientes carpetas
- **src:** LA cual contiene el codigo y logica del servicio
  - **src/models:** Esta carpeta contiene la capa de persistencia, donde se definen el modelo de la entidad usuario.
  - **src/commands:** Contiene el codigo para cada caso de uso, por ejemplo "crear usuario", "generar token, etc"
  - **src/blueprints:** Esta carpeta alberga la capa de aplicación de nuestro microservicio, encargada de definir y desarrollar cada servicio API que exponemos.
  - **src/errors:** Para devolver errores HTTP en los blueprints
- **tests:** En la cual estan implementados los tests unitarios
- **Dockerfile:** Define cómo se debe construir la imagen de la aplicación.
- **docker-compose.yml:** Encargado de montar la base de datos y la aplicación.
- **.env:** Almacena variables de entorno como configuraciones y credenciales de manera segura

## Ejecución
En la raiz del servicio utilizar como plantilla el archivo "env.template" y crear uno denominado "env.development", con la siguiente informacion:
VERSION=1.0
* DB_USER=postgres
* DB_PASSWORD=postgres
* DB_HOST=post_db
* DB_PORT=5432
* DB_NAME=post_db
* USER_PATH="http://users:3000"

Seguidamente, ejecutar el siguiente comando:
```bash
docker-compose up --build
```
## Uso
Despues de iniciarse los contenedores, puede ejecutar los endpoints de acuerdo a la siguiente detale:

# Servicio de Gestión de Publicaciones

El servicio de gestión de publicaciones permite crear, buscar, eliminar y consultar publicaciones.

## 1. Creación de Publicación

Crea una publicación asociada al usuario al que pertenece el token.

- **Método:** `POST`
- **Ruta:** `/posts`
- **Parámetros:** N/A
- **Encabezados:**
  - `Authorization: Bearer token`
- **Cuerpo:**
  ```json
  {
    "routeId": "id del trayecto",
    "expireAt": "fecha y hora máxima en que se recibirán ofertas en formato ISO"
  }

## Pruebas
- Ejecutar la BD de pruebas
```
docker run --name postgres-pruebas-local \
  -e POSTGRES_USER=user_management_user \
  -e POSTGRES_PASSWORD=user_management_pass \
  -e POSTGRES_DB=user_management_db \
  -p 5432:5432 \
  -d postgres:13
```
- Dirigirse a la carpeta  "user_management"
- Activar el entorno virtual, puede utilizar los siguientes comandos en linux:
  - python3 -m venv venv
  - source venv/bin/activate
- Instalar las dependencias:
  - pip install -r requirements.txt
- Ejecutar las pruebas:
  - pytest --cov-fail-under=70 --cov=src

### Respuestas

| Código | Descripción                                                                | Cuerpo                                                                                                                                |
|--------|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 401    | El token no es válido o está vencido.                                      | N/A                                                                                                                                   |
| 403    | No hay token en la solicitud.                                              | N/A                                                                                                                                   |
| 400    | Alguno de los campos no está presente en la solicitud o no tiene el formato esperado. | N/A                                                                                                                                   |
| 412    | La fecha de expiración no es en el futuro o no es válida.                  | `{ "msg": "La fecha expiración no es válida" }`                                                                                       |
| 201    | La publicación se ha creado con éxito.                                     | `{ "id": "id de la publicación", "userId": "id del usuario que creó la publicación", "createdAt": "fecha y hora de creación en formato ISO" }` |

### 2. Ver y filtrar publicaciones

Retorna el listado de publicaciones que coinciden con los parámetros brindados. Solo un usuario autorizado puede realizar esta operación.

- **Método:** GET
- **Ruta:** `/posts?expire={true|false}&route={routeId}&owner={id|me}`
- **Parámetros:** Todos los parámetros son opcionales, y su funcionamiento es de tipo AND.
  - `expire`: filtra por publicaciones expiradas o no expiradas.
  - `route`: id del trayecto que se desea usar para el envío.
  - `owner`: dueño de la publicación. Se reciben ids o el valor `me` que indica al usuario del token.

  En el caso de que ninguno esté presente se devolverá la lista de datos sin filtrar. Es decir, todas las publicaciones.

- **Encabezados:** 
  - `Authorization: Bearer token`

- **Cuerpo:** N/A

#### Respuestas

| Código | Descripción                                                                  | Cuerpo                                                                                                                              |
|--------|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| 401    | El token no es válido o está vencido.                                        | N/A                                                                                                                                 |
| 403    | No hay token en la solicitud.                                                | N/A                                                                                                                                 |
| 400    | Alguno de los campos de búsqueda no tiene el formato esperado.               | N/A                                                                                                                                 |
| 200    | Listado de publicaciones que corresponden a la búsqueda.                     | `[ { "id": "id de la publicación", "routeId": "id del trayecto", "userId": "id del usuario owner de la publicación", "expireAt": "fecha y hora máxima en que se recibirán ofertas en formato ISO", "createdAt": "fecha y hora de creación de la publicación en formato ISO" } ]` |

### 3. Consultar una publicación

Retorna una publicación, solo un usuario autorizado puede realizar esta operación.

- **Método:** GET
- **Ruta:** `/posts/{id}`
- **Parámetros:** 
  - `id`: identificador de la publicación

- **Encabezados:** 
  - `Authorization: Bearer token`

- **Cuerpo:** N/A

#### Respuestas

| Código | Descripción                                             | Cuerpo                                                                                                                            |
|--------|---------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 401    | El token no es válido o está vencido.                   | N/A                                                                                                                               |
| 403    | No hay token en la solicitud.                           | N/A                                                                                                                               |
| 400    | El id no es un valor string con formato UUID.           | N/A                                                                                                                               |
| 404    | La publicación con ese id no existe.                    | N/A                                                                                                                               |
| 200    | Publicación que corresponde al identificador.           | `{ "id": "id de la publicación", "routeId": "id del trayecto", "userId": "id del usuario owner de la publicación", "expireAt": "fecha y hora máxima en que se recibirán ofertas en formato ISO", "createdAt": "fecha y hora de creación de la publicación en formato ISO" }` |


### 4. Eliminar publicación

Elimina una publicación, solo un usuario autorizado puede realizar esta operación.

- **Método:** DELETE
- **Ruta:** `/posts/{id}`
- **Parámetros:** 
  - `id`: identificador de la publicación.

- **Encabezados:** 
  - `Authorization: Bearer token`

- **Cuerpo:** N/A

#### Respuestas

| Código | Descripción                                             | Cuerpo                              |
|--------|---------------------------------------------------------|-------------------------------------|
| 401    | El token no es válido o está vencido.                   | N/A                                 |
| 403    | No hay token en la solicitud.                           | N/A                                 |
| 400    | El id no es un valor string con formato UUID.           | N/A                                 |
| 404    | La publicación con ese id no existe.                    | N/A                                 |
| 200    | La publicación fue eliminada.                           | `{ "msg": "la publicación fue eliminada" }` |


### 5. Consulta de salud del servicio

Usado para verificar el estado del servicio.

- **Método:** GET
- **Ruta:** `/posts/ping`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:** N/A

#### Respuestas

| Código | Descripción                                    | Cuerpo |
|--------|------------------------------------------------|--------|
| 200    | Solo para confirmar que el servicio está arriba. | `pong` |

### 6. Restablecer base de datos

Usado para limpiar la base de datos del servicio.

- **Método:** POST
- **Ruta:** `/posts/reset`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:** N/A

#### Respuestas

| Código | Descripción                        | Cuerpo                                   |
|--------|------------------------------------|------------------------------------------|
| 200    | Todos los datos fueron eliminados. | `{ "msg": "Todos los datos fueron eliminados" }` |


## Otras Caracteristicas
- El servicio fue desarrollado en  Python con Flask
- Para la persistencia en base de datos, se utilizó Postgresql

## Autor
Cristian Arnulfo Arias Vargas
- correo: ca.ariasv1@uniandes.edu.co

# Gestión de ofertas
Este servicio corresponde a la creación de ofertas, su consulta y su eliminación. 
## Índice
1. Estructura
2. Ejecucion
3. Uso
4. Pruebas Postman 
5. Autor

## 1. Estructura

La estructura del proyecto es la siguiente:

- **auth/**: Realiza la validacion de verificacion del usuario.
- **globals/**: Son variables que pueden ser usadas muchas veces en el codigo.
- **db/**: Se realiza la conexión a la base de datos.
- **migration/**: Contiene consultas que no se pueden ejecutar directamente con GORM.
- **models/**: Aquí se encuentran las entidades o tablas. Estos modelos hacen uso de GORM.
- **routes/**: Contiene los manejadores de las rutas definidas en `main.go`. Aquí se almacena la lógica de negocio que se ejecuta en las rutas.
- **main.go**: Es el archivo principal de la aplicación.
- **go.mod**: Archivo que almacena los paquetes necesarios para que la aplicación funcione correctamente.
- **Dockerfile**: Define cómo se debe construir la imagen de la aplicación.

## 2. Ejecución

Este servicio es muy fácil de ejecutar. Simplemente ejecuta el siguiente comando en el root:

```bash
docker-compose up --build
```

## 3. Uso

1. **Realizar Solicitudes al Servidor**

   Una vez que los servicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

    - **Base URL**: `http://localhost:3003`

   Aquí están los endpoints disponibles:

    - **Crear una oferta**
        - **Método**: POST
        - **Ruta**: `/offers`
        - **Descripción**: Crea una nueva oferta.
        - **Cuerpo de la solicitud**:
          ```json
          {
            "postId": "string",
            "userId": "string",
            "description": "string",
            "size": "LARGE|MEDIUM|SMALL",
            "fragile": true|false,
            "offer": 0.00
          }
          ```

    - **Obtener todas las ofertas**
        - **Método**: GET
        - **Ruta**: `/offers`
        - **Descripción**: Obtiene una lista de todas las ofertas.

    - **Obtener una oferta específica**
        - **Método**: GET
        - **Ruta**: `/offers/{id}`
        - **Descripción**: Obtiene los detalles de una oferta específica.

    - **Eliminar una oferta**
        - **Método**: DELETE
        - **Ruta**: `/offers/{id}`
        - **Descripción**: Elimina una oferta específica.

    - **Verificar la salud del servicio**
        - **Método**: GET
        - **Ruta**: `/offers/ping`
        - **Descripción**: Verifica que el servicio está en funcionamiento.

    - **Restablecer la base de datos**
        - **Método**: POST
        - **Ruta**: `/offers/reset`
        - **Descripción**: Restablece la base de datos a su estado inicial.

## 4. Pruebas Postman

## Pasos previos antes de ejecutar las pruebas

1. **Ejecutar Docker Compose:**
   Asegúrate de haber ejecutado el archivo `docker-compose` en el root para iniciar todos los servicios necesarios.

2. **Creación de usuario y autenticación:**
   - Visita la documentación del servicio de usuarios para el endpoint `http://localhost:3000/users` el cual permite crear un usuario.
   - Para obtener un token de autenticación, dirígete a la documentación del servicio de usuarios y revisa el siguiente endpoint `localhost:3000/users/auth`. Este token será necesario para realizar las solicitudes a otros endpoints.

## Endpoints de ofertas

### 1. Creación de una oferta

```bash
curl --location 'localhost:3003/offers' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN' \
--data '{
    "postId": "550e8400-e29b-41d4-a716-446655440000",
    "description": "Test Offer",
    "size": "LARGE",
    "fragile": true,
    "offer": 10.00
}'
```

### 2. Consultar todas las ofertas

```bash
curl --location 'localhost:3003/offers' \
--header 'Authorization: Bearer TOKEN'
```

### 3. Consultar una oferta por ID

```bash
curl --location 'localhost:3003/offers/ID_OFERTA' \
--header 'Authorization: Bearer TOKEN'
```

### 4. Eliminar una oferta

```bash
curl --location --request DELETE 'localhost:3003/offers/ID_OFERTA' \
--header 'Authorization: Bearer TOKEN'
```

### 5. Consultar el estado del servicio (Health Check)

```bash
curl --location 'localhost:3003/offers/ping'
```

### 6. Eliminar todos los datos de la base de datos

```bash
curl --location --request POST 'localhost:3003/offers/reset'
```

---

Asegúrate de reemplazar `TOKEN` con el token real obtenido durante el proceso de autenticación y `ID_OFERTA` con el ID de la oferta que deseas consultar o eliminar.

## 5. Autor

Juan Camilo Vallejos Guerrero  
Correo electrónico: j.vallejosg@uniandes.edu.co

# Scores

Este servicio corresponde a la gestion de la nueva entidad scores.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Otras Caracteristicas](#otras-caracteristicas)
6. [Autor](#autor)


## Estructura
Segun lo recomendado se construyeron las siguientes carpetas
- **src:** LA cual contiene el codigo y logica del servicio
  - **src/models:** Esta carpeta contiene la capa de persistencia, donde se definen el modelo de la entidad usuario.
  - **src/commands:** Contiene el codigo para cada caso de uso, por ejemplo "crear score", "obtener score"
  - **src/blueprints:** Esta carpeta alberga la capa de aplicación de nuestro microservicio, encargada de definir y desarrollar cada servicio API que exponemos.
  - **src/errors:** Para devolver errores HTTP en los blueprints
- **tests:** En la cual estan implementados los tests unitarios
- **Dockerfile:** Define cómo se debe construir la imagen de la aplicación.
- **docker-compose.yml:** Encargado de montar la base de datos y la aplicación.
- **.env:** Almacena variables de entorno como configuraciones y credenciales de manera segura

## Ejecución
En la raiz del servicio utilizar como plantilla el archivo "env.template" y crear uno denominado "env.development", con la siguiente informacion:
* DB_USER=admin
* DB_PASSWORD=adminpassword
* DB_HOST=localhost
* DB_PORT=5432
* DB_NAME=scores_management_db
* USERS_PATH=http://localhost:3000
* 
Seguidamente, ejecutar el siguiente comando:
```bash
docker-compose up --build
```
## Uso
Despues de iniciarse los contenedores, puede ejecutar los endpoints de acuerdo a la siguiente detale:
El servicio de gestión de usuarios permite crear usuarios y validar la identidad de un usuario por medio de tokens.

  - **Creación de scores**
    - **Método:** POST  
    - **Ruta:** /scores
    - **Parámetros:** N/A
    - **Encabezados:** Authorization: Bearer token
    - **Cuerpo:**
```json
{
  "offerId": "identificador de la oferta",
  "utility": "utilidad"
}
```
  - **Consulta de Score**
    - **Método:** GET
    - **Ruta:** /scores/offer/<id>
    - **Parámetros:** id: identificador de score
    - **Encabezados:** Authorization: Bearer token
    - **Cuerpo:** N/A
  - **Consulta de salud del servicio**
    - **Método:** GET
    - **Ruta:** /scores/ping
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:** N/A
  - **Restablecer base de datos**
    - **Método:** POST
    - **Ruta:** /scores/reset
    - **Parámetros:** N/A
    - **Encabezados:** N/A
    - **Cuerpo:** N/A

## Pruebas
- Ejecutar la BD de pruebas
```
docker run --name postgres-pruebas-local \
  -e POSTGRES_USER=scores_management_user \
  -e POSTGRES_PASSWORD=scores_management_pass \
  -e POSTGRES_DB=scores_management_db \
  -p 5432:5432 \
  -d postgres:13
```
- Dirigirse a la carpeta  "scores"
- Activar el entorno virtual, puede utilizar los siguientes comandos en linux:
  - pipenv shell  
- Instalar las dependencias:
  - pipenv install
- Ejecutar las pruebas:
  - pytest --cov-fail-under=70 --cov=src

## Otras Caracteristicas
- El servicio fue desarrollado en  Python con Flask
- Para la persistencia en base de datos, se utilizó Postgresql

## Autor
Emerson Chaparro Ampa
- correo: e.chaparroa@uniandes.edu.co

# RF003

Este servicio corresponde a la creación de publicaciones.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas en postman](#Otras\_Caracteristicas)
5. [Autor](#autor)

## 1. Estructura

La estructura del proyecto es la siguiente:

- **app.py**: este archivo contiene el código fuente del microservicio.
- **test.py**: este archivo contiene los tests de `app.py`.
- **Dockerfile**: este archivo contiene la imagen que se va a crear para ser usada en Kubernetes.


## 2. Ejecucion

El siguiente microservicio puede ser desplegado en Kubernetes a través del siguiente comando:

```sh
cd deployment
kubectl apply -f k8s-new-services-deployment.yaml
```
Con esto bastaría para desplegar el microservicio en caso de que sea necesario desplegarlo en Kubernetes.

## 3. Uso

Una vez que los microservicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

**URL del microservicio:**  
`http://<IP_DEL_CLUSTER>/rf003/posts`

#### Descripción

| Método   | Ruta           | Parámetros | Encabezados                   |
|----------|----------------|------------|-------------------------------|
| `POST`   | `/rf003/posts` | N/A        | `Authorization: Bearer <token>` |

#### Cuerpo de la solicitud

El cuerpo de la solicitud debe contener los siguientes campos en formato JSON:

```json
{
    "flightId": "identificador del vuelo",
    "expireAt": "fecha y hora máxima para recibir ofertas en formato ISO",
    "plannedStartDate": "fecha y hora planeada de salida en formato ISO",
    "plannedEndDate": "fecha y hora planeada de llegada en formato ISO",
    "origin": {
        "airportCode": "código del aeropuerto de origen",
        "country": "nombre del país de origen"
    },
    "destiny": {
        "airportCode": "código del aeropuerto de destino",
        "country": "nombre del país de destino"
    },
    "bagCost": "costo de envío de maleta en dólares"
}
```

### Campos:

- **flightId**: Identificador único del vuelo.
- **expireAt**: Fecha y hora máxima en la que se recibirán ofertas sobre la publicación (en formato ISO).
- **plannedStartDate**: Fecha y hora planeada de salida del vuelo (en formato ISO).
- **plannedEndDate**: Fecha y hora planeada de llegada del vuelo (en formato ISO).
- **origin**: Información sobre el aeropuerto de origen, con los siguientes subcampos:
  - **airportCode**: Código del aeropuerto de origen.
  - **country**: Nombre del país de origen.
- **destiny**: Información sobre el aeropuerto de destino, con los siguientes subcampos:
  - **airportCode**: Código del aeropuerto de destino.
  - **country**: Nombre del país de destino.
- **bagCost**: Costo de envío de la maleta en dólares.

Recuerda reemplazar `<IP_DEL_CLUSTER>` y `<token>` con la dirección IP del clúster y el token de autenticación obtenido anteriormente.

### 4. Pruebas postman

#### 4.1 Creación del Usuario

Primero, es necesario crear un usuario para poder interactuar con el sistema. Para ello, envía una solicitud `POST` al endpoint de creación de usuarios:

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/users`

**Ejemplo de solicitud `POST` para crear un usuario:**

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "juan1",
  "password": "tuContraseñaSegura",
  "email": "j.vallejos1g@uniandes.edu.co",
  "dni": "123456789",
  "fullName": "Juan Vallejos",
  "phoneNumber": "+573001234567"
}'
```

#### 4.2 Obtención del Token
Una vez creado el usuario, debes autenticarte para obtener un token que te permitirá hacer solicitudes al microservicio rf003.

URL para obtener el token de autenticación:
http://<IP_DEL_CLUSTER>/users/auth

Ejemplo de solicitud POST para autenticar y obtener el token:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users/auth' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "juan1",
  "password": "tuContraseñaSegura"
}'
```

El token obtenido deberá ser incluido en las siguientes solicitudes a los endpoints.

#### 4.3 Solicitudes al Microservicio rf003
Después de obtener el token de autenticación, ya puedes interactuar con el microservicio rf003. Aquí tienes un ejemplo de cómo crear un post utilizando el token.

URL del microservicio rf003:
http://<IP_DEL_CLUSTER>/rf003/posts

Ejemplo de solicitud POST para crear un post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf003/posts' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "flightId": "2",
    "expireAt": "2024-09-15T23:59:59Z",
    "plannedStartDate": "2024-09-22T05:17:59.814Z",
    "plannedEndDate": "2024-09-28T05:17:59.814Z",
    "origin": {
        "airportCode": "BOG",
        "country": "Colombia"
    },
    "destiny": {
        "airportCode": "LGW",
        "country": "Inglaterra"
    },
    "bagCost": 688
}'
```

Recuerda reemplazar <IP_DEL_CLUSTER> por la dirección IP del clúster y <TOKEN> por el token de autenticación que obtuviste en el paso anterior.

## 5. Autor

Juan Camilo Vallejos Guerrero  
Correo electrónico: j.vallejosg@uniandes.edu.co



# RF004

Este servicio corresponde a crear una oferta para una publicación.

## Índice

1. [Disposición](#1-disposición)
2. [Despliegue](#2-despliegue)
3. [Consumo](#3-consumo)
4. [Pruebas en postman](#4-pruebas-postman-2)
5. [Autor](#5-autor-2)

## 1. Disposición

La disposición del servicio es la siguiente:

/rf004
  |-mocks // mocks
  |  |-mock_http.go
  |  |-mock_authenticator.go
  |-go.mod // manejador de versiones
  |-Dockerfile // Dockerfile
  |-utils // utilidades comunes
  |  |-config.go
  |  |-auth.go
  |  |-http.go
  |  |-parse.go
  |-go.sum
  |-.gitignore
  |-model // modelos
  |  |-models.go
  |-service // servicios de llamado externos + tests
  |  |-get_route_test.go
  |  |-create_utility_test.go
  |  |-create_offer_test.go
  |  |-delete_offer_test.go
  |  |-get_route.go
  |  |-delete_offer.go
  |  |-interface.go
  |  |-get_post_test.go
  |  |-create_utility.go
  |  |-create_offer.go
  |  |-get_post.go
  |-test.sh // script para correr las pruebas
  |-routes // rutas de gin + tests
  |  |-post.go
  |  |-post_test.go
  |-coverage // carpeta de coverage de go (creada automáticamente sin versionar)
  |  |-coverage.out
  |-main.go // entrypoint
  |-main_test.go


## 2. Despliegue

El siguiente microservicio puede ser desplegado en Kubernetes a través del siguiente comando:

```sh
cd deployment
kubectl apply -f k8s-new-services-deployment.yaml
```
Con esto bastaría para desplegar el microservicio en caso de que sea necesario desplegarlo en Kubernetes. Es importante tener en cuenta que se tiene que tener la última imágen y esta imágen debe ser accesible desde su cluster.

## 3. Consumo

Una vez que los microservicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

**URL del microservicio:**  
`http://<IP_DEL_CLUSTER>/rf005/posts/<ID>`

#### Descripción

La siguiente es la definición de endpoint que permite crear una Oferta cumpliendo con los criterios de aceptación definidos para el requerimiento RF-004-Posts.

#### Método
POST

#### Ruta
/rf004/posts/{id}/offer

#### Parámetros
Identificador de la publicación a la que se quiere asociar la oferta.

#### Encabezados
`Authorization: Bearer <token>`

#### Cuerpo
```json
{
  "description": "descripción del paquete a llevar",
  "size": "LARGE | MEDIUM | SMALL",
  "fragile": "booleano que indica si es un paquete delicado o no",
  "offer": "valor en dólares de la oferta para llevar el paquete"
}


### 4. Pruebas postman

#### 4.1 Creación del Usuario

Primero, es necesario crear un usuario para poder interactuar con el sistema. Para ello, envía una solicitud `POST` al endpoint de creación de usuarios:

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/users`

**Ejemplo de solicitud `POST` para crear un usuario:**

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "andres",
  "password": "tuContraseñaSegura",
  "email": "af.losada@uniandes.edu.co",
  "dni": "123456789",
  "fullName": "AndresLosada",
  "phoneNumber": "+573001234567"
}'
```

#### 4.2 Obtención del Token
Una vez creado el usuario, debes autenticarte para obtener un token que te permitirá hacer solicitudes al microservicio rf003.

URL para obtener el token de autenticación:
http://<IP_DEL_CLUSTER>/users/auth

Ejemplo de solicitud POST para autenticar y obtener el token:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users/auth' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "andres",
  "password": "tuContraseñaSegura"
}'
```

El token obtenido deberá ser incluido en las siguientes solicitudes a los endpoints.

#### 4.3 Solicitudes al Microservicio rf004
Después de obtener el token de autenticación, ya puedes interactuar con el microservicio rf004. Aquí tienes un ejemplo de cómo crear un post utilizando el token.

URL del microservicio rf004:
http://<IP_DEL_CLUSTER>/rf004/posts

Ejemplo de solicitud POST para crear un post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf004/posts' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
  "description": "descripción del paquete a llevar",
  "size": "LARGE | MEDIUM | SMALL",
  "fragile": "booleano que indica si es un paquete delicado o no",
  "offer": "valor en dólares de la oferta para llevar el paquete"
}'
```

## 5. Autor

Andrés Felipe Losada Luna
Correo electrónico: af.losada@uniandes.edu.co


# RF005

Este servicio corresponde a consultar una publicación y mostrar todas las ofertas asociadas a esa publicación ordenadas de manera descendente según su utilidad. Esto facilita la identificación rápida de la oferta más valiosa, optimizando el proceso de selección de ofertas.



## Índice

1. [Disposición](#1-disposición)
2. [Despliegue](#2-despliegue)
3. [Consumo](#3-consumo)
4. [Pruebas en postman](#4-pruebas-postman-2)
5. [Autor](#5-autor-2)

## 1. Disposición

La disposición del servicio es la siguiente:

- **app.py**: este archivo contiene el código fuente del microservicio.
- **test.py**: este archivo contiene los tests de `app.py`.
- **Dockerfile**: este archivo contiene la imagen que se va a crear para ser usada en Kubernetes.


## 2. Despliegue

El siguiente microservicio puede ser desplegado en Kubernetes a través del siguiente comando:

```sh
cd deployment
kubectl apply -f k8s-new-services-deployment.yaml
```
Con esto bastaría para desplegar el microservicio en caso de que sea necesario desplegarlo en Kubernetes.

## 3. Consumo

Una vez que los microservicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

**URL del microservicio:**  
`http://<IP_DEL_CLUSTER>/rf005/posts/<ID>`

#### Descripción

| Método   | Ruta                | Parámetros | Encabezados                    |
|----------|---------------------|------------|--------------------------------|
| `GET`    | `/rf005/posts/<ID>` | N/A        | `Authorization: Bearer <token>`|

	
Recuerda reemplazar `<IP_DEL_CLUSTER>`, <ID> y `<token>` con la dirección IP del clúster, el id de la publicacion que desea buscar y el token de autenticación obtenido anteriormente.
```
### Respuesta:
Response Status: `200`
{
    "data": {
        "id": identificador de la publicación,
        "expireAt": fecha y hora máxima en que se reciben ofertas en formato IDO,
        "route": {
            "id": identificador del trayecto,
            "flightId": identificador del vuelo,
            "origin": {
                "airportCode": código del aeropuerto de origen,
                "country": nombre del país de origen
            },
            "destiny": {
                "airportCode": código del aeropuerto de destino,
                "country": nombre del país de destino
            },
            "bagCost": costo de envío de maleta
        },
        "plannedStartDate": fecha y hora en que se planea el inicio del viaje en formato ISO,
        "plannedEndDate": fecha y hora en que se planea la finalización del viaje en formato ISO,
        "createdAt": fecha y hora de creación de la publicación en formato ISO,
        "offers": [
            {
                "id": identificador de la oferta,
                "userId": identificador del usuario que hizo la oferta,
                "description": descripción del paquete a llevar,
                "size": LARGE ó MEDIUM ó SMALL,
                "fragile": booleano que indica si es un paquete delicado o no,
                "offer": valor en dólares de la oferta para llevar el paquete,
                "score": utilidad que deja llevar este paquete en la maleta,
                "createdAt": fecha y hora de creación de la publicación en formato ISO
            }
        ]
    }
}
```

### Campos:
- **ID:** Identificador de la publicación
- **ExpireAt:** Fecha y hora máxima en que se reciben ofertas (formato ISO)
- **Route:**
  - **ID:** Identificador del trayecto
  - **FlightId:** Identificador del vuelo
  - **Origin:**
    - **AirportCode:** Código del aeropuerto de origen
    - **Country:** Nombre del país de origen
  - **Destiny:**
    - **AirportCode:** Código del aeropuerto de destino
    - **Country:** Nombre del país de destino
  - **BagCost:** Costo de envío de maleta
- **PlannedStartDate:** Fecha y hora en que se planea el inicio del viaje (formato ISO)
- **PlannedEndDate:** Fecha y hora en que se planea la finalización del viaje (formato ISO)
- **CreatedAt:** Fecha y hora de creación de la publicación (formato ISO)
- **Offers:**
  - **ID:** Identificador de la oferta
  - **UserId:** Identificador del usuario que hizo la oferta
  - **Description:** Descripción del paquete a llevar
  - **Size:** LARGE, MEDIUM o SMALL
  - **Fragile:** Booleano que indica si es un paquete delicado o no
  - **Offer:** Valor en dólares de la oferta para llevar el paquete
  - **Score:** Utilidad que deja llevar este paquete en la maleta
  - **CreatedAt:** Fecha y hora de creación de la oferta (formato ISO)

### 4. Pruebas postman

#### 4.1 Creación del Usuario

Primero, es necesario crear un usuario para poder interactuar con el sistema. Para ello, envía una solicitud `POST` al endpoint de creación de usuarios:

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/users`

**Ejemplo de solicitud `POST` para crear un usuario:**

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "juan1",
  "password": "tuContraseñaSegura",
  "email": "j.vallejos1g@uniandes.edu.co",
  "dni": "123456789",
  "fullName": "Juan Vallejos",
  "phoneNumber": "+573001234567"
}'
```

#### 4.2 Obtención del Token
Una vez creado el usuario, debes autenticarte para obtener un token que te permitirá hacer solicitudes al microservicio rf003.

URL para obtener el token de autenticación:
http://<IP_DEL_CLUSTER>/users/auth

Ejemplo de solicitud POST para autenticar y obtener el token:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users/auth' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "juan1",
  "password": "tuContraseñaSegura"
}'
```

El token obtenido deberá ser incluido en las siguientes solicitudes a los endpoints.

#### 4.3 Solicitudes al Microservicio rf003
Después de obtener el token de autenticación, ya puedes interactuar con el microservicio rf003. Aquí tienes un ejemplo de cómo crear un post utilizando el token.

URL del microservicio rf003:
http://<IP_DEL_CLUSTER>/rf003/posts

Ejemplo de solicitud POST para crear un post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf003/posts' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "flightId": "2",
    "expireAt": "2024-09-15T23:59:59Z",
    "plannedStartDate": "2024-09-22T05:17:59.814Z",
    "plannedEndDate": "2024-09-28T05:17:59.814Z",
    "origin": {
        "airportCode": "BOG",
        "country": "Colombia"
    },
    "destiny": {
        "airportCode": "LGW",
        "country": "Inglaterra"
    },
    "bagCost": 688
}'
```

#### 4.4 Solicitudes al Microservicio rf004
Despues de las solicitudes de creacion del post se realizan las solicitudes al servicio rf004 para crear las ofertas y la utilidad.

URL del microservicio rf004:
http://<IP_DEL_CLUSTER>/rf004/posts/<id>/offers

Ejemplo de solicitud POST para crear una post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf004/posts/<id>/offers' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
					"description": descripción del paquete a llevar,
					"size": LARGE ó MEDIUM ó SMALL,
					"fragile" : booleano que indica si es un paquete delicado o no,
					"offer": valor en dólares de la oferta para llevar el paquete
				}'
```

Recuerda reemplazar `<IP_DEL_CLUSTER>`, <ID> y `<TOKEN>` con la dirección IP del clúster, el id de la publicacion que desea buscar y el token de autenticación obtenido anteriormente.


#### 4.5 Solicitudes al Microservicio rf005
Despues de realizadas los pasos anteriores sigue realizar la solicitud get al microservicio rf005 para obtener la publicacion con las ofertas creadas. 

URL del microservicio rf004:
http://<IP_DEL_CLUSTER>/rf005/posts/<id>

Ejemplo de solicitud GET para crear una post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf005/posts/<id>' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
```

Recuerda reemplazar `<IP_DEL_CLUSTER>`, <ID> y `<TOKEN>` con la dirección IP del clúster, el id de la publicacion que desea buscar y el token de autenticación obtenido anteriormente.

## 5. Autor

Cristian Arnulfo Arias Vargas  
Correo electrónico: ca.ariasv1@uniandes.edu.co


# EMAIL MANAGEMENT

Este servicio corresponde al servicio de notificaciones de usuario. 

## Índice

1. [Estructura](#1-estructura)
2. [Despliegue](#2-despliegue)
3. [Pruebas en Postman](#3-pruebas-en-postman)
4. [Autor](#4-autor)

## 1. Estructura

La estructura del servicio incluye los siguientes componentes:

- **controllers/emailController.js**: Contiene la logica de validacion de campos en el body del request y solicita al servicio la funcion encargada de enviar los emails.
- **routes/emailRoutes.js**: Contiene las rutas del servicio.
- **services/emailService.js**: Contiene la lógica para el envío de correos electrónicos utilizando nodemailer y las variables de entorno necesarias para la configuración del servidor SMTP.
- **app.js**: Archivo principal que configura los endpoints de la API y gestiona las solicitudes para enviar notificaciones.

## 2. Despliegue

### Ejecutar el Proyecto Localmente

Para ejecutar el proyecto localmente, asegúrate de tener Node.js y npm instalados. Luego, ejecuta el siguiente comando en la terminal:

MAIL_MAILER='smtp' MAIL_HOST='smtp.your_host.com' MAIL_PORT='587' MAIL_USERNAME='tu_usuario' MAIL_PASSWORD='tu_contraseña' MAIL_ENCRYPTION='tls' MAIL_FROM_ADDRESS='tu_correo' npm start


### Despliegue en Google Cloud Platform (GCP) - Cloud Run

Para desplegar el servicio en Cloud Run, sigue estos pasos:

1. **Construir la imagen de Docker**:
   Asegúrate de tener un Dockerfile en tu proyecto. Luego, ejecuta el siguiente comando:

   ```bash 
   gcloud builds submit --tag gcr.io/uandes-native-433403/email-service
   ```

2. **Desplegar en Cloud Run**:
  Una vez que la imagen esté construida, despliega el servicio usando el siguiente comando:
  ```bash 
  gcloud run deploy email-service \
  --image gcr.io/uandes-native-433403/email-service \
  --platform managed \
  --region us-central1 \ 
  --allow-unauthenticated \
  --set-env-vars MAIL_MAILER='smtp',MAIL_HOST='smtp.tu_hosting.com',MAIL_PORT='587',MAIL_USERNAME='tu_usuario',MAIL_PASSWORD='tu_contraseña',MAIL_ENCRYPTION='tls',MAIL_FROM_ADDRESS='tu_correo'
  ```

## 3. Pruebas en Postman

Los endpoints disponibles para enviar notificaciones son:

### 1. Notificación de Tarjeta de Crédito

**Endpoint**: `POST https://email-service-441252389525.us-central1.run.app/api/emails/notify-credit-card`

**Cuerpo JSON**:

```json
{ 
  "email": "jcamilovallejos@gmail.com", 
  "cardStatus": "ACEPTADA", 
  "cardLastDigits": "1234", 
  "token": "TOKEN123", 
  "RUV": "RUV123456"
}

```

**Campos Requeridos:**
- `email`: Correo electrónico del usuario.
- `cardStatus`: Estado de la tarjeta, debe ser `ACEPTADA` o `RECHAZADA`.
- `cardLastDigits`: Últimos 4 dígitos de la tarjeta de crédito.
- `token`: Token generado (solo si `cardStatus` es `ACEPTADA`).
- `RUV`: Número de identificación del usuario.

**Respuestas:**
- `200 OK`: Correo electrónico enviado con éxito.
- `404 Not Found`: Faltan datos requeridos para enviar el correo electrónico.
- `400 Bad Request`: El estado de la tarjeta debe ser `ACEPTADA` o `RECHAZADA`.

### 2. Notificación de Verificación de Usuario

**Endpoint**: `POST https://email-service-441252389525.us-central1.run.app/api/emails/notify-user-verification`

**Cuerpo JSON**:

```json
{ 
  "email": "jcamilovallejos@gmail.com", "userStatus": "VERIFICADO", 
  "RUV": "RUV123456" 
}
```

**Campos Requeridos:**
- `email`: Correo electrónico del usuario.
- `userStatus`: Estado del usuario, debe ser `VERIFICADO` o `NO_VERIFICADO`.
- `RUV`: Número de identificación del usuario.

**Respuestas:**
- `200 OK`: Correo electrónico enviado con éxito.
- `404 Not Found`: Faltan datos requeridos para enviar el correo electrónico.
- `400 Bad Request`: El estado del usuario debe ser `VERIFICADO` o `NO_VERIFICADO`.

## 4. Autor

Juan Camilo Vallejos Guerreor



# RF006

Este servicio corresponde a crear una oferta para una publicación.

## Índice

1. [Disposición](#1-disposición)
2. [Despliegue](#2-despliegue)
3. [Consumo](#3-consumo)
4. [Pruebas en postman](#4-pruebas-postman-2)
5. [Autor](#5-autor-2)

## 1. Disposición

La disposición del servicio es la siguiente:
```
rf006
│   .gitignore
│   Dockerfile
│   fileTree.txt
│   go.mod
│   go.sum
│   main.go
│   test.sh
│
├───mocks
│       mock_authenticator.go
│       mock_http.go
│
├───model
│       credit_card.go
│       models.go
│
├───routes
│       get.go
│       post.go
│       reset.go
│
├───services
│       poller.go
│
└───utils
        auth.go
        config.go
        http.go
        parse.go
```


## 2. Despliegue

El siguiente microservicio puede ser desplegado en Kubernetes a través del siguiente comando:

```sh
cd deployment
kubectl apply -f k8s-componentes-entrega-3.yaml
kubectl apply -f k8s-true-native-deployment.yaml
kubectl apply -f k8s-ingress-true-native.yaml
```
Con esto bastaría para desplegar el microservicio en caso de que sea necesario desplegarlo en Kubernetes. Es importante tener en cuenta que se tiene que tener la última imágen y esta imágen debe ser accesible desde su cluster.

## 3. Consumo

Una vez que los microservicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

**URL del microservicio:**  
`http://<IP_DEL_CLUSTER>/credit-cards`

#### Descripción

La siguiente es la definición de endpoint que permite crear una Tarjeta de Credito

#### Método
POST

#### Ruta
/rf006/credit-cards

#### Parámetros
Identificador de la publicación a la que se quiere asociar la oferta.

#### Encabezados
`Authorization: Bearer <token>`

#### Cuerpo
```json
{
    "cardNumber": "numero de tarjeta",
    "cvv": "cvv tarjeta",
    "expirationDate": "expiracion de tarjeta en formato YY/MM",
    "cardHolderName": "Nombre del dueño de la"
} 
```

### 4. Pruebas postman

#### 4.1 Creación del Usuario

Primero, es necesario crear un usuario para poder interactuar con el sistema. Para ello, envía una solicitud `POST` al endpoint de creación de usuarios:

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/users`

**Ejemplo de solicitud `POST` para crear un usuario:**

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "andres",
  "password": "tuContraseñaSegura",
  "email": "af.losada@uniandes.edu.co",
  "dni": "123456789",
  "fullName": "AndresLosada",
  "phoneNumber": "+573001234567"
}'
```

#### 4.2 Obtención del Token
Una vez creado el usuario, debes autenticarte para obtener un token que te permitirá hacer solicitudes al microservicio rf003.

URL para obtener el token de autenticación:
http://<IP_DEL_CLUSTER>/users/auth

Ejemplo de solicitud POST para autenticar y obtener el token:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users/auth' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "andres",
  "password": "tuContraseñaSegura"
}'
```

El token obtenido deberá ser incluido en las siguientes solicitudes a los endpoints.

#### 4.3 Solicitudes al Microservicio rf006
Después de obtener el token de autenticación, ya puedes interactuar con el microservicio rf006. Aquí tienes un ejemplo de cómo crear un post utilizando el token.

URL del microservicio rf006:
http://<IP_DEL_CLUSTER>/rf006/credit-cards

Ejemplo de solicitud POST para crear un post:

```bash
curl --location 'http://<IP_DEL_CLUSTER>/rf006/credit-cards' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "cardNumber": "{{CARD_NUMBER}}",
    "cvv": "{{CARD_CVV}}",
    "expirationDate": "{{CARD_EXPIRATIONDATE}}",
    "cardHolderName": "{{CARD_HOLDERNAME}}"
}'
```

## 5. Autor

Andrés Felipe Losada Luna
Correo electrónico: af.losada@uniandes.edu.co




# RF007

Este servicio corresponde a la verificación de identidad de un usuario cuando es creado.


## Índice

1. [Disposición](#1-disposición-3)
2. [Despliegue](#2-despliegue-4)
3. [Consumo](#3-consumo-3)
4. [Pruebas en postman](#4-pruebas-postman-4)
5. [Autores](#5-autores)

## 1. Disposición

La disposición del servicio es la siguiente:
```
user_management/
│   Dockerfile
│   Pipfile
│   Pipfile.lock
│   README.md
│   docker-compose.yml
│   requirements.txt
│
├───src
│   │   __init__.py
│   │   main.py
│   │   session.py
│   ├───blueprints
│   │       users.py
│   ├───commands
│   │       __init__.py
│   │       base_command.py
│   │       create_user.py
│   │       generate_token.py
│   │       get_user.py
│   │       reset.py
│   │       update_score.py
│   │       update_user.py
│   │       user_verification.py
│   ├───errors
│   │       __init__.py
│   │       errors.py
│   └───models
│           __init__.py
│           model.py
│           user.py
│
└───tests
    │   __init__.py
    │   conftest.py
    ├───blueprints
    │       test_users.py
    ├───commands
    │       test_create_user.py
    │       test_generate_token.py
    │       test_get_user.py
    │       test_reset.py
    │       test_update_user.py
    └───utils
            constants.py
```


## 2. Despliegue

para el siguiente microservicio, es necesario generar el despliegue de la imagen del TrueNative y el microservicio de gestion de usuarios, estos pueden ser desplegados en Kubernetes a través del siguiente comando:

```sh
cd deployment
kubectl apply -f k8s-componentes-entrega-3.yaml
kubectl apply -f k8s-true-native-deployment.yaml
kubectl apply -f k8s-ingress-true-native.yaml
```
Con esto bastaría para desplegar el microservicio en caso de que sea necesario desplegarlo en Kubernetes. Es importante tener en cuenta que se tiene que tener la última imágen y esta imágen debe ser accesible desde su cluster.

## 3. Consumo

Una vez que los microservicios estén en ejecución, puedes hacer solicitudes al servidor en la siguiente dirección:

Primero podemos validar el estado del despliegue del servidor TrueNative de la siguiente forma. }

**URL del TrueNative:**  
`http://<IP_DEL_CLUSTER>/native/ping`

este debe devolver como respuesta pong.

Una vez validado el servicio del TrueNative, procedemos a realizar la creacion de un nuevo usuario. 
**URL del microservicio:**  
```
curl --location 'http://{{IP_DEL_CLUSTER}}/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "{{USER_USERNAME}}",
    "password": "{{USER_PASSWORD}}",
    "email": "{{USER_EMAIL}}",
    "dni": "{{USER_DNI}}",
    "fullName": "{{USER_FULLNAME}}",
    "phoneNumber": "{{USER_PHONENUMBER}}"
}'
```

#### Descripción

La siguiente es la definición del endpoint realiza la creacion de usuario, a su vez realiza la solicitud para la verificación de identidad de usuarios a travez del servidor del TrueNative.

#### Método
POST

#### Ruta
/users

#### Parámetros
Datos del usuario que requiere verificación de identidad, como identificación y otros datos personales.

#### Encabezados
`Authorization: Bearer <token>`

#### Cuerpo
```json
{
    "username": "nombre de cuenta del usuario",
    "password": "contraseña del usuario",
    "email": "email del usuario",
    "dni": "Numero de identidad",
    "fullName": "nombre completo del usuario",
    "phoneNumber": "numero telefonico del usuario"
}
```

### 4. Pruebas postman

#### 4.1 Creación del Usuario

Primero, es necesario crear un usuario con el estado POR_VERIFICAR. Para ello, envía una solicitud POST al endpoint de creación de usuarios:

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/users`

**Ejemplo de solicitud `POST` para crear un usuario:**

```bash
curl --location 'http://<IP_DEL_CLUSTER>/users' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "Cristian",
  "password": "tuContraseñaSegura",
  "email": "ca.ariasv1@uniandes.edu.co",
  "dni": "123456789",
  "fullName": "CristianArias",
  "phoneNumber": "+573152988336"
}'
```

Una vez realizada la solicitud `POST` de creacion del usuario podemos validar el estado en el cual se encuentra la verificacion del usuario

**URL para la creación del usuario:**  
`http://<IP_DEL_CLUSTER>/native/verify/log`

```bash
curl -X GET http://<IP_DEL_CLUSTER>/native/verify/log
```
Este devuelve o muestra un log de eventos de creacion y validacion de usuarios con la siguiente estructura.

```json
[
  {
    "RUV": "{{RUV}}",  // Identificador único de la verificación proporcionado por el proveedor externo.
    "createdAt": "{{CREATED_AT}}",  // Fecha y hora en que se creó la solicitud de verificación.
    "processedAt": "{{PROCESSED_AT}}",  // Fecha y hora en que se procesó la verificación por el sistema.
    "score": "{{SCORE}}",  // Puntaje asignado por el proveedor de verificación (1-100) en función de los datos del usuario.
    "status": "{{STATUS}}",  // Estado actual del proceso de verificación (ej. "VERIFICADO", "NO_VERIFICADO").
    "task_status": "{{TASK_STATUS}}",  // Estado de la tarea de verificación (ej. "ACCEPTED" para aceptada).
    "transactionIdentifier": "{{TRANSACTION_ID}}",  // Identificador único de la transacción o proceso de verificación.
    "user": {
      "dni": "{{USER_DNI}}",  // Documento nacional de identidad del usuario.
      "email": "{{USER_EMAIL}}",  // Correo electrónico del usuario.
      "fullName": "{{USER_FULLNAME}}",  // Nombre completo del usuario.
      "phone": "{{USER_PHONE}}",  // Número de teléfono del usuario.
    },
    "userIdentifier": "{{USER_IDENTIFIER}}",  // Identificador único del usuario en el sistema.
    "userWebhook": "{{USER_WEBHOOK}}"  // Webhook o URL de retorno para notificar al sistema sobre el resultado de la verificación.
  }
]
```
Ejemplos para validacion: 

 - Primera respuesta: 
 
```json
[
  {
    "RUV": "MGZhYThmMjktZTdiYS00OWFiLThlMjUtYzdkNzY1MzE1Y2ViojBmMWFjODY0LTUwNTctNGM1MC1kZDg",
    "createdAt": "Wed, 25 Sep 2024 20:52:42 GMT",
    "processedAt": "Wed, 25 Sep 2024 20:53:25 GMT",
    "score": null,
    "status": null,
    "task_status": "ACCEPTED",
    "transactionIdentifier": "0faa8f29-e7ba-49ab-8e25-c7d765315ceb",
    "user": {
      "dni": "695",
      "email": "raymundo.howe19@gmail.com",
      "fullName": "anita wiegand",
      "phone": "3133057675"
    },
    "userIdentifier": "0f1ac864-5057-4c50-a34f-968600f0ac8e",
    "userWebhook": "http://<IP_DEL_CLUSTER>/users/hook"
  }
]
```

 - Respuesta en proceso: 
 
```json
[
  {
    "RUV": "MGZhYThmMjktZTdiYS00OWFiLThlMjUtYzdkNzY1MzE1Y2ViojBmMWFjODY0LTUwNTctNGM1MC1kZDg",
    "createdAt": "Wed, 25 Sep 2024 20:52:42 GMT",
    "processedAt": "Wed, 25 Sep 2024 20:53:25 GMT",
    "score": 61, // puntajes superiores a 60 dan un status como verificado. 
    "status": "POR_VERIFICAR",
    "task_status": "IN_PROCESS",
    "transactionIdentifier": "0faa8f29-e7ba-49ab-8e25-c7d765315ceb",
    "user": {
      "dni": "695",
      "email": "raymundo.howe19@gmail.com",
      "fullName": "anita wiegand",
      "phone": "3133057675"
    },
    "userIdentifier": "0f1ac864-5057-4c50-a34f-968600f0ac8e",
    "userWebhook": "http://<IP_DEL_CLUSTER>/users/hook"
  }
]
```


 - Respuesta Negativa: 
 
```json
[
  {
    "RUV": "MGZhYThmMjktZTdiYS00OWFiLThlMjUtYzdkNzY1MzE1Y2ViojBmMWFjODY0LTUwNTctNGM1MC1kZDg",
    "createdAt": "Wed, 25 Sep 2024 20:52:42 GMT",
    "processedAt": "Wed, 25 Sep 2024 20:53:25 GMT",
    "score": 30, // puntajes superiores a 60 dan un status como verificado. 
    "status": "NO_VERIFICADO",
    "task_status": "PROCESSED",
    "transactionIdentifier": "0faa8f29-e7ba-49ab-8e25-c7d765315ceb",
    "user": {
      "dni": "695",
      "email": "raymundo.howe19@gmail.com",
      "fullName": "anita wiegand",
      "phone": "3133057675"
    },
    "userIdentifier": "0f1ac864-5057-4c50-a34f-968600f0ac8e",
    "userWebhook": "http://<IP_DEL_CLUSTER>/users/hook"
  }
]
```

 - Respuesta Positiva: 
 
```json
[
  {
    "RUV": "MGZhYThmMjktZTdiYS00OWFiLThlMjUtYzdkNzY1MzE1Y2ViojBmMWFjODY0LTUwNTctNGM1MC1kZDg",
    "createdAt": "Wed, 25 Sep 2024 20:52:42 GMT",
    "processedAt": "Wed, 25 Sep 2024 20:53:25 GMT",
    "score": 61, // puntajes superiores a 60 dan un status como verificado. 
    "status": "VERIFICADO",
    "task_status": "PROCESSED",
    "transactionIdentifier": "0faa8f29-e7ba-49ab-8e25-c7d765315ceb",
    "user": {
      "dni": "695",
      "email": "raymundo.howe19@gmail.com",
      "fullName": "anita wiegand",
      "phone": "3133057675"
    },
    "userIdentifier": "0f1ac864-5057-4c50-a34f-968600f0ac8e",
    "userWebhook": "http://<IP_DEL_CLUSTER>/users/hook"
  }
]
```
Validamos la notificacion que debe llegar al correo

## 5. Autores

Emerson Chaparro Ampa
Correo electrónico: e.chaparroa@uniandes.edu.co

Cristian Arnulfo Arias Vargas
Correo electrónico: ca.ariasv1@uniandes.edu.co
