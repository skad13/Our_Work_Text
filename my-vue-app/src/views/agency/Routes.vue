<template>
  <div class="routes-container">
    <h2>线路管理</h2>
    <p>这里是旅行社线路管理界面的内容</p>
    <div class="routes-list">
      <div class="route-item" v-for="route in routes" :key="route.id">
        <h3>{{ route.name }}</h3>
        <p>目的地: {{ route.destination }}</p>
        <p>价格: ¥{{ route.price }}</p>
        <p>持续时间: {{ route.duration }}天</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RoutesView',
  data() {
    return {
      routes: [
        { id: 1, name: '北京三日游', destination: '北京', price: 1500, duration: 3 },
        { id: 2, name: '西安历史文化之旅', destination: '西安', price: 2000, duration: 4 },
        { id: 3, name: '海南阳光沙滩游', destination: '三亚', price: 3000, duration: 5 }
      ]
    }
  }
}
</script>

<style scoped>
.routes-container {
  padding: 20px;
}
h2 {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.routes-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.route-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.route-item h3 {
  margin-bottom: 10px;
  color: #2c3e50;
}
</style>