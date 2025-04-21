<template>
  <div class="login-container">
    <div class="login-box">
      <h2>OTA旅行管理系统</h2>
      <div class="form-group">
        <label for="username">用户名</label>
        <input 
          type="text" 
          id="username" 
          v-model="loginForm.username" 
          placeholder="请输入用户名"
        >
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input 
          type="password" 
          id="password" 
          v-model="loginForm.password" 
          placeholder="请输入密码"
        >
      </div>
      <div class="form-group">
        <label for="userType">用户类型</label>
        <select id="userType" v-model="loginForm.userType">
          <option value="tourist">游客</option>
          <option value="guide">导游</option>
          <option value="agency">旅行社</option>
          <option value="admin">主管部门</option>
        </select>
      </div>
      <div class="form-actions">
        <button class="btn-login" @click="handleLogin">登录</button>
        <button class="btn-register" @click="goToRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        userType: 'tourist'
      }
    }
  },
  methods: {
    handleLogin() {
      // 简单前端验证
      if (!this.loginForm.username || !this.loginForm.password) {
        alert('请输入用户名和密码');
        return;
      }
      
      // 模拟登录成功
      console.log('登录信息:', this.loginForm);
      
      // 保存登录状态到本地存储
      localStorage.setItem('token', 'demo_token_' + Date.now());
      localStorage.setItem('userRole', this.loginForm.userType);
      localStorage.setItem('username', this.loginForm.username);
      
      // 根据用户类型跳转到不同页面
      this.$router.push('/' + this.loginForm.userType);
      
      console.log('登录成功，正在跳转到:', '/' + this.loginForm.userType);
    },
    goToRegister() {
      this.$router.push('/register');
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #83a4d4, #b6fbff);
}

.login-box {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 350px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn-login, .btn-register {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-login {
  background-color: #4CAF50;
  color: white;
  flex: 1;
  margin-right: 10px;
}

.btn-register {
  background-color: #2196F3;
  color: white;
  flex: 1;
}
</style>