<template>
  <div class="home-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <div class="icon-wrapper">
        <span class="icon">✈️</span>
      </div>
      <h1 class="page-title">智能旅行助手</h1>
      <p class="page-subtitle">基于AI的个性化旅行规划,让每一次出行都完美无忧</p>
    </div>

    <a-card class="form-card" :bordered="false">
      <a-form
        :model="formData"
        layout="vertical"
        @finish="handleSubmit"
      >
        <!-- 第一步:目的地和日期 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">📍</span>
            <span class="section-title">目的地与日期</span>
          </div>

          <a-row :gutter="24">
            <a-col :span="8">
              <a-form-item name="city" :rules="[{ required: true, message: '请输入目的地城市' }]">
                <template #label>
                  <span class="form-label">目的地城市</span>
                </template>
                <a-input
                  v-model:value="formData.city"
                  placeholder="例如: 北京"
                  size="large"
                  class="custom-input"
                >
                  <template #prefix>
                    <span style="color: #1890ff;">🏙️</span>
                  </template>
                </a-input>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item name="start_date" :rules="[{ required: true, message: '请选择开始日期' }]">
                <template #label>
                  <span class="form-label">开始日期</span>
                </template>
                <a-date-picker
                  v-model:value="formData.start_date"
                  style="width: 100%"
                  size="large"
                  class="custom-input"
                  placeholder="选择日期"
                />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item name="end_date" :rules="[{ required: true, message: '请选择结束日期' }]">
                <template #label>
                  <span class="form-label">结束日期</span>
                </template>
                <a-date-picker
                  v-model:value="formData.end_date"
                  style="width: 100%"
                  size="large"
                  class="custom-input"
                  placeholder="选择日期"
                />
              </a-form-item>
            </a-col>
            <a-col :span="4">
              <a-form-item>
                <template #label>
                  <span class="form-label">旅行天数</span>
                </template>
                <div class="days-display-compact">
                  <span class="days-value">{{ formData.travel_days }}</span>
                  <span class="days-unit">天</span>
                </div>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <!-- 第二步:偏好设置 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">⚙️</span>
            <span class="section-title">偏好设置</span>
          </div>

          <a-row :gutter="24">
            <a-col :span="8">
              <a-form-item name="transportation">
                <template #label>
                  <span class="form-label">交通方式</span>
                </template>
                <a-select v-model:value="formData.transportation" size="large" class="custom-select">
                  <a-select-option value="公共交通">🚇 公共交通</a-select-option>
                  <a-select-option value="自驾">🚗 自驾</a-select-option>
                  <a-select-option value="步行">🚶 步行</a-select-option>
                  <a-select-option value="混合">🔀 混合</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="accommodation">
                <template #label>
                  <span class="form-label">住宿偏好</span>
                </template>
                <a-select v-model:value="formData.accommodation" size="large" class="custom-select">
                  <a-select-option value="经济型酒店">💰 经济型酒店</a-select-option>
                  <a-select-option value="舒适型酒店">🏨 舒适型酒店</a-select-option>
                  <a-select-option value="豪华酒店">⭐ 豪华酒店</a-select-option>
                  <a-select-option value="民宿">🏡 民宿</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="preferences">
                <template #label>
                  <span class="form-label">旅行偏好</span>
                </template>
                <div class="preference-tags">
                  <a-checkbox-group v-model:value="formData.preferences" class="custom-checkbox-group">
                    <a-checkbox value="历史文化" class="preference-tag">🏛️ 历史文化</a-checkbox>
                    <a-checkbox value="自然风光" class="preference-tag">🏞️ 自然风光</a-checkbox>
                    <a-checkbox value="美食" class="preference-tag">🍜 美食</a-checkbox>
                    <a-checkbox value="购物" class="preference-tag">🛍️ 购物</a-checkbox>
                    <a-checkbox value="艺术" class="preference-tag">🎨 艺术</a-checkbox>
                    <a-checkbox value="休闲" class="preference-tag">☕ 休闲</a-checkbox>
                  </a-checkbox-group>
                </div>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <!-- 第三步:额外要求 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">💬</span>
            <span class="section-title">额外要求</span>
          </div>

          <a-form-item name="free_text_input">
            <a-textarea
              v-model:value="formData.free_text_input"
              placeholder="请输入您的额外要求,例如:想去看升旗、需要无障碍设施、对海鲜过敏等..."
              :rows="3"
              size="large"
              class="custom-textarea"
            />
          </a-form-item>
        </div>

        <!-- 提交按钮 -->
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading"
            size="large"
            block
            class="submit-button"
          >
            <template v-if="!loading">
              <span class="button-icon">🚀</span>
              <span>开始规划我的旅行</span>
            </template>
            <template v-else>
              <span>正在生成中...</span>
            </template>
          </a-button>
        </a-form-item>

        <!-- 加载进度条 -->
        <a-form-item v-if="loading">
          <div class="loading-container">
            <a-progress
              :percent="loadingProgress"
              status="active"
              :stroke-color="{
                '0%': '#667eea',
                '100%': '#764ba2',
              }"
              :stroke-width="10"
            />
            <p class="loading-status">
              {{ loadingStatus }}
            </p>
          </div>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api'
import type { TripFormData } from '@/types'
import type { Dayjs } from 'dayjs'

const router = useRouter()
const loading = ref(false)
const loadingProgress = ref(0)
const loadingStatus = ref('')

const formData = reactive<TripFormData & { start_date: Dayjs | null; end_date: Dayjs | null }>({
  city: '',
  start_date: null,
  end_date: null,
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: ''
})

// 监听日期变化,自动计算旅行天数
watch([() => formData.start_date, () => formData.end_date], ([start, end]) => {
  if (start && end) {
    const days = end.diff(start, 'day') + 1
    if (days > 0 && days <= 30) {
      formData.travel_days = days
    } else if (days > 30) {
      message.warning('旅行天数不能超过30天')
      formData.end_date = null
    } else {
      message.warning('结束日期不能早于开始日期')
      formData.end_date = null
    }
  }
})

const handleSubmit = async () => {
  if (!formData.start_date || !formData.end_date) {
    message.error('请选择日期')
    return
  }

  loading.value = true
  loadingProgress.value = 0
  loadingStatus.value = '正在初始化...'

  // 模拟进度更新
  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 10

      // 更新状态文本
      if (loadingProgress.value <= 30) {
        loadingStatus.value = '🔍 正在搜索景点...'
      } else if (loadingProgress.value <= 50) {
        loadingStatus.value = '🌤️ 正在查询天气...'
      } else if (loadingProgress.value <= 70) {
        loadingStatus.value = '🏨 正在推荐酒店...'
      } else {
        loadingStatus.value = '📋 正在生成行程计划...'
      }
    }
  }, 500)

  try {
    const requestData: TripFormData = {
      city: formData.city,
      start_date: formData.start_date.format('YYYY-MM-DD'),
      end_date: formData.end_date.format('YYYY-MM-DD'),
      travel_days: formData.travel_days,
      transportation: formData.transportation,
      accommodation: formData.accommodation,
      preferences: formData.preferences,
      free_text_input: formData.free_text_input
    }

    const response = await generateTripPlan(requestData)

    clearInterval(progressInterval)
    loadingProgress.value = 100
    loadingStatus.value = '✅ 完成!'

    if (response.success && response.data) {
      // 保存到sessionStorage
      sessionStorage.setItem('tripPlan', JSON.stringify(response.data))

      message.success('旅行计划生成成功!')

      // 短暂延迟后跳转
      setTimeout(() => {
        router.push('/result')
      }, 500)
    } else {
      message.error(response.message || '生成失败')
    }
  } catch (error: any) {
    clearInterval(progressInterval)
    message.error(error.message || '生成旅行计划失败,请稍后重试')
  } finally {
    setTimeout(() => {
      loading.value = false
      loadingProgress.value = 0
      loadingStatus.value = ''
    }, 1000)
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: 48px 24px;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -150px;
  left: -150px;
  animation-delay: 0s;
}

.circle-2 {
  width: 300px;
  height: 300px;
  top: 40%;
  right: -100px;
  animation-delay: 5s;
}

.circle-3 {
  width: 200px;
  height: 200px;
  bottom: -80px;
  left: 25%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-40px) rotate(180deg);
  }
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 48px;
  animation: fadeInDown 0.8s ease-out;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  margin-bottom: 24px;
}

.icon {
  font-size: 96px;
  display: inline-block;
  animation: bounce 2.5s infinite;
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.3));
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-24px) scale(1.05);
  }
}

.page-title {
  font-size: 64px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 20px;
  text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.4);
  letter-spacing: 3px;
  background: linear-gradient(135deg, #ffffff 0%, #ffeaa7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 22px;
  color: rgba(255, 255, 255, 0.98);
  margin: 0;
  font-weight: 400;
  letter-spacing: 1px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

/* 表单卡片 */
.form-card {
  max-width: 1400px;
  margin: 0 auto;
  border-radius: 32px;
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.45);
  animation: fadeInUp 0.8s ease-out;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.98) !important;
  overflow: hidden;
}

.form-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}

/* 表单分区 */
.form-section {
  margin-bottom: 36px;
  padding: 28px;
  background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
  border-radius: 20px;
  border: 1px solid #e0e4f0;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.form-section:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
  transform: translateY(-4px);
  border-color: #667eea;
}

.form-section:hover::before {
  opacity: 1;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e8ecf8;
  position: relative;
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.section-icon {
  font-size: 28px;
  margin-right: 14px;
  filter: drop-shadow(0 2px 8px rgba(102, 126, 234, 0.3));
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a1a2e 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 表单标签 */
.form-label {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  letter-spacing: 0.3px;
}

/* 自定义输入框 */
.custom-input :deep(.ant-input),
.custom-input :deep(.ant-picker) {
  border-radius: 14px;
  border: 2px solid #e8ecf8;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fafbff;
}

.custom-input :deep(.ant-input:hover),
.custom-input :deep(.ant-picker:hover) {
  border-color: #667eea;
  background: #ffffff;
}

.custom-input :deep(.ant-input:focus),
.custom-input :deep(.ant-picker-focused) {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
  background: #ffffff;
}

/* 自定义选择框 */
.custom-select :deep(.ant-select-selector) {
  border-radius: 14px !important;
  border: 2px solid #e8ecf8 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fafbff !important;
}

.custom-select:hover :deep(.ant-select-selector) {
  border-color: #667eea !important;
  background: #ffffff !important;
}

.custom-select :deep(.ant-select-focused .ant-select-selector) {
  border-color: #667eea !important;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
  background: #ffffff !important;
}

/* 天数显示 - 紧凑版 */
.days-display-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 14px;
  color: white;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.days-display-compact .days-value {
  font-size: 26px;
  font-weight: 800;
  margin-right: 6px;
}

.days-display-compact .days-unit {
  font-size: 15px;
  font-weight: 500;
  opacity: 0.95;
}

/* 偏好标签 */
.preference-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.custom-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
}

.preference-tag :deep(.ant-checkbox-wrapper) {
  margin: 0 !important;
  padding: 10px 20px;
  border: 2px solid #e8ecf8;
  border-radius: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #ffffff;
  font-size: 14px;
  font-weight: 500;
}

.preference-tag :deep(.ant-checkbox-wrapper:hover) {
  border-color: #667eea;
  background: #f0f4ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.preference-tag :deep(.ant-checkbox-wrapper-checked) {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* 自定义文本域 */
.custom-textarea :deep(.ant-input) {
  border-radius: 14px;
  border: 2px solid #e8ecf8;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fafbff;
}

.custom-textarea :deep(.ant-input:hover) {
  border-color: #667eea;
  background: #ffffff;
}

.custom-textarea :deep(.ant-input:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
  background: #ffffff;
}

/* 提交按钮 */
.submit-button {
  height: 64px;
  border-radius: 32px;
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border: none;
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 1px;
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.submit-button:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 16px 48px rgba(102, 126, 234, 0.6);
}

.submit-button:active {
  transform: translateY(-2px) scale(0.98);
}

.button-icon {
  margin-right: 10px;
  font-size: 24px;
}

/* 加载容器 */
.loading-container {
  text-align: center;
  padding: 32px;
  background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
  border-radius: 20px;
  border: 2px dashed #667eea;
  position: relative;
  overflow: hidden;
}

.loading-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.loading-status {
  margin-top: 20px;
  color: #667eea;
  font-size: 18px;
  font-weight: 600;
  position: relative;
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

