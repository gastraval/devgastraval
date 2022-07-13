.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License: LGPL-3

=============
Mrp Extension
=============

Este módulo permite:

    * Añadir en la vista kanban de órdenes de producción la 'fecha planificada' (De inicio).
    * En órdenes de trabajo el botón "Marcar como hecho y cerrar op" cierra la órden de trabajo y también la de producción (si no quedan trabajos pendientes).
    * En las órdenes de trabajo se puede fabricar más y menos cantidad de la planificada y consumir misma cantidad planificada de componentes o recalcularlos dependiendo de la casilla "Activar mermas".
    * Se añade en la vista tablet un botón para imprimir etiquetas. Estas etiquetas se van a
      imprimir según el producto la tenga asignada. Si el producto tiene asignada una
      etiqueta de tipo caja, el botón imprimirá dicha etiqueta. En caso de no tener ninguna
      etiqueta, se muestra un mensaje de error.
    * Se añade unos checkbox de "Imprimir etiqueta pallet" en centros de producción y productos.
      Si las dos están activadas, al registrar producción en este producto se imprimirá la etiqueta "CARTEL SSCC PAQUETE"

Contributors
------------

* Pablo Álvarez <pablo.alvarez@studio73.es>


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/Studio73/gastraval-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Maintainer
----------

.. image:: https://www.studio73.es/logo.png
   :alt: Studio73
   :target: https://www.studio73.es/

This module is maintained by Studio73.
