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

## EDITAR EL PERFIL

- IDEA 1 - Podriem fer que pos un POP up

- IDEA 2 - Podriem fer que la part superior canvi nomes
[![Image from Gyazo](https://i.gyazo.com/ea4834df9491d7b2db80da7289a9c71e.png)](https://gyazo.com/ea4834df9491d7b2db80da7289a9c71e)

## POSTS

- posar fa nosequants minuts...


## EDITAR I ELIMINAR POTST

Si estem al nostre perfil, mostrar 2 botons a costat de cada post.

s'obrirá pop up per editar on es podra modificar el contingut, acceptar o cancelar


s'obrira pop up per eliminar dient, si esta segur que el vol eliminar.






# SERGI FIco les idees noves que tinc.
## Sobre el home: 
  - El side bar de la esquerra, fer ho mes com si fos botons
  - marcar en quin lloc del side bar estar. - DONE
  - ficar un fons diferent al side bar (crec que quedarà millor).
  -
  - el enter a text buscar una terminal per ficar de fons.
  - he vist que si esta el text buit i li dones a enviar no tenim la excepció contorlada - DONE

  - els post a lo millor modificaria el text perq ue no es vegues tant a la esquerra.

Perfil:
Mirar el sin titulo.png