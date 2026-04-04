# Tipos de Consulta — Guía para el Equipo

Ejemplos de preguntas útiles para consultar a los usuarios sintéticos.
Cada sección incluye la plantilla de pregunta y un ejemplo de respuesta esperada.

---

## Reacción a un feature o cambio

**Plantilla:**
```
Soy [nombre de persona], acabo de ver que el producto ahora [descripción del cambio].
¿Cuál es tu reacción inmediata? ¿Lo usarías? ¿Qué te genera dudas?
```

**Ejemplo de respuesta esperada:**

> ## Martín — interesado pero con una duda puntual
>
> Bueno, si puedo ver el historial de mis operaciones sin tener que guardar los mails...
> eso sí me sirve. A veces necesito revisar a qué tasa cambié el mes pasado para saber
> si esta vez está mejor o peor. Lo usaría. La duda que me queda es si el historial
> muestra la tasa que recibí yo, no la tasa de mercado en ese momento — porque son
> cosas distintas y necesito el número concreto de mi operación.

---

## Revisar un flujo o pantalla

**Plantilla:**
```
Como [nombre de persona], estás intentando [tarea concreta].
Te muestro los pasos que tendrías que seguir:
[descripción del flujo o pegar screenshot/texto]

¿Dónde te trabas? ¿Qué no entendés? ¿Llegás al final?
```

**Ejemplo de respuesta esperada:**

> ## Ana — llega al paso 3 pero ahí frena
>
> El primer paso me queda claro, ingreso el monto y veo cuánto va a recibir mi mamá.
> Eso me gusta. En el paso 2, cuando pide "método de entrega", no entiendo bien si
> "pago móvil" es lo mismo que el pago móvil venezolano que usa ella. No dice el banco
> ni nada — yo necesito estar segura de que es el mismo antes de confirmar. Ahí pararía
> y buscaría el chat de soporte.

---

## Evaluar un mensaje o copy

**Plantilla:**
```
Como [nombre de persona], ves este mensaje en el producto:
"[texto del mensaje]"

¿Qué entendés? ¿Te genera acción, confusión, o lo ignorás?
```

**Ejemplo de respuesta esperada:**

> ## Carlos — lo lee, entiende el mensaje, pero necesita más
>
> Entiendo lo que dice. "Tu operación fue recibida" me indica que llegó. Pero lo que
> necesito saber es cuándo acredita, no solo que fue recibida. Para mí "recibida" no
> es lo mismo que "confirmada". Si no dice cuándo voy a tener los dólares disponibles,
> voy a mandar un mensaje al soporte de todas formas.

---

## Priorización de features

**Plantilla:**
```
Tenemos estas opciones para el próximo trimestre:
1. [Feature A]
2. [Feature B]
3. [Feature C]

Como [nombre de persona], ¿cuál te importa más? ¿Cuál cambiaría más tu día a día?
Ordenarlas de mayor a menor impacto para vos.
```

**Ejemplo de respuesta esperada:**

> ## Martín — el orden importa y es claro
>
> 1. Notificaciones de estado en tiempo real — eso me sacaría la ansiedad de la espera.
>    Es lo que más me molesta del proceso ahora mismo.
> 2. Ver la tasa histórica de mis operaciones — útil para comparar, pero no urgente.
> 3. Poder programar operaciones — nunca lo usaría. Yo opero cuando me cae el pago,
>    no cuando quiero. No tengo un schedule predecible.

---

## Panel completo (todas las personas)

**Plantilla:**
```
Quiero la perspectiva de todas las personas disponibles sobre:
[pregunta o situación]

Para cada una: reacción, razón, y si hay evidencia en los datos que la respalde.
Terminar con una tabla comparativa.
```

**Ejemplo de respuesta esperada (fragmento):**

> ## Martín — a favor si no agrega pasos
> Si puedo activar la autenticación de dos factores sin que eso me ralentice cada vez
> que opero, lo activo. Si me va a pedir un código cada vez que confirmo un cambio,
> lo dejo desactivado. La velocidad es lo primero.
>
> ---
>
> ## Carlos — lo activa por seguridad, sin dudarlo
> Para los montos que manejo, cualquier capa extra de seguridad es bienvenida.
> Un código al iniciar sesión no me molesta. Prefiero eso a estar expuesto.
>
> ---
>
> ## Para el equipo
> El 2FA es bienvenido pero la implementación importa: si bloquea el flujo de
> confirmación de operación, Martín (y posiblemente Ana) lo van a desactivar.
> Si solo protege el login, todos lo adoptan. Diferencia clave: dónde está el paso.

---

## Detectar fricción en onboarding

**Plantilla:**
```
Como [nombre de persona], es tu primer día usando el producto.
Describí cómo sería tu experiencia tratando de [tarea de onboarding].
¿En qué momento perdés motivación? ¿Qué te haría abandonar?
```

**Ejemplo de respuesta esperada:**

> ## Martín — abandona en el paso de verificación si es muy largo
>
> Entro, veo que puedo iniciar sin cuenta. Bien. Creo el pedido, todo claro hasta ahora.
> Cuando me pide email + contraseña para guardar la operación, lo hago. Si después de
> eso me pide documento o selfie antes de poder confirmar la operación... ahí me voy.
> No porque desconfíe del producto, sino porque hay tres exchanges que hacen lo mismo
> sin pedirme eso para el primer cambio.

---

## Evaluar una propuesta de valor o pricing

> **Importante:** estas consultas son orientativas, no predictivas.
> No usar para tomar decisiones de precio sin validación real con usuarios.

**Plantilla:**
```
Como [nombre de persona], te cuento que el producto va a cambiar a este modelo:
[descripción del cambio]

¿Cómo reaccionás? ¿Qué preguntas te surgirían antes de aceptar?
```

**Ejemplo de respuesta esperada:**

> ## Ana — su primer instinto es calcular el impacto en su familia
>
> Lo primero que hago es calcular cuánto le llega a mi mamá si hay una comisión fija
> por envío. Si mando USD 50 y la comisión es USD 3, eso son 6 puntos. Eso es mucho.
> Si la comisión es proporcional al monto, quiero ver el número concreto antes de
> decidir. No me importa tanto si es más caro en términos absolutos — me importa
> saber el número exacto que recibe ella.

---

## Preguntas que NO funcionan bien

Evitar estas consultas porque los usuarios sintéticos no tienen datos para responderlas con fundamento:

- "¿Cuánto pagarías por esto?" → requiere test de precios real
- "¿Recomendarías el producto?" → el NPS real es más confiable
- "¿Qué tan probable es que abandones?" → requiere análisis de comportamiento real
- Preguntas sobre segmentos sin datos cargados en el proyecto
- "¿Qué piensa el usuario colombiano?" → no hay persona colombiana activa aún (ver lista de espera en personas.md)
