# Guía Técnica Exhaustiva: Creación Programática de Campañas Publicitarias en Facebook a Través de la API de Graph

## Introducción
La API de Marketing de Facebook representa una herramienta fundamental para la automatización y escalabilidad de las iniciativas publicitarias en las plataformas de Meta, incluyendo Facebook, Instagram, Messenger y Audience Network. Su naturaleza RESTful, que se integra con la API de Graph, permite una interacción programática con los objetos publicitarios, lo que resulta indispensable para anunciantes a gran escala, agencias y empresas de comercio electrónico que buscan optimizar sus operaciones y maximizar el rendimiento de sus inversiones publicitarias.

La comprensión de la estructura jerárquica de los objetos publicitarios es crucial para una integración exitosa con la API. Esta jerarquía se compone de Campañas, que engloban Conjuntos de Anuncios (Ad Sets); los Conjuntos de Anuncios, a su vez, contienen Anuncios (Ads); y cada Anuncio se vincula a una Creatividad Publicitaria (Ad Creative). Cada uno de estos objetos cumple un propósito específico en el ciclo de vida de la publicidad, desde la definición del objetivo general hasta la presentación final del contenido al usuario.

## I. Conceptos Fundamentales para la Integración con la API

Esta sección establece las bases para cualquier interacción con la API de Marketing de Facebook, abordando los requisitos esenciales y las mejores prácticas para una integración robusta.

### Acceso y Autenticación de la API (Tokens de Acceso, Permisos, Alcances)
Todas las solicitudes a la API requieren un access_token para la autenticación. Existen diferentes tipos de tokens de acceso, como los de Usuario, Página y Usuario del Sistema, cada uno adecuado para distintos casos de uso en publicidad. Para sistemas programáticos, es vital emplear tokens de acceso de larga duración para mantener la continuidad operativa.

Además del token, el token de acceso debe poseer los permisos necesarios, como ads_management y ads_read, para ejecutar acciones específicas. Estos permisos se otorgan durante el proceso de revisión de la aplicación. Es imperativo que todas las llamadas a la API relacionadas con objetos publicitarios se realicen dentro del contexto de una Cuenta Publicitaria específica, identificada típicamente con el prefijo act_ (por ejemplo, act_<ACCOUNT_ID>).

La dependencia de un access_token y un act_<ACCOUNT_ID> para cada llamada a la API subraya una dependencia de seguridad crítica. Si un token de acceso se ve comprometido, la cuenta publicitaria completa, o incluso múltiples cuentas si el token posee permisos amplios, podría quedar expuesta a riesgos, lo que podría resultar en gasto publicitario no autorizado o en violaciones de datos. Esta realidad exige la implementación de medidas de seguridad robustas que superen el simple almacenamiento de tokens. Los desarrolladores deben asegurar el almacenamiento de los tokens de acceso, por ejemplo, mediante variables de entorno o bóvedas seguras, establecer políticas de rotación de tokens y adherirse al principio de mínimo privilegio, otorgando solo los permisos estrictamente necesarios. Adicionalmente, el manejo de errores debe ser capaz de distinguir entre fallos de autenticación y otros tipos de errores de la API para una respuesta adecuada.

### Versionado de la API y Mejores Prácticas para la Estabilidad
Es crucial especificar la versión de la API (por ejemplo, vX.Y) en la URL de las solicitudes para garantizar la estabilidad y predictibilidad del comportamiento de la API. Se desaconseja el uso de la versión "latest" en entornos de producción debido a la posibilidad de cambios que rompan la compatibilidad.

El ciclo de vida de la API de Meta incluye actualizaciones regulares y deprecaciones, lo que exige que los desarrolladores se mantengan informados y planifiquen las migraciones. Aunque la especificación de vX.Y asegura la estabilidad para una versión dada, la evolución continua de Meta significa que las versiones antiguas eventualmente serán deprecadas. Esto no solo afecta la funcionalidad del código actual, sino que también es fundamental para la sostenibilidad a largo plazo del sistema. La dependencia indefinida de una versión fija de la API, sin un plan de actualización, conducirá inevitablemente a fallos del sistema. Por lo tanto, los integradores de la API deben establecer procesos para la actualización regular de las versiones de la API, incluyendo pruebas exhaustivas y la adaptación de sus bases de código. Esto implica la necesidad de un pipeline de integración continua/despliegue continuo (CI/CD) para los sistemas de gestión de anuncios, en lugar de un enfoque de "configurar y olvidar". Asimismo, sugiere la construcción de código modular que facilite el cambio de versiones de la API o la implementación de lógica condicional para manejar diferencias entre versiones.

### Comprensión de la Estructura y Jerarquía de la Cuenta Publicitaria
La jerarquía Campaña > Conjunto de Anuncios > Anuncio > Creatividad Publicitaria constituye el principio organizativo fundamental dentro de la API de Marketing. Cada objeto en esta estructura hereda propiedades o se vincula a su objeto padre, lo que influye directamente en la entrega general de la campaña.

## II. Creación de Campañas: Definiendo el Objetivo Publicitario

Esta sección detalla el objeto de nivel superior en la jerarquía publicitaria, centrándose en los objetivos y la configuración inicial.

### Explicación Detallada de los Objetivos de Campaña y sus Mapeos en la API
El campo objective es el parámetro primordial para una campaña, ya que define su propósito y determina los objetivos de optimización y los eventos de facturación disponibles a nivel del conjunto de anuncios.

Entre los objetivos más comunes se encuentran:

- **OBJECTIVE_CONVERSIONS**: Diseñado para impulsar acciones valiosas en un sitio web o aplicación.
- **OBJECTIVE_LEAD_GENERATION**: Orientado a la recopilación de información de clientes potenciales a través de formularios instantáneos.
- **OBJECTIVE_MESSAGES**: Para iniciar conversaciones en Messenger, Instagram Direct o WhatsApp.

Otros objetivos relevantes incluyen REACH, TRAFFIC, APP_INSTALLS, VIDEO_VIEWS, BRAND_AWARENESS, STORE_VISITS y SALES, según la documentación de Meta.    

El campo objective no es meramente una etiqueta; es una restricción fundamental que moldea la configuración subsiguiente. Por ejemplo, la elección de OBJECTIVE_LEAD_GENERATION impone que la creatividad publicitaria deba ser un formulario de clientes potenciales, y el optimization_goal del conjunto de anuncios se alineará probablemente con LEAD_GENERATION. De manera similar, OBJECTIVE_CONVERSIONS implica la necesidad de un pixel_id y un optimization_goal relacionados con las conversiones. En consecuencia, los integradores de la API deben implementar lógica que ajuste dinámicamente los parámetros disponibles para los conjuntos de anuncios y las creatividades publicitarias en función del objetivo de campaña seleccionado. Esto requiere una capa robusta de mapeo o configuración en su aplicación para evitar llamadas inválidas a la API y asegurar la integridad de la campaña. Además, esta estructura de la API sugiere que el diseño de la misma impone un flujo lógico, guiando a los usuarios hacia configuraciones válidas.

### Campos y Parámetros Clave de la Campaña

- **name**: Un nombre descriptivo para la campaña.
- **objective**: El objetivo principal de la campaña.
- **status**: El estado actual de la campaña (ACTIVE, PAUSED, ARCHIVED, DELETED). Las campañas nuevas suelen iniciarse como PAUSED.
- **special_ad_categories**: Crucial para la conformidad normativa. Debe establecerse para anuncios relacionados con vivienda, empleo, crédito, asuntos sociales, elecciones o política. Este campo tiene implicaciones legales y éticas significativas que deben ser consideradas.
- **buying_type**: Típicamente AUCTION para la mayoría de las campañas, aunque existen otros tipos (por ejemplo, RESERVED).### Implementación del Presupuesto de Campaña Advantage+ (CBO) a Través de la API
El CBO (Campaign Budget Optimization) tiene como propósito optimizar la distribución del presupuesto entre los conjuntos de anuncios dentro de una campaña. Su implementación a través de la API se logra configurando budget_optimization a true a nivel de campaña. Esta acción transfiere la gestión del presupuesto de los conjuntos de anuncios individuales a la campaña.    

Establecer budget_optimization: true a nivel de campaña modifica fundamentalmente la gestión del presupuesto. En lugar de presupuestos fijos por conjunto de anuncios, el presupuesto de la campaña es asignado dinámicamente por el sistema de Meta. Esto representa un cambio de un control manual y granular a una optimización algorítmica. Aunque pueda parecer más sencillo, el CBO exige confianza en los algoritmos de Meta y un enfoque de monitoreo diferente. Los desarrolladores deben informar a los usuarios que los presupuestos individuales de los conjuntos de anuncios se convierten en sugerencias bajo el CBO, no en límites estrictos. Sus sistemas de informes deben reflejar el gasto a nivel de campaña, no solo el gasto por conjunto de anuncios. Este método de gestión de presupuesto es particularmente beneficioso para campañas con múltiples conjuntos de anuncios que se dirigen a audiencias similares o que tienen diferentes potenciales de rendimiento, permitiendo al sistema encontrar la asignación de gasto más eficiente.

### Ejemplos de Llamadas a la API para Crear Campañas con Diversos Objetivos

A continuación, se presentan ejemplos prácticos de cómo construir las solicitudes a la API para la creación de campañas con diferentes configuraciones:

#### Ejemplo 1: Campaña Básica de Conversiones

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/campaigns
{
  "name": "My Conversions Campaign API",
  "objective": "CONVERSIONS",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo ilustra la creación de una campaña orientada a conversiones, estableciendo su nombre, objetivo y estado inicial como pausado.

#### Ejemplo 2: Campaña de Generación de Clientes Potenciales con Categoría de Anuncio Especial

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/campaigns
{
  "name": "Housing Lead Gen Campaign API",
  "objective": "LEAD_GENERATION",
  "status": "PAUSED",
  "special_ad_categories": ["HOUSING"],
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Aquí se muestra cómo crear una campaña de generación de clientes potenciales, especificando además una categoría de anuncio especial, lo cual es obligatorio para ciertos tipos de anuncios.

#### Ejemplo 3: Campaña con Presupuesto de Campaña Advantage+ (CBO)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/campaigns
{
  "name": "CBO Sales Campaign API",
  "objective": "SALES",
  "status": "PAUSED",
  "budget_optimization": true,
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo demuestra la habilitación del Presupuesto de Campaña Advantage+ (CBO) para una campaña de ventas, permitiendo a Meta optimizar la distribución del presupuesto entre los conjuntos de anuncios.

#### Ejemplo 4: Campaña Advantage+ Shopping Campaign (ASC)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/campaigns
{
  "name": "My Advantage+ Shopping Campaign",
  "objective": "OUTCOME_SALES",
  "smart_promotion_type": "AUTOMATED_SHOPPING_ADS",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo muestra la creación de una Campaña Advantage+ Shopping Campaign (ASC), que utiliza la automatización y la IA de Meta para optimizar el rendimiento de las ventas.

### Tabla Imprescindible: Tabla Completa de Campos del Objeto Campaña

La siguiente tabla proporciona una referencia consolidada y rápida para todos los parámetros críticos del objeto Campaña. Para un desarrollador, disponer de una lista clara de campos, sus tipos de datos y sus restricciones (como los valores válidos para special_ad_categories o los enumeradores de objective) es invaluable para construir cargas útiles de API correctas y validar la entrada. Esta tabla aborda directamente la necesidad del usuario de conocer "todos los campos posibles" y de que "no deje campos sin detallar".

| Campo | Tipo de Dato | Descripción | Requerido/Opcional | Valores Válidos/Ejemplos |
|-------|--------------|-------------|-------------------|-------------------------|
| name | String | Nombre descriptivo de la campaña | Requerido | "Campaña de Ventas Q3" |
| objective | Enum | El objetivo principal de la campaña | Requerido | CONVERSIONS, LEAD_GENERATION, MESSAGES, SALES, TRAFFIC, OUTCOME_SALES, etc. |
| status | Enum | Estado actual de la campaña | Opcional | ACTIVE, PAUSED, ARCHIVED, DELETED |
| special_ad_categories | Array of Enums | Categorías de anuncios especiales (vivienda, empleo, crédito, etc.). Requerido si aplica | Opcional | ["HOUSING"], ["EMPLOYMENT"], ["CREDIT"] |
| budget_optimization | Boolean | Habilita el Presupuesto de Campaña Advantage+ (CBO) | Opcional | true, false |
| buying_type | Enum | Tipo de compra de la campaña | Opcional | AUCTION, RESERVED |
| smart_promotion_type | Enum | Indica si la campaña es una Campaña Advantage+ Shopping (ASC) | Opcional (Requerido para ASC) | AUTOMATED_SHOPPING_ADS |
| created_time | DateTime | Marca de tiempo de creación de la campaña | Solo lectura | - |
| id | String | ID único de la campaña | Solo lectura | - |
| updated_time | DateTime | Marca de tiempo de la última actualización de la campaña | Solo lectura | - |

## III. Configuración del Conjunto de Anuncios: Segmentación, Presupuesto y Optimización

Esta sección se adentra en el núcleo de la entrega de anuncios, cubriendo la definición de la audiencia, la asignación de presupuesto y los objetivos de rendimiento.

### Exploración Profunda de los Parámetros de Segmentación de Audiencia
El campo targeting es el más complejo dentro de un conjunto de anuncios, permitiendo un control granular sobre quién verá los anuncios. Es un objeto JSON que contiene diversas especificaciones de audiencia.

**Demografía:**

- **geo_locations**: Permite especificar países, regiones, ciudades o incluso códigos postales para la segmentación geográfica.
- **age_min, age_max**: Definen el rango de edad de la audiencia.
- **genders**: Permite segmentar por género.
- **locales**: Para la segmentación por idioma.

**Segmentación Detallada**: El campo `flexible_spec` se utiliza para intereses, comportamientos y datos demográficos detallados.

**Audiencias Personalizadas y Similares (Lookalikes)**: Se explica cómo incluir o excluir audiencias personalizadas (custom_audiences) y audiencias similares (lookalike_audiences) predefinidas que se han creado fuera del flujo de creación del conjunto de anuncios.La combinación de geo_locations, age_min/age_max y genders, junto con otras opciones de segmentación detallada, no solo define quién verá los anuncios, sino que también determina el tamaño y la calidad de la audiencia potencial. Una segmentación excesivamente estrecha puede llevar a CPMs altos y a una entrega limitada, mientras que una segmentación demasiado amplia podría resultar en un desperdicio de presupuesto. Existe un equilibrio delicado en este proceso. En consecuencia, los integradores de la API deberían considerar la implementación de funciones de estimación de audiencia (si la API de Meta las proporciona, o mediante llamadas iterativas) para ofrecer retroalimentación a los usuarios sobre el alcance estimado de sus parámetros de segmentación. Esto ayuda a evitar que las campañas sean demasiado restrictivas o demasiado amplias. Además, esto sugiere que la creación programática efectiva de anuncios requiere un paso de pre-análisis para dimensionar la audiencia de manera óptima.

### Opciones de Presupuesto

- **Presupuesto Diario (daily_budget)**: La cantidad promedio que se gastará por día.
- **Presupuesto Total (lifetime_budget)**: La cantidad total a gastar durante la duración programada del conjunto de anuncios.
- **Relación con CBO**: Si el CBO está habilitado a nivel de campaña (budget_optimization: true), los presupuestos individuales de los conjuntos de anuncios se convierten en sugerencias o mínimos, no en límites estrictos.

### Estrategias de Puja y Objetivos de Optimización

- **optimization_goal**: Lo que el sistema de Meta debe optimizar (por ejemplo, LINK_CLICKS, IMPRESSIONS, LEAD_GENERATION, CONVERSIONS, VIDEO_VIEWS). Este objetivo debe alinearse con el objetivo de la campaña.
- **billing_event**: Cuándo se realiza el cargo (por ejemplo, IMPRESSIONS, LINK_CLICKS).
- **bid_strategy**: Cómo debe pujar Meta para alcanzar el objetivo de optimización (por ejemplo, LOWEST_COST_WITHOUT_CAP, COST_CAP, BID_CAP).El optimization_goal y el billing_event no son solo configuraciones; son instrucciones directas al algoritmo de entrega de Meta sobre qué priorizar y cómo cobrar. Elegir LINK_CLICKS para la optimización pero IMPRESSIONS para la facturación significa que se paga por las impresiones independientemente de los clics, aunque el sistema intente obtener clics. Una desalineación en este punto puede llevar a un gasto ineficiente. Por consiguiente, los sistemas programáticos deben presentar estas opciones de manera clara y, posiblemente, incluso recomendar combinaciones óptimas basadas en los objetivos de la campaña. Por ejemplo, para una campaña de conversiones, el optimization_goal debería ser CONVERSIONS y el billing_event típicamente IMPRESSIONS (ya que Meta optimiza para conversiones pero cobra por la entrega). Esto resalta la necesidad de una comprensión profunda del sistema de subastas de Meta.

### Opciones de Ubicación (Placements)

- **Ubicaciones Automáticas (Advantage+ Placements)**: Generalmente recomendadas por Meta para un mayor alcance y una mejor optimización.
- **Ubicaciones Manuales**: Permiten especificar exactamente dónde aparecerán los anuncios utilizando campos como publisher_platforms (facebook, instagram, audience_network, messenger), facebook_positions, instagram_positions, messenger_positions, audience_network_positions.    

### Campos y Configuraciones Detalladas del Conjunto de Anuncios

- **name**: Nombre del conjunto de anuncios.
- **campaign_id**: Enlaza con la campaña padre.
- **daily_budget / lifetime_budget**: Configuración del presupuesto.
- **start_time, end_time**: Programan la duración del conjunto de anuncios.
- **status**: ACTIVE, PAUSED, etc.
- **promoted_object**: Para instalaciones de aplicaciones, "me gusta" de página, etc.
- **delivery_status**: Campo de solo lectura que indica el estado de entrega.### Ejemplos de Llamadas a la API para Diversas Configuraciones de Conjuntos de Anuncios

#### Ejemplo 1: Conjunto de Anuncios Básico con Presupuesto Diario y Segmentación Amplia

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adsets
{
  "name": "Daily Budget Broad Audience",
  "campaign_id": "<CAMPAIGN_ID>",
  "daily_budget": "100000", // $100.00 USD (en centavos)
  "targeting": {
    "geo_locations": {"countries": ["US"]},
    "age_min": 18,
    "age_max": 65,
    "genders": [1, 2] // 1 para masculino, 2 para femenino
  },
  "optimization_goal": "LINK_CLICKS",
  "billing_event": "IMPRESSIONS",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo demuestra la creación de un conjunto de anuncios con un presupuesto diario, segmentación geográfica y demográfica, y objetivos de optimización y facturación específicos.

#### Ejemplo 2: Conjunto de Anuncios con Presupuesto Total, Ubicaciones Específicas y Programación

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adsets
{
  "name": "Lifetime Budget Instagram Only",
  "campaign_id": "<CAMPAIGN_ID>",
  "lifetime_budget": "500000", // $500.00 USD
  "start_time": "2024-07-01T10:00:00-0700",
  "end_time": "2024-07-31T23:59:59-0700",
  "targeting": {
    "geo_locations": {"countries": ["CA"]}
  },
  "publisher_platforms": ["instagram"],
  "instagram_positions": ["feed", "explore"],
  "optimization_goal": "IMPRESSIONS",
  "billing_event": "IMPRESSIONS",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo ilustra la configuración de un conjunto de anuncios con un presupuesto total, una programación específica y la restricción de ubicaciones a plataformas y posiciones concretas dentro de Instagram.

#### Ejemplo 3: Conjunto de Anuncios para Creatividad Dinámica

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adsets
{
  "name": "Dynamic Creative AdSet",
  "campaign_id": "<CAMPAIGN_ID>",
  "optimization_goal": "APP_INSTALLS",
  "billing_event": "IMPRESSIONS",
  "is_dynamic_creative": true,
  "promoted_object": {
    "object_store_url": "https://itunes.apple.com/us/app/facebook/id284882215",
    "application_id": "<ADVERTISED_APP_ID>"
  },
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo muestra la creación de un conjunto de anuncios configurado para usar Creatividad Dinámica, lo que permite a Meta probar automáticamente diferentes combinaciones de activos creativos.

### Tabla Imprescindible: Tabla Completa de Campos del Objeto Conjunto de Anuncios

El objeto Conjunto de Anuncios es, posiblemente, el más complejo debido a su campo targeting y la interacción entre presupuesto, puja y optimización. Una tabla detallada es esencial para que los desarrolladores naveguen por la miríada de opciones y aseguren una configuración correcta, especialmente al tratar con estructuras JSON anidadas para la segmentación. Esta tabla cumple directamente con el requisito de "todos los campos posibles" para este objeto crítico.

| Campo | Tipo de Dato | Descripción | Requerido/Opcional | Valores Válidos/Ejemplos |
|-------|--------------|-------------|-------------------|-------------------------|
| name | String | Nombre descriptivo del conjunto de anuncios | Requerido | "AdSet Retargeting Web" |
| campaign_id | String | ID de la campaña a la que pertenece este conjunto de anuncios | Requerido | 1234567890 |
| daily_budget | String | Presupuesto diario en centavos de moneda local | Opcional (si lifetime_budget no está presente o CBO deshabilitado) | "10000" (100 USD) |
| lifetime_budget | String | Presupuesto total en centavos de moneda local para la duración del ad set | Opcional (si daily_budget no está presente o CBO deshabilitado) | "500000" (5000 USD) |
| targeting | Object | Objeto JSON que define la audiencia a la que se dirige el anuncio | Requerido | Ver subcampos a continuación |
| targeting.geo_locations | Object | Ubicaciones geográficas | Opcional | {"countries": ["US"]} |
| targeting.age_min | Integer | Edad mínima de la audiencia | Opcional | 18 |
| targeting.age_max | Integer | Edad máxima de la audiencia | Opcional | 65 |
| targeting.genders | Array of Integers | Géneros a los que se dirige. 1=Masculino, 2=Femenino | Opcional | [1, 2] |
| optimization_goal | Enum | Objetivo de optimización para la entrega del anuncio | Requerido | LINK_CLICKS, IMPRESSIONS, LEAD_GENERATION, CONVERSIONS, VIDEO_VIEWS, APP_INSTALLS |
| billing_event | Enum | Evento por el cual se factura el anuncio | Requerido | IMPRESSIONS, LINK_CLICKS |
| bid_strategy | Enum | Estrategia de puja para el conjunto de anuncios | Opcional | LOWEST_COST_WITHOUT_CAP, COST_CAP, BID_CAP, LOWEST_COST_WITH_MIN_ROAS |
| publisher_platforms | Array of Enums | Plataformas donde se mostrará el anuncio | Opcional | ["facebook", "instagram", "audience_network", "messenger"] |
| facebook_positions | Array of Enums | Posiciones específicas en Facebook | Opcional | ["feed", "right_hand_column"] |
| instagram_positions | Array of Enums | Posiciones específicas en Instagram | Opcional | ["feed", "explore", "story"] |
| messenger_positions | Array of Enums | Posiciones específicas en Messenger | Opcional | ["inbox", "story"] |
| audience_network_positions | Array of Enums | Posiciones específicas en Audience Network | Opcional | ["classic", "instream_video"] |
| start_time | DateTime | Fecha y hora de inicio del conjunto de anuncios | Opcional | "YYYY-MM-DDTHH:MM:SS-ZZZZ" |
| end_time | DateTime | Fecha y hora de finalización del conjunto de anuncios | Opcional | "YYYY-MM-DDTHH:MM:SS-ZZZZ" |
| status | Enum | Estado actual del conjunto de anuncios | Opcional | ACTIVE, PAUSED, ARCHIVED, DELETED |
| promoted_object | Object | Objeto que se promociona (ej. ID de aplicación para instalaciones) | Opcional | {"application_id": "<APP_ID>"} |
| is_dynamic_creative | Boolean | Habilita la creatividad dinámica a nivel del conjunto de anuncios | Opcional | true, false |
| id | String | ID único del conjunto de anuncios | Solo lectura | - |

## IV. Desarrollo de Creatividades Publicitarias: Creación de Contenido Atractivo

Esta sección se centra en los componentes visuales y textuales de un anuncio, con un fuerte énfasis en el video.

### Formatos de Creatividad Soportados

Meta soporta una variedad de formatos de creatividad, cada uno con requisitos de campo únicos:

- **Imagen**: Incluye formatos como Imagen Única, Carrusel y Colección.
- **Video**: Abarca Video Único y Video en Carrusel.
- **Creatividad Dinámica**: Permite la generación automática de variaciones de anuncios.
- **Formulario de Clientes Potenciales**: Específico para campañas de generación de leads.    

### Campos Esenciales de la Creatividad

- **name**: Nombre de la creatividad.
- **body**: El texto principal del anuncio.
- **title**: El titular del anuncio.
- **link_url**: La URL de destino a la que se dirige el usuario al hacer clic en el anuncio.
- **call_to_action**: Un botón con un tipo (por ejemplo, LEARN_MORE, SHOP_NOW, APPLY_NOW) y un valor opcional (por ejemplo, la URL del sitio web).
- **page_id**: El ID de la página de Facebook asociada con el anuncio. Este campo es esencial para la mayoría de los tipos de anuncios.
- **instagram_actor_id**: El ID de la cuenta de Instagram si el anuncio va a aparecer en Instagram. (Nota: instagram_actor_id está siendo deprecado, se recomienda usar instagram_user_id).### Enfoque Especial: Creatividades de Anuncios de Video (Carga, Formatos, Mejores Prácticas, Integración con la API)

#### Proceso de Carga de Video
La carga de videos es un proceso de varios pasos. El primer paso implica subir el video al endpoint /videos de la cuenta publicitaria. Esta es una acción separada de la creación de la creatividad publicitaria en sí.    

Es importante destacar que las cargas de video son asíncronas. La API devuelve un upload_phase y un status que deben ser monitoreados. El video_id solo será utilizable una vez que el video esté completamente procesado. Para las creatividades de video, se puede proporcionar un image_hash para la miniatura. Este hash se obtiene subiendo una imagen al endpoint /adimages. [1, 3, 4,    

#### Integración de la API para Creatividades de Video

Una vez que el video ha sido cargado y procesado, su video_id se utiliza en la carga útil de la creatividad publicitaria. Los campos de ejemplo incluyen video_id, image_hash (para la miniatura), call_to_action, body, title y link_url.

#### Mejores Prácticas para Anuncios de Video

Se recomienda considerar formatos de video óptimos, relaciones de aspecto, duración y estrategias de contenido específicas para las plataformas de Meta para maximizar el rendimiento.A diferencia de las creatividades de imagen, donde un image_hash puede ser cargado y utilizado con relativa rapidez, las creatividades de video requieren un proceso de dos pasos: la carga del video y luego la creación del ad_creative utilizando el video_id. La presencia de upload_phase y status indica una operación asíncrona. Esto implica una cadena de dependencias y el potencial de condiciones de carrera o retrasos. Por lo tanto, los sistemas programáticos deben implementar un manejo asíncrono robusto para las cargas de video, incluyendo mecanismos de sondeo o webhooks para confirmar la finalización del procesamiento del video antes de intentar crear la creatividad publicitaria. Esto añade complejidad en comparación con los anuncios de imagen estáticos y requiere un manejo cuidadoso de errores para cargas incompletas o fallos de procesamiento. Además, esto significa que una única llamada a la API no es suficiente para la creación de anuncios de video; se trata de un flujo de trabajo.

### Creatividad Dinámica y Consideraciones de Creatividad Advantage+

**Creatividad Dinámica**: Al establecer `use_dynamic_creative` en true (a nivel de ad set) y proporcionar un `asset_feed_spec` en la creatividad, Meta puede generar automáticamente múltiples variaciones de anuncios combinando diferentes activos (imágenes, videos, texto, llamadas a la acción).

**asset_feed_spec**: Este campo permite especificar múltiples activos creativos (imágenes, videos, cuerpos de texto, títulos, descripciones, llamadas a la acción, URLs de enlace) que Meta combinará automáticamente.

**Creatividad Advantage+**: El campo `asset_feed_id` se utilizaba para capacidades de creatividad dinámica más avanzadas, pero ha sido deprecado en versiones recientes de la API. Ahora se recomienda usar `asset_feed_spec`.

**Dynamic Media para Advantage+ Catalog Ads**: Permite que los videos de tu catálogo se usen dinámicamente en tus anuncios. Se habilita configurando `media_type_automation` a `OPT_IN` dentro de `degrees_of_freedom_spec` en la creatividad.La configuración de use_dynamic_creative: true y el uso de asset_feed_spec van más allá de ser simples campos; representan la orientación de Meta hacia la optimización de creatividades impulsada por inteligencia artificial. En lugar de pruebas A/B manuales, el sistema encuentra automáticamente las mejores combinaciones. Esto implica una compensación: menos control manual sobre variaciones de anuncios específicas, pero potencialmente un mayor rendimiento a través de pruebas automatizadas y personalización. Los desarrolladores que construyen herramientas programáticas deben guiar a los usuarios sobre cómo proporcionar un conjunto diverso de activos (imágenes, videos, variaciones de texto) para la Creatividad Advantage+ con el fin de maximizar su efectividad. La infraestructura de informes también debe ser capaz de interpretar el rendimiento a través de estas variaciones generadas dinámicamente, en lugar de solo IDs de creatividades estáticas. Esto desplaza el enfoque de "crear un anuncio perfecto" a "proporcionar al sistema suficientes ingredientes para crear muchos anuncios perfectos".

### Ejemplos de Llamadas a la API para Diversos Tipos de Creatividades

#### Ejemplo 1: Creatividad de Anuncio de Imagen

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "My Image Creative",
  "object_story_spec": {
    "page_id": "<PAGE_ID>",
    "link_data": {
      "image_hash": "<IMAGE_HASH_FROM_UPLOAD>",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {"link": "https://www.example.com/shop"}
      },
      "message": "Check out our new collection!",
      "name": "New Arrivals"
    }
  },
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo demuestra la creación de una creatividad de anuncio de imagen, incluyendo el hash de la imagen, la llamada a la acción, el mensaje y el título, vinculados a una página de Facebook.

#### Ejemplo 2: Creatividad de Anuncio de Video (asumiendo que el video ya está cargado y procesado)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "My Video Creative",
  "object_story_spec": {
    "page_id": "<PAGE_ID>",
    "video_data": {
      "video_id": "<VIDEO_ID_FROM_UPLOAD>",
      "image_hash": "<OPTIONAL_THUMBNAIL_IMAGE_HASH>",
      "call_to_action": {
        "type": "WATCH_MORE",
        "value": {"link": "https://www.example.com/videos"}
      },
      "message": "Watch our latest product demo!",
      "title": "Product Demo"
    }
  },
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo ilustra la creación de una creatividad de video, donde se utiliza el ID del video previamente cargado y procesado, junto con una miniatura opcional y la llamada a la acción.

#### Ejemplo 3: Creatividad Dinámica con asset_feed_spec (Imágenes y Textos)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "Dynamic Creative with Images and Text",
  "object_story_spec": {
    "page_id": "<PAGE_ID>"
  },
  "asset_feed_spec": {
    "images": [
      {"hash": "<IMAGE_HASH_1>"},
      {"hash": "<IMAGE_HASH_2>"}
    ],
    "bodies": [
      {"text": "Discover our amazing products!"},
      {"text": "Shop now and save big!"}
    ],
    "titles": [
      {"text": "Great Deals"},
      {"text": "Limited Time Offer"}
    ],
    "call_to_action_types": ["SHOP_NOW", "LEARN_MORE"],
    "link_urls": [
      {"url": "https://www.example.com/shop", "url_tags": "link=link1"},
      {"url": "https://www.example.com/learn", "url_tags": "link=link2"}
    ],
    "ad_formats": ["SINGLE_IMAGE", "CAROUSEL"]
  },
  "access_token": "YOUR_ACCESS_TOKEN"
}
```
Este ejemplo muestra cómo crear una creatividad dinámica utilizando asset_feed_spec para proporcionar múltiples imágenes, cuerpos de texto, títulos, tipos de llamadas a la acción y URLs de enlace. Meta combinará estos activos para encontrar las mejores variaciones.    

#### Ejemplo 4: Creatividad Dinámica con asset_feed_spec (Videos y Textos)

```json

POST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "Dynamic Creative with Videos and Text",
  "object_story_spec": {
    "page_id": "<PAGE_ID>"
  },
  "asset_feed_spec": {
    "videos": [
      {"video_id": "<VIDEO_ID_1>"},
      {"video_id": "<VIDEO_ID_2>"}
    ],
    "bodies": [
      {"text": "Watch our amazing product demo!"},
      {"text": "See how it works in action!"}
    ],
    "titles": [
      {"text": "Product Demo"},
      {"text": "How It Works"}
    ],
    "call_to_action_types": ["WATCH_MORE", "LEARN_MORE"],
    "link_urls": [
      {"url": "https://www.example.com/videos", "url_tags": "link=link1"},
      {"url": "https://www.example.com/download", "url_tags": "link=link2"}
    ],
    "ad_formats": ["SINGLE_VIDEO", "CAROUSEL"]
  },
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Este ejemplo ilustra la creación de una creatividad dinámica con asset_feed_spec que incluye múltiples videos, cuerpos de texto, títulos, llamadas a la acción y URLs de enlace.

#### Ejemplo 5: Creatividad para Advantage+ Catalog Ads con Dynamic Media (Colección con Video del Catálogo)

```jsonPOST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "Dynamic Media Collection Ad Creative",
  "object_story_spec": {
    "template_data": {
      "format_option": "collection_video",
      "link": "https://fb.com/canvas_doc/<CANVAS_ID>",
      "message": "Your Collection Ad",
      "name": "Dynamic Collection",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {"link": "https://www.example.com/shop"}
      }
    },
    "page_id": "<PAGE_ID>"
  },
  "degrees_of_freedom_spec": {
    "creative_features_spec": {
      "media_type_automation": {
        "enroll_status": "OPT_IN"
      }
    }
  },
  "product_set_id": "<PRODUCT_SET_ID>",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Este ejemplo muestra cómo crear una creatividad para Advantage+ Catalog Ads que utiliza Dynamic Media en formato de Colección. El media_type_automation configurado como OPT_IN permite que los videos de tu catálogo reemplacen el medio principal (hero media) si están disponibles.

#### Ejemplo 6: Creatividad para Advantage+ Catalog Ads con Dynamic Media (Video Único del Catálogo)

```jsonPOST /vX.Y/act_<AD_ACCOUNT_ID>/adcreatives
{
  "name": "Dynamic Media Single Video Ad Creative",
  "object_story_spec": {
    "template_data": {
      "format_option": "single_video",
      "link": "https://www.example.com/product",
      "message": "Check out this product video!",
      "name": "Product Video Ad",
      "call_to_action": {
        "type": "WATCH_MORE",
        "value": {"link": "https://www.example.com/product-video"}
      }
    },
    "page_id": "<PAGE_ID>"
  },
  "degrees_of_freedom_spec": {
    "creative_features_spec": {
      "media_type_automation": {
        "enroll_status": "OPT_IN"
      }
    }
  },
  "product_set_id": "<PRODUCT_SET_ID>",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Este ejemplo ilustra la creación de una creatividad para Advantage+ Catalog Ads que utiliza Dynamic Media en formato de video único, permitiendo que un video de tu catálogo se muestre como el activo principal.### Tabla Imprescindible: Tabla Completa de Campos del Objeto Creatividad de Anuncio

Las creatividades de anuncios varían significativamente según el formato. Una tabla completa es esencial para diferenciar los requisitos para imágenes, videos, carruseles y otros tipos de creatividades. Ayuda a los desarrolladores a comprender qué campos son condicionales y cómo estructurar correctamente el object_story_spec o el asset_feed_spec para cada formato, abordando directamente la necesidad del usuario de "todos los campos posibles" en todos los tipos de creatividades.

| Campo | Tipo de Dato | Descripción | Requerido/Opcional | Valores Válidos/Ejemplos |
|-------|--------------|-------------|-------------------|-------------------------|
| name | String | Nombre de la creatividad | Requerido | "Creatividad Producto Nuevo" |
| object_story_spec | Object | Especificación del contenido del anuncio (imagen, video, etc.) | Requerido | Ver subcampos a continuación |
| object_story_spec.page_id | String | ID de la página de Facebook asociada | Requerido | 1234567890 |
| object_story_spec.link_data.message | String | Texto principal del anuncio | Requerido (para link ads) | "Descubre nuestra nueva colección!" |
| object_story_spec.link_data.name | String | Título del anuncio | Requerido (para link ads) | "¡Grandes Ofertas!" |
| object_story_spec.link_data.link | String | URL de destino | Requerido (para link ads) | https://www.example.com |
| object_story_spec.link_data.image_hash | String | Hash de la imagen para creatividades de imagen | Requerido (para imagen) | <HASH_DE_IMAGEN> |
| object_story_spec.video_data.video_id | String | ID del video para creatividades de video | Requerido (para video) | <ID_DE_VIDEO> |
| object_story_spec.video_data.image_hash | String | Hash de la imagen para miniatura de video (opcional) | Opcional (para video) | <HASH_DE_IMAGEN> |
| object_story_spec.call_to_action | Object | Botón de llamada a la acción | Opcional | {"type": "SHOP_NOW", "value": {"link": "https://example.com"}} |
| object_story_spec.template_data.format_option | Enum | Formato de la creatividad para Advantage+ Catalog Ads | Requerido (para Advantage+ Catalog Ads) | collection_video, single_video |
| instagram_actor_id | String | ID de la cuenta de Instagram para anuncios en Instagram (deprecado) | Opcional | 9876543210 |
| instagram_user_id | String | ID de la cuenta de Instagram para anuncios en Instagram (recomendado) | Opcional | 9876543210 |
| use_dynamic_creative | Boolean | Habilita la creatividad dinámica (a nivel de ad set) | Opcional | true, false |
| asset_feed_spec | Object | Especificación de activos para Creatividad Dinámica | Opcional (Requerido para Creatividad Dinámica) | Ver subcampos a continuación |
| asset_feed_spec.images | Array of Objects | Lista de imágenes para Creatividad Dinámica | Opcional | [{"hash": "<IMAGE_HASH>"}] |
| asset_feed_spec.videos | Array of Objects | Lista de videos para Creatividad Dinámica | Opcional | [{"video_id": "<VIDEO_ID>"}] |
| asset_feed_spec.bodies | Array of Objects | Lista de cuerpos de texto para Creatividad Dinámica | Opcional | [{"text": "Texto del anuncio"}] |
| asset_feed_spec.titles | Array of Objects | Lista de títulos para Creatividad Dinámica | Opcional | [{"text": "Título del anuncio"}] |
| asset_feed_spec.descriptions | Array of Objects | Lista de descripciones para Creatividad Dinámica | Opcional | [{"text": "Descripción del anuncio"}] |
| asset_feed_spec.call_to_action_types | Array of Objects | Lista de tipos de CTA para Creatividad Dinámica | Opcional | ["SHOP_NOW", "LEARN_MORE"] |
| asset_feed_spec.link_urls | Array of Objects | Lista de URLs de enlace para Creatividad Dinámica | Opcional | [{"url": "https://example.com", "url_tags": "tag"}] |
| asset_feed_spec.ad_formats | Array of Enums | Formatos de anuncio para Creatividad Dinámica | Opcional | ["SINGLE_IMAGE", "CAROUSEL", "SINGLE_VIDEO"] |
| asset_feed_id | String | ID del feed de activos (deprecado) | Opcional | <ID_DE_FEED_DE_ACTIVOS> |
| degrees_of_freedom_spec | Object | Especifica transformaciones habilitadas para la creatividad | Opcional | Ver subcampos a continuación |
| degrees_of_freedom_spec.creative_features_spec.media_type_automation.enroll_status | Enum | Habilita Dynamic Media para Advantage+ Catalog Ads | Opcional (Requerido para Dynamic Media) | OPT_IN |
| product_set_id | String | ID del conjunto de productos para Advantage+ Catalog Ads | Requerido (para Advantage+ Catalog Ads) | <PRODUCT_SET_ID> |
| status | Enum | Estado de la creatividad | Solo lectura | ACTIVE, PAUSED |
| id | String | ID único de la creatividad | Solo lectura | - |object_story_spec.link_data.image_hash	String	Hash de la imagen para creatividades de imagen.	Requerido (para imagen)	<HASH_DE_IMAGEN>	
object_story_spec.video_data.video_id	String	ID del video para creatividades de video.	Requerido (para video)	<ID_DE_VIDEO>	
object_story_spec.video_data.image_hash	String	Hash de la imagen para miniatura de video (opcional).	Opcional (para video)	<HASH_DE_IMAGEN>	
1   

object_story_spec.call_to_action	Object	Botón de llamada a la acción.	Opcional	{"type": "SHOP_NOW", "value": {"link": "https://example.com"}}	
object_story_spec.template_data.format_option	Enum	Formato de la creatividad para Advantage+ Catalog Ads.	Requerido (para Advantage+ Catalog Ads)	collection_video, single_video	
instagram_actor_id	String	ID de la cuenta de Instagram para anuncios en Instagram (deprecado).	Opcional	9876543210	
8   

instagram_user_id	String	ID de la cuenta de Instagram para anuncios en Instagram (recomendado).	Opcional	9876543210	
use_dynamic_creative	Boolean	Habilita la creatividad dinámica (a nivel de ad set).	Opcional	true, false	
asset_feed_spec	Object	Especificación de activos para Creatividad Dinámica.	Opcional (Requerido para Creatividad Dinámica)	Ver subcampos a continuación	
asset_feed_spec.images	Array of Objects	Lista de imágenes para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.videos	Array of Objects	Lista de videos para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.bodies	Array of Objects	Lista de cuerpos de texto para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.titles	Array of Objects	Lista de títulos para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.descriptions	Array of Objects	Lista de descripciones para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.call_to_action_types	Array of Objects	Lista de tipos de CTA para Creatividad Dinámica.	Opcional	``	
asset_feed_spec.link_urls	Array of Objects	Lista de URLs de enlace para Creatividad Dinámica.	Opcional	[{"url": "https://example.com", "url_tags": "tag"}]	
asset_feed_spec.ad_formats	Array of Enums	Formatos de anuncio para Creatividad Dinámica.	Opcional	, , ,	
asset_feed_id	String	ID del feed de activos (deprecado).	Opcional	<ID_DE_FEED_DE_ACTIVOS>	
9,    

degrees_of_freedom_spec	Object	Especifica transformaciones habilitadas para la creatividad.	Opcional	Ver subcampos a continuación	
degrees_of_freedom_spec.creative_features_spec.media_type_automation.enroll_status	Enum	Habilita Dynamic Media para Advantage+ Catalog Ads.	Opcional (Requerido para Dynamic Media)	OPT_IN	
product_set_id	String	ID del conjunto de productos para Advantage+ Catalog Ads.	Requerido (para Advantage+ Catalog Ads)	<PRODUCT_SET_ID>	
status	Enum	Estado de la creatividad.	Solo lectura	ACTIVE, PAUSED	
id	String	ID único de la creatividad.	Solo lectura		
  
### Tabla Imprescindible: Campos Específicos y Flujo de Trabajo para Creatividades de Anuncios de Video

Dado el énfasis explícito del usuario en los anuncios de video, una tabla dedicada que detalle los campos específicos y el flujo de trabajo de varios pasos para las creatividades de video (carga, procesamiento, creación de la creatividad) es invaluable. Consolida la información dispersa en múltiples fuentes en una secuencia clara y accionable, lo cual es fundamental para integraciones complejas de la API.

| Campo/Endpoint | Descripción | Propósito | Paso del Flujo de Trabajo |
|---------------|-------------|-----------|---------------------------|
| /videos endpoint | Endpoint para cargar archivos de video | Iniciar la carga de un video a la cuenta publicitaria | 1. Carga de Video |
| video_id | ID único asignado al video cargado | Referenciar el video en la creatividad publicitaria | 2. Creación de Creatividad |
| upload_phase | Estado actual de la fase de carga del video | Monitorear el progreso de la carga | 1. Carga de Video (Monitoreo) |
| status | Estado de procesamiento del video (ej. processing, ready) | Indicar si el video está listo para ser usado en una creatividad | 1. Carga de Video (Monitoreo) |
| image_hash (para miniatura) | Hash de una imagen cargada para usar como miniatura del video | Proporcionar una imagen de vista previa para el video | 2. Creación de Creatividad (Opcional) |
| /adimages endpoint | Endpoint para cargar archivos de imagen | Obtener un image_hash para miniaturas de video | 1. Carga de Imagen (para miniatura) |

## V. Creación de Anuncios: Vinculación de Creatividades con Audiencias

Este objeto final en la jerarquía conecta el contenido creativo con la audiencia definida y la configuración de entrega.

### Conexión de Creatividades de Anuncios con Conjuntos de Anuncios

El adset_id vincula el anuncio a su audiencia objetivo y presupuesto. El ad_creative_id vincula el anuncio al contenido que mostrará. Un anuncio es el envoltorio final que une estos dos componentes.

### Campos y Parámetros del Anuncio

- **name**: Un nombre descriptivo para el anuncio.
- **adset_id**: El ID del conjunto de anuncios al que pertenece este anuncio.
- **ad_creative_id**: El ID de la creatividad de anuncio a utilizar.
- **status**: El estado actual del anuncio (ACTIVE, PAUSED, ARCHIVED, DELETED).
- **url_tags**: Parámetros opcionales que se añaden a la URL de destino para fines de seguimiento (por ejemplo, parámetros UTM).
- **tracking_specs**: Configuraciones de seguimiento avanzadas.

### Integración de Formularios de Clientes Potenciales (Instant Forms) para Campañas de Generación de Clientes Potenciales

Para las campañas de generación de clientes potenciales, es un prerrequisito que la campaña tenga el objective: LEAD_GENERATION. Los formularios de clientes potenciales se crean como objetos separados (por ejemplo, a través del endpoint /leadgen_forms) y poseen su propio form_id único.Para un anuncio de clientes potenciales, la ad_creative debe hacer referencia al form_id dentro de su link_url o valor de call_to_action, a menudo dentro de una estructura object_story_spec. La link_url para una creatividad de formulario de clientes potenciales suele ser un marcador de posición, ya que el formulario se sirve directamente en las plataformas de Meta.

La mención explícita de OBJECTIVE_LEAD_GENERATION y la necesidad de un form_id en la creatividad indican que la generación de clientes potenciales es un flujo de conversión distinto y autocontenido dentro del ecosistema de Meta. Este flujo evita los sitios web externos, manteniendo a los usuarios en la plataforma. Esto implica un conjunto diferente de requisitos de seguimiento y manejo de datos en comparación con las conversiones tradicionales en sitios web. Por consiguiente, los sistemas programáticos para campañas de generación de clientes potenciales no solo deben crear la creatividad del anuncio, sino también gestionar el ciclo de vida de los propios formularios de clientes potenciales (creación, pre-llenado, obtención de clientes potenciales a través de la API). Esto requiere la integración con la API de Lead Ads para recuperar los clientes potenciales enviados, añadiendo otra capa de complejidad más allá de la mera creación de anuncios. Además, esto sugiere que los formularios de clientes potenciales ofrecen una tasa de conversión potencialmente más alta debido a la reducción de la fricción, pero requieren consideraciones específicas de la pipeline de datos post-conversión.

### Ejemplos de Llamadas a la API para la Creación de Anuncios, Incluyendo Anuncios de Clientes Potenciales

#### Ejemplo 1: Creación de Anuncio Estándar (Imagen/Video)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/ads
{
  "name": "My First Ad",
  "adset_id": "<ADSET_ID>",
  "ad_creative_id": "<AD_CREATIVE_ID>",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Este ejemplo muestra la creación de un anuncio estándar, vinculando un conjunto de anuncios y una creatividad de anuncio específicos.

#### Ejemplo 2: Creación de Anuncio de Clientes Potenciales (asumiendo que la creatividad del formulario de clientes potenciales ya está creada)

```json
POST /vX.Y/act_<AD_ACCOUNT_ID>/ads
{
  "name": "My Lead Generation Ad",
  "adset_id": "<LEAD_ADSET_ID>",
  "ad_creative_id": "<LEAD_AD_CREATIVE_ID_REFERENCING_FORM_ID>",
  "status": "PAUSED",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Este ejemplo ilustra la creación de un anuncio de clientes potenciales, donde la creatividad del anuncio ya ha sido configurada para hacer referencia a un formulario de clientes potenciales.

### Tabla Imprescindible: Tabla Completa de Campos del Objeto Anuncio

El objeto Anuncio es el más simple en términos de campos, pero es el vínculo crucial que une la campaña, el conjunto de anuncios y la creatividad. Una tabla asegura que los desarrolladores mapeen correctamente los IDs de los objetos creados previamente, lo cual es fundamental para un anuncio funcional. Refuerza la dependencia jerárquica.

| Campo | Tipo de Dato | Descripción | Requerido/Opcional | Valores Válidos/Ejemplos |
|-------|--------------|-------------|-------------------|-------------------------|
| name | String | Nombre descriptivo del anuncio | Requerido | "Anuncio de Video Principal" |
| adset_id | String | ID del conjunto de anuncios al que pertenece este anuncio | Requerido | 1234567890 |
| ad_creative_id | String | ID de la creatividad de anuncio a utilizar | Requerido | 0987654321 |
| status | Enum | Estado actual del anuncio | Opcional | ACTIVE, PAUSED, ARCHIVED, DELETED |
| url_tags | String | Parámetros de seguimiento que se añaden a la URL de destino | Opcional | utm_source=facebook&utm_campaign=sales |
| tracking_specs | Object | Configuraciones avanzadas de seguimiento | Opcional | {"action_type": "offsite_conversions"} |
| id | String | ID único del anuncio | Solo lectura | - |

## VI. Temas Avanzados y Mejores Prácticas para la Integración con la API

Esta sección aborda aspectos operativos cruciales para construir sistemas publicitarios robustos y escalables.

### Manejo de Límites de Tasa de la API y Respuestas de Error

Meta impone varios límites de tasa a su API, incluyendo límites por número de llamadas, por tiempo y por gasto. Es fundamental implementar mecanismos de reintento con retroceso exponencial para gestionar estos límites de manera efectiva. Además, es vital detallar los códigos de error y mensajes comunes, y desarrollar estrategias para analizarlos y manejarlos de manera elegante, distinguiendo entre errores temporales y permanentes.

Las interacciones con la API son inherentemente propensas a errores transitorios (problemas de red, interrupciones temporales del servicio de Meta) y errores permanentes (parámetros inválidos, problemas de permisos). Simplemente reintentar todos los errores o ignorarlos conducirá a una entrega de anuncios poco fiable o a un desperdicio de recursos. Un sistema robusto necesita interpretar inteligentemente los códigos de error. Por consiguiente, las soluciones programáticas deben implementar una lógica sofisticada de manejo de errores, incluyendo la categorización de errores, el registro, las alertas y las estrategias de reintento adaptativas. Esto va más allá de los bloques básicos de try-catch para lograr una arquitectura más resiliente, crucial para mantener operaciones publicitarias continuas y minimizar la intervención manual.

### Monitoreo e Informes a Través de la API (Visión General de la Obtención de Datos)

La API de Marketing de Meta permite la obtención de datos de rendimiento (insights) a nivel de campaña, conjunto de anuncios y anuncio. Esta capacidad es fundamental para monitorear el rendimiento de la campaña y optimizar las estrategias de manera programática.

Aunque la consulta principal se centra en la creación, la capacidad de obtener datos de rendimiento a través de la API es el siguiente paso lógico para cualquier sistema sofisticado de gestión de anuncios. La creación sin monitoreo es una operación ciega. El objetivo de "crear cualquier tipo de campaña" implica un deseo de campañas efectivas, lo cual requiere retroalimentación sobre el rendimiento. Por lo tanto, una solución programática completa se extiende más allá de la creación para incluir la generación de informes automatizados y, potencialmente, bucles de optimización automatizados. Esto significa que la integración de la API debe considerar no solo las solicitudes POST para la creación, sino también las solicitudes GET para recuperar datos de rendimiento (endpoints /insights) para cerrar el ciclo del flujo de trabajo publicitario.

### Mejores Prácticas para una Integración de API Escalable y Robusta

- **Idempotencia**: Diseñar las llamadas a la API para que sean idempotentes siempre que sea posible, con el fin de prevenir efectos secundarios no deseados de los reintentos.
- **Solicitudes por Lotes**: Utilizar solicitudes API por lotes para reducir la sobrecarga HTTP en operaciones múltiples.
- **Webhooks**: Aprovechar los webhooks para recibir notificaciones en tiempo real sobre cambios en el estado de los anuncios o envíos de formularios de clientes potenciales, lo que reduce la necesidad de sondeo constante.
- **Diseño Modular**: Estructurar la base de código para separar las preocupaciones (por ejemplo, autenticación, creación de objetos, manejo de errores) para facilitar el mantenimiento.

## Conclusión

La API de Marketing de Facebook es una herramienta poderosa pero compleja para la gestión programática de anuncios. La comprensión de la naturaleza jerárquica de los objetos publicitarios —Campañas, Conjuntos de Anuncios, Anuncios y Creatividades— y el papel específico de cada campo dentro de estos objetos es fundamental para una integración exitosa. Aspectos críticos como la autenticación segura, el versionado de la API y el manejo robusto de errores son pilares para construir sistemas fiables y escalables.

Además, la API ofrece características especializadas como la gestión de anuncios de video, las capacidades de Advantage+ y la integración de formularios de clientes potenciales. Estas funciones requieren un enfoque cuidadoso en el diseño de la integración, incluyendo el manejo de procesos asíncronos para la carga de videos y la gestión del ciclo de vida de los formularios de clientes potenciales. La capacidad de Meta para optimizar dinámicamente las creatividades a través de la inteligencia artificial, así como la importancia de alinear los objetivos de optimización con los eventos de facturación, subraya la necesidad de una comprensión profunda de la lógica interna de la plataforma.

Para una optimización continua, se recomienda explorar temas avanzados como las conversiones personalizadas, las conversiones offline y las capacidades de informes avanzadas. La evolución constante de la API de Meta exige un aprendizaje continuo y una adaptación proactiva para mantener la eficacia de las estrategias publicitarias programáticas.

## Apéndices

### Glosario de Términos Clave de la API

- **ID de Cuenta Publicitaria (Ad Account ID)**: Identificador único de una cuenta publicitaria en Meta, prefijado con act_.
- **Token de Acceso (Access Token)**: Credencial de seguridad necesaria para autenticar las solicitudes a la API.
- **Especificación de la Historia del Objeto (Object Story Spec)**: Objeto JSON que define el contenido principal de una creatividad de anuncio (imagen, video, texto).
- **Especificación de Segmentación (Targeting Spec)**: Objeto JSON que define los parámetros de audiencia para un conjunto de anuncios.
- **CBO (Campaign Budget Optimization)**: Optimización del presupuesto a nivel de campaña, donde Meta distribuye el presupuesto entre los conjuntos de anuncios.
- **Creatividad Dinámica (Dynamic Creative)**: Función que permite a Meta generar automáticamente múltiples variaciones de anuncios a partir de diferentes activos.
- **Formulario de Clientes Potenciales (Lead Form / Instant Form)**: Formulario integrado en las plataformas de Meta para la recopilación de información de usuarios.
- **Advantage+ Shopping Campaigns (ASC)**: Solución que utiliza automatización e IA para optimizar campañas de comercio electrónico y minoristas.
- **Advantage+ Catalog Ads**: Permite promocionar elementos relevantes de un catálogo completo en cualquier dispositivo, mostrando anuncios para miles de artículos a la audiencia correcta y automatizando el proceso.
- **Dynamic Media**: Característica de Advantage+ Catalog Ads que permite entregar activos de video de tu catálogo en tus anuncios.

### Referencias a la Documentación Oficial de Meta para Desarrolladores

- **Marketing API Overview**: https://developers.facebook.com/docs/marketing-api/overview
- **Campaigns**: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
- **Ad Sets**: https://developers.facebook.com/docs/marketing-api/reference/ad-set
- **Ad Creatives**: https://developers.facebook.com/docs/marketing-api/reference/ad-creative
- **Ads**: https://developers.facebook.com/docs/marketing-api/reference/ad
- **Video Uploads**: https://developers.facebook.com/docs/marketing-api/guides/video-uploads
- **Lead Ads**: https://developers.facebook.com/docs/marketing-api/guides/lead-ads
- **Advantage+ Creative**: https://developers.facebook.com/docs/marketing-api/creative/advantage-creative/
- **Advantage+ Shopping Campaigns**: https://developers.facebook.com/docs/marketing-api/advantage-shopping-campaigns/
- **Advantage+ Catalog Ads**: https://developers.facebook.com/docs/marketing-api/advantage-catalog-ads/
- **Dynamic Media (Advantage+ Catalog Ads)**: https://developers.facebook.com/docs/marketing-api/advantage-catalog-ads/dynamic-media/
- **Asset Feed Spec**: https://developers.facebook.com/docs/marketing-api/ad-creative/asset-feed-spec/
- **Dynamic Creative (Asset Feed Spec)**: https://developers.facebook.com/docs/marketing-api/ad-creative/asset-feed-spec/dynamic-creative/ 