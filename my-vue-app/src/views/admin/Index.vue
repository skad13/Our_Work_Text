<template>
    <div class="admin-dashboard">
      <header class="dashboard-header">
        <h1>主管部门管理后台</h1>
        <div class="user-info">
          <span>{{ username }}</span>
          <button @click="logout" class="logout-btn">退出登录</button>
        </div>
      </header>
      
      <div class="dashboard-content">
        <div class="sidebar">
          <div class="menu-item" 
               v-for="(item, index) in menuItems" 
               :key="index"
               :class="{ active: currentSection === item.id }"
               @click="currentSection = item.id">
            <i class="icon">{{ item.icon }}</i>
            <span>{{ item.name }}</span>
          </div>
        </div>
        
        <div class="main-content">
          <!-- 概览面板 -->
          <div v-if="currentSection === 'overview'" class="section">
            <h2>系统概览</h2>
            <div class="stats-container">
              <div class="stat-card">
                <div class="stat-value">{{ stats.agencyCount }}</div>
                <div class="stat-label">旅行社</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ stats.guideCount }}</div>
                <div class="stat-label">导游</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ stats.touristCount }}</div>
                <div class="stat-label">游客</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ stats.activeTrips }}</div>
                <div class="stat-label">活跃行程</div>
              </div>
            </div>
            
            <h3>最近活动</h3>
            <div class="activity-list">
              <div class="activity-item" v-for="(activity, index) in recentActivities" :key="index">
                <div class="activity-icon">{{ activity.icon }}</div>
                <div class="activity-details">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-description">{{ activity.description }}</div>
                  <div class="activity-time">{{ activity.time }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 旅行社管理 -->
          <div v-if="currentSection === 'agencies'" class="section">
            <h2>旅行社管理</h2>
            <div class="table-actions">
              <input type="text" placeholder="搜索旅行社..." class="search-input">
              <button class="btn-add">添加旅行社</button>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>名称</th>
                  <th>许可证号</th>
                  <th>负责人</th>
                  <th>联系电话</th>
                  <th>状态</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(agency, index) in agencies" :key="index">
                  <td>{{ agency.id }}</td>
                  <td>{{ agency.name }}</td>
                  <td>{{ agency.licenseNumber }}</td>
                  <td>{{ agency.manager }}</td>
                  <td>{{ agency.contact }}</td>
                  <td>
                    <span class="status-badge" :class="agency.status">
                      {{ agency.statusText }}
                    </span>
                  </td>
                  <td>
                    <button class="btn-action">查看</button>
                    <button class="btn-action">编辑</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 导游管理 -->
          <div v-if="currentSection === 'guides'" class="section">
            <h2>导游管理</h2>
            <div class="filter-panel">
              <select class="filter-select">
                <option value="">全部状态</option>
                <option value="active">在职</option>
                <option value="inactive">离职</option>
                <option value="suspended">暂停执业</option>
              </select>
              <button class="btn-primary">筛选</button>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>姓名</th>
                  <th>导游证号</th>
                  <th>等级</th>
                  <th>工作年限</th>
                  <th>状态</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(guide, index) in guides" :key="index">
                  <td>{{ guide.id }}</td>
                  <td>{{ guide.name }}</td>
                  <td>{{ guide.licenseNumber }}</td>
                  <td>{{ guide.level }}</td>
                  <td>{{ guide.yearsOfExperience }}</td>
                  <td>
                    <span class="status-badge" :class="guide.status">
                      {{ guide.statusText }}
                    </span>
                  </td>
                  <td>
                    <button class="btn-action">查看</button>
                    <button class="btn-action">管理</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 系统设置 -->
          <div v-if="currentSection === 'settings'" class="section">
            <h2>系统设置</h2>
            <div class="settings-section">
              <h3>通知设置</h3>
              <div class="setting-item">
                <div class="setting-label">
                  <div class="setting-title">系统通知</div>
                  <div class="setting-description">向所有用户发送重要系统更新通知</div>
                </div>
                <div class="setting-control">
                  <label class="switch">
                    <input type="checkbox" checked>
                    <span class="slider"></span>
                  </label>
                </div>
              </div>
              
              <div class="setting-item">
                <div class="setting-label">
                  <div class="setting-title">紧急事件通知</div>
                  <div class="setting-description">自动向相关部门发送紧急情况报告</div>
                </div>
                <div class="setting-control">
                  <label class="switch">
                    <input type="checkbox" checked>
                    <span class="slider"></span>
                  </label>
                </div>
              </div>
              
              <h3>安全设置</h3>
              <div class="setting-item">
                <div class="setting-label">
                  <div class="setting-title">双因素认证</div>
                  <div class="setting-description">为管理员账户启用额外安全保护</div>
                </div>
                <div class="setting-control">
                  <label class="switch">
                    <input type="checkbox">
                    <span class="slider"></span>
                  </label>
                </div>
              </div>
              
              <div class="setting-item">
                <div class="setting-label">
                  <div class="setting-title">密码过期策略</div>
                  <div class="setting-description">设置管理员密码有效期</div>
                </div>
                <div class="setting-control">
                  <select class="settings-select">
                    <option value="30">30天</option>
                    <option value="60">60天</option>
                    <option value="90" selected>90天</option>
                    <option value="never">永不过期</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="settings-actions">
              <button class="btn-primary">保存设置</button>
              <button class="btn-secondary">恢复默认</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        username: localStorage.getItem('username') || '管理员',
        currentSection: 'overview',
        menuItems: [
          { id: 'overview', name: '系统概览', icon: '📊' },
          { id: 'agencies', name: '旅行社管理', icon: '🏢' },
          { id: 'guides', name: '导游管理', icon: '👤' },
          { id: 'tourists', name: '游客管理', icon: '👥' },
          { id: 'reports', name: '报告分析', icon: '📈' },
          { id: 'settings', name: '系统设置', icon: '⚙️' }
        ],
        stats: {
          agencyCount: 48,
          guideCount: 215,
          touristCount: 3842,
          activeTrips: 127
        },
        recentActivities: [
          {
            icon: '🔔',
            title: '新旅行社注册',
            description: '北京假日旅行社提交了注册申请',
            time: '2小时前'
          },
          {
            icon: '✅',
            title: '导游证书审核',
            description: '已完成5位导游的证书年检',
            time: '昨天'
          },
          {
            icon: '⚠️',
            title: '游客投诉处理',
            description: '收到关于"西湖三日游"的服务投诉',
            time: '2天前'
          }
        ],
        agencies: [
          {
            id: 'A001',
            name: '阳光国际旅行社',
            licenseNumber: 'L-BJ00123',
            manager: '王经理',
            contact: '010-12345678',
            status: 'active',
            statusText: '正常'
          },
          {
            id: 'A002',
            name: '环球旅行社',
            licenseNumber: 'L-BJ00456',
            manager: '李经理',
            contact: '010-87654321',
            status: 'review',
            statusText: '审核中'
          },
          {
            id: 'A003',
            name: '快乐旅游',
            licenseNumber: 'L-BJ00789',
            manager: '张经理',
            contact: '010-45678901',
            status: 'suspended',
            statusText: '已暂停'
          }
        ],
        guides: [
          {
            id: 'G001',
            name: '张小明',
            licenseNumber: 'GD12345',
            level: '高级导游',
            yearsOfExperience: 8,
            status: 'active',
            statusText: '在职'
          },
          {
            id: 'G002',
            name: '李华',
            licenseNumber: 'GD23456',
            level: '中级导游',
            yearsOfExperience: 5,
            status: 'active',
            statusText: '在职'
          },
          {
            id: 'G003',
            name: '王强',
            licenseNumber: 'GD34567',
            level: '高级导游',
            yearsOfExperience: 10,
            status: 'inactive',
            statusText: '离职'
          }
        ]
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
  .admin-dashboard {
    min-height: 100vh;
    background-color: #f5f5f5;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background-color: #3f51b5;
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
    width: 220px;
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
  
  .menu-item:hover, .menu-item.active {
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
  
  h3 {
    margin: 20px 0 15px;
    color: #2c3e50;
  }
  
  .stats-container {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .stat-card {
    flex: 1;
    background-color: #f8f8f8;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  
  .stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #3f51b5;
    margin-bottom: 5px;
  }
  
  .stat-label {
    color: #666;
  }
  
  .activity-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .activity-item {
    display: flex;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    align-items: center;
  }
  
  .activity-icon {
    margin-right: 15px;
    font-size: 24px;
  }
  
  .activity-details {
    flex: 1;
  }
  
  .activity-title {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .activity-time {
    color: #999;
    font-size: 12px;
    margin-top: 5px;
  }
  
  .table-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .search-input {
    padding: 8px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 300px;
  }
  
  .btn-add {
    padding: 8px 15px;
    background-color: #3f51b5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .data-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  .data-table th, .data-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  .data-table th {
    background-color: #f2f2f2;
    color: #333;
  }
  
  .status-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
  }
  
  .status-badge.active {
    background-color: #e8f5e9;
    color: #4CAF50;
  }
  
  .status-badge.review {
    background-color: #fff8e1;
    color: #ff9800;
  }
  
  .status-badge.suspended, .status-badge.inactive {
    background-color: #ffebee;
    color: #f44336;
  }
  
  .btn-action {
    padding: 5px 10px;
    margin-right: 5px;
    background-color: #e0e0e0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .filter-panel {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .filter-select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 200px;
  }
  
  .btn-primary {
    padding: 8px 15px;
    background-color: #3f51b5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .settings-section {
    margin-bottom: 30px;
  }
  
  .setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
  }
  
  .setting-title {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .setting-description {
    color: #666;
    font-size: 14px;
  }
  
  .switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
  }
  
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;
  }
  
  .slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }
  
  input:checked + .slider {
    background-color: #3f51b5;
  }
  
  input:checked + .slider:before {
    transform: translateX(26px);
  }
  
  .settings-select {
    padding: 8px;
    width: 120px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .settings-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  .btn-secondary {
    padding: 8px 15px;
    background-color: #e0e0e0;
    color: #333;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>