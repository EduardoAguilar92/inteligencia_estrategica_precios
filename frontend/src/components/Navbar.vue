<script setup lang="ts">
type ViewKey = 'inicio' | 'dashboard' | 'reportes' | 'configuracion'

const props = defineProps<{
  activeView: ViewKey
}>()

const emit = defineEmits<{
  (e: 'navigate', view: ViewKey): void
}>()

const onNavigate = (view: ViewKey) => {
  emit('navigate', view)
}
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Título a la izquierda -->
      <div class="logo">
        <img alt="Logo" class="logo-img" src="@/assets/2Logotipo Chapur-BCO.png" height="40" />
        INTELIGENCIA ESTRATÉGICA DE PRECIOS
      </div>

      <!-- Lista a la derecha -->
      <ul class="nav-links">
        <li>
          <a
            href="#"
            :class="['nav-item', { active: props.activeView === 'inicio' }]"
            @click.prevent="onNavigate('inicio')"
          >
            Inicio
          </a>
        </li>
        <li>
          <a
            href="#"
            :class="['nav-item', { active: props.activeView === 'dashboard' }]"
            @click.prevent="onNavigate('dashboard')"
          >
            Dashboard
          </a>
        </li>
        <li>
          <a
            href="#"
            :class="['nav-item', { active: props.activeView === 'reportes' }]"
            @click.prevent="onNavigate('reportes')"
          >
            Reportes
          </a>
        </li>
        <li>
          <a
            href="#"
            :class="['nav-item', { active: props.activeView === 'configuracion' }]"
            @click.prevent="onNavigate('configuracion')"
          >
            Configuración
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>


<style scoped>
.navbar {
  width: 100%;
  background-color: #c01823; /* Rojo Gran Chapur */
  color: white;
  padding: 1rem 0;
  font-family: sans-serif;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  /* CAMBIA ESTO: */
  width: 100%;           /* Ocupa todo el ancho disponible */
  max-width: 100%;       /* Elimina cualquier restricción de ancho máximo */
  padding: 0 10px;       /* Reduce el espacio lateral (ajusta el 10px a tu gusto) */
  box-sizing: border-box; /* Asegura que el padding no estire la barra */
}


.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  font-size: 1.2rem;
  letter-spacing: 1px;
}

.logo-img {
  display: block;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 25px;            /* Espacio entre los elementos de la lista */
  margin: 0;
  padding: 0;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: opacity 0.2s;
}

.nav-item:hover {
  opacity: 0.8;
}

.active {
  border-bottom: 2px solid white;
  padding-bottom: 5px;
}
</style>
