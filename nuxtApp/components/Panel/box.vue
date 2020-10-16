<template>
  <div class="template-box">
    <div class="template-header">{{ title }}</div>
    <div class="template-content">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Box',
  props: {
    title: {
      required: true,
      type: String,
    },
  },
}
</script>

<style>
.template-header {
  background-color: #ccc;
  line-height: 40px;
  padding-left: 10px;
  font-size: 16px;
  font-weight: bold;
}

.template-content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 14px 10px;
}
</style>
