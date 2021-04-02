- Fer un diseny minimament xulu!

- Heroku publish

TO DO

### HOME

Mirat el que he fet i apunta cosetes que es podrien retocar o algo que trobis a faltar...

- FER LA INTERACCIÓ DEL MENÚ

  - Quan es fa click et porti al lloc on toca

  ! Es pot fer amb un javascript - Exemple a sidebar.js

  ```javascript
  $(document).ready(function () {
    $(".sidebar__menu__option").click(function () {
      window.location.replace("{% url 'home' %}");
    });
  });
  ```

  ---- De moment que nomes redireccioni al de veure perfil, tema veure els teus twits i seguidors ja veurem

- Modificar plantilles perque sigui dinamiquies, objectes de BD

- Modificar vista home ( views.py -> home) perque al context afageixi els usuaris que no seguiex qui s'ha logejat

### PERFIL

La meva idea es que el menú segueixi alla, pero que canvii tot el de la esquerra

[![Image from Gyazo](https://i.gyazo.com/3afbbe9526d0ae3d39cd9cd5becab481.png)](https://gyazo.com/3afbbe9526d0ae3d39cd9cd5becab481)

No se exactament com ferlo pero hauria de tenir un estil semblant al home




////////////////////
FIco les idees noves que tinc.
Sobre el home: 
  -El side bar de la esquerra, fer ho mes com si fos botons
  -marcar en quin lloc del side bar estar. - DONE
  -ficar un fons diferent al side bar (crec que quedarà millor).
  -
  - el enter a text buscar una terminal per ficar de fons.
  - he vist que si esta el text buit i li dones a enviar no tenim la excepció contorlada - DONE

  - els post a lo millor modificaria el text perq ue no es vegues tant a la esquerra.

Perfil:
Mirar el sin titulo.png