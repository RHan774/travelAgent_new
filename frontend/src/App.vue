<template>
  <div id="app">
    <a-layout class="main-layout">
      <a-layout-header class="app-header">
        <div class="header-content">
          <div class="logo-wrapper">
            <span class="logo-icon">✈️</span>
            <span class="logo-text">HelloAgents智能旅行助手</span>
          </div>
        </div>
      </a-layout-header>
      <a-layout-content class="app-content">
        <router-view />
      </a-layout-content>
      <a-layout-footer class="app-footer">
        <div class="footer-content">
          <span class="footer-text">HelloAgents智能旅行助手 ©2025</span>
          <span class="footer-divider">|</span>
          <span class="footer-sub">基于HelloAgents框架</span>
        </div>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif;
  height: 100%;
}

.main-layout {
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f4ff 0%, #e8eefc 100%);
}

.app-header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 0;
  height: 72px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 100;
}

.app-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}

.header-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 36px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

.logo-text {
  color: #ffffff;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #ffffff 0%, #a8d8ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-content {
  padding: 0;
  min-height: calc(100vh - 72px - 64px);
}

.app-footer {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.footer-text {
  font-weight: 500;
}

.footer-divider {
  opacity: 0.4;
}

.footer-sub {
  opacity: 0.7;
}
</style>

