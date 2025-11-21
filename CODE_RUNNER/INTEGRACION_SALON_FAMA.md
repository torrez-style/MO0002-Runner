# Integración del Salón de la Fama con Usuarios

## Estado Actual

Se ha implementado:
- **salon_de_la_fama.py**: Módulo completo con funciones para ranking, puntuaciones por usuario y estadísticas
- **Importación en menu.py**: Se importó la clase SalonDeLaFama en MenuPrincipal
- **Inicialización**: Se agregaron los atributos `self.salon`, `self.mostrar_salon` y `self.usuario_actual`

## Pasos para Completar la Integración

### 1. Agregar Visualización en menu.py

En el método `dibujar()`, agregar:

```python
if self.mostrar_salon:
    self._dibujar_salon_fama()
elif self.en_subadministracion:
    # ... código existente
```

### 2. Agregar Método _dibujar_salon_fama()

```python
def _dibujar_salon_fama(self):
    """Muestra el ranking global del salón de la fama."""
    fondo = pygame.Surface((700, 450))
    fondo.fill((42, 42, 52))
    rect = fondo.get_rect()
    rect.center = (self.vista.ancho//2, self.vista.alto//2)
    self.vista.pantalla.blit(fondo, rect)
    
    fuente_titulo = pygame.font.SysFont(None, 40)
    fuente_texto = pygame.font.SysFont(None, 28)
    
    titulo = fuente_titulo.render("SALÓN DE LA FAMA", True, (255, 215, 0))
    self.vista.pantalla.blit(titulo, (rect.left+150, rect.top+20))
    
    ranking = self.salon.obtener_ranking_global(10)
    
    y_pos = rect.top + 70
    if ranking:
        for idx, entrada in enumerate(ranking, 1):
            texto = f"{idx}. {entrada['usuario']} - {entrada['puntuacion']} pts"
            surf = fuente_texto.render(texto, True, (200, 255, 200))
            self.vista.pantalla.blit(surf, (rect.left+30, y_pos))
            y_pos += 30
    else:
        sin_datos = fuente_texto.render("Sin datos aún", True, (200, 200, 200))
        self.vista.pantalla.blit(sin_datos, (rect.left+30, y_pos))
    
    instruccion = fuente_texto.render("ENTER: Volver", True, (180, 180, 180))
    self.vista.pantalla.blit(instruccion, (rect.left+30, rect.bottom-40))
```

### 3. Agregar Manejo de Eventos en manejar_eventos()

Agregar en el bloque cuando NO está en input_activo:

```python
if self.mostrar_salon:
    if evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
        self.mostrar_salon = False
    return
```

### 4. Conectar "SALÓN DE LA FAMA" en el Menú

En `manejar_eventos()`, donde se procesa la selección del menú:

```python
elif opcion == "SALÓN DE LA FAMA":
    self.mostrar_salon = True
```

### 5. Integrar en juego.py

Al terminar una partida exitosamente, registrar la puntuación:

```python
from salon_de_la_fama import SalonDeLaFama

# En la clase del juego, agregar:
self.salon = SalonDeLaFama()

# Cuando el jugador gana:
salon.registrar_puntuacion(
    usuario=self.usuario_actual,  # Necesitas pasar el usuario
    puntuacion=self.puntuacion,
    nivel=self.nivel_actual,
    nombre_laberinto=self.laberinto_actual
)
```

## Estructura de Datos

**puntuaciones.json:**
```json
{
  "USUARIO1": [
    {
      "puntuacion": 1500,
      "fecha": "2025-11-20 19:30:45",
      "nivel": 3,
      "laberinto": "nivel_facil.json"
    }
  ],
  "USUARIO2": [ ... ]
}
```

## Métodos Disponibles en SalonDeLaFama

- `registrar_puntuacion(usuario, puntuacion, nivel, nombre_laberinto)`
- `obtener_mejores_puntuaciones(usuario, limite=10)`: Top 10 del usuario
- `obtener_ranking_global(limite=10)`: Top 10 global
- `obtener_estadisticas_usuario(usuario)`: Estadísticas completas
- `eliminar_usuario(usuario)`: Borra puntuaciones del usuario
- `reiniciar_salon_completo()`: Limpia todo el ranking

## Próximos Pasos

1. Completa la integración visual en menu.py
2. Conecta juego.py para registrar puntuaciones
3. Prueba el flujo completo: crear usuario → jugar → ver ranking
