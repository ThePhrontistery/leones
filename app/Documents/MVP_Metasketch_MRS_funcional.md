Metasketch

# Introducción

Metasketch es una herramienta colaborativa para transformar ideas, requisitos y documentación en diseños funcionales vivos.

# 🧩 Funcionalidades principales

La aplicación se compone de varios paneles que se mostrarán en español. A continuación, se define cada una de las funcionalidades para cada panel:

Login de usuarios

Panel de carga de documentos

Árbol de contenidos (índices/enlaces)

Análisis Funcional. Editor Markdown con vista previa

Chat lateral con IA

Botón de exportación (Word/PDF)

### Login del usuario

En esta pantalla se permitirá al usuario introducir el usuario y el password para hacer login de la aplicación, a continuación, se mostrará la pantalla con todos los proyectos del sistema: documentos de entrada y funcional generado (si existe).

### Panel de carga de documentos

Todos los documentos se mostrarán en modo árbol (expandir/contraer). Desde la raíz del árbol es un proyecto del cual colgarán los distintos documentos que pertenecen a dicho proyecto.

Este panel contendrá las siguientes funcionalidades a nivel de Proyecto:

Crear Proyecto:  Se mostrará un botón de Crear Proyecto, que permite al usuario crear un proyecto desde donde colgarán los distintos documentos que servirán para generar el documento funcional.

Abrir Proyecto:  Una vez que el usuario seleccione el proyecto desde el árbol sobre el cual va a trabajar, se bloqueará el proyecto y sus documentos para ese usuario y ningún otro usuario podrá seleccionar el proyecto ya que solo le mostrará un mensaje “Proyecto bloqueado por usuario XXXX”.

Cargar documento: aparecerá un botón Upload habilitado el cual permitirá al usuario cargar un documento desde su local y asociarlo al proyecto.

Al pulsar sobre un proyecto permitirá cargar documentos dentro de ese proyecto si no se ha generado aun un documento funcional base, además el usuario indicará el tipo de documento / categoría que se está subiendo mediante un desplegable.

El botón Upload se deshabilitará una vez generado el documento funcional base.

Borrar documento: Al pulsar sobre un documento cargado aparecerá un botón Borrar habilitado que permitirá borrar documentos si no se ha generado aun un documento funcional base

El botón Borrar se deshabilitará una vez generado el documento funcional base.

Generar funcional: Al pulsar sobre un proyecto aparecerá también un botón de “Generar funcional”, el cual generará un documento funcional de acuerdo con la plantilla y tomando como base todos los documentos asociados al proyecto, mediante un prompt definido para IA para estos fines.

La plantilla indicará la estructura del indice que debe contener el funcional y no será modificable.

Al generar el funcional debe actualizar el árbol de Contenido con el índice del documento y en el editor mostrar todo el documento, de forma similar a cómo funciona el modo de visualización de la tabla de contenidos de Word.

No se permitirá regeneración de funcional.

### Árbol de contenidos (índices/enlaces)

Contiene los elementos de índice del documento funcional, los cuales se podrán contraer y/o expandir. Si no hay ningún documento funcional, se mostrará en blanco tanto este como el del Editor.

Al generar el documento funcional este tendrá inicialmente los ítems de la plantilla. El usuario solo puede agregar ítems nuevos debajo de los ítems principales de la plantilla, estos se deben reflejar en este panel.

Cuando se selecciona uno de los elementos del índice, se debe mostrar en el panel de Editor, el contenido con un editor Markdown, todo el documento ubicado en el item seleccionado, pudiendo el usuario subir o bajar en su documento.

### Panel Editor. Editor Markdown con vista previa

La primera vez que ingresa el usuario se mostrará el documento completo, si se ha seleccionado un item en el árbol de contenidos, se visualizará el documento ubicado el item seleccionado.

Se editará con el Editor Markdown. El usuario dispondrá de los siguientes botones:

Botón de ayuda: mostrará una página con la sintaxis de Markdown.

Botón de Preview para visualizar el documento tal como queda.

Botón Guardar Cambios: Se habilitará el botón de Guardar Cambios cuando exista un funcional generado.Este permitirá guardar los cambios realizados por el usuario en el funcional.

### Panel Chat con IA

Permitirá que el usuario interactúe con la IA en modo Ask para le haga sugerencias de textos en su documento funcional. El usuario podrá trasladar la sugerencia al panel editor para que sea incluida en la generación del documento mediante copy-paste.

### Botón de exportación (Word/PDF)

Al pulsar en el botón “Exportar Funcional” (el documento cargado en memoria se implementará en el formato elegido).

