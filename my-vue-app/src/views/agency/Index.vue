<template>
  <div class="agency-dashboard">
    <!-- 顶部导航栏 -->
    <header class="dashboard-header">
      <h1>旅行社管理系统</h1>
      <div class="user-info">
        <span>{{ username }}</span>
        <button @click="logout" class="logout-btn">退出登录</button>
      </div>
    </header>
    
    <div class="dashboard-layout">
      <!-- 侧边菜单 -->
      <div class="sidebar">
        <h2>功能菜单</h2>
        <nav>
          <a href="/agency/routes">线路管理</a>
          <a href="/agency/tourists">游客管理</a>
          <a href="/agency/itineraries">行程管理</a>
        </nav>
      </div>
      
      <!-- 主内容区域 -->
      <div class="main-content">
        <div class="welcome-panel">
          <h2>欢迎使用旅行社管理系统</h2>
          <p>请从左侧菜单选择要使用的功能</p>
          <div class="quick-stats">
            <div class="stat-card">
              <h3>线路数量</h3>
              <div class="stat-value">12</div>
            </div>
            <div class="stat-card">
              <h3>当前游客</h3>
              <div class="stat-value">45</div>
            </div>
            <div class="stat-card">
              <h3>进行中行程</h3>
              <div class="stat-value">8</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgencyIndex',
  data() {
    return {
      username: localStorage.getItem('username') || '旅行社管理员'
    }
  },
  methods: {
    logout() {
      // 清除登录状态
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      localStorage.removeItem('username');
      
      // 跳转到登录页
      window.location.href = '/login';
    }
  }
}
</script>

<style scoped>
.agency-dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #1976D2;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 15px;
}

.logout-btn {
  padding: 5px 10px;
  background-color: rgba(255,255,255,0.2);
  border: 1px solid white;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.dashboard-layout {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 220px;
  background-color: #263238;
  color: white;
  padding: 20px 0;
}

.sidebar h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 18px;
  padding: 0 20px;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
}

.sidebar a {
  color: white;
  padding: 12px 20px;
  text-decoration: none;
  transition: background-color 0.3s;
  border-left: 4px solid transparent;
}

.sidebar a:hover {
  background-color: #37474F;
}

.sidebar a.active {
  background-color: #37474F;
  border-left-color: #1976D2;
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f5f5;
  overflow-y: auto;
}

.welcome-panel {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: center;
}

.welcome-panel h2 {
  color: #1976D2;
  margin-top: 0;
  margin-bottom: 15px;
}

.quick-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.stat-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  width: 30%;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stat-card h3 {
  margin-top: 0;
  color: #555;
  font-size: 16px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #1976D2;
  margin-top: 10px;
}
</style>