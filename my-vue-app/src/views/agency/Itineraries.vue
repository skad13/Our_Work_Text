<template>
  <div class="itineraries-container">
    <h2>行程管理</h2>
    <p>这里是旅行社行程管理界面的内容</p>
    <div class="itinerary-list">
      <div class="itinerary-item" v-for="itinerary in itineraries" :key="itinerary.id">
        <div class="itinerary-header">
          <h3>{{ itinerary.name }}</h3>
          <span :class="['status', itinerary.status === '进行中' ? 'active' : '']">
            {{ itinerary.status }}
          </span>
        </div>
        <div class="itinerary-details">
          <p><strong>日期:</strong> {{ itinerary.date }}</p>
          <p><strong>导游:</strong> {{ itinerary.guide }}</p>
          <p><strong>游客数:</strong> {{ itinerary.touristCount }}人</p>
          <p><strong>线路:</strong> {{ itinerary.route }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItinerariesView',
  data() {
    return {
      itineraries: [
        { 
          id: 201, 
          name: '北京三日游-5月团', 
          date: '2023-05-15 至 2023-05-18',
          guide: '刘导游',
          touristCount: 20,
          route: '北京三日游',
          status: '计划中'
        },
        { 
          id: 202, 
          name: '西安历史文化之旅-6月团', 
          date: '2023-06-05 至 2023-06-09',
          guide: '张导游',
          touristCount: 15,
          route: '西安历史文化之旅',
          status: '进行中'
        },
        { 
          id: 203, 
          name: '海南阳光沙滩游-7月团', 
          date: '2023-07-10 至 2023-07-15',
          guide: '王导游',
          touristCount: 25,
          route: '海南阳光沙滩游',
          status: '已完成'
        }
      ]
    }
  }
}
</script>

<style scoped>
.itineraries-container {
  padding: 20px;
}
h2 {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.itinerary-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.itinerary-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}
.itinerary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #eee;
}
.itinerary-header h3 {
  margin: 0;
  color: #2c3e50;
}
.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  background-color: #eee;
}
.status.active {
  background-color: #4CAF50;
  color: white;
}
.itinerary-details {
  padding: 15px;
}
.itinerary-details p {
  margin: 8px 0;
}
</style>