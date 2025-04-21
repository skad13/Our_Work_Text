<template>
  <div class="guide-dashboard">
    <header class="dashboard-header">
      <h1>导游工作台</h1>
      <div class="user-info">
        <span>{{ username }}</span>
        <button @click="logout" class="logout-btn">退出登录</button>
      </div>
    </header>
    
    <div class="dashboard-content">
      <div class="sidebar">
        <div class="menu-item" @click="activeSection = 'upcoming'">
          <i class="icon">📅</i>
          <span>即将开始的行程</span>
        </div>
        <div class="menu-item" @click="activeSection = 'tourists'">
          <i class="icon">👥</i>
          <span>游客信息</span>
        </div>
        <div class="menu-item" @click="activeSection = 'history'">
          <i class="icon">📝</i>
          <span>历史行程</span>
        </div>
        <div class="menu-item" @click="activeSection = 'profile'">
          <i class="icon">👤</i>
          <span>个人资料</span>
        </div>
      </div>
      
      <div class="main-content">
        <!-- 即将开始的行程 -->
        <div v-if="activeSection === 'upcoming'" class="section">
          <h2>即将开始的行程</h2>
          <div class="trip-card">
            <div class="trip-title">北京三日游</div>
            <div class="trip-details">
              <div><strong>日期：</strong>2023-07-15 至 2023-07-18</div>
              <div><strong>游客数量：</strong>20人</div>
              <div><strong>集合地点：</strong>北京首都国际机场T2航站楼</div>
              <div><strong>集合时间：</strong>上午9:00</div>
            </div>
            <div class="trip-actions">
              <button class="btn-primary">查看详情</button>
              <button class="btn-secondary">下载行程表</button>
            </div>
          </div>
        </div>
        
        <!-- 游客信息 -->
        <div v-if="activeSection === 'tourists'" class="section">
          <h2>游客信息</h2>
          <p>当前带团游客信息列表</p>
          <table class="tourists-table">
            <thead>
              <tr>
                <th>姓名</th>
                <th>性别</th>
                <th>年龄</th>
                <th>联系方式</th>
                <th>备注</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(tourist, index) in tourists" :key="index">
                <td>{{ tourist.name }}</td>
                <td>{{ tourist.gender }}</td>
                <td>{{ tourist.age }}</td>
                <td>{{ tourist.contact }}</td>
                <td>{{ tourist.notes }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 历史行程 -->
        <div v-if="activeSection === 'history'" class="section">
          <h2>历史行程</h2>
          <p>您之前已完成的行程列表</p>
          <div class="history-list">
            <div class="history-item">
              <div class="history-date">2023-06-10 至 2023-06-15</div>
              <div class="history-title">海南五日游</div>
              <div class="history-tourists">带团人数：18人</div>
            </div>
            <div class="history-item">
              <div class="history-date">2023-05-01 至 2023-05-03</div>
              <div class="history-title">杭州西湖三日游</div>
              <div class="history-tourists">带团人数：22人</div>
            </div>
          </div>
        </div>
        
        <!-- 个人资料 -->
        <div v-if="activeSection === 'profile'" class="section">
          <h2>个人资料</h2>
          <div class="profile-card">
            <div class="profile-avatar">
              <div class="avatar-placeholder">导</div>
            </div>
            <div class="profile-details">
              <div class="profile-item">
                <label>姓名:</label>
                <span>{{ guideInfo.name }}</span>
              </div>
              <div class="profile-item">
                <label>导游证号:</label>
                <span>{{ guideInfo.licenseNumber }}</span>
              </div>
              <div class="profile-item">
                <label>工作年限:</label>
                <span>{{ guideInfo.yearsOfExperience }}年</span>
              </div>
              <div class="profile-item">
                <label>语言能力:</label>
                <span>{{ guideInfo.languages.join(", ") }}</span>
              </div>
              <div class="profile-item">
                <label>擅长地区:</label>
                <span>{{ guideInfo.specialties.join(", ") }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GuideDashboard',
  data() {
    return {
      username: localStorage.getItem('username') || '导游用户',
      activeSection: 'upcoming',
      tourists: [
        { name: '张三', gender: '男', age: 35, contact: '13800138000', notes: '素食' },
        { name: '李四', gender: '女', age: 28, contact: '13900139000', notes: '有老人陪同' },
        { name: '王五', gender: '男', age: 45, contact: '13700137000', notes: '无' },
        { name: '赵六', gender: '女', age: 30, contact: '13600136000', notes: '带一小孩' }
      ],
      guideInfo: {
        name: '李导游',
        licenseNumber: 'GD12345678',
        yearsOfExperience: 5,
        languages: ['中文', '英语', '日语'],
        specialties: ['北京', '西安', '成都']
      }
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      localStorage.removeItem('username');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.guide-dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #34495e;
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
  background-color: transparent;
  border: 1px solid white;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.dashboard-content {
  display: flex;
  height: calc(100vh - 60px);
}

.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px 0;
}

.menu-item {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu-item:hover {
  background-color: #34495e;
}

.icon {
  margin-right: 10px;
  font-size: 18px;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.trip-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.trip-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #2c3e50;
}

.trip-details {
  margin-bottom: 15px;
}

.trip-details div {
  margin-bottom: 5px;
}

.trip-actions {
  display: flex;
  gap: 10px;
}

.btn-primary, .btn-secondary {
  padding: 8px 15px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-secondary {
  background-color: #e9e9e9;
  color: #333;
}

.tourists-table {
  width: 100%;
  border-collapse: collapse;
}

.tourists-table th, .tourists-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.tourists-table th {
  background-color: #f2f2f2;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.history-date {
  color: #666;
  font-size: 14px;
}

.history-title {
  font-weight: bold;
  font-size: 16px;
  margin: 5px 0;
}

.profile-card {
  display: flex;
  gap: 20px;
}

.profile-avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  background-color: #3498db;
  color: white;
  border-radius: 50%;
  font-size: 40px;
}

.avatar-placeholder {
  font-weight: bold;
}

.profile-details {
  flex: 1;
}

.profile-item {
  margin-bottom: 10px;
}

.profile-item label {
  font-weight: bold;
  display: inline-block;
  width: 100px;
}
</style>