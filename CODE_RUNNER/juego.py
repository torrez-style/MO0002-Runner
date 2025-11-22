class ManejadorColisiones:
    def __init__(self, juego, administrador):
        self.juego = juego
        administrador.registrar(EventoColisionEnemigo, self)

    def notificar(self, evento):
        j = self.juego
        if j.potenciador_activo == "invulnerable":
            return
        # FIX: Usar evento.posicion_jugador, no evento.posicion
        if evento.posicion_jugador in [(e[0], e[1]) for e in j.enemigos]:
            if evento.posicion_jugador == (j.posicion_x, j.posicion_y):
                j.vidas -= 1
                if j.vidas > 0:
                    j.posicion_x, j.posicion_y = j._obtener_celda_libre_jugador()
                    j._recolocar_enemigos_si_vacio(j.niveles[j.nivel_actual])
                else:
                    j._cambiar_a_fin_de_juego()
