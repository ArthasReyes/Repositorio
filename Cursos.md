# Seguidor de línea - AR
## Empatizar
### Seguidor de línea
Un seguidor de línea es un robot autónomo capaz de seguir una línea que contrasta con el fondo, por ejemplo amazon utiliza robots que siguen líneas naranjas para llegar de forma eficiente a los racks de sus bodegas y transportar repisas o productos.

![](General/seguidor_linea_industrial.png)

En el ámbito educacional, los seguidores de línea son parte de las competencias clásicas de robótica, y en Chile uno de los torneos más famosos son los organizados por la [liga robótica](https://www.torneorobotica.cl) 

![](General/seguidor_linea_educacion.jpg)

### La Robótica y sus aristas

La __robótica__ es la intersección de 3 áreas de estudio e ingeniería: Mecánica, Electrónica y Computación

La __mecánica__ es la encargada de crear el objeto fisico, se hace cargo del tamaño, la forma, las uniones, el desgaste, el peso, el roce con el suelo, su centro de masa, entre muchas otras cosas.

La __electrónica__ es la encargada de decidir los modelos de los actuadores y sensores, su alimentación y conexiones con el microcontrolador.

La __computación__ es la encargada de diseñar la lógica del robot, el cómo movera los actuadores según los valores obtenidos en los sensores. Decide además el lenguaje de programación, los protocolos de comunicación y el algoritmo a utilizar.

## Definir

El objetivo de este documento es lograr crear un robot seguidor de línea de nivel escolar, pensado para cursos de alto rendimiento escolar, y proponer posibles mejoras a estos.

### Mecánica
A nivel mecánico, debemos mantenernos dentro de los márgenes solicitados por los torneos a cual se planea asistir y proponer luego las características básicas que este debiese tener. 

#### Restricciones por Bases del torneo

A nivel físico, solo se encuentra la restricción física de caber en un cubo de lado 20cm.

#### Características del Móvil esperado
Para nuestra primera iteración responderemos las siguientes preguntas con el mínimo valor posible, para poder iterar desde allí

| Pregunta | Respuesta |
|-|-|
| ¿cuántos pisos? | 1 |
|¿cuántas ruedas?| 2 móviles, 1 libre |
|¿Algún requisito aerodinámico? | No
| ¿Cerrado o abierto? | Abierto |

### Electricidad
A nivel eléctrico, debemos mantenernos dentro de los márgenes solicitados por los torneos a cual se planea asistir y proponer luego las características básicas que este debiese tener. Asímismo en primera instancia nos limitaremos a sensores, actuadores, formas de alimentación y microcontroladores fáciles de encontrar, programar y económicos 

#### Restricciones por Bases del torneo
| Restricción | Comentario |
| - | - |
| Sensores| Ninguno |
| Actuadores| Ninguno |
| Comunicación| No puede comunicarse con dispositivos externos |
| Alimentación | Ninguno |
| Microcontrolador | Ninguno |

#### Características de los componentes a utilizar
| Necesidad | Componentes | Modelo | Detalle |
| - | - |- |- |
| Reconocer la línea del suelo | 2 QTI | [Tcrt5000](https://afel.cl/producto/sensor-infrarrojo-tcrt5000-seguidor-de-lineas/) | Precio de 2300 pesos cada uno |
| Mover las ruedas | 2 Servomotores de giro contínuo | [Servomotor mg996r](https://afel.cl/producto/servomotor-mg996r-engranajes-metalicos/) | Precio de 6000 pesos cada uno
| Fuente de alimentación para autonomía | 2 baterías 18650 + portapila |  Neoeduca | - |
| Circuito (Shield, protobard o pcb) | Shield | Neoeduca | - |
| Lógica del móvil | Raspberry PI | [pico w](https://raspberrypi.cl/raspberry-pi-zero-w/) |  Precio de 12000 pesos

### Programación
A nivel de programación, debemos mantenernos dentro de los márgenes solicitados por los torneos a cual se planea asistir y proponer luego las características básicas que este debiese tener. En primera instancia nos limitaremos a las características al editor Thonny, con micropython y librerías estándar de los componentes. Además se trabajará con elementos de programación básicos: funciones, variables, if, while, for. Dejando para más adelante elementos como estructuras de datos, 

#### Restricciones por Bases del torneo
Los torneos restringen la cantidad de programas que tiene el robot

#### Selección de características del desarrollo
* Se trabajará con [micropython](https://micropython.org/)
* Se utilizará [Thonny](https://thonny.org/) como editor


## Diseñar
### Mecánica
Varios diseños diversos


### Electricidad

La imagen fue obtenida de [wowki](https://wokwi.com), simulador que no tiene qtis, fueron usado sensores de temperatura por coincidir en conexión
![Circuito base](Electrónica/circuito_base.png)



### Programación

El sistema tiene 2 sensores QTI de lectura analógica, por medio de la separación de clusters podemos identificar los rangos para lecturas de color blanco (B) y otras de color negro (N). En adelante nos referiremos a estos rangos por su etiqueta o inicial, y al valor que diferencia a ambas etiquetas como umbral.

Respecto a los sensores, estos nos permiten exactamente 4 posibilidades 

| QTI izquierdo | QTI derecho | Acción |
|-|-|-|
|Blanco|Blanco|Avanzar|
|Blanco|Negro|Girar derecha|
|Negro|Blanco|Girar izquierda|
|Negro|Negro|Saltar la línea|

La lógica será captar datos del QTI y según estos tomar la acción según el caso

![base.png](Programación/base.png)  

## Prototipar

### Mecánica

Se usarán los modelos 3D de Neoeduca

![](Mecánica/ADAPTADOR-SENOSRES.png) 
![](Mecánica/chasis.png)
![](Mecánica/codos.png)
![](Mecánica/llantas.jpg)

Resultado final

![](Mecánica/seguidorDeLinea.png)

### Electricidad

Circuito de verdad

### Programación

Programa en python


## Testear

Probar en pistas propias
* Curvas amplias
* Curvas cerradas
* Ángulos de 90°
* Cruces

## Definir futuras mejoras

Las pistas de competencias tienen desafíos del tipo:
* Código de barra
* Obstáculos
* Colores
* otros

### Mejoras a la mecánica
* Espacio para 1 led por cada qti
* Usar 4 Qtis
* Portasensor
* Mejorar Ruedas aumentando su superficie
* Mejorar centro de masa, abarcando más área del autito
* Cambiar servomotores, por motor dc + encoder

### Mejoras a la electrónica
* Añadir 2 qtis adicionales
* Añadir 4 leds

### Mejoras a la programación
* Añadir el código para 4 Qtis
* Añadir código para tener leds según umbral
* Programa básico para calibrar ruedas
* Programa básico para calibrar qtis
* Tener un calibrador automático con Kmeans

## Anexos

### Design Thinking

### QTI

### Tipos de desafíos

### Pseudocódigo

### Centro de masa

### Protoboard

### Diseño 3D: 3D Builder

### Python
