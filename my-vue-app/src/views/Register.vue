<template>
    <div class="register-container">
      <div class="register-box">
        <h2>用户注册</h2>
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="registerForm.username" 
            placeholder="请设置用户名"
          >
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="registerForm.password" 
            placeholder="请设置密码"
          >
        </div>
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="registerForm.confirmPassword" 
            placeholder="请再次输入密码"
          >
        </div>
        <div class="form-group">
          <label for="phone">手机号</label>
          <input 
            type="tel" 
            id="phone" 
            v-model="registerForm.phone" 
            placeholder="请输入手机号"
          >
        </div>
        <div class="form-group">
          <label for="userType">注册类型</label>
          <select id="userType" v-model="registerForm.userType">
            <option value="tourist">游客</option>
            <option value="guide">导游</option>
            <option value="agency">旅行社</option>
          </select>
        </div>
        <div class="form-actions">
          <button class="btn-register" @click="handleRegister">注册</button>
          <button class="btn-back" @click="goToLogin">返回登录</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RegisterView',
    data() {
      return {
        registerForm: {
          username: '',
          password: '',
          confirmPassword: '',
          phone: '',
          userType: 'tourist'
        }
      }
    },
    methods: {
      handleRegister() {
        // 表单验证
        if (!this.registerForm.username || !this.registerForm.password || 
            !this.registerForm.confirmPassword || !this.registerForm.phone) {
          alert('请填写完整信息')
          return
        }
        
        if (this.registerForm.password !== this.registerForm.confirmPassword) {
          alert('两次输入的密码不一致')
          return
        }
        
        // 实际项目中这里应该调用API进行注册
        console.log('注册信息', this.registerForm)
        
        // 模拟注册成功
        alert('注册成功，请登录')
        this.goToLogin()
      },
      goToLogin() {
        this.$router.push('/login')
      }
    }
  }
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #83a4d4, #b6fbff);
  }
  
  .register-box {
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
  
  button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
  }
  
  .btn-register {
    background-color: #2196F3;
    color: white;
    flex: 1;
    margin-right: 10px;
  }
  
  .btn-back {
    background-color: #757575;
    color: white;
    flex: 1;
  }
  
  button:hover {
    opacity: 0.9;
  }
  </style>