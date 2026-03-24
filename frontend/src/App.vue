<script setup lang="ts">
import { computed, ref } from 'vue'

import Navbar from './components/Navbar.vue'
import Inicio from './components/Inicio.vue'
import Dashboard from './components/Dashboards.vue'
import Reportes from './components/Reportes.vue'
import Configuracion from './components/Configuracion.vue'

type ViewKey = 'inicio' | 'dashboard' | 'reportes' | 'configuracion'

const currentView = ref<ViewKey>('inicio')

const views = {
  inicio: Inicio,
  dashboard: Dashboard,
  reportes: Reportes,
  configuracion: Configuracion,
}

const activeComponent = computed(() => views[currentView.value])

const handleNavigate = (view: ViewKey) => {
  currentView.value = view
}

</script>

<template>
  <header>
    <Navbar :active-view="currentView" @navigate="handleNavigate" />
  </header>
  <main>
    <component :is="activeComponent" />
  </main>
</template>

<style scoped>

</style>
