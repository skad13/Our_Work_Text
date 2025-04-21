<template>
  <div class="tourist-dashboard">
    <header class="dashboard-header">
      <h1>旅游体验中心</h1>
      <div class="user-info">
        <span>{{ username }}</span>
        <button @click="logout" class="logout-btn">退出登录</button>
      </div>
    </header>
    
    <div class="dashboard-content">
      <div class="main-panel">
        <div class="welcome-banner">
          <h2>欢迎使用旅游体验中心</h2>
          <p>在这里您可以浏览旅游线路、预订行程、查看游记等</p>
        </div>
        
        <div class="section-title">推荐线路</div>
        <div class="route-cards">
          <div class="route-card" v-for="(route, index) in recommendedRoutes" :key="index">
            <div class="route-image" :style="`background-image: url(${route.imageUrl})`">
              <div class="route-price">¥{{ route.price }}</div>
            </div>
            <div class="route-info">
              <h3>{{ route.name }}</h3>
              <div class="route-tags">
                <span class="tag" v-for="(tag, i) in route.tags" :key="i">{{ tag }}</span>
              </div>
              <p>{{ route.description }}</p>
              <div class="route-footer">
                <div class="route-duration">{{ route.duration }}天</div>
                <button class="btn-book" @click="bookRoute(route)">立即预订</button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="section-title">我的行程</div>
        <div class="my-trips" v-if="myTrips.length > 0">
          <div class="trip" v-for="(trip, index) in myTrips" :key="index">
            <div class="trip-status" :class="trip.status">{{ trip.statusText }}</div>
            <div class="trip-info">
              <h3>{{ trip.name }}</h3>
              <div class="trip-date">{{ trip.date }}</div>
              <div class="trip-participants">{{ trip.participants }}人</div>
            </div>
            <div class="trip-actions">
              <button class="btn-trip-detail">查看详情</button>
              <button class="btn-trip-cancel" v-if="trip.status === 'booked'">取消行程</button>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p>您还没有预订任何行程</p>
          <button class="btn-browse">浏览线路</button>
        </div>
      </div>
      
      <div class="sidebar">
        <div class="user-profile">
          <div class="avatar-placeholder">游</div>
          <h3>{{ username }}</h3>
          <p>会员等级: {{ userInfo.level }}</p>
        </div>
        
        <div class="quick-links">
          <h3>快速链接</h3>
          <a href="#" class="link">我的订单</a>
          <a href="#" class="link">我的收藏</a>
          <a href="#" class="link">旅行计划</a>
          <a href="#" class="link">我的游记</a>
        </div>
        
        <div class="travel-tips">
          <h3>旅行小贴士</h3>
          <div class="tip">
            <h4>行李打包建议</h4>
            <p>根据目的地气候准备合适衣物，记得带上常用药品和充电器。</p>
          </div>
          <div class="tip">
            <h4>安全提示</h4>
            <p>旅行时保管好贵重物品，保持通讯畅通。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TouristDashboard',
  data() {
    return {
      username: localStorage.getItem('username') || '游客用户',
      userInfo: {
        level: '白银会员'
      },
      recommendedRoutes: [
        {
          id: 1,
          name: '北京故宫、长城三日游',
          imageUrl: 'https://via.placeholder.com/300x200?text=北京',
          price: 1299,
          duration: 3,
          tags: ['文化', '历史'],
          description: '游览故宫、长城等北京著名景点，体验传统文化魅力。'
        },
        {
          id: 2,
          name: '张家界玻璃桥、天门山五日游',
          imageUrl: 'https://via.placeholder.com/300x200?text=张家界',
          price: 2499,
          duration: 5,
          tags: ['自然', '冒险'],
          description: '挑战世界最长玻璃桥，体验云中漫步的刺激，欣赏壮丽山景。'
        },
        {
          id: 3,
          name: '三亚蜈支洲岛、亚龙湾六日游',
          imageUrl: 'https://via.placeholder.com/300x200?text=三亚',
          price: 3699,
          duration: 6,
          tags: ['海滩', '度假'],
          description: '阳光沙滩，水上活动，尽享热带海岛风情。'
        }
      ],
      myTrips: [
        {
          id: 101,
          name: '杭州西湖游',
          date: '2023-09-15 至 2023-09-17',
          participants: 2,
          status: 'completed',
          statusText: '已完成'
        },
        {
          id: 102,
          name: '黄山三日游',
          date: '2023-12-05 至 2023-12-08',
          participants: 4,
          status: 'booked',
          statusText: '已预订'
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
    },
    bookRoute(route) {
      alert(`您已选择"${route.name}"，即将进入预订流程！`);
    }
  }
}
</script>

<style scoped>
.tourist-dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #2196F3;
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
  padding: 20px;
  gap: 20px;
}

.main-panel {
  flex: 3;
}

.sidebar {
  flex: 1;
  min-width: 250px;
}

.welcome-banner {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.welcome-banner h2 {
  color: #2196F3;
  margin-top: 0;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin: 20px 0 10px;
  color: #333;
}

.route-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.route-card {
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.route-image {
  height: 160px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.route-price {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background-color: rgba(0,0,0,0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
}

.route-info {
  padding: 15px;
}

.route-tags {
  margin: 10px 0;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  background-color: #e9f5ff;
  color: #2196F3;
  border-radius: 4px;
  margin-right: 5px;
  font-size: 12px;
}

.route-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.route-duration {
  color: #666;
}

.btn-book {
  padding: 6px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.my-trips {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.trip {
  display: flex;
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.trip-status {
  width: 80px;
  text-align: center;
  padding: 5px 0;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 15px;
  height: fit-content;
}

.trip-status.completed {
  background-color: #e0f2f1;
  color: #009688;
}

.trip-status.booked {
  background-color: #fff8e1;
  color: #ff9800;
}

.trip-info {
  flex: 1;
}

.trip-info h3 {
  margin: 0 0 10px;
}

.trip-date, .trip-participants {
  color: #666;
  font-size: 14px;
  margin-bottom: 5px;
}

.trip-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
}

.btn-trip-detail, .btn-trip-cancel {
  padding: 5px 10px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.btn-trip-detail {
  background-color: #e0e0e0;
  color: #333;
}

.btn-trip-cancel {
  background-color: #ffebee;
  color: #f44336;
}

.user-profile, .quick-links, .travel-tips {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.user-profile {
  text-align: center;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  background-color: #2196F3;
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  margin: 0 auto 10px;
}

.quick-links h3, .travel-tips h3 {
  margin-top: 0;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.link {
  display: block;
  padding: 8px 0;
  color: #2196F3;
  text-decoration: none;
}

.link:hover {
  color: #0b7dda;
}

.tip {
  margin-bottom: 15px;
}

.tip h4 {
  margin: 0 0 5px;
}

.tip p {
  color: #666;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 30px;
  background-color: white;
  border-radius: 8px;
}

.btn-browse {
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}
</style>